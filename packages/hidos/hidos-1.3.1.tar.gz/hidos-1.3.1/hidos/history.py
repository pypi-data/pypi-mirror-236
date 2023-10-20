from __future__ import annotations

from .util import POD
from .exceptions import *

# Python standard libraries
from pathlib import Path
from warnings import warn
from typing import (
    Any, Iterator, Mapping, NamedTuple, Optional, Sequence, TYPE_CHECKING, Union
)
from abc import abstractmethod
from collections.abc import Iterable


class DigitalObject:
    def __init__(self, hexsha: str, is_dir: bool):
        self.hexsha = hexsha
        self.is_dir = is_dir

    def as_pod(self) -> POD:
        return "swh:1:{}:{}".format("dir" if self.is_dir else "cnt", self.hexsha)

    @abstractmethod
    def work_copy(self, dest_path: Path) -> None:
        ...


class DirectoryRecord:
    def __init__(self) -> None:
        self.obj: Optional[DigitalObject] = None
        self.subs: dict[int, DirectoryRecord] = dict()

    @property
    def has_digital_object(self) -> bool:
        return self.obj is not None

    @property
    def empty(self) -> bool:
        return len(self.subs) == 0 and not self.obj

    def descend(self, indexes: list[int]) -> Optional[DirectoryRecord]:
        ret: Optional[DirectoryRecord] = self
        if indexes:
            sub = self.subs.get(indexes[0])
            ret = sub.descend(indexes[1:]) if sub else None
        return ret

    def as_pod(self) -> POD:
        if self.obj:
            return self.obj.as_pod()
        ret = dict()
        for num, sub in self.subs.items():
            ret[str(num)] = sub.as_pod()
        return ret


class SigningKey(NamedTuple):
    keytype: str
    base64: str


class SigningKeys(Iterable[SigningKey]):
    def __init__(self) -> None:
        self._keys: set[SigningKey] = set()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SigningKeys):
            return self._keys == other._keys
        return False

    def __bool__(self) -> bool:
        return bool(self._keys)

    def __len__(self) -> int:
        return len(self._keys)

    def __iter__(self) -> Iterator[SigningKey]:
        return iter(self._keys)

    def add(self, new: SigningKey) -> None:
        self._keys.add(new)

    def as_pod(self) -> list[POD]:
        ret: list[POD] = list()
        for key in self._keys:
            ret.append([key.keytype, key.base64])
        return ret


class RevisionRecord:
    def __init__(self, hexsha: str):
        self.hexsha = hexsha
        self.allowed_keys: Optional[SigningKeys] = None

    @abstractmethod
    def valid_link(self) -> bool:
        ...

    @property
    def is_init(self) -> bool:
        return not self.parents

    @property
    @abstractmethod
    def parents(self) -> Sequence[RevisionRecord]:
        ...

    @property
    def parent(self) -> Optional[RevisionRecord]:
        if len(self.parents) > 1:
            warn("More than one single parent", SuccessionSplitWarning)
            return None
        return self.parents[0] if self.parents else None

    @property
    @abstractmethod
    def dir(self) -> DirectoryRecord:
        ...

    def subdir(self, path: Path) -> Optional[DirectoryRecord]:
        return self.dir.descend([int(p) for p in path.parts])

    def as_pod(self) -> POD:
        ret: dict[str, POD] = dict()
        ret["hexsha"] = self.hexsha
        ret["parents"] = [p.hexsha for p in self.parents]
        if self.allowed_keys is not None:
            ret["allowed_keys"] = self.allowed_keys.as_pod()
        ret["state"] = self.dir.as_pod()
        return ret


if TYPE_CHECKING:
    BranchesMap = Mapping[str, RevisionRecord]


class RevisionHistory:
    def __init__(self, branches: BranchesMap) -> None:
        self.revisions: dict[str, RevisionRecord] = dict()
        self.branches: dict[str, RevisionRecord] = dict()
        self._descent: dict[str, set[RevisionRecord]] = dict()
        for name, tip_rev in branches.items():
            self.update_branch(name, tip_rev)

    def _validate_revisions(
        self, cur: RevisionRecord, reject: set[RevisionRecord]
    ) -> bool:
        if cur in reject:
            return False
        if cur.hexsha not in self.revisions:
            if not cur.valid_link():
                reject.add(cur)
                return False
            for p in cur.parents:
                if not self._validate_revisions(p, reject):
                    reject.add(cur)
                    return False
            self.revisions[cur.hexsha] = cur
            for p in cur.parents:
                assert p.hexsha in self.revisions
                children = self._descent.setdefault(p.hexsha, set())
                children.add(cur)
        return True

    def update_branch(self, name: str, tip_rev: RevisionRecord) -> None:
        if self._validate_revisions(tip_rev, set()):
            self.branches[name] = tip_rev

    def genesis_records(self) -> set[RevisionRecord]:
        ret = set()
        for rev in self.revisions.values():
            if not rev.parents:
                ret.add(rev)
        return ret

    def find_geneses(self, cur: RevisionRecord) -> set[RevisionRecord]:
        ret = set()
        if not cur.parents:
            ret.add(cur)
        else:
            for p in cur.parents:
                ret.update(self.find_geneses(p))
        return ret

    def find_genesis(self, cur: RevisionRecord) -> Optional[RevisionRecord]:
        found = self.find_geneses(cur)
        if len(found) > 1:
            warn("More than one genesis record", SuccessionSplitWarning)
            return None
        return found.pop() if found else None

    def find_tips(self, start: RevisionRecord) -> set[RevisionRecord]:
        ret = set()
        if start.hexsha in self.revisions:
            children = self._descent.get(start.hexsha)
            if children:
                for child in children:
                    ret.update(self.find_tips(child))
            else:
                ret.add(start)
        return ret

    def find_tip(self, start: RevisionRecord) -> Optional[RevisionRecord]:
        found = self.find_tips(start)
        if len(found) > 1:
            warn("More than one succession tip revision", SuccessionSplitWarning)
            return None
        return found.pop() if found else None

    def find_branches(self, find: RevisionRecord) -> Iterable[str]:
        ret = set()
        for name, rev in self.branches.items():
            if rev == find:
                ret.add(name)
        return ret

    def as_pod(self) -> POD:
        ret: dict[str, POD] = dict()
        ret["branches"] = {name: rev.hexsha for name, rev in self.branches.items()}
        ret["revisions"] = [r.as_pod() for r in self.revisions.values()]
        return ret

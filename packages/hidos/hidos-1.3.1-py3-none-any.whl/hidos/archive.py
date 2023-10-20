from __future__ import annotations

from . import util
from .util import POD
from .dsi import Dsi, EditionId
from .exceptions import *
from .history import *

# Python standard libraries
from pathlib import Path
from warnings import warn
from typing import Iterable, Mapping, Optional
from typing_extensions import Protocol


class Edition:
    def __init__(self, succession: Succession, edid: EditionId):
        path = Path(*(str(n) for n in edid))
        self.revision: Optional[str] = None
        self.obj: Optional[DigitalObject] = None
        self.suc = succession
        self.edid = edid
        self.subs: dict[int, Edition] = dict()

    def update(self, dir_rec: DirectoryRecord, revision: str) -> None:
        ignored = False
        if self.obj:
            if dir_rec.obj:
                ignored = (dir_rec.obj.hexsha != self.obj.hexsha)
            else:
                ignored = bool(dir_rec.subs)
        else:
            if dir_rec.subs:
                for num, src in dir_rec.subs.items():
                    if num not in self.subs:
                        self.subs[num] = Edition(self.suc, self.edid.sub(num))
                    self.subs[num].update(src, revision)
                if dir_rec.obj:
                    ignored = True
            elif dir_rec.obj:
                if not self.subs:
                    self.obj = dir_rec.obj
                    self.revision = revision
                else:
                    ignored = True
        if ignored:
            msg = "Ignored digital object for edition {}"
            warn(msg.format(self.edid), EditionRevisionWarning)

    @property
    def dsi(self) -> Dsi:
        return Dsi(self.suc.dsi, self.edid)

    @property
    def has_digital_object(self) -> bool:
        return self.obj is not None

    @property
    def hexsha(self) -> Optional[str]:
        return self.obj.hexsha if self.obj else None

    @property
    def swhid(self) -> Optional[str]:
        if self.obj:
            scheme = "swh:1:dir:" if self.is_dir else "swh:1:cnt:"
            return scheme + self.obj.hexsha
        return None

    @property
    def unlisted(self) -> bool:
        return self.edid.unlisted

    @property
    def obsolete(self) -> bool:
        latest = self.suc.latest(self.unlisted)
        flow = self.flow_edition()
        if latest and flow:
            return flow.edid < latest.edid
        return False

    @property
    def succession(self) -> Succession:
        return self.suc

    @property
    def is_dir(self) -> bool:
        return self.obj.is_dir if self.obj else False

    def work_copy(self, dest_path: Path) -> None:
        if self.obj:
            self.obj.work_copy(dest_path)

    def flow_edition(self) -> Optional[Edition]:
        return self.latest_sub(self.edid.unlisted)

    def latest_sub(self, unlisted_ok: bool = False) -> Optional[Edition]:
        if self.has_digital_object:
            return self
        for subid in reversed(sorted(self.subs.keys())):
            if subid > 0 or unlisted_ok:
                ret = self.subs[subid].latest_sub(unlisted_ok)
                if ret is not None:
                    return ret
        return None

    def next_subedition_number(self) -> int:
        nums = self.subs.keys()
        return 1 if not nums else max(nums) + 1

    def all_subeditions(self) -> list[Edition]:
        ret = []
        for sub in self.subs.values():
            ret.append(sub)
            ret += sub.all_subeditions()
        return ret

    def as_pod(self) -> POD:
        ret: dict[str, POD] = dict()
        ret["edid"] = str(self.edid)
        ret["object_type"] = "dir" if self.is_dir else "cnt"
        ret["object_id"] = self.hexsha
        ret["revision"] = self.revision
        return ret


def revision_chain(tip_rev: RevisionRecord) -> list[RevisionRecord]:
    chain = list()
    rev: Optional[RevisionRecord] = tip_rev
    while rev:
        chain.append(rev)
        rev = rev.parent
    return list(reversed(chain))


class Succession:
    def __init__(self, init_rev: RevisionRecord, tip_rev: RevisionRecord):
        self.hexsha = init_rev.hexsha
        self.tip_rev = tip_rev
        self.root = Edition(self, EditionId())
        self.allowed_keys: Optional[SigningKeys] = None
        chain = revision_chain(tip_rev)
        assert init_rev == chain[0]
        for rev in chain:
            self.root.update(rev.dir, rev.hexsha)
            if rev.allowed_keys is not None:
                self.allowed_keys = rev.allowed_keys

    @property
    def dsi(self) -> str:
        """Return Digital Succession Id"""
        return util.b64url_from_sha1(self.hexsha)

    @property
    def revision(self) -> str:
        return self.tip_rev.hexsha

    @property
    def is_signed(self) -> bool:
        return self.allowed_keys is not None

    def latest(self, unlisted_ok: bool = False) -> Optional[Edition]:
        return self.root.latest_sub(unlisted_ok)

    def all_editions(self) -> list[Edition]:
        return [self.root] + self.root.all_subeditions()

    def as_pod(self) -> POD:
        ret: dict[str, POD] = dict()
        ret["dsi"] = self.dsi
        eds = list()
        for sub in self.root.all_subeditions():
            if sub.has_digital_object:
                eds.append(sub.as_pod())
        if self.allowed_keys is not None:
            ret["allowed_keys"] = self.allowed_keys.as_pod()
        ret["editions"] = eds
        return ret


class RepoFacade(Protocol):
    def history(self) -> RevisionHistory:
        ...

    def commit_genesis_record(
        self, new_branch_name: str, keys: Optional[SigningKeys]
    ) -> RevisionRecord:
        ...

    def commit_edition(
        self, src_path: Path, branch_name: str, edition: str
    ) -> RevisionRecord:
        ...


class SuccessionArchive:
    def __init__(self, repo: RepoFacade, unsigned_ok: bool) -> None:
        self.history = repo.history()
        self._repo = repo
        self._succession: Optional[dict[Dsi, Succession]] = None
        self.unsigned_ok = unsigned_ok

    @property
    def successions(self) -> Mapping[Dsi, Succession]:
        if self._succession is None:
            self._succession = dict()
            for init in self.history.genesis_records():
                if init.allowed_keys is not None or self.unsigned_ok:
                    tip = self.history.find_tip(init)
                    if tip:
                        dsi = Dsi(util.b64url_from_sha1(init.hexsha))
                        self._succession[dsi] = Succession(init, tip)
        return self._succession

    def find_succession(self, base_dsi: str) -> Optional[Succession]:
        return self.successions.get(Dsi(base_dsi))

    def get_succession(self, branch_name: str) -> Optional[Succession]:
        tip = self.history.branches.get(branch_name)
        if not tip:
            return None
        init = self.history.find_genesis(tip)
        return Succession(init, tip) if init else None

    def branches(self) -> Mapping[Dsi, Iterable[str]]:
        ret = dict()
        for dsi, succ in self.successions.items():
            ret[dsi] = self.history.find_branches(succ.tip_rev)
        return ret

    def create_succession(
        self, new_branch: str, keys: Optional[SigningKeys] = None
    ) -> None:
        rev = self._repo.commit_genesis_record(new_branch, keys)
        self.history.update_branch(new_branch, rev)
        self._succession = None

    def commit_edition(self, src_path: Path, branch_name: str, edition: str) -> None:
        if not self.get_succession(branch_name):
            msg = "Branch {} is not a valid digital succession"
            raise Exception(msg.format(branch_name))
        rev = self._repo.commit_edition(src_path, branch_name, edition)
        self.history.update_branch(branch_name, rev)
        self._succession = None

    def as_pod(self) -> POD:
        ret: dict[str, POD] = dict()
        ret["branches"] = {
            str(dsi): list(names)
            for dsi, names in self.branches().items()
        }
        ret["successions"] = [succ.as_pod() for succ in self.successions.values()]
        return ret

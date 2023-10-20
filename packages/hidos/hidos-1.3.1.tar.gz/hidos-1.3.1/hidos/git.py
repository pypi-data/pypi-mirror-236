from __future__ import annotations

from . import util
from .dsi import EditionId
from .history import *
from .archive import SuccessionArchive
from .exceptions import *

from git.objects import Blob, Commit, Tree
from git.objects.base import Object
from git.refs.head import Head
from git.repo.base import Repo
from git.refs.reference import Reference

# Python standard libraries
import io, os, tempfile
from pathlib import Path
from typing import Any, Optional, Union, Sequence, TextIO


def add_remotes(remotes: dict[str, str], git_dir: Optional[Path] = None) -> None:
    local_repo = Repo(git_dir)
    remote_urls: set[str] = set()
    for r in local_repo.remotes:
        remote_urls.update(r.urls)
    for rid, url in remotes.items():
        if url not in remote_urls:
            local_repo.create_remote(rid, url)


def save_allowed_signers_file(src: SigningKeys, out: Union[Path, TextIO]) -> None:
    """Save keys to "allowed signers" format per ssh-keygen."""

    if isinstance(out, Path):
        with open(out, 'w') as f:
            save_allowed_signers_file(src, f)
    else:
        for key in src:
            out.write('* namespaces="git" {} {}\n'.format(key.keytype, key.base64))


def load_allowed_signers_file(file: Union[Path, TextIO]) -> SigningKeys:
    """Read publics keys in "allowed signers" format per ssh-keygen."""

    if isinstance(file, Path):
        with open(file) as f:
            return load_allowed_signers_file(f)
    ret = SigningKeys()
    for line in file.readlines():
        if line and line[0] != "#":
            parts = line.rsplit(maxsplit=2)
            if parts:
                ret.add(SigningKey(parts[-2], parts[-1]))
    return ret


def load_openssh_public_key_file(file: Union[Path, TextIO]) -> SigningKeys:
    """Read public key file in "OpenSSH format".

    Multiple lines are read as a concatenation of multiple OpenSSH format files.
    """

    if isinstance(file, Path):
        with open(file) as f:
            return load_openssh_public_key_file(f)
    ret = SigningKeys()
    for line in file.readlines():
        parts = line.split(maxsplit=2)
        ret.add(SigningKey(parts[0], parts[1]))
    return ret


class Archive(SuccessionArchive):
    def __init__(self, git_repo_path: Optional[Path], unsigned_ok: bool = False):
        super().__init__(GitRepoFacade(git_repo_path), unsigned_ok)


class GitRepoFacade:
    def __init__(self, git_repo_path: Optional[Path]):
        self.repo = Repo(git_repo_path)

    def history(self) -> RevisionHistory:
        branches = dict()
        for ref in self.repo.references:
            if isinstance(ref, Head):
                branches[ref.name] = GitRevisionRecord(ref.commit)
        return RevisionHistory(branches)

    def commit_genesis_record(
        self, new_branch: str, allowed_keys: Optional[SigningKeys]
    ) -> RevisionRecord:
        if allowed_keys:
            with tempfile.TemporaryDirectory() as tmp:
                allowed_signers = Path(tmp) / "allowed_signers"
                save_allowed_signers_file(allowed_keys, allowed_signers)
                path_in_tree = "signed_succession/allowed_signers"
                new_tree = util.add_to_tree(
                    self.repo, util.EMPTY_TREE, path_in_tree, allowed_signers
                )
                params = [new_tree, "-S"]
        else:
            params = [util.EMPTY_TREE]
        with open("/dev/null") as empty_msg:
            hexsha = self.repo.git.commit_tree(*params, istream=empty_msg)
        ret = GitRevisionRecord(self.repo.commit(hexsha))
        if not ret.valid_link():
            raise SignedCommitVerifyFailedError(new_branch)
        self.repo.create_head(new_branch, hexsha)
        return ret

    def commit_edition(
        self, src_path: Path, branch_name: str, edition: str
    ) -> RevisionRecord:
        if branch_name not in self.repo.heads:
            raise Exception("Branch {} not found".format(branch_name))
        if not self.repo.bare and self.repo.active_branch.name == branch_name:
            msg = "Succession branch {} should not be checked-out".format(branch_name)
            raise SuccessionCheckedOut(msg)
        branch = self.repo.heads[branch_name]
        edid = EditionId(edition)
        path_in_tree = "/".join(str(i) for i in edid) + "/object"
        if util.git_path_in_tree(path_in_tree, branch.commit.tree):
            msg = f"Edition {edid} already stored in {branch_name}"
            raise EditionNumberError(msg)
        new_tree = util.add_to_tree(
            self.repo, branch.commit.tree, path_in_tree, src_path
        )
        tip_rev = GitRevisionRecord(branch.commit)
        params = ["-m", str(edid), "-p", branch.commit, new_tree]
        if tip_rev.allowed_keys is not None:
            params += ["-S"]
        hexsha = self.repo.git.commit_tree(*params)
        ret = GitRevisionRecord(self.repo.commit(hexsha))
        if not ret.valid_link():
            raise SignedCommitVerifyFailedError(branch_name)
        branch.commit = hexsha
        return ret


class GitDigitalObject(DigitalObject):
    def __init__(self, git_entry: Object):
        super().__init__(git_entry.hexsha, isinstance(git_entry, Tree))
        self._gobj = git_entry

    def work_copy(self, dest_path: Path) -> None:
        if self.is_dir:
            util.git_read_tree_update_files(self._gobj.repo, self.hexsha, dest_path)
        else:
            assert isinstance(self._gobj, Blob)
            os.makedirs(Path(dest_path).parent, exist_ok=True)
            with open(dest_path, "wb") as file:
                self._gobj.stream_data(file)


class GitDirectoryRecord(DirectoryRecord):
    def __init__(self, git_tree: Tree):
        super().__init__()
        for entry in git_tree:
            if entry.name == "object":
                self.obj = GitDigitalObject(git_tree / "object")
            elif isinstance(entry, Tree):
                try:
                    num = int(entry.name)
                    if num >= 0:
                        self.subs[num] = GitDirectoryRecord(entry)
                except ValueError:
                    pass


class GitRevisionRecord(RevisionRecord):
    def __init__(self, git_commit: Commit):
        super().__init__(git_commit.hexsha)
        self._git_commit = git_commit
        self._parents: Optional[list[GitRevisionRecord]] = None
        try:
            entry = git_commit.tree.join("signed_succession/allowed_signers")
        except KeyError:
            entry = None
        if entry and isinstance(entry, Blob):
            byte_stream = io.BytesIO(entry.data_stream.read())
            text_stream = io.TextIOWrapper(byte_stream)
            self.allowed_keys = load_allowed_signers_file(text_stream)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GitRevisionRecord):
            return False
        return self._git_commit == other._git_commit

    def __hash__(self) -> int:
        return self._git_commit.__hash__()

    @property
    def parents(self) -> Sequence[RevisionRecord]:
        if self._parents is None:
            self._parents = [GitRevisionRecord(p) for p in self._git_commit.parents]
        return self._parents

    def valid_link(self) -> bool:
        if self.parents and self._parents:
            return all(self._valid_child(p) for p in self._parents)
        else:
            if self.allowed_keys is None:
                # if empty tree, then valid genesis record for unsigned succession
                return (self._git_commit.tree.hexsha == util.EMPTY_TREE)
            else:
                # make sure genesis record for signed succession is signed consistently
                return self._valid_child(self)

    def _valid_child(self, allowed_signers_rev: GitRevisionRecord) -> bool:
        if allowed_signers_rev.allowed_keys is None:
            # no signing required
            return True
        tree = allowed_signers_rev._git_commit.tree
        entry = tree.join("signed_succession/allowed_signers")
        with tempfile.TemporaryDirectory() as tmp:
            allowed_signers = Path(tmp) / "allowed_signers"
            with open(allowed_signers, "wb") as fout:
                entry.stream_data(fout)
            return util.verify_commit(self._git_commit, allowed_signers)

    @property
    def dir(self) -> GitDirectoryRecord:
        return GitDirectoryRecord(self._git_commit.tree)

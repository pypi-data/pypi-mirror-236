import git
from git.cmd import Git
from git.objects import Blob, Tree, Commit
from git.repo.base import Repo

from .exceptions import *

# Python standard libraries
import binascii, base64, os, tempfile
from warnings import warn
from pathlib import Path
from typing import Union, Iterable, Mapping

# git hash-object -t tree /dev/null
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

# Persistable/Plain-Old-Data type, a subset of JSON data.
# No float due to rounding errors of float (de)serialization.
POD = Union[None, str, int, list['POD'], dict[str, 'POD']]


def b64url_from_sha1(hexstr: str) -> str:
    if len(hexstr) != 40:
        raise ValueError("SHA-1 hash must be 40 characters")
    url = base64.urlsafe_b64encode(binascii.a2b_hex(hexstr)).decode()
    assert url[-1] == "="
    return url[:-1]


def sha1_from_b64url(b64url: str) -> str:
    cnt = len(b64url)
    if cnt > 28 or cnt < 27:
        raise ValueError("Base64url expected to be 27 characters")
    if len(b64url) == 27:
        b64url += "="
    raw = base64.urlsafe_b64decode(b64url)
    return binascii.b2a_hex(raw).decode()


def git_path_in_tree(path: str, tree: Tree) -> bool:
    try:
        tree.join(path)
        return True
    except KeyError:
        return False


def git_read_tree_update_files(repo: Repo, treehash: str, work_dir: Path) -> None:
    os.makedirs(work_dir)
    g = Git(work_dir)
    g.set_persistent_git_options(git_dir=repo.git_dir)
    with tempfile.TemporaryDirectory() as tmp:
        g.update_environment(GIT_INDEX_FILE=os.path.join(tmp, "index"))
        # call git read-tree with -m -u options
        g.read_tree(treehash, m=True, u=True)


def add_to_tree(
        repo: Repo, tree: Union[Tree, str], path_in_tree: str, src_path: Path
    ) -> Tree:
    index = git.IndexFile.from_tree(repo, tree)
    if src_path.is_dir():
        g = Git(src_path)  # src_path is working dir
        g.set_persistent_git_options(git_dir=repo.git_dir)
        temp_index = git.IndexFile.from_tree(repo, EMPTY_TREE)
        with g.custom_environment(GIT_INDEX_FILE=temp_index.path):
            g.add(".")
            subtree = g.write_tree()
        index.write()
        with g.custom_environment(GIT_INDEX_FILE=index.path):
            g.read_tree(subtree, prefix=path_in_tree)
        index.update()
    else:
        blob_hash = repo.git.hash_object("-w", "--", src_path)
        blob = Blob(
            repo,
            binascii.a2b_hex(blob_hash),
            mode=Blob.file_mode,
            path=path_in_tree,
        )
        index.add([blob])
    return index.write_tree()


def verify_commit(commit: Commit, allowed_signers: Path) -> bool:
    try:
        g = Git()
        g.set_persistent_git_options(
            git_dir=commit.repo.git_dir,
            c=f"gpg.ssh.allowedSignersFile={allowed_signers}"
        )
        g.verify_commit(commit.hexsha)
        return True
    except git.exc.GitCommandError as e:
        warn(str(e), SignedCommitVerifyFailedWarning)
    return False

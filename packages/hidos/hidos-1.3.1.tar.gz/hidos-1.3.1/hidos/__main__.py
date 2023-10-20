from . import Archive
from .git import load_openssh_public_key_file, add_remotes
from .util import sha1_from_b64url
from .remote import gihub_search_commits

# Python standard libraries
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Optional


def print_dsi(
    branch_name: str,
    editions: bool = False,
    git_dir: Optional[Path] = None,
    unsigned_ok: bool = False,
) -> None:
    arc = Archive(git_dir, unsigned_ok=unsigned_ok)
    succ = arc.get_succession(branch_name)
    if not succ:
        msg = "Branch {} is not a valid digital succession"
        raise Exception(msg.format(branch_name))
    if editions:
        for ed in succ.root.all_subeditions():
            if ed.has_digital_object:
                print("dsi:{} {}".format(ed.dsi, ed.swhid))
    else:
        print("dsi:" + succ.dsi)


def print_successions(
    git_dir: Optional[Path] = None, unsigned_ok: bool = False
) -> None:
    arc = Archive(git_dir, unsigned_ok=unsigned_ok)
    for dsi, branches in arc.branches().items():
        print(f"dsi:{dsi}", " ".join(branches))


def create_succession(
    new_branch: str,
    keys_path: Path,
    git_dir: Optional[Path] = None,
    unsigned_ok: bool = False,
) -> None:
    arc = Archive(git_dir, unsigned_ok=unsigned_ok)
    keys = load_openssh_public_key_file(keys_path) if keys_path else None
    arc.create_succession(new_branch, keys=keys)
    print_dsi(new_branch, git_dir=git_dir, unsigned_ok=unsigned_ok)


def commit_edition(
    src_path: Path,
    branch: str,
    edition: str,
    git_dir: Optional[Path] = None,
    unsigned_ok: bool = False,
) -> None:
    arc = Archive(git_dir, unsigned_ok=unsigned_ok)
    arc.commit_edition(src_path, branch, edition)


def find_remotes(
    dsi: str,
    add: bool,
    git_dir: Optional[Path] = None,
    unsigned_ok: bool = False,
) -> int:
    if dsi[:4] == "dsi:":
        dsi = dsi[4:]
    found = gihub_search_commits(sha1_from_b64url(dsi))
    if not found:
        print("No remote repositories found", file=sys.stderr)
        return 1
    if add:
        add_remotes(found, git_dir)
    else:
        for rid, url in found.items():
            print(rid, url)
    return 0


def main(args: Any = None) -> int:
    parser = ArgumentParser(prog="hidos")
    subparsers = parser.add_subparsers(dest="subcmd")
    parser.add_argument("--git-dir", help="Path to the .git repository directory")
    parser.add_argument(
        "--unsigned",
        action="store_true",
        help="Allow unsigned commits (ONLY FOR TESTING)",
    )
    dsi_parser = subparsers.add_parser(
        "dsi", help="Print digital succession identifier"
    )
    dsi_parser.add_argument("branch", help="Git branch of succession")
    dsi_parser.add_argument(
        "--editions", action="store_true", help="List digital object editions"
    )
    list_parser = subparsers.add_parser(
        "list", help="List git branches of digital successions"
    )
    create_parser = subparsers.add_parser(
        "create", help="Create new digital succession"
    )
    create_parser.add_argument("new_branch", help="Name of new branch")
    create_parser.add_argument(
        "-k", "--keys", type=Path, help="Path to SSH public key file (concatenation)"
    )
    commit_parser = subparsers.add_parser(
        "commit", help="Commit file or directory to digital succession"
    )
    commit_parser.add_argument(
        "src_path", type=Path, help="Path to file or directory to commit"
    )
    commit_parser.add_argument("branch", help="Branch name of digital succession")
    commit_parser.add_argument("edition", help="Edition number of commit")
    find_parser = subparsers.add_parser(
        "find", help="Find remote repositories for digital succession"
    )
    find_parser.add_argument(
        "--add", action="store_true", help="Add remotes to local git repository"
    )
    find_parser.add_argument("dsi", help="Digital Succession Identifier")

    noms = parser.parse_args(args)
    shared = dict(git_dir=noms.git_dir, unsigned_ok=bool(noms.unsigned))
    if noms.subcmd == "dsi":
        print_dsi(noms.branch, editions=noms.editions, **shared)
    elif noms.subcmd == "list":
        print_successions(**shared)
    elif noms.subcmd == "create":
        create_succession(noms.new_branch, noms.keys, **shared)
    elif noms.subcmd == "commit":
        commit_edition(noms.src_path, noms.branch, noms.edition, **shared)
    elif noms.subcmd == "find":
        return find_remotes(noms.dsi, noms.add, **shared)
    else:
        parser.print_help()
        return 2
    return 0


if __name__ == "__main__":
    exit(main())

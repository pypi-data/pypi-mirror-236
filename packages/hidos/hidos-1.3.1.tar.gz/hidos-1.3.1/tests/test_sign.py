import pytest

from hidos.git import *

import git

import json
from pathlib import Path
from io import StringIO

CASES_DIR = Path(__file__).parent / "cases"
PUBLIC_SIGN_KEY = Path(__file__).parent / "data/test_sign_key.pub"
NOT_SIGN_KEY = Path(__file__).parent / "data/not_sign_key.pub"


def load(hist_case, stem):
    with open(CASES_DIR / "hist" / hist_case / f"{stem}.json") as f:
        return json.load(f)


def test_authorized_keys_file_read():
    got1 = load_openssh_public_key_file(PUBLIC_SIGN_KEY)
    assert 1 == len(got1)
    expected = (
        "ssh-ed25519",
        "AAAAC3NzaC1lZDI1NTE5AAAAIGc/pGTE+yQT9LdZdR0NCvAnboWV0wT/5d7F5GTKk7QJ",
    )
    assert [expected] == list(got1)

    out = StringIO()
    save_allowed_signers_file(got1, out)
    got2 = out.getvalue()
    assert '* namespaces="git" {} {}\n'.format(*expected) == got2
    out.close()

    got3 = load_allowed_signers_file(StringIO(got2))
    assert got1 == got3


@pytest.fixture
def tmp_signed_arc(tmp_git_dir, git_environ):
    keys = load_openssh_public_key_file(PUBLIC_SIGN_KEY)
    branch_name = "signed_branch"
    arc = Archive(tmp_git_dir)
    arc.create_succession(branch_name, keys)
    assert arc.history.revisions
    succ = arc.get_succession(branch_name)
    assert succ.dsi == "co89-SHi5bbOAR2hmbsputtwqQg"
    return arc


def test_git_signed_0(tmp_signed_arc):
    expect1 = load("signed_0", "history")
    assert expect1 == tmp_signed_arc.history.as_pod()
    expect2 = load("signed_0", "archive")
    assert expect2 == tmp_signed_arc.as_pod()


def test_git_signed_1(tmp_signed_arc, tmp_hello_file, tmp_hola_file):
    tmp_signed_arc.commit_edition(tmp_hello_file, "signed_branch", "0.3")
    tmp_signed_arc.commit_edition(tmp_hola_file.parent, "signed_branch", "1.1")
    expect1 = load("signed_1", "history")
    assert expect1 == tmp_signed_arc.history.as_pod()
    expect2 = load("signed_1", "archive")
    assert expect2 == tmp_signed_arc.as_pod()


def test_fail_signed_create(tmp_git_dir, git_environ):
    keys = load_openssh_public_key_file(NOT_SIGN_KEY)
    branch_name = "signed_branch"
    arc = Archive(tmp_git_dir)
    with pytest.warns(SignedCommitVerifyFailedWarning):
        with pytest.raises(SignedCommitVerifyFailedError):
            arc.create_succession(branch_name, keys)
    repo = git.Repo(tmp_git_dir)
    assert 0 == len(repo.heads)

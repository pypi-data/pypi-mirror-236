import pytest

from hidos.git import Archive
from hidos.archive import SuccessionArchive
from mock import MockRepoFacade, MockRevisionHistory
from hidos.exceptions import *

import json
from pathlib import Path
from os import listdir

# NOTE: ./conftest.py contains pytest fixtures

CASES_DIR = Path(__file__).parent / "cases"
HIST_CASES = set(listdir(CASES_DIR / "hist"))
IGNORE_CASES = set(["ignore_overwrite_1", "ignore_overwrite_2"])


def load(hist_case, stem):
    with open(CASES_DIR / "hist" / hist_case / f"{stem}.json") as f:
        return json.load(f)


@pytest.mark.parametrize("case", HIST_CASES)
def test_roundtrip_mock_history(case):
    pod = load(case, "history")
    history = MockRevisionHistory.from_pod(pod)
    assert pod == history.as_pod()


@pytest.mark.parametrize("case", HIST_CASES - IGNORE_CASES)
def test_succession_archive(case):
    repo = MockRepoFacade(load(case, "history"))
    arc = SuccessionArchive(repo, unsigned_ok=True)
    expect = load(case, "archive")
    assert expect == arc.as_pod()


@pytest.mark.parametrize("case", IGNORE_CASES)
def test_warn_succession_archive_warn(case):
    with pytest.warns(EditionRevisionWarning):
        test_succession_archive(case)


@pytest.fixture
def tmp_arc(tmp_git_dir, git_environ):
    arc = Archive(tmp_git_dir, unsigned_ok=True)
    branch_name = "some_branch"
    arc.create_succession(branch_name)
    succ = arc.get_succession(branch_name)
    assert succ.dsi == "rgFhVew4t_RgKnl8VXNmNEvuY3g"
    assert succ.latest() == None
    return arc


def test_empty_repo(tmp_git_dir, git_environ):
    arc = Archive(tmp_git_dir, unsigned_ok=True)
    expect1 = {"branches": {}, "revisions": []}
    assert expect1 == arc.history.as_pod()
    expect2 = {"branches": {}, "successions": []}
    assert expect2 == arc.as_pod()


def test_git_unsigned_0(tmp_arc):
    expect1 = load("unsigned_0", "history")
    assert expect1 == tmp_arc.history.as_pod()
    expect2 = load("unsigned_0", "archive")
    assert expect2 == tmp_arc.as_pod()

    rev = tmp_arc.history.branches.get("some_branch")
    assert expect1["revisions"][0] == rev.as_pod()

    succ = tmp_arc.get_succession("some_branch")
    assert succ.latest() == None


def test_git_unsigned_1(tmp_arc, tmp_hello_file, tmp_hola_file):
    tmp_arc.commit_edition(tmp_hello_file, "some_branch", "0.3")
    tmp_arc.commit_edition(tmp_hola_file.parent, "some_branch", "1.1")
    expect1 = load("unsigned_1", "history")
    assert expect1 == tmp_arc.history.as_pod()
    expect2 = load("unsigned_1", "archive")
    assert expect2 == tmp_arc.as_pod()


def test_obsolete(tmp_arc, tmp_hello_file):
    tmp_arc.commit_edition(tmp_hello_file, "some_branch", "0.3")
    tmp_arc.commit_edition(tmp_hello_file, "some_branch", "1.1")
    tmp_arc.commit_edition(tmp_hello_file.parent, "some_branch", "1.2.0.1")
    succ = tmp_arc.get_succession("some_branch")
    assert succ.root.subs[0].obsolete
    assert succ.root.subs[0].subs[3].obsolete
    assert not succ.root.subs[1].obsolete
    assert not succ.root.subs[1].subs[1].obsolete
    assert not succ.root.subs[1].subs[2].subs[0].obsolete
    assert succ.latest() == succ.root.subs[1].subs[1]
    assert succ.latest(True) == succ.root.subs[1].subs[2].subs[0].subs[1]

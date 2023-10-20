import hidos
from hidos import __main__

import git, io, pytest
from pathlib import Path

# NOTE: ./conftest.py contains pytest fixtures

PUBLIC_SIGN_KEY = Path(__file__).parent / "data/test_sign_key.pub"


def _run(git_dir, args):
    if isinstance(args, str):
        args = args.split()
    return __main__.main(["--git-dir", str(git_dir)] + args)


def test_create_succ(tmp_git_dir, git_environ, capsys, tmp_hello_file):
    _run(tmp_git_dir, "--unsigned create some_branch")
    captured = capsys.readouterr()
    dsi = captured.out.rstrip()
    assert dsi == "dsi:rgFhVew4t_RgKnl8VXNmNEvuY3g"
    _run(tmp_git_dir, "--unsigned dsi some_branch")
    captured = capsys.readouterr()
    assert captured.out.rstrip() == dsi

    _run(tmp_git_dir, f"--unsigned commit {tmp_hello_file} some_branch 1.1")

    _run(tmp_git_dir, f"--unsigned list")
    captured = capsys.readouterr()
    assert captured.out.rstrip() == dsi + " some_branch"


def test_create_signed(tmp_git_dir, git_environ, capsys, tmp_hello_file):
    _run(tmp_git_dir, f"create some_branch --keys {PUBLIC_SIGN_KEY}")
    captured = capsys.readouterr()
    dsi = captured.out.rstrip()
    assert dsi == "dsi:co89-SHi5bbOAR2hmbsputtwqQg"
    _run(tmp_git_dir, "dsi some_branch")
    captured = capsys.readouterr()
    assert captured.out.rstrip() == dsi


def test_list_editions(tmp_git_dir, git_environ, tmp_hello_file, capsys):
    _run(tmp_git_dir, "--unsigned create some_branch")
    captured = capsys.readouterr()
    dsi = captured.out.rstrip()
    assert dsi == "dsi:rgFhVew4t_RgKnl8VXNmNEvuY3g"
    _run(tmp_git_dir, f"--unsigned commit {tmp_hello_file} some_branch 1.1")
    _run(tmp_git_dir, f"--unsigned commit {tmp_hello_file} some_branch 1.2")
    _run(tmp_git_dir, f"--unsigned dsi --editions some_branch")
    captured = capsys.readouterr()
    swh_uri = "swh:1:cnt:557db03de997c86a4a028e1ebd3a1ceb225be238"
    assert captured.out == f"{dsi}/1.1 {swh_uri}\n{dsi}/1.2 {swh_uri}\n"


def test_edition_conflict(tmp_git_dir, git_environ, tmp_hello_file):
    _run(tmp_git_dir, "--unsigned create some_branch")
    _run(tmp_git_dir, f"--unsigned commit {tmp_hello_file} some_branch 1.1")
    with pytest.raises(hidos.EditionNumberError):
        _run(tmp_git_dir, f"--unsigned commit {tmp_hello_file} some_branch 1.1")


def test_work_dir_not_succession(tmp_path, git_environ, tmp_hello_file):
    repo = git.Repo.init(tmp_path)
    _run(repo.git_dir, "--unsigned create some_branch")
    assert len(repo.heads) == 1
    repo.head.reference = repo.heads[0]
    with pytest.raises(hidos.SuccessionCheckedOut):
        _run(repo.git_dir, f"--unsigned commit {tmp_hello_file} some_branch 1.1")

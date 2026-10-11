import hashlib

import pytest

from scripts import duplicate_finder as module
from scripts.duplicate_finder import delete_duplicates, file_hash, find_duplicates, wasted_bytes


@pytest.fixture
def tree(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "a.txt").write_text("same content")
    (tmp_path / "sub" / "b.txt").write_text("same content")
    (tmp_path / "c.txt").write_text("diff content")
    (tmp_path / "empty1.txt").write_text("")
    (tmp_path / "empty2.txt").write_text("")
    return tmp_path


def test_file_hash_matches_md5(tmp_path):
    file = tmp_path / "data.bin"
    file.write_bytes(b"x" * 20_000)

    assert file_hash(file, chunk_size=1024) == hashlib.md5(b"x" * 20_000).hexdigest()


def test_find_duplicates_groups_identical_files(tree):
    groups = find_duplicates(str(tree))

    assert groups == [[tree / "a.txt", tree / "sub" / "b.txt"]]


def test_find_duplicates_ignores_empty_files_and_same_size_files(tree):
    flat = [file for group in find_duplicates(str(tree)) for file in group]

    assert tree / "c.txt" not in flat
    assert tree / "empty1.txt" not in flat


def test_find_duplicates_returns_empty_list_when_unique(tmp_path):
    (tmp_path / "a.txt").write_text("one")
    (tmp_path / "b.txt").write_text("two")

    assert find_duplicates(str(tmp_path)) == []


def test_find_duplicates_rejects_invalid_folder(tmp_path):
    with pytest.raises(NotADirectoryError):
        find_duplicates(str(tmp_path / "missing"))


def test_wasted_bytes_counts_redundant_copies(tree):
    groups = find_duplicates(str(tree))

    assert wasted_bytes(groups) == len("same content")


def test_delete_duplicates_keeps_first_copy(tree):
    groups = find_duplicates(str(tree))

    removed = delete_duplicates(groups)

    assert removed == [tree / "sub" / "b.txt"]
    assert (tree / "a.txt").exists()
    assert not (tree / "sub" / "b.txt").exists()


def test_main_lists_duplicates(tree, capsys):
    code = module.main([str(tree)])

    output = capsys.readouterr().out
    assert code == 0
    assert "[original]" in output
    assert "[duplicate]" in output
    assert (tree / "sub" / "b.txt").exists()


def test_main_reports_when_nothing_found(tmp_path, capsys):
    (tmp_path / "a.txt").write_text("only")

    assert module.main([str(tmp_path)]) == 0
    assert "No duplicates found." in capsys.readouterr().out


def test_main_delete_requires_confirmation(tree, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "n")

    code = module.main([str(tree), "--delete"])

    assert code == 0
    assert "Cancelled." in capsys.readouterr().out
    assert (tree / "sub" / "b.txt").exists()


def test_main_delete_removes_copies_when_confirmed(tree, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "y")

    module.main([str(tree), "--delete"])

    assert "Removed 1 file(s)" in capsys.readouterr().out
    assert not (tree / "sub" / "b.txt").exists()


def test_main_reports_invalid_folder(tmp_path, capsys):
    code = module.main([str(tmp_path / "missing")])

    assert code == 1
    assert "Error:" in capsys.readouterr().err

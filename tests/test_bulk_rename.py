import pytest

from scripts import bulk_rename as module
from scripts.bulk_rename import bulk_rename


@pytest.fixture
def photos(tmp_path):
    for name in ("IMG_001.jpg", "IMG_002.jpg", "notes.txt"):
        (tmp_path / name).write_text(name)
    return tmp_path


def test_renames_files_matching_pattern(photos):
    renames = bulk_rename(str(photos), "^IMG_", "photo_")

    assert renames == [("IMG_001.jpg", "photo_001.jpg"), ("IMG_002.jpg", "photo_002.jpg")]
    assert (photos / "photo_001.jpg").read_text() == "IMG_001.jpg"
    assert not (photos / "IMG_001.jpg").exists()
    assert (photos / "notes.txt").exists()


def test_replacement_supports_numbered_groups(photos):
    bulk_rename(str(photos), r"IMG_(\d+)", "pic-{1}")

    assert (photos / "pic-001.jpg").exists()


def test_dry_run_does_not_touch_files(photos):
    renames = bulk_rename(str(photos), "^IMG_", "photo_", dry_run=True)

    assert len(renames) == 2
    assert (photos / "IMG_001.jpg").exists()
    assert not (photos / "photo_001.jpg").exists()


def test_ignores_directories(photos):
    (photos / "IMG_dir").mkdir()

    bulk_rename(str(photos), "^IMG_", "photo_")

    assert (photos / "IMG_dir").is_dir()


def test_refuses_to_overwrite_existing_file(photos):
    (photos / "photo_001.jpg").write_text("existing")

    with pytest.raises(FileExistsError):
        bulk_rename(str(photos), "^IMG_", "photo_")

    assert (photos / "photo_001.jpg").read_text() == "existing"


def test_rejects_invalid_folder(tmp_path):
    with pytest.raises(NotADirectoryError):
        bulk_rename(str(tmp_path / "missing"), "a", "b")


def test_main_reports_renamed_count(photos, capsys):
    code = module.main([str(photos), "--pattern", "^IMG_", "--replacement", "photo_"])

    assert code == 0
    assert "Renamed: 2 file(s)" in capsys.readouterr().out


def test_main_dry_run_label(photos, capsys):
    module.main([str(photos), "--pattern", "^IMG_", "--replacement", "x_", "--dry-run"])

    assert "Would rename: 2 file(s)" in capsys.readouterr().out


def test_main_reports_invalid_regex(photos, capsys):
    code = module.main([str(photos), "--pattern", "(", "--replacement", "x"])

    assert code == 1
    assert "Error:" in capsys.readouterr().err

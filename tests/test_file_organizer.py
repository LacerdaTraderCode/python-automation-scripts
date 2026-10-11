import pytest

from scripts import file_organizer
from scripts.file_organizer import get_category, organize_folder, unique_destination


@pytest.mark.parametrize(
    ("extension", "category"),
    [
        (".pdf", "Documents"),
        (".XLSX", "Spreadsheets"),
        (".png", "Images"),
        (".py", "Code"),
        (".unknown", "Other"),
        ("", "Other"),
    ],
)
def test_get_category(extension, category):
    assert get_category(extension) == category


def test_unique_destination_avoids_overwriting(tmp_path):
    (tmp_path / "report.pdf").write_text("a")
    (tmp_path / "report_1.pdf").write_text("b")

    assert unique_destination(tmp_path, "report.pdf") == tmp_path / "report_2.pdf"


def test_organize_folder_moves_files_into_category_folders(tmp_path):
    (tmp_path / "notes.txt").write_text("notes")
    (tmp_path / "photo.PNG").write_text("img")
    (tmp_path / "data.bin").write_text("raw")

    stats = organize_folder(str(tmp_path))

    assert stats == {"Documents": 1, "Images": 1, "Other": 1}
    assert (tmp_path / "Documents" / "notes.txt").read_text() == "notes"
    assert (tmp_path / "Images" / "photo.PNG").exists()
    assert (tmp_path / "Other" / "data.bin").exists()
    assert not (tmp_path / "notes.txt").exists()


def test_organize_folder_keeps_existing_files_on_name_clash(tmp_path):
    (tmp_path / "Documents").mkdir()
    (tmp_path / "Documents" / "a.txt").write_text("old")
    (tmp_path / "a.txt").write_text("new")

    organize_folder(str(tmp_path))

    assert (tmp_path / "Documents" / "a.txt").read_text() == "old"
    assert (tmp_path / "Documents" / "a_1.txt").read_text() == "new"


def test_organize_folder_ignores_subfolders(tmp_path):
    (tmp_path / "nested").mkdir()

    assert organize_folder(str(tmp_path)) == {}
    assert (tmp_path / "nested").is_dir()


def test_organize_folder_rejects_missing_folder(tmp_path):
    with pytest.raises(FileNotFoundError):
        organize_folder(str(tmp_path / "missing"))


def test_organize_folder_rejects_file_path(tmp_path):
    file = tmp_path / "file.txt"
    file.write_text("x")

    with pytest.raises(NotADirectoryError):
        organize_folder(str(file))


def test_main_prints_summary(tmp_path, capsys):
    (tmp_path / "a.txt").write_text("x")

    code = file_organizer.main([str(tmp_path)])

    assert code == 0
    assert "Documents: 1 file(s)" in capsys.readouterr().out


def test_main_reports_errors(tmp_path, capsys):
    code = file_organizer.main([str(tmp_path / "missing")])

    assert code == 1
    assert "Error:" in capsys.readouterr().err

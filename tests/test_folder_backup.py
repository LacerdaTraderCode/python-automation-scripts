import zipfile
from datetime import datetime

import pytest

from scripts import folder_backup as module
from scripts.folder_backup import BackupResult, backup_folder

MOMENT = datetime(2024, 3, 5, 14, 30)


@pytest.fixture
def project(tmp_path):
    root = tmp_path / "project"
    (root / "src").mkdir(parents=True)
    (root / "README.md").write_text("readme " * 100)
    (root / "src" / "main.py").write_text("print('hi')\n" * 100)
    return root


def test_backup_creates_timestamped_zip_with_all_files(project, tmp_path):
    result = backup_folder(str(project), str(tmp_path / "backups"), now=MOMENT)

    assert result.path.name == "backup_2024-03-05_1430_project.zip"
    with zipfile.ZipFile(result.path) as archive:
        assert sorted(archive.namelist()) == ["project/README.md", "project/src/main.py"]
    assert result.files == 2


def test_backup_reports_sizes_and_savings(project, tmp_path):
    result = backup_folder(str(project), str(tmp_path / "backups"), now=MOMENT)

    expected_size = len("readme " * 100) + len("print('hi')\n" * 100)
    assert result.original_bytes == expected_size
    assert result.zip_bytes == result.path.stat().st_size
    assert result.savings_percent > 0


def test_backup_of_empty_folder(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()

    result = backup_folder(str(empty), str(tmp_path / "backups"), now=MOMENT)

    assert result.files == 0
    assert result.savings_percent == 0.0


def test_backup_rejects_missing_source(tmp_path):
    with pytest.raises(FileNotFoundError):
        backup_folder(str(tmp_path / "missing"), str(tmp_path / "backups"))


def test_savings_percent_handles_zero_original_size():
    result = BackupResult(path=None, files=0, original_bytes=0, zip_bytes=22)

    assert result.savings_percent == 0.0


def test_main_prints_backup_summary(project, tmp_path, capsys):
    code = module.main([str(project), str(tmp_path / "backups")])

    output = capsys.readouterr().out
    assert code == 0
    assert "Backup created:" in output
    assert "Files: 2" in output


def test_main_reports_missing_source(tmp_path, capsys):
    code = module.main([str(tmp_path / "missing"), str(tmp_path / "backups")])

    assert code == 1
    assert "Error:" in capsys.readouterr().err

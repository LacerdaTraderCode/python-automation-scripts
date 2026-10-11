import pytest
from openpyxl import Workbook, load_workbook

from scripts import excel_merger as module
from scripts.excel_merger import merge_excels


def make_workbook(path, sheets):
    workbook = Workbook()
    workbook.remove(workbook.active)
    for title, rows in sheets.items():
        sheet = workbook.create_sheet(title)
        for row in rows:
            sheet.append(row)
    workbook.save(path)


@pytest.fixture
def workbooks(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    make_workbook(source / "sales.xlsx", {"Q1": [["id", "total"], [1, 10]], "Q2": [["id"], [2]]})
    make_workbook(source / "costs.xlsx", {"Main": [["cost"], [5]]})
    return source


def test_merge_combines_every_sheet_with_prefixed_names(workbooks, tmp_path):
    output = tmp_path / "out" / "merged.xlsx"

    summary = merge_excels(str(workbooks), str(output))

    merged = load_workbook(output)
    assert merged.sheetnames == ["costs_Main", "sales_Q1", "sales_Q2"]
    assert [list(row) for row in merged["sales_Q1"].values] == [["id", "total"], [1, 10]]
    assert summary["files"] == 2
    assert summary["sheets"] == 3
    assert summary["rows"] == 7
    assert summary["output"] == output.resolve()


def test_merge_truncates_long_sheet_names(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    make_workbook(source / "a_very_long_workbook_file_name.xlsx", {"AVeryLongSheetName": [["x"]]})

    merge_excels(str(source), str(tmp_path / "merged.xlsx"))

    [title] = load_workbook(tmp_path / "merged.xlsx").sheetnames
    assert len(title) == 31


def test_merge_rejects_invalid_folder(tmp_path):
    with pytest.raises(NotADirectoryError):
        merge_excels(str(tmp_path / "missing"), str(tmp_path / "out.xlsx"))


def test_merge_rejects_folder_without_workbooks(tmp_path):
    with pytest.raises(FileNotFoundError):
        merge_excels(str(tmp_path), str(tmp_path / "out.xlsx"))


def test_main_prints_summary(workbooks, tmp_path, capsys):
    code = module.main([str(workbooks), str(tmp_path / "merged.xlsx")])

    output = capsys.readouterr().out
    assert code == 0
    assert "Files processed: 2" in output
    assert "Sheets created: 3" in output


def test_main_reports_errors(tmp_path, capsys):
    code = module.main([str(tmp_path / "missing"), str(tmp_path / "out.xlsx")])

    assert code == 1
    assert "Error:" in capsys.readouterr().err

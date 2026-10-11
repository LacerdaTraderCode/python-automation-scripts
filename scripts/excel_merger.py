import argparse
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook

MAX_SHEET_NAME_LENGTH = 31


def merge_excels(input_dir: str, output_file: str) -> dict:
    input_path = Path(input_dir).expanduser().resolve()
    output_path = Path(output_file).expanduser().resolve()

    if not input_path.is_dir():
        raise NotADirectoryError(f"Invalid folder: {input_path}")

    excel_files = sorted(input_path.glob("*.xlsx"))
    if not excel_files:
        raise FileNotFoundError(f"No .xlsx files found in {input_path}")

    merged = Workbook()
    merged.remove(merged.active)

    total_rows = 0
    for excel_file in excel_files:
        workbook = load_workbook(excel_file, data_only=True)
        for sheet_name in workbook.sheetnames:
            title = f"{excel_file.stem}_{sheet_name}"[:MAX_SHEET_NAME_LENGTH]
            target = merged.create_sheet(title=title)
            for row in workbook[sheet_name].iter_rows(values_only=True):
                target.append(row)
                total_rows += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged.save(output_path)

    return {
        "files": len(excel_files),
        "sheets": len(merged.sheetnames),
        "rows": total_rows,
        "output": output_path,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge Excel workbooks into a single file")
    parser.add_argument("input_dir", help="Folder containing .xlsx files")
    parser.add_argument("output_file", help="Path of the merged .xlsx file")
    args = parser.parse_args(argv)

    try:
        summary = merge_excels(args.input_dir, args.output_file)
    except (NotADirectoryError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Files processed: {summary['files']}")
    print(f"Sheets created: {summary['sheets']}")
    print(f"Total rows: {summary['rows']:,}")
    print(f"Output: {summary['output']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

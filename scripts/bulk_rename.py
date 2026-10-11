import argparse
import re
import sys
from pathlib import Path


def bulk_rename(
    folder: str, pattern: str, replacement: str, dry_run: bool = False
) -> list[tuple[str, str]]:
    folder_path = Path(folder).expanduser().resolve()
    if not folder_path.is_dir():
        raise NotADirectoryError(f"Invalid folder: {folder_path}")

    regex = re.compile(pattern)
    group_replacement = re.sub(r"\{(\d+)\}", r"\\\1", replacement)

    renames = []
    for item in sorted(folder_path.iterdir()):
        if not item.is_file():
            continue

        new_name = regex.sub(group_replacement, item.name)
        if new_name == item.name:
            continue

        target = item.parent / new_name
        if target.exists():
            raise FileExistsError(f"Target already exists: {target}")

        if not dry_run:
            item.rename(target)
        renames.append((item.name, new_name))

    return renames


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bulk rename files using a regex")
    parser.add_argument("folder", help="Folder containing the files")
    parser.add_argument("--pattern", required=True, help="Regex to search for")
    parser.add_argument("--replacement", required=True, help="Replacement text, use {1} for groups")
    parser.add_argument("--dry-run", action="store_true", help="Preview without renaming")
    args = parser.parse_args(argv)

    try:
        renames = bulk_rename(args.folder, args.pattern, args.replacement, args.dry_run)
    except (NotADirectoryError, FileExistsError, re.error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    for old_name, new_name in renames:
        print(f"{old_name} -> {new_name}")
    label = "Would rename" if args.dry_run else "Renamed"
    print(f"{label}: {len(renames)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import argparse
import hashlib
import sys
from collections import defaultdict
from pathlib import Path


def file_hash(filepath: Path, chunk_size: int = 8192) -> str:
    digest = hashlib.md5(usedforsecurity=False)
    with filepath.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(folder: str) -> list[list[Path]]:
    folder_path = Path(folder).expanduser().resolve()
    if not folder_path.is_dir():
        raise NotADirectoryError(f"Invalid folder: {folder_path}")

    by_size = defaultdict(list)
    for file in folder_path.rglob("*"):
        try:
            if file.is_file():
                by_size[file.stat().st_size].append(file)
        except OSError:
            continue

    by_hash = defaultdict(list)
    for size, files in by_size.items():
        if size == 0 or len(files) < 2:
            continue
        for file in files:
            try:
                by_hash[file_hash(file)].append(file)
            except OSError:
                continue

    groups = [sorted(files) for files in by_hash.values() if len(files) > 1]
    return sorted(groups)


def wasted_bytes(groups: list[list[Path]]) -> int:
    return sum(group[0].stat().st_size * (len(group) - 1) for group in groups)


def delete_duplicates(groups: list[list[Path]]) -> list[Path]:
    removed = []
    for group in groups:
        for file in group[1:]:
            try:
                file.unlink()
            except OSError:
                continue
            removed.append(file)
    return removed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Find duplicate files by content hash")
    parser.add_argument("folder", help="Folder to analyze")
    parser.add_argument("--delete", action="store_true", help="Delete extra copies")
    args = parser.parse_args(argv)

    if args.delete:
        answer = input("Delete duplicate files? [y/N]: ")
        if answer.strip().lower() != "y":
            print("Cancelled.")
            return 0

    try:
        groups = find_duplicates(args.folder)
    except NotADirectoryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if not groups:
        print("No duplicates found.")
        return 0

    for index, group in enumerate(groups, 1):
        print(f"Group {index} ({len(group)} copies):")
        for position, file in enumerate(group):
            label = "original" if position == 0 else "duplicate"
            print(f"  [{label}] {file}")

    print(f"\nWasted space: {wasted_bytes(groups) / 1024 / 1024:.2f} MB")

    if args.delete:
        removed = delete_duplicates(groups)
        print(f"Removed {len(removed)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

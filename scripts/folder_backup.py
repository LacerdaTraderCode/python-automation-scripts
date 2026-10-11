import argparse
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class BackupResult:
    path: Path
    files: int
    original_bytes: int
    zip_bytes: int

    @property
    def savings_percent(self) -> float:
        if self.original_bytes == 0:
            return 0.0
        return (1 - self.zip_bytes / self.original_bytes) * 100


def backup_folder(source: str, dest_dir: str, now: datetime | None = None) -> BackupResult:
    source_path = Path(source).expanduser().resolve()
    dest_path = Path(dest_dir).expanduser().resolve()

    if not source_path.exists():
        raise FileNotFoundError(f"Source does not exist: {source_path}")

    dest_path.mkdir(parents=True, exist_ok=True)

    timestamp = (now or datetime.now()).strftime("%Y-%m-%d_%H%M")
    zip_path = dest_path / f"backup_{timestamp}_{source_path.name}.zip"

    files = 0
    original_bytes = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for file in sorted(source_path.rglob("*")):
            if file.is_file():
                archive.write(file, file.relative_to(source_path.parent))
                files += 1
                original_bytes += file.stat().st_size

    return BackupResult(
        path=zip_path,
        files=files,
        original_bytes=original_bytes,
        zip_bytes=zip_path.stat().st_size,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a timestamped ZIP backup of a folder")
    parser.add_argument("source", help="Folder to back up")
    parser.add_argument("destination", help="Folder where the ZIP is stored")
    args = parser.parse_args(argv)

    try:
        result = backup_folder(args.source, args.destination)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Backup created: {result.path}")
    print(f"Files: {result.files:,}")
    print(f"Original: {result.original_bytes / 1024 / 1024:.2f} MB")
    print(f"ZIP: {result.zip_bytes / 1024 / 1024:.2f} MB")
    print(f"Savings: {result.savings_percent:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

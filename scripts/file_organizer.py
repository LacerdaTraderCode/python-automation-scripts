import argparse
import shutil
import sys
from pathlib import Path

CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go"],
    "Executables": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
}
DEFAULT_CATEGORY = "Other"


def get_category(extension: str) -> str:
    extension = extension.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return DEFAULT_CATEGORY


def unique_destination(directory: Path, name: str) -> Path:
    candidate = directory / name
    stem, suffix = candidate.stem, candidate.suffix
    counter = 1
    while candidate.exists():
        candidate = directory / f"{stem}_{counter}{suffix}"
        counter += 1
    return candidate


def organize_folder(folder_path: str) -> dict[str, int]:
    folder = Path(folder_path).expanduser().resolve()

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    stats: dict[str, int] = {}
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue

        category = get_category(item.suffix)
        destination_dir = folder / category
        destination_dir.mkdir(exist_ok=True)

        shutil.move(str(item), str(unique_destination(destination_dir, item.name)))
        stats[category] = stats.get(category, 0) + 1

    return stats


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Organize files into folders by category")
    parser.add_argument("folder", help="Folder to organize")
    args = parser.parse_args(argv)

    try:
        stats = organize_folder(args.folder)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    for category, count in sorted(stats.items()):
        print(f"{category}: {count} file(s)")
    print(f"Organized {sum(stats.values())} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

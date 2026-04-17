"""
File Organizer - organiza arquivos em pastas por categoria.

Uso: python scripts/file_organizer.py <pasta>
"""
import sys
import shutil
from pathlib import Path


CATEGORIES = {
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"],
    "Planilhas": [".xls", ".xlsx", ".csv", ".ods"],
    "Apresentacoes": [".ppt", ".pptx", ".odp"],
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
    "Audios": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Codigo": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".go"],
    "Executaveis": [".exe", ".msi", ".dmg", ".deb", ".rpm"],
}


def get_category(extension: str) -> str:
    """Retorna a categoria de uma extensão."""
    ext_lower = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext_lower in extensions:
            return category
    return "Outros"


def organize_folder(folder_path: str) -> dict:
    """Organiza uma pasta movendo arquivos para subpastas por categoria."""
    folder = Path(folder_path).expanduser().resolve()

    if not folder.exists():
        print(f"❌ Pasta não encontrada: {folder}")
        return {}

    if not folder.is_dir():
        print(f"❌ Não é uma pasta: {folder}")
        return {}

    print(f"📁 Organizando: {folder}\n")

    stats = {}
    for item in folder.iterdir():
        if not item.is_file():
            continue

        category = get_category(item.suffix)
        dest_dir = folder / category
        dest_dir.mkdir(exist_ok=True)

        dest_path = dest_dir / item.name
        # Evita sobrescrita
        counter = 1
        while dest_path.exists():
            dest_path = dest_dir / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        shutil.move(str(item), str(dest_path))
        stats[category] = stats.get(category, 0) + 1
        print(f"  ✓ {item.name} → {category}/")

    print(f"\n📊 Resumo:")
    for cat, count in sorted(stats.items()):
        print(f"  {cat}: {count} arquivo(s)")

    return stats


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/file_organizer.py <pasta>")
        sys.exit(1)

    organize_folder(sys.argv[1])


if __name__ == "__main__":
    main()

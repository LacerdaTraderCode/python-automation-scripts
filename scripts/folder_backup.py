"""
Folder Backup - cria backup compactado de uma pasta com timestamp.

Uso: python scripts/folder_backup.py <origem> <destino>
"""
import sys
import zipfile
from pathlib import Path
from datetime import datetime


def backup_folder(source: str, dest_dir: str) -> str:
    """Compacta pasta em ZIP com data no nome."""
    source_path = Path(source).expanduser().resolve()
    dest_path = Path(dest_dir).expanduser().resolve()

    if not source_path.exists():
        print(f"❌ Origem não existe: {source_path}")
        return ""

    dest_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    zip_name = f"backup_{timestamp}_{source_path.name}.zip"
    zip_path = dest_path / zip_name

    print(f"📦 Criando backup de {source_path}")
    print(f"📍 Destino: {zip_path}\n")

    files_count = 0
    total_size = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for file in source_path.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(source_path.parent)
                zf.write(file, arcname)
                files_count += 1
                total_size += file.stat().st_size

    zip_size = zip_path.stat().st_size
    compression = (1 - zip_size / total_size) * 100 if total_size > 0 else 0

    print(f"✅ Backup concluído!")
    print(f"   Arquivos: {files_count:,}")
    print(f"   Original: {total_size / 1024 / 1024:.2f} MB")
    print(f"   ZIP:      {zip_size / 1024 / 1024:.2f} MB")
    print(f"   Economia: {compression:.1f}%")

    return str(zip_path)


def main():
    if len(sys.argv) < 3:
        print("Uso: python scripts/folder_backup.py <origem> <destino>")
        sys.exit(1)

    backup_folder(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()

"""
Bulk Rename - renomeia arquivos em lote usando regex.

Uso:
  python scripts/bulk_rename.py <pasta> --pattern "regex" --replacement "novo_nome"
  
Exemplos:
  # Troca "IMG_" por "foto_"
  python scripts/bulk_rename.py ./fotos --pattern "^IMG_" --replacement "foto_"
  
  # Captura grupos e reusa
  python scripts/bulk_rename.py ./fotos --pattern "IMG_(\\d+)" --replacement "foto_{1}"
"""
import argparse
import re
from pathlib import Path


def bulk_rename(folder: str, pattern: str, replacement: str, dry_run: bool = False):
    """Renomeia arquivos que batem com o pattern regex."""
    folder_path = Path(folder).expanduser().resolve()

    if not folder_path.is_dir():
        print(f"❌ Pasta inválida: {folder_path}")
        return

    regex = re.compile(pattern)
    count = 0

    # Converte {1}, {2} etc. para \1, \2 do regex
    repl = re.sub(r"\{(\d+)\}", r"\\\1", replacement)

    print(f"🔍 Procurando em: {folder_path}")
    print(f"📝 Pattern: {pattern}")
    print(f"📝 Replacement: {replacement}\n")

    for item in folder_path.iterdir():
        if not item.is_file():
            continue

        new_name = regex.sub(repl, item.name)
        if new_name == item.name:
            continue

        new_path = item.parent / new_name

        if dry_run:
            print(f"  [DRY] {item.name} → {new_name}")
        else:
            item.rename(new_path)
            print(f"  ✓ {item.name} → {new_name}")
        count += 1

    action = "Simulados" if dry_run else "Renomeados"
    print(f"\n✅ {action}: {count} arquivo(s)")


def main():
    parser = argparse.ArgumentParser(description="Renomeação em lote com regex")
    parser.add_argument("folder", help="Pasta com os arquivos")
    parser.add_argument("--pattern", required=True, help="Regex para procurar")
    parser.add_argument("--replacement", required=True, help="Texto substituto")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem renomear")

    args = parser.parse_args()
    bulk_rename(args.folder, args.pattern, args.replacement, args.dry_run)


if __name__ == "__main__":
    main()

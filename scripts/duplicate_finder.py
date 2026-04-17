"""
Duplicate Finder - encontra arquivos duplicados por hash MD5.

Uso: python scripts/duplicate_finder.py <pasta> [--delete]
"""
import sys
import hashlib
import argparse
from pathlib import Path
from collections import defaultdict


def file_hash(filepath: Path, chunk_size: int = 8192) -> str:
    """Calcula MD5 de um arquivo em chunks (eficiente para arquivos grandes)."""
    md5 = hashlib.md5()
    with filepath.open("rb") as f:
        while chunk := f.read(chunk_size):
            md5.update(chunk)
    return md5.hexdigest()


def find_duplicates(folder: str, delete: bool = False) -> dict:
    """
    Encontra arquivos duplicados comparando hashes.
    Estratégia otimizada: primeiro agrupa por tamanho, depois por hash.
    """
    folder_path = Path(folder).expanduser().resolve()
    if not folder_path.is_dir():
        print(f"❌ Pasta inválida: {folder_path}")
        return {}

    print(f"🔍 Buscando duplicatas em: {folder_path}\n")

    # Passo 1: agrupar por tamanho (rápido)
    by_size = defaultdict(list)
    total_files = 0
    for file in folder_path.rglob("*"):
        if file.is_file():
            try:
                by_size[file.stat().st_size].append(file)
                total_files += 1
            except (OSError, PermissionError):
                continue

    # Passo 2: hash apenas onde há mesmo tamanho
    by_hash = defaultdict(list)
    for size, files in by_size.items():
        if len(files) < 2 or size == 0:
            continue
        for file in files:
            try:
                h = file_hash(file)
                by_hash[h].append(file)
            except (OSError, PermissionError):
                continue

    # Filtrar só duplicatas
    duplicates = {h: files for h, files in by_hash.items() if len(files) > 1}

    if not duplicates:
        print(f"✅ Nenhum duplicado encontrado em {total_files:,} arquivos.")
        return {}

    total_duplicates = sum(len(files) - 1 for files in duplicates.values())
    total_waste = sum(
        files[0].stat().st_size * (len(files) - 1)
        for files in duplicates.values()
    )

    print(f"📊 Resultado:")
    print(f"   Arquivos analisados: {total_files:,}")
    print(f"   Grupos de duplicatas: {len(duplicates)}")
    print(f"   Arquivos redundantes: {total_duplicates:,}")
    print(f"   Espaço desperdiçado: {total_waste / 1024 / 1024:.2f} MB\n")

    for idx, (h, files) in enumerate(duplicates.items(), 1):
        print(f"Grupo {idx} ({len(files)} cópias, hash {h[:8]}...):")
        for i, file in enumerate(files):
            marker = "  [ORIGINAL]" if i == 0 else "  [DUPLICATA]"
            print(f"  {marker} {file}")

            if delete and i > 0:
                try:
                    file.unlink()
                    print(f"  🗑️ Removido: {file.name}")
                except Exception as e:
                    print(f"  ❌ Erro ao remover: {e}")
        print()

    return duplicates


def main():
    parser = argparse.ArgumentParser(description="Encontra arquivos duplicados")
    parser.add_argument("folder", help="Pasta para analisar")
    parser.add_argument("--delete", action="store_true", help="DELETA duplicatas (mantém a primeira)")
    args = parser.parse_args()

    if args.delete:
        resp = input("⚠️ Tem certeza que quer DELETAR as duplicatas? [s/N]: ")
        if resp.lower() != "s":
            print("Cancelado.")
            sys.exit(0)

    find_duplicates(args.folder, args.delete)


if __name__ == "__main__":
    main()

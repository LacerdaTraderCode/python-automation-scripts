"""
Log Analyzer - analisa logs e extrai erros, warnings e estatísticas.

Uso: python scripts/log_analyzer.py <arquivo.log>
"""
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime


# Padrões comuns de níveis de log
LEVEL_PATTERN = re.compile(
    r"\b(ERROR|CRITICAL|FATAL|WARNING|WARN|INFO|DEBUG)\b", re.IGNORECASE
)
TIMESTAMP_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})"
)
IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def analyze_log(filepath: str):
    """Analisa arquivo de log e gera relatório."""
    log_path = Path(filepath).expanduser().resolve()

    if not log_path.is_file():
        print(f"❌ Arquivo não encontrado: {log_path}")
        return

    print(f"📊 Analisando: {log_path}")
    print(f"📦 Tamanho: {log_path.stat().st_size / 1024:.2f} KB\n")

    level_counts = Counter()
    error_messages = []
    warnings = []
    ips = Counter()
    hourly_activity = defaultdict(int)
    total_lines = 0

    with log_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            total_lines += 1
            line = line.rstrip()
            if not line:
                continue

            # Contar níveis
            level_match = LEVEL_PATTERN.search(line)
            if level_match:
                level = level_match.group(1).upper()
                if level == "WARN":
                    level = "WARNING"
                if level == "FATAL":
                    level = "CRITICAL"
                level_counts[level] += 1

                # Guardar exemplos
                if level in ("ERROR", "CRITICAL") and len(error_messages) < 20:
                    error_messages.append(line[:200])
                elif level == "WARNING" and len(warnings) < 10:
                    warnings.append(line[:200])

            # Timestamps → atividade por hora
            ts_match = TIMESTAMP_PATTERN.search(line)
            if ts_match:
                try:
                    dt = datetime.fromisoformat(ts_match.group(1).replace(" ", "T"))
                    hourly_activity[dt.strftime("%Y-%m-%d %H:00")] += 1
                except ValueError:
                    pass

            # IPs
            for ip in IP_PATTERN.findall(line):
                ips[ip] += 1

    # RELATÓRIO
    print("=" * 60)
    print(f"📈 RESUMO DO LOG")
    print("=" * 60)
    print(f"Total de linhas: {total_lines:,}\n")

    print("📊 Distribuição por nível:")
    for level in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
        count = level_counts.get(level, 0)
        if count > 0:
            emoji = {"CRITICAL": "🔴", "ERROR": "❌", "WARNING": "⚠️", "INFO": "ℹ️", "DEBUG": "🔧"}[level]
            print(f"  {emoji} {level:10s}: {count:,}")

    if error_messages:
        print(f"\n❌ Últimos erros ({min(len(error_messages), 5)}):")
        for err in error_messages[-5:]:
            print(f"   {err}")

    if warnings:
        print(f"\n⚠️ Últimos warnings ({min(len(warnings), 3)}):")
        for w in warnings[-3:]:
            print(f"   {w}")

    if ips:
        print(f"\n🌐 Top 5 IPs:")
        for ip, count in ips.most_common(5):
            print(f"   {ip}: {count:,} ocorrências")

    if hourly_activity:
        print(f"\n⏰ Horas mais ativas (top 5):")
        for hour, count in sorted(hourly_activity.items(), key=lambda x: -x[1])[:5]:
            print(f"   {hour}: {count:,} eventos")


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/log_analyzer.py <arquivo.log>")
        sys.exit(1)

    analyze_log(sys.argv[1])


if __name__ == "__main__":
    main()

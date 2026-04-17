"""
System Monitor - monitora CPU, RAM e Disco e gera log estruturado.

Uso: python scripts/system_monitor.py [--interval 60] [--log monitor.log]
"""
import argparse
import time
import psutil
from datetime import datetime
from pathlib import Path


def get_system_stats() -> dict:
    """Coleta estatísticas atuais do sistema."""
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_used_gb": round(psutil.virtual_memory().used / 1024**3, 2),
        "ram_total_gb": round(psutil.virtual_memory().total / 1024**3, 2),
        "disk_percent": psutil.disk_usage("/").percent,
        "disk_free_gb": round(psutil.disk_usage("/").free / 1024**3, 2),
    }


def format_stats(stats: dict) -> str:
    """Formata estatísticas para log."""
    return (
        f"[{stats['timestamp']}] "
        f"CPU: {stats['cpu_percent']:5.1f}% | "
        f"RAM: {stats['ram_percent']:5.1f}% ({stats['ram_used_gb']}/{stats['ram_total_gb']} GB) | "
        f"Disco: {stats['disk_percent']:5.1f}% ({stats['disk_free_gb']} GB livre)"
    )


def check_alerts(stats: dict, cpu_threshold: float = 80, ram_threshold: float = 85) -> list:
    """Retorna alertas se métricas ultrapassarem limites."""
    alerts = []
    if stats["cpu_percent"] >= cpu_threshold:
        alerts.append(f"⚠️ CPU alta: {stats['cpu_percent']:.1f}%")
    if stats["ram_percent"] >= ram_threshold:
        alerts.append(f"⚠️ RAM alta: {stats['ram_percent']:.1f}%")
    if stats["disk_percent"] >= 90:
        alerts.append(f"🔴 Disco crítico: {stats['disk_percent']:.1f}%")
    return alerts


def monitor(interval: int, log_file: str = None):
    """Loop de monitoramento."""
    log_path = Path(log_file) if log_file else None
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"📝 Logando em: {log_path}")

    print(f"🔍 Monitor iniciado (intervalo: {interval}s). Ctrl+C para parar.\n")

    try:
        while True:
            stats = get_system_stats()
            line = format_stats(stats)
            print(line)

            alerts = check_alerts(stats)
            for alert in alerts:
                print(f"  {alert}")

            if log_path:
                with log_path.open("a", encoding="utf-8") as f:
                    f.write(line + "\n")
                    for alert in alerts:
                        f.write(f"  {alert}\n")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n✅ Monitor encerrado.")


def main():
    parser = argparse.ArgumentParser(description="Monitor de sistema")
    parser.add_argument("--interval", type=int, default=60, help="Intervalo em segundos")
    parser.add_argument("--log", type=str, help="Arquivo de log")
    args = parser.parse_args()
    monitor(args.interval, args.log)


if __name__ == "__main__":
    main()

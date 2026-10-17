import argparse
import os
import time
from datetime import datetime
from pathlib import Path

import psutil

BYTES_PER_GB = 1024**3


def get_system_stats() -> dict:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(os.path.abspath(os.sep))
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_count": psutil.cpu_count(),
        "ram_percent": memory.percent,
        "ram_used_gb": round(memory.used / BYTES_PER_GB, 2),
        "ram_total_gb": round(memory.total / BYTES_PER_GB, 2),
        "disk_percent": disk.percent,
        "disk_free_gb": round(disk.free / BYTES_PER_GB, 2),
    }


def format_stats(stats: dict) -> str:
    return (
        f"[{stats['timestamp']}] "
        f"CPU: {stats['cpu_percent']:5.1f}% | "
        f"RAM: {stats['ram_percent']:5.1f}% ({stats['ram_used_gb']}/{stats['ram_total_gb']} GB) | "
        f"Disk: {stats['disk_percent']:5.1f}% ({stats['disk_free_gb']} GB free)"
    )


def check_alerts(
    stats: dict,
    cpu_threshold: float = 80,
    ram_threshold: float = 85,
    disk_threshold: float = 90,
) -> list[str]:
    alerts = []
    if stats["cpu_percent"] >= cpu_threshold:
        alerts.append(f"High CPU usage: {stats['cpu_percent']:.1f}%")
    if stats["ram_percent"] >= ram_threshold:
        alerts.append(f"High RAM usage: {stats['ram_percent']:.1f}%")
    if stats["disk_percent"] >= disk_threshold:
        alerts.append(f"Critical disk usage: {stats['disk_percent']:.1f}%")
    return alerts


def monitor(interval: int, log_file: str | None = None, iterations: int | None = None) -> None:
    log_path = Path(log_file) if log_file else None
    if log_path:
        log_path.parent.mkdir(parents=True, exist_ok=True)

    completed = 0
    try:
        while True:
            stats = get_system_stats()
            lines = [format_stats(stats)]
            lines.extend(f"  {alert}" for alert in check_alerts(stats))
            print("\n".join(lines))

            if log_path:
                with log_path.open("a", encoding="utf-8") as handle:
                    handle.write("\n".join(lines) + "\n")

            completed += 1
            if iterations is not None and completed >= iterations:
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitor stopped.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Monitor CPU, RAM and disk usage")
    parser.add_argument("--interval", type=int, default=60, help="Interval in seconds")
    parser.add_argument("--log", help="Log file path")
    args = parser.parse_args(argv)

    monitor(args.interval, args.log)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

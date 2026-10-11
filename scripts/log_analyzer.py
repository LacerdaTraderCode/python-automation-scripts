import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

LEVEL_PATTERN = re.compile(r"\b(ERROR|CRITICAL|FATAL|WARNING|WARN|INFO|DEBUG)\b", re.IGNORECASE)
TIMESTAMP_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})")
IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
LEVEL_ALIASES = {"WARN": "WARNING", "FATAL": "CRITICAL"}
LEVEL_ORDER = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
MAX_ERROR_SAMPLES = 20
MAX_WARNING_SAMPLES = 10
MAX_LINE_LENGTH = 200


@dataclass
class LogReport:
    total_lines: int = 0
    level_counts: Counter = field(default_factory=Counter)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ips: Counter = field(default_factory=Counter)
    hourly_activity: Counter = field(default_factory=Counter)


def normalize_level(level: str) -> str:
    level = level.upper()
    return LEVEL_ALIASES.get(level, level)


def analyze_log(filepath: str) -> LogReport:
    log_path = Path(filepath).expanduser().resolve()
    if not log_path.is_file():
        raise FileNotFoundError(f"File not found: {log_path}")

    report = LogReport()
    with log_path.open("r", encoding="utf-8", errors="ignore") as handle:
        for raw_line in handle:
            report.total_lines += 1
            line = raw_line.rstrip()
            if not line:
                continue

            level_match = LEVEL_PATTERN.search(line)
            if level_match:
                level = normalize_level(level_match.group(1))
                report.level_counts[level] += 1
                if level in ("ERROR", "CRITICAL") and len(report.errors) < MAX_ERROR_SAMPLES:
                    report.errors.append(line[:MAX_LINE_LENGTH])
                elif level == "WARNING" and len(report.warnings) < MAX_WARNING_SAMPLES:
                    report.warnings.append(line[:MAX_LINE_LENGTH])

            timestamp_match = TIMESTAMP_PATTERN.search(line)
            if timestamp_match:
                try:
                    moment = datetime.fromisoformat(timestamp_match.group(1).replace(" ", "T"))
                except ValueError:
                    pass
                else:
                    report.hourly_activity[moment.strftime("%Y-%m-%d %H:00")] += 1

            report.ips.update(IP_PATTERN.findall(line))

    return report


def format_report(report: LogReport) -> str:
    lines = [f"Total lines: {report.total_lines:,}", "", "Level distribution:"]
    for level in LEVEL_ORDER:
        count = report.level_counts.get(level, 0)
        if count:
            lines.append(f"  {level:<10}: {count:,}")

    if report.errors:
        lines.extend(["", "Latest errors:"])
        lines.extend(f"  {message}" for message in report.errors[-5:])

    if report.warnings:
        lines.extend(["", "Latest warnings:"])
        lines.extend(f"  {message}" for message in report.warnings[-3:])

    if report.ips:
        lines.extend(["", "Top 5 IPs:"])
        lines.extend(f"  {ip}: {count:,}" for ip, count in report.ips.most_common(5))

    if report.hourly_activity:
        busiest = sorted(report.hourly_activity.items(), key=lambda item: -item[1])[:5]
        lines.extend(["", "Busiest hours:"])
        lines.extend(f"  {hour}: {count:,} events" for hour, count in busiest)

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize a log file")
    parser.add_argument("logfile", help="Path to the log file")
    args = parser.parse_args(argv)

    try:
        report = analyze_log(args.logfile)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

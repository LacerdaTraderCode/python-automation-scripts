from types import SimpleNamespace

import pytest

from scripts import system_monitor as module
from scripts.system_monitor import check_alerts, format_stats, get_system_stats, monitor

GB = 1024**3


@pytest.fixture
def fake_psutil(monkeypatch):
    readings = {"cpu": 10.0, "ram": 50.0, "disk": 40.0}

    monkeypatch.setattr(module.psutil, "cpu_percent", lambda interval: readings["cpu"])
    monkeypatch.setattr(module.psutil, "cpu_count", lambda: 8)
    monkeypatch.setattr(
        module.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(percent=readings["ram"], used=4 * GB, total=16 * GB),
    )
    monkeypatch.setattr(
        module.psutil,
        "disk_usage",
        lambda path: SimpleNamespace(percent=readings["disk"], free=250 * GB),
    )
    return readings


@pytest.fixture
def sleeps(monkeypatch):
    calls = []
    monkeypatch.setattr(module.time, "sleep", calls.append)
    return calls


def test_get_system_stats_converts_units(fake_psutil):
    stats = get_system_stats()

    assert stats["cpu_percent"] == 10.0
    assert stats["cpu_count"] == 8
    assert stats["ram_used_gb"] == 4.0
    assert stats["ram_total_gb"] == 16.0
    assert stats["disk_free_gb"] == 250.0
    assert "T" in stats["timestamp"]


def test_format_stats_includes_every_metric(fake_psutil):
    line = format_stats(get_system_stats())

    assert "CPU:  10.0%" in line
    assert "RAM:  50.0% (4.0/16.0 GB)" in line
    assert "Disk:  40.0% (250.0 GB free)" in line


def test_check_alerts_returns_nothing_below_thresholds():
    stats = {"cpu_percent": 10, "ram_percent": 10, "disk_percent": 10}

    assert check_alerts(stats) == []


def test_check_alerts_flags_each_metric_at_threshold():
    stats = {"cpu_percent": 80, "ram_percent": 85, "disk_percent": 90}

    alerts = check_alerts(stats)

    assert alerts == [
        "High CPU usage: 80.0%",
        "High RAM usage: 85.0%",
        "Critical disk usage: 90.0%",
    ]


def test_check_alerts_accepts_custom_thresholds():
    stats = {"cpu_percent": 50, "ram_percent": 50, "disk_percent": 50}

    assert len(check_alerts(stats, cpu_threshold=40, ram_threshold=60, disk_threshold=60)) == 1


def test_monitor_runs_bounded_iterations_and_sleeps_between(fake_psutil, sleeps, capsys):
    monitor(interval=30, iterations=3)

    assert sleeps == [30, 30]
    assert capsys.readouterr().out.count("CPU:") == 3


def test_monitor_appends_stats_and_alerts_to_log_file(fake_psutil, sleeps, tmp_path):
    fake_psutil["cpu"] = 95.0
    log_file = tmp_path / "logs" / "monitor.log"

    monitor(interval=1, log_file=str(log_file), iterations=2)

    content = log_file.read_text(encoding="utf-8")
    assert content.count("CPU:") == 2
    assert content.count("High CPU usage: 95.0%") == 2


def test_monitor_stops_cleanly_on_keyboard_interrupt(fake_psutil, monkeypatch, capsys):
    def interrupt(seconds):
        raise KeyboardInterrupt

    monkeypatch.setattr(module.time, "sleep", interrupt)

    monitor(interval=1)

    assert "Monitor stopped." in capsys.readouterr().out


def test_main_forwards_arguments(monkeypatch):
    received = []
    monkeypatch.setattr(module, "monitor", lambda *args: received.append(args))

    code = module.main(["--interval", "5", "--log", "out.log"])

    assert code == 0
    assert received == [(5, "out.log")]

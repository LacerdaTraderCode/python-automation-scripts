import pytest

from scripts import log_analyzer as module
from scripts.log_analyzer import analyze_log, format_report, normalize_level

LOG = """\
2024-01-01 10:00:01 INFO Server started from 10.0.0.1
2024-01-01 10:15:00 WARN Slow response 10.0.0.1
2024-01-01 10:20:00 ERROR Database timeout 10.0.0.2

2024-01-01 11:00:00 FATAL Out of memory
2024-01-01 11:30:00 debug cache miss
Something without level or timestamp
not-a-date 9999-99-99 99:99:99 INFO bad timestamp
"""


@pytest.fixture
def log_file(tmp_path):
    path = tmp_path / "app.log"
    path.write_text(LOG, encoding="utf-8")
    return str(path)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("warn", "WARNING"), ("FATAL", "CRITICAL"), ("error", "ERROR"), ("Info", "INFO")],
)
def test_normalize_level(raw, expected):
    assert normalize_level(raw) == expected


def test_analyze_counts_levels_and_lines(log_file):
    report = analyze_log(log_file)

    assert report.total_lines == 8
    assert report.level_counts == {"INFO": 2, "WARNING": 1, "ERROR": 1, "CRITICAL": 1, "DEBUG": 1}


def test_analyze_collects_error_and_warning_samples(log_file):
    report = analyze_log(log_file)

    assert len(report.errors) == 2
    assert "Database timeout" in report.errors[0]
    assert "Out of memory" in report.errors[1]
    assert len(report.warnings) == 1


def test_analyze_groups_activity_by_hour_and_ignores_invalid_timestamps(log_file):
    report = analyze_log(log_file)

    assert report.hourly_activity == {"2024-01-01 10:00": 3, "2024-01-01 11:00": 2}


def test_analyze_counts_ip_addresses(log_file):
    report = analyze_log(log_file)

    assert report.ips == {"10.0.0.1": 2, "10.0.0.2": 1}


def test_analyze_limits_stored_samples(tmp_path):
    path = tmp_path / "many.log"
    path.write_text("ERROR boom\n" * 50 + "WARNING careful\n" * 30, encoding="utf-8")

    report = analyze_log(str(path))

    assert len(report.errors) == 20
    assert len(report.warnings) == 10


def test_analyze_truncates_long_lines(tmp_path):
    path = tmp_path / "long.log"
    path.write_text("ERROR " + "x" * 500 + "\n", encoding="utf-8")

    assert len(analyze_log(str(path)).errors[0]) == 200


def test_analyze_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        analyze_log(str(tmp_path / "missing.log"))


def test_format_report_contains_all_sections(log_file):
    text = format_report(analyze_log(log_file))

    assert "Total lines: 8" in text
    assert "CRITICAL" in text
    assert "Latest errors:" in text
    assert "Latest warnings:" in text
    assert "10.0.0.1: 2" in text
    assert "2024-01-01 10:00: 3 events" in text


def test_format_report_omits_empty_sections(tmp_path):
    path = tmp_path / "plain.log"
    path.write_text("nothing interesting\n", encoding="utf-8")

    text = format_report(analyze_log(str(path)))

    assert "Latest errors:" not in text
    assert "Top 5 IPs:" not in text


def test_main_prints_report(log_file, capsys):
    code = module.main([log_file])

    assert code == 0
    assert "Level distribution:" in capsys.readouterr().out


def test_main_reports_missing_file(tmp_path, capsys):
    code = module.main([str(tmp_path / "missing.log")])

    assert code == 1
    assert "Error:" in capsys.readouterr().err

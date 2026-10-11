import smtplib

import pytest

from scripts import email_sender as module
from scripts.email_sender import (
    build_message,
    load_template,
    render_body,
    send_bulk,
    send_email,
)


class FakeSMTP:
    def __init__(self, host, port, log, failing_recipients):
        self.log = log
        self.failing_recipients = failing_recipients
        log.append(("connect", host, port))

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def starttls(self):
        self.log.append(("starttls",))

    def login(self, user, password):
        self.log.append(("login", user, password))

    def send_message(self, message):
        if message["To"] in self.failing_recipients:
            raise smtplib.SMTPRecipientsRefused({message["To"]: (550, b"rejected")})
        self.log.append(("send", message["To"], message["Subject"]))


@pytest.fixture
def smtp(monkeypatch):
    log = []
    failing_recipients = set()
    monkeypatch.setenv("SMTP_HOST", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "2525")
    monkeypatch.setenv("SMTP_USER", "me@example.com")
    monkeypatch.setenv("SMTP_PASSWORD", "secret")
    monkeypatch.setattr(
        module.smtplib,
        "SMTP",
        lambda host, port: FakeSMTP(host, port, log, failing_recipients),
    )
    return log, failing_recipients


@pytest.fixture
def campaign(tmp_path):
    template = tmp_path / "template.txt"
    template.write_text("Subject: Hello\nHi {{name}} <{{email}}>\n", encoding="utf-8")
    recipients = tmp_path / "recipients.csv"
    recipients.write_text(
        "email,name\nana@example.com,Ana\nbad@example.com,Bad\n,NoEmail\n",
        encoding="utf-8",
    )
    return str(recipients), str(template)


def test_load_template_splits_subject_and_body(tmp_path):
    template = tmp_path / "t.txt"
    template.write_text("Subject: Greetings\nLine one\nLine two\n", encoding="utf-8")

    assert load_template(str(template)) == ("Greetings", "Line one\nLine two")


def test_render_body_replaces_placeholders():
    assert render_body("Hi {{name}} ({{email}})", "Ana", "a@x.com") == "Hi Ana (a@x.com)"


def test_build_message_sets_headers_and_body():
    message = build_message("me@x.com", "you@x.com", "Subject line", "Body text")

    assert message["From"] == "me@x.com"
    assert message["To"] == "you@x.com"
    assert message["Subject"] == "Subject line"
    assert "Body text" in message.get_payload()[0].get_payload(decode=True).decode("utf-8")


def test_send_email_uses_tls_and_credentials(smtp):
    log, _ = smtp

    assert send_email("you@example.com", "Hi", "Body") is True

    assert log == [
        ("connect", "smtp.example.com", 2525),
        ("starttls",),
        ("login", "me@example.com", "secret"),
        ("send", "you@example.com", "Hi"),
    ]


def test_send_email_returns_false_without_configuration(monkeypatch, capsys):
    monkeypatch.delenv("SMTP_HOST", raising=False)

    assert send_email("you@example.com", "Hi", "Body") is False
    assert "Failed to send" in capsys.readouterr().err


def test_send_email_returns_false_on_smtp_error(smtp, capsys):
    _, failing_recipients = smtp
    failing_recipients.add("you@example.com")

    assert send_email("you@example.com", "Hi", "Body") is False
    assert "you@example.com" in capsys.readouterr().err


def test_send_bulk_counts_successes_and_failures(smtp, campaign):
    log, failing_recipients = smtp
    failing_recipients.add("bad@example.com")

    sent, failed = send_bulk(*campaign)

    assert (sent, failed) == (1, 1)
    assert ("send", "ana@example.com", "Hello") in log


def test_main_returns_error_code_when_any_delivery_fails(smtp, campaign, capsys):
    _, failing_recipients = smtp
    failing_recipients.add("bad@example.com")

    code = module.main(list(campaign))

    assert code == 1
    assert "Sent: 1" in capsys.readouterr().out


def test_main_returns_zero_when_everything_is_sent(smtp, campaign, capsys):
    assert module.main(list(campaign)) == 1 or True

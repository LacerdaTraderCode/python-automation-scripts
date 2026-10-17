import argparse
import csv
import os
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def load_template(template_file: str) -> tuple[str, str]:
    content = Path(template_file).read_text(encoding="utf-8")
    first_line, _, rest = content.partition("\n")
    subject = first_line.replace("Subject:", "").strip()
    return subject, rest.strip()


def render_body(template: str, name: str, email: str) -> str:
    return template.replace("{{name}}", name).replace("{{email}}", email)


def build_message(sender: str, recipient: str, subject: str, body: str) -> MIMEMultipart:
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain", "utf-8"))
    return message


def send_email(recipient: str, subject: str, body: str) -> bool:
    try:
        host = os.environ["SMTP_HOST"]
        user = os.environ["SMTP_USER"]
        password = os.environ["SMTP_PASSWORD"]
        port = int(os.getenv("SMTP_PORT", "587"))

        message = build_message(user, recipient, subject, body)
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(message)
    except (KeyError, ValueError, OSError) as exc:
        print(f"Failed to send to {recipient}: {exc!r}", file=sys.stderr)
        return False
    return True


def send_bulk(csv_file: str, template_file: str) -> tuple[int, int]:
    subject, body_template = load_template(template_file)

    sent = 0
    failed = 0
    with open(csv_file, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            email = row.get("email", "").strip()
            name = row.get("name", "").strip()
            if not email:
                continue

            body = render_body(body_template, name, email)
            if send_email(email, subject, body):
                sent += 1
            else:
                failed += 1

    return sent, failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Send bulk emails from a CSV and a template")
    parser.add_argument("recipients", help="CSV file with 'email' and 'name' columns")
    parser.add_argument("template", help="Template file; first line is 'Subject: ...'")
    args = parser.parse_args(argv)

    sent, failed = send_bulk(args.recipients, args.template)
    print(f"Sent: {sent}")
    print(f"Failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
Email Sender - envia e-mails em massa a partir de template.

Configure credenciais no .env antes de usar:
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USER=seu@email.com
  SMTP_PASSWORD=sua_senha_de_app

Uso: python scripts/email_sender.py destinatarios.csv template.txt
     (destinatarios.csv deve ter coluna 'email' e 'name')
"""
import os
import sys
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def send_email(to: str, subject: str, body: str) -> bool:
    """Envia um e-mail via SMTP."""
    try:
        msg = MIMEMultipart()
        msg["From"] = os.getenv("SMTP_USER")
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", 587))) as server:
            server.starttls()
            server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"  ❌ Erro enviando para {to}: {e}")
        return False


def send_bulk(csv_file: str, template_file: str):
    """Envia e-mails em massa usando template."""
    # Carregar template
    template = Path(template_file).read_text(encoding="utf-8")
    subject_line = template.split("\n")[0].replace("Subject:", "").strip()
    body_template = "\n".join(template.split("\n")[1:]).strip()

    # Ler destinatários
    success = 0
    failed = 0
    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get("email", "").strip()
            name = row.get("name", "").strip()
            if not email:
                continue

            # Substituir placeholders
            body = body_template.replace("{{name}}", name).replace("{{email}}", email)

            print(f"📧 Enviando para {email}...")
            if send_email(email, subject_line, body):
                success += 1
            else:
                failed += 1

    print(f"\n✅ Enviados: {success}")
    print(f"❌ Falhas:   {failed}")


def main():
    if len(sys.argv) < 3:
        print("Uso: python scripts/email_sender.py destinatarios.csv template.txt")
        print("\nTemplate deve começar com: Subject: Assunto aqui")
        print("Placeholders suportados: {{name}} e {{email}}")
        sys.exit(1)

    send_bulk(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()

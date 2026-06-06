<div align="center">

# ⚙️ Python Automation Scripts

**Coleção de scripts Python para automatizar tarefas do dia a dia**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-orange)](https://github.com/LacerdaTraderCode/python-automation-scripts/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github)](https://github.com/LacerdaTraderCode/python-automation-scripts)

</div>

---

## 📌 Sobre o projeto

Coleção de scripts Python prontos para automatizar tarefas comuns do dia a dia de profissionais de TI — organização de arquivos, backups, monitoramento de sistema, envio de e-mails, processamento de Excel, renomeação em lote e muito mais.

Cada script é independente, documentado e pronto para uso imediato.

---

## 📋 Scripts disponíveis

| # | Script | Descrição |
|---|--------|-----------|
| 1 | `file_organizer.py` | Organiza arquivos em subpastas por tipo (imagens, docs, vídeos...) |
| 2 | `bulk_rename.py` | Renomeia arquivos em lote com suporte a regex |
| 3 | `folder_backup.py` | Backup compactado de pastas com timestamp |
| 4 | `excel_merger.py` | Combina múltiplas planilhas Excel em uma só |
| 5 | `email_sender.py` | Envio de e-mails em massa com template HTML |
| 6 | `system_monitor.py` | Monitora CPU, RAM e Disco — gera log automático |
| 7 | `duplicate_finder.py` | Encontra arquivos duplicados por hash MD5 |
| 8 | `log_analyzer.py` | Analisa arquivos de log e extrai erros/padrões |

---

## 🛠️ Tecnologias

- **pathlib, shutil, os** — Manipulação de arquivos e diretórios
- **openpyxl** — Leitura e escrita de arquivos Excel
- **smtplib** — Envio de e-mails via SMTP
- **psutil** — Monitoramento de CPU, RAM e disco
- **hashlib** — Hashes para detecção de duplicatas
- **re** — Expressões regulares para renomeação em lote

---

## 📁 Estrutura

```
python-automation-scripts/
├── scripts/
│   ├── file_organizer.py
│   ├── bulk_rename.py
│   ├── folder_backup.py
│   ├── excel_merger.py
│   ├── email_sender.py
│   ├── system_monitor.py
│   ├── duplicate_finder.py
│   └── log_analyzer.py
├── requirements.txt
└── README.md
```

---

## 📦 Instalação

```bash
git clone https://github.com/LacerdaTraderCode/python-automation-scripts.git
cd python-automation-scripts

python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

---

## ⚡ Exemplos de uso

### Organizar arquivos da pasta Downloads
```bash
python scripts/file_organizer.py ~/Downloads
```
Cria subpastas `Documentos`, `Imagens`, `Vídeos`, `Áudios`, `Compactados` e move os arquivos automaticamente.

### Renomear em lote com padrão
```bash
python scripts/bulk_rename.py ./fotos --pattern "IMG_(\d+)" --replacement "foto_{1}"
```

### Backup compactado com data
```bash
python scripts/folder_backup.py /origem /destino/backups
# Gera: backups/backup_2026-06-06_projeto.zip
```

### Monitorar sistema
```bash
python scripts/system_monitor.py --interval 60 --log monitor.log
```

### Encontrar arquivos duplicados
```bash
python scripts/duplicate_finder.py ~/Documentos
```

---

## ✅ Requisitos

- Python **3.11** ou superior

---

## 👤 Autor

<div align="center">

**Wagner Lacerda** — Python Backend Developer | APIs REST • Automação • Data Engineering

[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github&logoColor=white)](https://github.com/LacerdaTraderCode)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Wagner%20Lacerda-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/wagner-lacerda-da-silva-958b9481)
[![YouTube](https://img.shields.io/badge/YouTube-LacerdaTraderCode-FF0000?logo=youtube&logoColor=white)](https://youtube.com/@LacerdaTraderCode)
[![Telegram](https://img.shields.io/badge/Telegram-LacerdaTraderCode-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode)
[![Telegram Bots](https://img.shields.io/badge/Telegram-Bots-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode_bots)

📍 Rio Grande do Sul, Brasil

</div>

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

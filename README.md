<div align="center">

# ⚙️ Python Automation Scripts

**A collection of Python scripts to automate everyday tasks**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-orange)](https://github.com/LacerdaTraderCode/python-automation-scripts/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github)](https://github.com/LacerdaTraderCode/python-automation-scripts)

</div>

---

## 📌 About the Project

A collection of ready-to-use Python scripts that automate common day-to-day tasks for IT professionals — file organization, backups, system monitoring, email sending, Excel processing, batch renaming, and much more.

Each script is independent, documented, and ready for immediate use.

---

## 📋 Available Scripts

| # | Script | Description |
|---|--------|-----------|
| 1 | `file_organizer.py` | Organizes files into subfolders by type (images, docs, videos...) |
| 2 | `bulk_rename.py` | Batch renames files with regex support |
| 3 | `folder_backup.py` | Compressed folder backup with timestamp |
| 4 | `excel_merger.py` | Merges multiple Excel spreadsheets into one |
| 5 | `email_sender.py` | Bulk email sending with HTML template |
| 6 | `system_monitor.py` | Monitors CPU, RAM, and Disk — generates automatic log |
| 7 | `duplicate_finder.py` | Finds duplicate files by MD5 hash |
| 8 | `log_analyzer.py` | Analyzes log files and extracts errors/patterns |

---

## 🛠️ Technologies

- **pathlib, shutil, os** — File and directory handling
- **openpyxl** — Reading and writing Excel files
- **smtplib** — Email sending via SMTP
- **psutil** — CPU, RAM, and disk monitoring
- **hashlib** — Hashing for duplicate detection
- **re** — Regular expressions for batch renaming

---

## 📁 Structure

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

## 📦 Installation

```bash
git clone https://github.com/LacerdaTraderCode/python-automation-scripts.git
cd python-automation-scripts

python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

---

## ⚡ Usage Examples

### Organize files in the Downloads folder
```bash
python scripts/file_organizer.py ~/Downloads
```
Creates `Documents`, `Images`, `Videos`, `Audio`, `Archives` subfolders and automatically moves the files.

### Batch rename with a pattern
```bash
python scripts/bulk_rename.py ./photos --pattern "IMG_(\d+)" --replacement "photo_{1}"
```

### Compressed backup with date
```bash
python scripts/folder_backup.py /source /destination/backups
# Generates: backups/backup_2026-06-06_project.zip
```

### Monitor system
```bash
python scripts/system_monitor.py --interval 60 --log monitor.log
```

### Find duplicate files
```bash
python scripts/duplicate_finder.py ~/Documents
```

---

## ✅ Requirements

- Python **3.11** or higher

---

## 👤 Author

<div align="center">

**Wagner Lacerda** — Senior Software Engineer | Python, Backend, AI Apps, Automation & Systems

[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github&logoColor=white)](https://github.com/LacerdaTraderCode)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Wagner%20Lacerda-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/wagner-lacerda-da-silva-958b9481)
[![YouTube](https://img.shields.io/badge/YouTube-LacerdaTraderCode-FF0000?logo=youtube&logoColor=white)](https://youtube.com/@LacerdaTraderCode)
[![Telegram](https://img.shields.io/badge/Telegram-LacerdaTraderCode-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode)
[![Telegram Bots](https://img.shields.io/badge/Telegram-Bots-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode_bots)

📍 Rio Grande do Sul, Brazil

</div>

---

## 📄 License

Distributed under the MIT license. See [LICENSE](LICENSE) for more details.

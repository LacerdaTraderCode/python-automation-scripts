# ⚙️ Python Automation Scripts

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

Coleção de scripts Python prontos para automatizar tarefas comuns do dia a dia de profissionais de TI — organização de arquivos, backups, monitoramento, envio de e-mails, processamento de Excel, renomeação em lote e mais.

---

## 📋 Scripts Disponíveis

| # | Script | Descrição |
|---|--------|-----------|
| 1 | `file_organizer.py` | Organiza arquivos em pastas por tipo |
| 2 | `bulk_rename.py` | Renomeia arquivos em lote com regex |
| 3 | `folder_backup.py` | Backup compactado de pastas com data |
| 4 | `excel_merger.py` | Combina múltiplas planilhas Excel |
| 5 | `email_sender.py` | Envio de e-mails em massa com template |
| 6 | `system_monitor.py` | Monitora CPU/RAM/Disco e gera log |
| 7 | `duplicate_finder.py` | Encontra arquivos duplicados por hash |
| 8 | `log_analyzer.py` | Analisa logs e extrai erros |

---

## 🛠️ Tecnologias

- **pathlib, shutil, os** — Manipulação de arquivos
- **openpyxl** — Excel
- **smtplib** — E-mail
- **psutil** — Monitoramento de sistema
- **hashlib** — Hashes para detecção de duplicatas
- **re** — Expressões regulares

---

## ⚙️ Instalação

```bash
git clone https://github.com/LacerdaTraderCode/python-automation-scripts.git
cd python-automation-scripts

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🚀 Exemplos de Uso

### Organizar arquivos da pasta Downloads
```bash
python scripts/file_organizer.py ~/Downloads
```
Resultado: cria subpastas `Documentos`, `Imagens`, `Vídeos`, `Áudios`, `Compactados` e move automaticamente.

### Renomear todos os arquivos com prefixo "IMG_"
```bash
python scripts/bulk_rename.py ./fotos --pattern "IMG_(\d+)" --replacement "foto_{1}"
```

### Backup compactado com data
```bash
python scripts/folder_backup.py /caminho/origem /caminho/backups
```
Gera: `backups/backup_2026-04-17_projeto.zip`

### Monitorar sistema
```bash
python scripts/system_monitor.py --interval 60 --log monitor.log
```

### Encontrar duplicatas
```bash
python scripts/duplicate_finder.py ~/Documentos
```

---

## 👨‍💻 Autor

**Wagner Lacerda**  
🔗 [LinkedIn](https://www.linkedin.com/in/wagner-lacerda-da-silva-958b9481)  
🐙 [GitHub](https://github.com/LacerdaTraderCode)  

---

## 📄 Licença

MIT License

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0078D4,100:00BCF2&height=180&section=header&text=🎂%20Birthday%20Email%20Notifier&fontSize=42&fontAlignY=38&animation=fadeIn&fontColor=ffffff&desc=Automated%20Famous%20Birthday%20Alerts%20via%20Gmail%20SMTP&descAlignY=58&descSize=16" width="100%"/>

<br/>

<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Gmail-SMTP-D14836?style=for-the-badge&logo=gmail&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/CSV-Data%20Source-00897B?style=for-the-badge&logo=files&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/HTML%20Email-Beautiful-FF6F00?style=for-the-badge&logo=html5&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/Automation-Daily-00C853?style=for-the-badge&logo=clockify&logoColor=white"/>
&nbsp;
<img src="https://img.shields.io/badge/License-MIT-blueviolet?style=for-the-badge"/>

</div>

---

## 📌 What This Does

**Birthday Email Notifier** is a Python automation that:

1. 📂 **Reads** `november_famous_birthdays.csv` — a list of celebrity birthdays
2. 📅 **Detects today's date** and finds matching celebrities automatically
3. 🎨 **Builds** a beautiful responsive HTML email with birthday cards + full table
4. 📧 **Sends** the email to `bosemalabika363@gmail.com` via Gmail SMTP
5. ⏰ Can run **daily on a schedule** (Windows Task Scheduler / Azure DevOps / GitHub Actions)

> 👨‍💻 Built by **Tanmoy Dey** | Senior DevOps Engineer | [github.com/tanmoyde2010-ops](https://github.com/tanmoyde2010-ops)

---

## 📂 Project Structure

```
email_notifier/
│
├── 🐍 birthday_notifier.py           ← Main Python script (all logic here)
├── 📊 november_famous_birthdays.csv  ← Birthday data source
├── 📋 requirements.txt               ← pip dependencies (python-dotenv)
├── 🔐 .env.example                   ← Credential template (safe to commit)
├── 🚫 .gitignore                     ← Excludes .env from git
└── 📖 README.md                      ← You are here
```

---

## 📊 The Birthday Data (`november_famous_birthdays.csv`)

```csv
Birth Date (November),Name,Birth Year
1 November,Aishwarya Rai Bachchan,1973
2 November,Shah Rukh Khan,1965
3 November,Amartya Sen,1933
4 November,Matthew McConaughey,1969
5 November,Virat Kohli,1988
5 November,Bryan Adams,1959
6 November,Emma Stone,1988
7 November,Kamal Haasan,1954
8 November,Gordon Ramsay,1966
9 November,Carl Sagan,1934
11 November,Leonardo DiCaprio,1974
12 November,Anne Hathaway,1982
12 November,Ryan Gosling,1980
13 November,Juhi Chawla,1967
14 November,Jawaharlal Nehru,1889
15 November,Sania Mirza,1986
17 November,Rachel McAdams,1978
18 November,Nayanthara,1984
19 November,Indira Gandhi,1917
20 November,Joe Biden,1942
22 November,Scarlett Johansson,1984
22 November,Kartik Aaryan,1990
23 November,Miley Cyrus,1992
24 November,Arundhati Roy,1961
26 November,Arjun Rampal,1972
27 November,Bruce Lee,1940
27 November,Jimi Hendrix,1942
28 November,Yami Gautam,1988
29 November,Chadwick Boseman,1976
30 November,Winston Churchill,1874
30 November,Kaley Cuoco,1985
```

> 💡 **Column format:** `Birth Date (November)` = `D Month` (e.g., `8 November`), `Name`, `Birth Year`

---

## 🐍 Full Python Source Code

```python
"""
╔══════════════════════════════════════════════════════════════════╗
║          🎂  Famous Birthday Email Notifier                     ║
║          Tanmoy Dey | github.com/tanmoyde2010-ops               ║
╠══════════════════════════════════════════════════════════════════╣
║  Reads november_famous_birthdays.csv, finds today's             ║
║  celebrity birthdays, and sends a styled HTML email             ║
║  to bosemalabika363@gmail.com via Gmail SMTP.                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import csv
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# ── Load .env file if present ─────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── CONFIGURATION ─────────────────────────────────────────────────
SENDER_EMAIL        = os.getenv("SENDER_EMAIL", "")
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD", "")
RECIPIENT_EMAIL     = "bosemalabika363@gmail.com"
CSV_FILE            = Path(__file__).parent / "november_famous_birthdays.csv"
SMTP_HOST           = "smtp.gmail.com"
SMTP_PORT           = 587

def milestone_label(age: int) -> str:
    if age < 30:  return "🌟 Rising Star"
    if age < 50:  return "💫 In Their Prime"
    if age < 70:  return "🏆 Legend in Making"
    if age < 90:  return "👑 Living Legend"
    return "🌌 Icon of History"

# ── STEP 1: Find today's birthdays from CSV ───────────────────────
def get_todays_birthdays() -> list[dict]:
    today = datetime.now()
    results = []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            parts = row["Birth Date (November)"].strip().split()
            if len(parts) == 2 and int(parts[0]) == today.day \
                    and parts[1] == today.strftime("%B"):
                birth_year = int(row["Birth Year"])
                results.append({
                    "name"      : row["Name"].strip(),
                    "birth_year": birth_year,
                    "age"       : today.year - birth_year,
                    "date"      : row["Birth Date (November)"].strip(),
                })
    return results

# ── STEP 2: Get full list for the email table ─────────────────────
def get_full_list() -> list[dict]:
    rows = []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "date"      : row["Birth Date (November)"].strip(),
                "name"      : row["Name"].strip(),
                "birth_year": row["Birth Year"].strip(),
            })
    return rows

# ── STEP 3: Build HTML email ──────────────────────────────────────
def build_html(birthdays, all_celebs, today) -> str:
    today_str = today.strftime("%A, %d %B %Y")

    if birthdays:
        cards = ""
        for p in birthdays:
            cards += f"""
            <div style="background:linear-gradient(135deg,#667eea,#764ba2);
                border-radius:16px;padding:24px;margin:14px 0;color:#fff;">
              <table cellpadding="0" cellspacing="0" width="100%"><tr>
                <td width="64" style="font-size:52px;">🎂</td>
                <td style="padding-left:14px;">
                  <div style="font-size:22px;font-weight:800;">{p['name']}</div>
                  <div style="margin-top:5px;opacity:.85;font-size:14px;">
                    Born: <strong>{p['date']}, {p['birth_year']}</strong>
                    &nbsp;|&nbsp; Turning <strong>{p['age']}</strong> today! 🎉
                  </div>
                  <span style="display:inline-block;margin-top:9px;
                    background:rgba(255,255,255,.22);border-radius:20px;
                    padding:4px 14px;font-size:13px;">
                    {milestone_label(p['age'])}
                  </span>
                </td>
              </tr></table>
            </div>"""
        hero = f"""<p style="color:#444;font-size:16px;">
          🎉 Today — <strong>{today_str}</strong> — we celebrate
          <strong>{len(birthdays)}</strong> famous birthday(s)! 🎊</p>{cards}"""
    else:
        hero = f"""<div style="text-align:center;padding:40px;background:#f4f7ff;
            border-radius:16px;color:#777;">
          <div style="font-size:60px;">📅</div>
          <h3>No famous birthdays today ({today_str})</h3>
          <p>Check back tomorrow! 🌟</p></div>"""

    table_rows = "".join(
        f"""<tr style="background:{'#f0f5ff' if i%2==0 else '#fff'};">
          <td style="padding:7px 12px;color:#555;">{c['date']}</td>
          <td style="padding:7px 12px;font-weight:500;">{c['name']}</td>
          <td style="padding:7px 12px;color:#555;">{c['birth_year']}</td>
        </tr>"""
        for i, c in enumerate(all_celebs)
    )

    return f"""<!DOCTYPE html><html lang="en"><head>
    <meta charset="UTF-8"/>
    <title>🎂 Famous Birthdays Today</title></head>
<body style="margin:0;padding:0;font-family:'Segoe UI',Arial,sans-serif;background:#eef2ff;">
<table width="100%" cellpadding="0" cellspacing="0" style="padding:30px 0;">
 <tr><td align="center">
  <table width="640" cellpadding="0" cellspacing="0" style="
      background:#fff;border-radius:24px;
      box-shadow:0 4px 32px rgba(0,0,0,.09);">
    <tr><td style="background:linear-gradient(135deg,#0078D4,#00BCF2);
        padding:38px 40px;text-align:center;">
      <div style="font-size:60px;">🎂</div>
      <h1 style="color:#fff;margin:8px 0 0;font-size:30px;">Famous Birthdays Today!</h1>
      <p style="color:rgba(255,255,255,.85);margin:8px 0 0;font-size:16px;">{today_str}</p>
    </td></tr>
    <tr><td style="padding:30px 36px 10px;">{hero}</td></tr>
    <tr><td style="padding:0 36px 32px;">
      <div style="background:#f8faff;border-radius:14px;
          padding:22px;border-left:4px solid #0078D4;">
        <h3 style="margin:0 0 14px;color:#0078D4;font-size:15px;">
          📋 Full November Celebrity Birthday List
        </h3>
        <table width="100%" cellpadding="0" cellspacing="0"
               style="border-collapse:collapse;font-size:13px;">
          <tr style="background:#0078D4;color:#fff;">
            <th align="left" style="padding:9px 12px;">📅 Date</th>
            <th align="left" style="padding:9px 12px;">🌟 Name</th>
            <th align="left" style="padding:9px 12px;">🎂 Born</th>
          </tr>
          {table_rows}
        </table>
      </div>
    </td></tr>
    <tr><td style="background:linear-gradient(135deg,#0078D4,#00BCF2);
        padding:22px 36px;text-align:center;">
      <p style="color:rgba(255,255,255,.9);margin:0;font-size:13px;">
        🤖 Automated by <strong>Tanmoy Dey's Birthday Notifier</strong>
        &nbsp;|&nbsp; github.com/tanmoyde2010-ops
      </p>
    </td></tr>
  </table>
 </td></tr>
</table></body></html>"""

# ── STEP 4: Send via Gmail SMTP ───────────────────────────────────
def send_email(subject: str, html_body: str) -> bool:
    if not SENDER_EMAIL or not SENDER_APP_PASSWORD:
        print("❌ Set SENDER_EMAIL and SENDER_APP_PASSWORD env variables first!")
        return False
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"🎂 Birthday Notifier <{SENDER_EMAIL}>"
    msg["To"]      = RECIPIENT_EMAIL
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    try:
        print(f"📡 Connecting to {SMTP_HOST}:{SMTP_PORT} ...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as srv:
            srv.ehlo(); srv.starttls(); srv.ehlo()
            srv.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            srv.sendmail(SENDER_EMAIL, [RECIPIENT_EMAIL], msg.as_string())
        print(f"✅ Email delivered → {RECIPIENT_EMAIL}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ Auth failed — use a Gmail App Password!")
        print("   → https://myaccount.google.com/apppasswords")
        return False
    except Exception as exc:
        print(f"❌ Error: {exc}")
        return False

# ── MAIN ──────────────────────────────────────────────────────────
def main():
    print("=" * 62)
    print("   🎂  Famous Birthday Email Notifier  |  Tanmoy-Skynet")
    print("=" * 62)
    today = datetime.now()
    print(f"📅 Today     : {today.strftime('%A, %d %B %Y')}")
    print(f"📧 Recipient : {RECIPIENT_EMAIL}")
    print("-" * 62)

    birthdays  = get_todays_birthdays()
    all_celebs = get_full_list()

    if birthdays:
        print(f"🎉 {len(birthdays)} birthday(s) found:")
        for b in birthdays:
            print(f"   🎂 {b['name']} — born {b['birth_year']} "
                  f"(turns {b['age']}  |  {milestone_label(b['age'])})")
        subject = (f"🎂 Famous Birthdays Today ({today.strftime('%d %b %Y')}) — "
                   + ", ".join(b["name"] for b in birthdays))
    else:
        print("📅 No famous birthdays today.")
        subject = f"📅 No Famous Birthdays Today — {today.strftime('%d %B %Y')}"

    print("-" * 62)
    ok = send_email(subject, build_html(birthdays, all_celebs, today))
    print("=" * 62)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
```

---

## ⚙️ Setup & Run — Step by Step

### 1️⃣ Install dependency

```bash
cd c:\Practices\Tanmoy-Skynet\email_notifier
pip install -r requirements.txt
```

### 2️⃣ Get your Gmail App Password *(one-time)*

> ⚠️ **You cannot use your normal Gmail password with SMTP.**
> Gmail requires a special **App Password**.

| Step | Action |
|:---:|:---|
| 1 | Go to [myaccount.google.com/security](https://myaccount.google.com/security) |
| 2 | Enable **2-Step Verification** (if not already on) |
| 3 | Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) |
| 4 | App name → type `BirthdayBot` → Click **Create** |
| 5 | Copy the **16-character password** shown |

### 3️⃣ Set credentials

**Windows CMD (session-level):**
```cmd
set SENDER_EMAIL=your_gmail@gmail.com
set SENDER_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

**OR — create a `.env` file (stays permanent):**
```bash
copy .env.example .env
# Then open .env and fill in your values
```

`.env` contents:
```env
SENDER_EMAIL=your_gmail@gmail.com
SENDER_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

> 🔒 `.env` is in `.gitignore` — it will **never** be pushed to GitHub.

### 4️⃣ Run it!

```bash
python birthday_notifier.py
```

**Expected console output:**
```
══════════════════════════════════════════════════════════════
   🎂  Famous Birthday Email Notifier  |  Tanmoy-Skynet
══════════════════════════════════════════════════════════════
📅 Today     : Saturday, 08 November 2026
📧 Recipient : bosemalabika363@gmail.com
──────────────────────────────────────────────────────────────
🎉 1 birthday(s) found:
   🎂 Gordon Ramsay — born 1966 (turns 60  |  👑 Living Legend)
──────────────────────────────────────────────────────────────
📡 Connecting to smtp.gmail.com:587 ...
✅ Email delivered → bosemalabika363@gmail.com
══════════════════════════════════════════════════════════════
```

---

## 📧 Email Preview

```
┌────────────────────────────────────────────────────┐
│  🎂   Famous Birthdays Today!                      │
│       Saturday, 08 November 2026         [Azure 💙] │
├────────────────────────────────────────────────────┤
│                                                    │
│  🎉 Today we celebrate 1 famous birthday! 🎊       │
│                                                    │
│  ╔════════════════════════════════════════════╗   │
│  ║  🎂  Gordon Ramsay                         ║   │
│  ║      Born: 8 November, 1966               ║   │
│  ║      Turning 60 today! 🎉                 ║   │
│  ║      👑 Living Legend                     ║   │
│  ╚════════════════════════════════════════════╝   │
│                                                    │
│  📋 Full November Birthday List (31 rows table)   │
│  ┌────────────┬──────────────────────┬────────┐   │
│  │ Date       │ Name                 │ Born   │   │
│  ├────────────┼──────────────────────┼────────┤   │
│  │ 1 November │ Aishwarya Rai...     │ 1973   │   │
│  │ 2 November │ Shah Rukh Khan       │ 1965   │   │
│  │ ...        │ ...                  │ ...    │   │
│  └────────────┴──────────────────────┴────────┘   │
│                                                    │
├────────────────────────────────────────────────────┤
│  🤖 Automated by Tanmoy Dey's Birthday Notifier   │
└────────────────────────────────────────────────────┘
```

---

## ⏰ Schedule It — Run Daily Automatically

### Option A — Windows Task Scheduler

```cmd
schtasks /create ^
  /tn "BirthdayNotifier" ^
  /tr "python C:\Practices\Tanmoy-Skynet\email_notifier\birthday_notifier.py" ^
  /sc daily /st 08:00 /f
```
> Runs every morning at **8:00 AM** automatically.

### Option B — Azure DevOps Scheduled Pipeline

```yaml
# azure-pipelines-birthday.yml
schedules:
  - cron: "30 2 * * *"       # 8:00 AM IST = 2:30 AM UTC
    displayName: Daily Birthday Notification
    branches:
      include: [main]

trigger: none

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: birthday-notifier-secrets   # Variable group in Azure DevOps

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'

  - script: pip install -r email_notifier/requirements.txt
    displayName: '📦 Install Dependencies'

  - script: python email_notifier/birthday_notifier.py
    displayName: '🎂 Send Birthday Email'
    env:
      SENDER_EMAIL:        $(SENDER_EMAIL)
      SENDER_APP_PASSWORD: $(SENDER_APP_PASSWORD)
```

### Option C — GitHub Actions

```yaml
# .github/workflows/birthday-notifier.yml
name: 🎂 Daily Birthday Notifier

on:
  schedule:
    - cron: '30 2 * * *'   # 8:00 AM IST
  workflow_dispatch:         # Manual trigger from GitHub UI

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r email_notifier/requirements.txt

      - name: Run Birthday Notifier
        run: python email_notifier/birthday_notifier.py
        env:
          SENDER_EMAIL:        ${{ secrets.SENDER_EMAIL }}
          SENDER_APP_PASSWORD: ${{ secrets.SENDER_APP_PASSWORD }}
```

> Add secrets in **GitHub → Settings → Secrets and Variables → Actions → New secret**

---

## 🏆 Milestone Badges (Auto-assigned by Age)

| Age Range | Badge | Label |
|:---:|:---:|:---|
| Under 30 | 🌟 | Rising Star |
| 30 – 49 | 💫 | In Their Prime |
| 50 – 69 | 🏆 | Legend in Making |
| 70 – 89 | 👑 | Living Legend |
| 90 + | 🌌 | Icon of History |

---

## 🔧 Troubleshooting

| ❌ Error | 🔍 Cause | ✅ Fix |
|:---|:---|:---|
| `SMTPAuthenticationError` | Using Gmail login password | Generate App Password at [apppasswords](https://myaccount.google.com/apppasswords) |
| `SENDER_EMAIL not set` | Env variable missing | Run `set SENDER_EMAIL=...` or create `.env` |
| `FileNotFoundError` | CSV not in script folder | Keep CSV in same folder as `birthday_notifier.py` |
| `ModuleNotFoundError: dotenv` | Dependency missing | Run `pip install -r requirements.txt` |
| Email lands in Spam | First time sending | Mark as "Not Spam" once; Gmail will learn |
| `SMTPConnectError` | No internet / firewall | Check port 587 is not blocked |

---

## 🤝 Contributing

```bash
# 1. Fork the repo
# 2. Create a feature branch (Trunk-Based Development)
git checkout -b feature/add-december-birthdays

# 3. Make changes and commit
git add .
git commit -m "feat: add December famous birthdays CSV"

# 4. Push and open PR
git push origin feature/add-december-birthdays
# → Open PR → Review → Approve → Merge to main → 🚀 Auto-runs pipeline
```

---

## 📄 License

MIT License — free to use, modify, and share.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00BCF2,100:0078D4&height=120&section=footer&animation=fadeIn" width="100%"/>

*Built with ❤️ by **[Tanmoy Dey](https://github.com/tanmoyde2010-ops)** — Senior DevOps Engineer*

⭐ *Star this repo if it helped you!*

</div>

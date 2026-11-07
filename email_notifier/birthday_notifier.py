"""
╔══════════════════════════════════════════════════════════════════╗
║          🎂  Famous Birthday Email Notifier                     ║
║          Tanmoy Dey | github.com/tanmoyde2010-ops               ║
╠══════════════════════════════════════════════════════════════════╣
║  Reads november_famous_birthdays.csv, finds today's             ║
║  celebrity birthdays, and sends a styled HTML email             ║
║  to bosemalabika363@gmail.com via Gmail SMTP.                   ║
╚══════════════════════════════════════════════════════════════════╝

QUICK START:
  1. pip install -r requirements.txt
  2. Set env vars:
       Windows CMD ► set SENDER_EMAIL=you@gmail.com
                    set SENDER_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
     OR create a .env file (copy .env.example → .env and fill in)
  3. python birthday_notifier.py

HOW TO GET GMAIL APP PASSWORD:
  → https://myaccount.google.com/apppasswords
  (Requires 2-Step Verification to be ON)
"""

import csv
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# ──────────────────────────────────────────────────────────────────
# Try loading .env file (optional — falls back to real env vars)
# ──────────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("🔐 Loaded credentials from .env file")
except ImportError:
    print("ℹ️  dotenv not found — reading from environment variables")

# ──────────────────────────────────────────────────────────────────
# CONFIGURATION  (Edit only if needed)
# ──────────────────────────────────────────────────────────────────
SENDER_EMAIL        = os.getenv("SENDER_EMAIL", "")
SENDER_APP_PASSWORD = os.getenv("SENDER_APP_PASSWORD", "")
RECIPIENT_EMAIL     = "bosemalabika363@gmail.com"
CSV_FILE            = Path(__file__).parent / "november_famous_birthdays.csv"
SMTP_HOST           = "smtp.gmail.com"
SMTP_PORT           = 587

# Milestone label based on current age
def milestone_label(age: int) -> str:
    if age < 30:   return "🌟 Rising Star"
    if age < 50:   return "💫 In Their Prime"
    if age < 70:   return "🏆 Legend in Making"
    if age < 90:   return "👑 Living Legend"
    return "🌌 Icon of History"


# ──────────────────────────────────────────────────────────────────
# STEP 1  Read CSV → find today's birthdays
# ──────────────────────────────────────────────────────────────────
def get_todays_birthdays() -> list[dict]:
    today        = datetime.now()
    today_day    = today.day
    today_month  = today.strftime("%B")   # e.g. "November"
    results      = []

    if not CSV_FILE.exists():
        print(f"❌ CSV not found: {CSV_FILE}")
        sys.exit(1)

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            parts = row["Birth Date (November)"].strip().split()
            if len(parts) == 2 and int(parts[0]) == today_day and parts[1] == today_month:
                birth_year = int(row["Birth Year"])
                results.append({
                    "name"      : row["Name"].strip(),
                    "birth_year": birth_year,
                    "age"       : today.year - birth_year,
                    "date"      : row["Birth Date (November)"].strip(),
                })
    return results


# ──────────────────────────────────────────────────────────────────
# STEP 2  Read CSV → full list for the table in email
# ──────────────────────────────────────────────────────────────────
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


# ──────────────────────────────────────────────────────────────────
# STEP 3  Build beautiful HTML email
# ──────────────────────────────────────────────────────────────────
def build_html(birthdays: list[dict], all_celebs: list[dict], today: datetime) -> str:
    today_str  = today.strftime("%A, %d %B %Y")

    # ── Today's birthday cards ──────────────────────────────────
    if birthdays:
        cards = ""
        for p in birthdays:
            cards += f"""
            <div style="
                background: linear-gradient(135deg,#667eea,#764ba2);
                border-radius:16px; padding:24px; margin:14px 0;
                color:#fff; box-shadow:0 8px 28px rgba(102,126,234,.35);
            ">
              <table cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td width="64" valign="middle" style="font-size:52px;">🎂</td>
                  <td valign="middle" style="padding-left:14px;">
                    <div style="font-size:22px;font-weight:800;">{p['name']}</div>
                    <div style="margin-top:5px;opacity:.85;font-size:14px;">
                      Born: <strong>{p['date']}, {p['birth_year']}</strong>
                      &nbsp;|&nbsp; Turning <strong>{p['age']}</strong> today! 🎉
                    </div>
                    <span style="
                      display:inline-block;margin-top:9px;
                      background:rgba(255,255,255,.22);border-radius:20px;
                      padding:4px 14px;font-size:13px;">
                      {milestone_label(p['age'])}
                    </span>
                  </td>
                </tr>
              </table>
            </div>"""

        hero = f"""
        <p style="color:#444;font-size:16px;line-height:1.7;">
          🎉 Today — <strong>{today_str}</strong> — we celebrate
          <strong>{len(birthdays)}</strong> famous
          {'birthday' if len(birthdays)==1 else 'birthdays'}! 🎊
        </p>
        {cards}"""
    else:
        hero = f"""
        <div style="text-align:center;padding:40px;background:#f4f7ff;
                    border-radius:16px;color:#777;">
          <div style="font-size:60px;">📅</div>
          <h3 style="color:#999;margin-top:14px;">
            No famous birthdays found for today<br/>({today_str})
          </h3>
          <p>Check back tomorrow — a new celebrity birthday awaits! 🌟</p>
        </div>"""

    # ── Full table rows ─────────────────────────────────────────
    table_rows = ""
    for i, c in enumerate(all_celebs):
        bg = "#f0f5ff" if i % 2 == 0 else "#ffffff"
        table_rows += f"""
        <tr style="background:{bg};">
          <td style="padding:7px 12px;color:#555;">{c['date']}</td>
          <td style="padding:7px 12px;color:#222;font-weight:500;">{c['name']}</td>
          <td style="padding:7px 12px;color:#555;">{c['birth_year']}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>🎂 Famous Birthdays Today</title>
</head>
<body style="margin:0;padding:0;font-family:'Segoe UI',Arial,sans-serif;background:#eef2ff;">

<table width="100%" cellpadding="0" cellspacing="0" style="padding:30px 0;background:#eef2ff;">
 <tr><td align="center">
  <table width="640" cellpadding="0" cellspacing="0" style="
      background:#fff;border-radius:24px;
      overflow:hidden;box-shadow:0 4px 32px rgba(0,0,0,.09);">

    <!-- HEADER -->
    <tr>
      <td style="
          background:linear-gradient(135deg,#0078D4 0%,#00BCF2 100%);
          padding:38px 40px;text-align:center;">
        <div style="font-size:60px;margin-bottom:6px;">🎂</div>
        <h1 style="color:#fff;margin:0;font-size:30px;font-weight:800;">
          Famous Birthdays Today!
        </h1>
        <p style="color:rgba(255,255,255,.85);margin:8px 0 0 0;font-size:16px;">
          {today_str}
        </p>
      </td>
    </tr>

    <!-- BODY — today's cards -->
    <tr><td style="padding:30px 36px 10px 36px;">{hero}</td></tr>

    <!-- DIVIDER -->
    <tr><td style="padding:0 36px;">
      <hr style="border:none;border-top:1px solid #e8edf8;margin:10px 0 24px;"/>
    </td></tr>

    <!-- FULL NOVEMBER TABLE -->
    <tr>
      <td style="padding:0 36px 32px 36px;">
        <div style="
            background:#f8faff;border-radius:14px;
            padding:22px;border-left:4px solid #0078D4;">
          <h3 style="margin:0 0 16px 0;color:#0078D4;font-size:15px;">
            📋 Full November Celebrity Birthday List
          </h3>
          <table width="100%" cellpadding="0" cellspacing="0"
                 style="border-collapse:collapse;font-size:13px;">
            <tr style="background:#0078D4;color:#fff;">
              <th align="left" style="padding:9px 12px;border-radius:8px 0 0 0;">
                📅 Date
              </th>
              <th align="left" style="padding:9px 12px;">🌟 Name</th>
              <th align="left" style="padding:9px 12px;border-radius:0 8px 0 0;">
                🎂 Born
              </th>
            </tr>
            {table_rows}
          </table>
        </div>
      </td>
    </tr>

    <!-- FOOTER -->
    <tr>
      <td style="
          background:linear-gradient(135deg,#0078D4 0%,#00BCF2 100%);
          padding:22px 36px;text-align:center;">
        <p style="color:rgba(255,255,255,.9);margin:0;font-size:13px;">
          🤖 Automated by <strong>Tanmoy Dey's Birthday Notifier</strong>
          &nbsp;|&nbsp; github.com/tanmoyde2010-ops
        </p>
        <p style="color:rgba(255,255,255,.65);margin:5px 0 0 0;font-size:12px;">
          Powered by Python 3 · Gmail SMTP · CSV Data Source
        </p>
      </td>
    </tr>

  </table>
 </td></tr>
</table>

</body>
</html>"""


# ──────────────────────────────────────────────────────────────────
# STEP 4  Send email via Gmail SMTP
# ──────────────────────────────────────────────────────────────────
def send_email(subject: str, html_body: str) -> bool:
    if not SENDER_EMAIL or not SENDER_APP_PASSWORD:
        print("\n❌  Credentials not set!")
        print("    Run the following commands first:\n")
        print("    Windows CMD:")
        print("      set SENDER_EMAIL=your@gmail.com")
        print("      set SENDER_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx\n")
        print("    Or create a .env file (see .env.example)\n")
        return False

    msg                  = MIMEMultipart("alternative")
    msg["Subject"]       = subject
    msg["From"]          = f"🎂 Birthday Notifier <{SENDER_EMAIL}>"
    msg["To"]            = RECIPIENT_EMAIL
    msg["X-Mailer"]      = "Tanmoy-Skynet Birthday Bot"
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        print(f"📡 Connecting to {SMTP_HOST}:{SMTP_PORT} ...")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as srv:
            srv.ehlo()
            srv.starttls()
            srv.ehlo()
            srv.login(SENDER_EMAIL, SENDER_APP_PASSWORD)
            srv.sendmail(SENDER_EMAIL, [RECIPIENT_EMAIL], msg.as_string())
        print(f"✅ Email delivered to → {RECIPIENT_EMAIL}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed — use a Gmail App Password, not your login password.")
        print("   Get one → https://myaccount.google.com/apppasswords")
        return False
    except smtplib.SMTPConnectError:
        print("❌ Could not connect to Gmail SMTP. Check your internet connection.")
        return False
    except smtplib.SMTPException as exc:
        print(f"❌ SMTP error: {exc}")
        return False
    except Exception as exc:
        print(f"❌ Unexpected error: {exc}")
        return False


# ──────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────
def main() -> None:
    print("=" * 62)
    print("   🎂  Famous Birthday Email Notifier  |  Tanmoy-Skynet")
    print("=" * 62)

    today = datetime.now()
    print(f"📅 Today          : {today.strftime('%A, %d %B %Y')}")
    print(f"📂 CSV source     : {CSV_FILE.name}")
    print(f"📧 Recipient      : {RECIPIENT_EMAIL}")
    print("-" * 62)

    birthdays  = get_todays_birthdays()
    all_celebs = get_full_list()

    if birthdays:
        print(f"🎉 Birthday(s) today  → {len(birthdays)} found:")
        for b in birthdays:
            print(f"   🎂 {b['name']} — born {b['birth_year']}  "
                  f"(turns {b['age']}  |  {milestone_label(b['age'])})")
        subject = (
            f"🎂 Famous Birthdays Today ({today.strftime('%d %b %Y')}) — "
            + ", ".join(b["name"] for b in birthdays)
        )
    else:
        print("📅 No famous birthdays today in the list.")
        subject = f"📅 No Famous Birthdays Today — {today.strftime('%d %B %Y')}"

    print("-" * 62)
    html = build_html(birthdays, all_celebs, today)
    ok   = send_email(subject, html)
    print("=" * 62)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

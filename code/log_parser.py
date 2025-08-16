#!/usr/bin/env python3
"""
log_parser.py

Parses phishing simulation logs:
 - GoPhish JSON logs (logs/gophish_logs.json)
 - Pixel open logs (logs/email_opens.log)
 - Credentials capture logs (logs/credentials.log)

Generates:
 - logs/phishing_report.csv

Usage:
    python code/log_parser.py
"""

import csv
import json
import re
from datetime import datetime
from pathlib import Path

# File paths (relative to repo root)
BASE = Path(__file__).resolve().parents[1]
LOGS_DIR = BASE / "logs"
GOPHISH_JSON = LOGS_DIR / "gophish_logs.json"
PIXEL_LOG = LOGS_DIR / "email_opens.log"
CREDENTIALS_LOG = LOGS_DIR / "credentials.log"
OUTPUT_CSV = LOGS_DIR / "phishing_report.csv"


def parse_gophish(json_path: Path) -> dict:
    """Parse GoPhish JSON events keyed by recipient email."""
    events = {}
    if not json_path.exists():
        print(f"[!] Missing: {json_path}")
        return events

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[!] Invalid JSON: {e}")
        return events

    for entry in data:
        email = entry.get("email", "unknown@example.com")
        events.setdefault(email, []).append({
            "source": "gophish",
            "status": entry.get("status", ""),
            "time": entry.get("time", "")
        })
    return events


def parse_pixel_log(pixel_path: Path) -> dict:
    """Parse pixel logs mapping email/ID to open timestamps."""
    opens = {}
    if not pixel_path.exists():
        print(f"[!] Missing: {pixel_path}")
        return opens

    with pixel_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(
                r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - .*?: (?P<id>.+)$",
                line
            )
            if m:
                ts = m.group("ts")
                rid = m.group("id").strip()
                email = rid if "@" in rid else rid
                opens.setdefault(email, []).append(ts)
    return opens


def parse_credentials_log(creds_path: Path) -> dict:
    """Parse credentials log mapping email/username to submissions."""
    creds = {}
    if not creds_path.exists():
        print(f"[!] Missing: {creds_path}")
        return creds

    with creds_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.match(
                r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - .*Username: (?P<user>[^ ]+).*Password: (?P<pwd>.*)$",
                line
            )
            if m:
                ts = m.group("ts")
                user = m.group("user").strip()
                pwd = m.group("pwd").strip()
                creds.setdefault(user, []).append({
                    "time": ts,
                    "password": pwd
                })
    return creds


def consolidate(gophish, pixels, creds) -> list:
    """Merge data sources into a per-recipient report."""
    emails = set(gophish) | {k for k in pixels if "@" in k} | set(creds)
    rows = []

    for email in sorted(emails):
        ev = gophish.get(email, [])
        op = pixels.get(email, [])
        cr = creds.get(email, [])

        sent = any("sent" in e["status"].lower() for e in ev)
        opened = bool(op) or any("open" in e["status"].lower() for e in ev)
        clicked = any("click" in e["status"].lower() for e in ev)
        submitted = bool(cr) or any("submitted" in e["status"].lower() for e in ev)

        rows.append({
            "Email/Recipient": email,
            "Email Sent": "Yes" if sent else "No",
            "Email Sent Timestamp": next((e["time"] for e in ev if "sent" in e["status"].lower()), ""),
            "Opened": "Yes" if opened else "No",
            "First Open Timestamp": op[0] if op else next((e["time"] for e in ev if "open" in e["status"].lower()), ""),
            "Clicked Link": "Yes" if clicked else "No",
            "First Click Timestamp": next((e["time"] for e in ev if "click" in e["status"].lower()), ""),
            "Credentials Submitted": "Yes" if submitted else "No",
            "First Submit Timestamp": cr[0]["time"] if cr else next((e["time"] for e in ev if "submitted" in e["status"].lower()), ""),
            "Captured Password (sample)": cr[0]["password"] if cr else ""
        })
    return rows


def write_csv(rows: list, out_path: Path):
    """Write report to CSV."""
    headers = [
        "Email/Recipient", "Email Sent", "Email Sent Timestamp",
        "Opened", "First Open Timestamp", "Clicked Link", "First Click Timestamp",
        "Credentials Submitted", "First Submit Timestamp", "Captured Password (sample)"
    ]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)
    print(f"[+] CSV report written to {out_path}")


def main():
    print("[*] Parsing GoPhish logs...")
    gophish_data = parse_gophish(GOPHISH_JSON)

    print("[*] Parsing pixel opens...")
    pixel_data = parse_pixel_log(PIXEL_LOG)

    print("[*] Parsing credentials...")
    creds_data = parse_credentials_log(CREDENTIALS_LOG)

    print("[*] Consolidating...")
    report_rows = consolidate(gophish_data, pixel_data, creds_data)

    print("[*] Writing CSV...")
    write_csv(report_rows, OUTPUT_CSV)


if __name__ == "__main__":
    main()

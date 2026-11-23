import csv
from pathlib import Path
from datetime import datetime
import pandas as pd


def read_csv_rows(path):
    if not path.exists():
        raise FileNotFoundError(f"Required CSV file not found: {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def load_contacts(path):
    rows = read_csv_rows(path)
    contacts = {}
    for row in rows:
        email = row.get("email", "").strip().lower()
        if email:
            contacts[email] = row
    return contacts


def load_reminders(path):
    return read_csv_rows(path)


def save_reminder_status(path, reminder_id, status, sent_at=""):
    """Update one reminder row while preserving the other rows."""
    rows = read_csv_rows(path)
    fieldnames = list(rows[0].keys()) if rows else [
        "reminder_id", "email", "send_at", "template_file", "status", "sent_at"
    ]
    if "sent_at" not in fieldnames:
        fieldnames.append("sent_at")

    for row in rows:
        if row.get("reminder_id") == reminder_id:
            row["status"] = status
            row["sent_at"] = sent_at

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_report(report_path, record):
    report_path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame([record])
    frame.to_csv(
        report_path,
        mode="a",
        header=not report_path.exists(),
        index=False,
        encoding="utf-8"
    )


def parse_send_time(value):
    """Expected format: YYYY-MM-DD HH:MM (local computer time)."""
    return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M")

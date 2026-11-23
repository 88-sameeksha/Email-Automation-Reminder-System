import logging
from datetime import datetime
from pathlib import Path

from src.data_manager import (
    load_contacts, load_reminders, parse_send_time,
    save_reminder_status, append_report
)
from src.template_engine import render_template
from src.email_sender import send_email


def process_due_reminders(base_dir, dry_run=False):
    data_dir = base_dir / "data"
    contacts = load_contacts(data_dir / "contacts.csv")
    reminder_path = data_dir / "reminders.csv"
    reminders = load_reminders(reminder_path)
    now = datetime.now()
    processed = 0

    for reminder in reminders:
        reminder_id = reminder.get("reminder_id", "").strip()
        status = reminder.get("status", "pending").strip().lower()
        if status != "pending":
            continue

        try:
            due_time = parse_send_time(reminder["send_at"])
            if due_time > now:
                continue

            recipient = reminder["email"].strip().lower()
            if recipient not in contacts:
                raise ValueError(f"No contact found for {recipient}")

            template_name = reminder["template_file"].strip()
            template_path = base_dir / "templates" / template_name
            subject, body = render_template(template_path, contacts[recipient])

            if dry_run:
                result = "dry_run"
                logging.info("[DRY RUN] Would send reminder %s to %s | Subject: %s",
                             reminder_id, recipient, subject)
                # Keep reminder pending so a later live run can send it.
            else:
                send_email(recipient, subject, body)
                result = "sent"
                save_reminder_status(
                    reminder_path, reminder_id, "sent",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

            append_report(base_dir / "outputs" / "email_report.csv", {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reminder_id": reminder_id,
                "recipient": recipient,
                "subject": subject,
                "status": result,
                "details": "Simulation only" if dry_run else "Accepted by SMTP server"
            })
            processed += 1

        except Exception as error:
            logging.exception("Reminder %s failed: %s", reminder_id, error)
            if not dry_run and reminder_id:
                save_reminder_status(
                    reminder_path, reminder_id, "failed",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            append_report(base_dir / "outputs" / "email_report.csv", {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reminder_id": reminder_id,
                "recipient": reminder.get("email", ""),
                "subject": "",
                "status": "failed",
                "details": str(error)
            })

    logging.info("Check complete. Reminders processed: %s", processed)
    return processed

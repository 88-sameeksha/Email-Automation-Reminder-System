import argparse
import logging
import time
from pathlib import Path

import schedule
from dotenv import load_dotenv

from src.automation import process_due_reminders
from src.config import configure_logging

BASE_DIR = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description="Email Automation & Reminder System")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simulate email sending; no email is sent and reminders stay pending.")
    parser.add_argument("--once", action="store_true",
                        help="Check due reminders once, then exit.")
    parser.add_argument("--interval", type=int, default=30,
                        help="Scheduler polling interval in seconds (default: 30).")
    args = parser.parse_args()

    load_dotenv(BASE_DIR / ".env")
    configure_logging(BASE_DIR / "logs" / "automation.log")
    logging.info("Email Automation & Reminder System started.")
    logging.info("Mode: %s", "DRY RUN" if args.dry_run else "LIVE SMTP")

    def job():
        process_due_reminders(BASE_DIR, dry_run=args.dry_run)

    if args.once:
        job()
        logging.info("One-time check completed.")
        return

    schedule.every(max(5, args.interval)).seconds.do(job)
    print(f"Scheduler running. Checking every {max(5, args.interval)} seconds.")
    print("Press Ctrl+C to stop.")
    job()  # Process already-due reminders immediately.
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Scheduler stopped by user.")
        print("\nScheduler stopped.")


if __name__ == "__main__":
    main()

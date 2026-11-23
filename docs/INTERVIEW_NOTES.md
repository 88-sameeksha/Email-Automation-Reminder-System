# Interview notes

## 30-second explanation
I built a Python-based Email Automation & Reminder System. It reads contacts and reminder schedules from CSV files, personalizes reusable templates, checks which reminders are due, and either simulates the send or submits the message through SMTP. It records activity in logs and a CSV report.

## Main modules
- `data_manager.py`: CSV loading, reminder status updates, report writing.
- `template_engine.py`: fills placeholders such as `{name}` and `{company}`.
- `email_sender.py`: creates an EmailMessage and sends it through SMTP with STARTTLS.
- `automation.py`: coordinates due-time checks, sending, status changes, and reporting.
- `main.py`: command-line options and scheduler loop.

## Important distinction
A successful SMTP submission means the SMTP server accepted the message for processing; it does not guarantee delivery to the recipient's inbox.

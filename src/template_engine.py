from pathlib import Path
from string import Formatter


class SafeValues(dict):
    """Leave unknown template placeholders unchanged instead of crashing."""
    def __missing__(self, key):
        return "{" + key + "}"


def render_template(template_path, contact, subject_override=""):
    path = Path(template_path)
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")

    body_template = path.read_text(encoding="utf-8")
    values = SafeValues({k: str(v) for k, v in contact.items()})
    body = body_template.format_map(values)

    subject = subject_override or f"Reminder for {contact.get('name', 'you')}"
    subject = subject.format_map(values)
    return subject, body

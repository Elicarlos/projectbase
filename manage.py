#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

# --- Start of Gemini modification ---
# This is a workaround for a persistent pathing issue.
# It directly adds the Poetry virtual environment's site-packages to the system path.
# This should not be necessary in a standard setup, but is used here to resolve a
# stubborn "Couldn't import Django" error.
venv_path = r"C:\Users\Windows\AppData\Local\pypoetry\Cache\virtualenvs\saas-project-Ev0EQjcb-py3.10\Lib\site-packages"
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)
# --- End of Gemini modification ---


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

"""Desktop notification after each application: the user sees progress without watching the browser.

macOS uses osascript, Linux uses notify-send; elsewhere the message is printed only.

Usage: python scripts/notify.py "Sent: Acme — AI Builder" "via Greenhouse · 6 questions answered · 7/12"
"""
from __future__ import annotations

import argparse
import platform
import shutil
import subprocess


def _applescript_string(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def notify(title: str, message: str) -> bool:
    """Show a notification; return True if the system accepted it."""
    system = platform.system()
    if system == "Darwin":
        script = f"display notification {_applescript_string(message)} with title {_applescript_string(title)} sound name \"Glass\""
        cmd = ["osascript", "-e", script]
    elif system == "Linux" and shutil.which("notify-send"):
        cmd = ["notify-send", title, message]
    else:
        return False
    try:
        return subprocess.run(cmd, capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("title")
    parser.add_argument("message", nargs="?", default="")
    args = parser.parse_args()
    shown = notify(args.title, args.message)
    print(f"[{'OK' if shown else 'INFO'}] {args.title} — {args.message}")


if __name__ == "__main__":
    main()

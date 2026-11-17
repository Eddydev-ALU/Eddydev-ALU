#!/usr/bin/env python3
"""Rewrite the daily quote and fun fact section of README.md.

Picks one quote and one fact per day, cycling through scripts/content.json.
Quotes and facts use different list lengths, so pairings keep changing.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CONTENT = ROOT / "scripts" / "content.json"

START = "<!--DAILY:START-->"
END = "<!--DAILY:END-->"


def main() -> int:
    data = json.loads(CONTENT.read_text(encoding="utf-8"))
    today = datetime.now(timezone.utc).date()
    day = today.toordinal()

    quote = data["quotes"][day % len(data["quotes"])]
    fact = data["facts"][day % len(data["facts"])]

    block = (
        f"{START}\n"
        f"> \"{quote['text']}\"\n"
        f"> <br>— *{quote['author']}*\n"
        f"\n"
        f"**Did you know?** {fact}\n"
        f"\n"
        f"<sub>Refreshed automatically on {today.strftime('%B %d, %Y')} (UTC)</sub>\n"
        f"{END}"
    )

    text = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(text):
        print("Markers not found in README.md", file=sys.stderr)
        return 1

    new_text = pattern.sub(lambda _: block, text)
    if new_text != text:
        README.write_text(new_text, encoding="utf-8")
        print("README updated")
    else:
        print("No change")
    return 0


if __name__ == "__main__":
    sys.exit(main())

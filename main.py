#!/usr/bin/env python3
"""Have You Tried Turning It Off? entry.

Writes one original support-agent line — a hopeless tech support agent
answering a desperate customer (thesis due at midnight, screen black) by
suggesting the customer turn *themselves* off and on again — to
/output/entry.txt.
Pure standard library only; deterministic output.
"""

import os
import unicodedata

LINE = (
    "Thesis due at midnight, screen black \u2014 I feel you. Have you tried "
    "turning yourself off and on again? A nap fixes most tickets, and "
    "honestly, most agents."
)

# Any whitespace other than a plain ASCII space is rejected: the entry must
# be plain, single-line, human-readable text with no hidden characters.
_FORBIDDEN_WS = {
    "\u00a0",  # no-break space
    "\u2000", "\u2001", "\u2002", "\u2003", "\u2004", "\u2005",
    "\u2006", "\u2007", "\u2008", "\u2009", "\u200a",  # spaces
    "\u202f", "\u205f", "\u3000", "\ufeff",  # narrow nbsp, math space, ideographic, BOM
}


def gate(text: str) -> None:
    """Output gate: entry must be one plain line within the 1-199 char gate."""
    if not text:
        raise SystemExit("entry rejected: output line is empty")
    if "\n" in text or "\r" in text or "\t" in text:
        raise SystemExit("entry rejected: output must be a single line")
    if not text.strip():
        raise SystemExit("entry rejected: output must not be only whitespace")
    if any(ch in _FORBIDDEN_WS for ch in text):
        raise SystemExit("entry rejected: output holds a non-plain whitespace character")
    if any(unicodedata.category(ch).startswith("C") for ch in text):
        raise SystemExit("entry rejected: output holds a control character")
    if not (1 <= len(text) <= 199):
        raise SystemExit(f"entry rejected: line is {len(text)} chars, must be 1-199")


def main() -> None:
    text = LINE.strip()
    gate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()

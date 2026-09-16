#!/usr/bin/env python3
"""Counts the assessed words in the report content.

Counted: headings, paragraphs, lists and tables in sections 1-8.
Not counted: the front page, contents, figures and their captions, code
(fenced blocks and inline code), the reference list and the appendices.
"""
import re
import sys
from pathlib import Path

CONTENT = Path(__file__).parent / "content"
WORD = re.compile(r"[A-Za-z0-9ΛλΘΟ][\w'’\-–./()≠←=]*")
LOW, HIGH = 3600, 4400  # 4,000 words ±10%


def count(text: str) -> int:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)       # fenced code
    text = re.sub(r"`[^`]*`", " ", text)                       # inline code
    text = re.sub(r"^!\[.*?\]\(.*?\)\s*$", " ", text, flags=re.M)  # figures
    text = re.sub(r"^\|?\s*-{3,}.*$", " ", text, flags=re.M)   # table rules
    text = text.replace("Table:", " ")
    text = re.sub(r"[#>*|]", " ", text)
    return len(WORD.findall(text))


def main() -> int:
    total = 0
    rows = []
    for path in sorted(CONTENT.glob("0*.md")):
        n = count(path.read_text(encoding="utf-8"))
        rows.append((path.stem, n))
        total += n
    for stem, n in rows:
        print(f"  {stem:<36}{n:>6}")
    print(f"  {'TOTAL':<36}{total:>6}")
    status = "within" if LOW <= total <= HIGH else "OUTSIDE"
    print(f"  {status} the permitted range {LOW:,}–{HIGH:,}")
    print(f"TOTAL_WORDS={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

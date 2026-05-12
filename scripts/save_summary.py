#!/usr/bin/env python3
"""Write stdin to <work-dir>/summary.md (UTF-8).

Used after the model composes its user-facing answer so summary.md matches
that text (watch.py only persists the transcript).
"""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: save_summary.py <work-dir>", file=sys.stderr)
        return 1
    work = Path(sys.argv[1]).expanduser().resolve()
    work.mkdir(parents=True, exist_ok=True)
    text = sys.stdin.read()
    if text and not text.endswith("\n"):
        text += "\n"
    (work / "summary.md").write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

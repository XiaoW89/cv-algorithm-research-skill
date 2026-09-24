#!/usr/bin/env python3
"""Initialize a CV algorithm research workspace without overwriting existing files."""

from pathlib import Path
from datetime import datetime, timezone
import shutil
import sys

ROOT = Path("research")

DIRS = [
    "problem",
    "literature",
    "datasets",
    "models",
    "hypotheses",
    "experiments",
    "failures",
    "conclusions",
]

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"

def copy_if_missing(src: Path, dst: Path):
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

def main():
    ROOT.mkdir(exist_ok=True)
    for d in DIRS:
        (ROOT / d).mkdir(exist_ok=True)

    copy_if_missing(TEMPLATES / "README.md", ROOT / "README.md")
    copy_if_missing(TEMPLATES / "STATE.md", ROOT / "STATE.md")
    copy_if_missing(TEMPLATES / "problem.md", ROOT / "problem" / "definition.md")
    copy_if_missing(TEMPLATES / "problem.md", ROOT / "problem" / "constraints.md")

    now = datetime.now(timezone.utc).isoformat()
    state = ROOT / "STATE.md"
    text = state.read_text(encoding="utf-8")
    if "created:" in text and "created:\n" in text:
        text = text.replace("created:\n", f"created: {now}\n", 1)
    if "last_updated:" in text and "last_updated:\n" in text:
        text = text.replace("last_updated:\n", f"last_updated: {now}\n", 1)
    state.write_text(text, encoding="utf-8")

    print(f"Research workspace ready: {ROOT.resolve()}")

if __name__ == "__main__":
    main()

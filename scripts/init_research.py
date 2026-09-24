#!/usr/bin/env python3
"""Initialize a CV algorithm research workspace without overwriting existing files."""

from pathlib import Path
from datetime import datetime, timezone
import argparse

DIRS = [
    "problem",
    "literature",
    "datasets",
    "models",
    "hypotheses",
    "experiments",
    "failures",
    "conclusions",
    "feasibility",
    "evaluation",
    "delivery",
]

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"

def copy_if_missing(src: Path, dst: Path, now: str):
    """Exclusive creation preserves existing bytes, timestamps, and user history."""
    text = src.read_text(encoding="utf-8")
    if src.name == "STATE.md":
        text = text.replace("  created:\n", f"  created: {now}\n", 1)
        text = text.replace("  last_updated:\n", f"  last_updated: {now}\n", 1)
    try:
        with dst.open("x", encoding="utf-8") as stream:
            stream.write(text)
    except FileExistsError:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("research"))
    args = parser.parse_args()
    root = args.root
    root.mkdir(parents=True, exist_ok=True)
    for d in DIRS:
        (root / d).mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    for template, target in {
        "README.md": "README.md",
        "STATE.md": "STATE.md",
        "problem.md": "problem/definition.md",
        "constraints.md": "problem/constraints.md",
        "acceptance.md": "problem/acceptance.md",
    }.items():
        copy_if_missing(TEMPLATES / template, root / target, now)
    print(f"Research workspace ready: {root.resolve()}")

if __name__ == "__main__":
    main()

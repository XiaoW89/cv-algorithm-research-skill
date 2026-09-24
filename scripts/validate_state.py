#!/usr/bin/env python3
"""Lightweight validation for the research workspace."""

from pathlib import Path
import sys

ROOT = Path("research")
REQUIRED = [
    ROOT / "README.md",
    ROOT / "STATE.md",
    ROOT / "problem" / "definition.md",
]

def main():
    missing = [str(p) for p in REQUIRED if not p.exists()]
    if missing:
        print("Missing required files:")
        for p in missing:
            print(f"  - {p}")
        return 1

    text = (ROOT / "STATE.md").read_text(encoding="utf-8")
    required_keys = ["research_stage:", "next_action:", "best_checkpoint:"]
    missing_keys = [k for k in required_keys if k not in text]
    if missing_keys:
        print("STATE.md is missing keys:")
        for k in missing_keys:
            print(f"  - {k}")
        return 1

    print("Research state is structurally valid.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

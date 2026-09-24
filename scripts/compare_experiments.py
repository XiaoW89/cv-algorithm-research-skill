#!/usr/bin/env python3
"""Extract experiment metadata for manual comparison.

This intentionally avoids inventing a universal experiment score.
"""

from pathlib import Path
import re

ROOT = Path("research/experiments")

def extract(text, heading):
    pattern = rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)"
    m = re.search(pattern, text, re.MULTILINE)
    if not m:
        return ""
    return " ".join(x.strip() for x in m.group(1).splitlines()).strip()

def main():
    rows = []
    for p in sorted(ROOT.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        rows.append({
            "file": p.name,
            "id": extract(text, "ID"),
            "hypothesis": extract(text, "Hypothesis"),
            "baseline": extract(text, "Baseline"),
            "outcome": extract(text, "Actual Outcome"),
            "interpretation": extract(text, "Interpretation"),
        })

    if not rows:
        print("No experiment Markdown files found.")
        return

    headers = ["file", "id", "hypothesis", "baseline", "outcome", "interpretation"]
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        print("| " + " | ".join(r[h].replace("|", "\\|") for h in headers) + " |")

if __name__ == "__main__":
    main()

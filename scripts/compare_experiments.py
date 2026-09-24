#!/usr/bin/env python3
"""Extract experiment metadata for manual comparison.

This intentionally avoids inventing a universal experiment score.
"""

from pathlib import Path
import re
import argparse

def extract(text, heading):
    pattern = rf"^## {re.escape(heading)}[ \t]*\r?$([\s\S]*?)(?=^## |\Z)"
    m = re.search(pattern, text, re.MULTILINE)
    if not m:
        return ""
    return " ".join(x.strip() for x in m.group(1).splitlines()).strip()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("research"))
    args = parser.parse_args()
    rows = []
    for p in sorted((args.root / "experiments").glob("*.md")):
        text = p.read_text(encoding="utf-8")
        rows.append({
            "file": p.name,
            "id": extract(text, "ID"),
            "hypothesis": extract(text, "Hypothesis"),
            "baseline": extract(text, "Baseline"),
            "evaluation_data": extract(text, "Evaluation Data ID"),
            "protocol": extract(text, "Protocol ID"),
            "outcome": extract(text, "Actual Outcome"),
            "interpretation": extract(text, "Interpretation"),
        })

    if not rows:
        print("No experiment Markdown files found.")
        return

    keys = ["evaluation_data", "protocol"]
    if any(not r[k] for r in rows for k in keys):
        print("WARNING: Missing evaluation data/protocol IDs; comparability is unverified.\n")
    elif any(len({r[k] for r in rows}) > 1 for k in keys):
        print("WARNING: Evaluation data/protocol IDs differ; do not rank results directly.\n")
    else:
        print("Protocol IDs match; verify actual metric definitions and run conditions.\n")
    headers = ["file", "id", "baseline", "evaluation_data", "protocol", "outcome", "interpretation"]
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        print("| " + " | ".join(r[h].replace("|", "\\|") for h in headers) + " |")

if __name__ == "__main__":
    main()

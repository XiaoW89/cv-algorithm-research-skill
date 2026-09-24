#!/usr/bin/env python3
"""Audit a neutral sample manifest for integrity and split leakage."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SPLITS = {"train", "val", "test"}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--data-root", type=Path)
    parser.add_argument("--check-files", action="store_true")
    parser.add_argument("--hash-files", action="store_true", help="compute file SHA-256; implies --check-files")
    parser.add_argument("--require-groups", action="store_true")
    parser.add_argument("--slice-column", action="append", default=[])
    args = parser.parse_args()
    errors: list[str] = []
    warnings: list[str] = []
    counts = Counter()
    slices = {name: defaultdict(Counter) for name in args.slice_column}
    path_to_splits: defaultdict[str, set[str]] = defaultdict(set)
    group_to_splits: defaultdict[str, set[str]] = defaultdict(set)
    hash_to_splits: defaultdict[str, set[str]] = defaultdict(set)
    hash_counts = Counter()
    groups_covered = 0
    hashes_covered = 0
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    rows = 0
    root = args.data_root or args.manifest.parent
    try:
        stream = args.manifest.open(newline="", encoding="utf-8")
    except OSError as exc:
        print(json.dumps({"errors": [str(exc)]}, indent=2))
        return 1
    with stream:
        reader = csv.DictReader(stream, strict=True)
        fields = set(reader.fieldnames or [])
        if len(fields) != len(reader.fieldnames or []):
            errors.append("duplicate CSV column names")
        for field in {"sample_id", "split", "path"} - fields:
            errors.append(f"missing required column: {field}")
        for column in args.slice_column:
            if column not in fields:
                errors.append(f"requested slice column missing: {column}")
        for number, row in enumerate(reader, start=2):
            rows += 1
            if None in row or any(value is None for value in row.values()):
                errors.append(f"row {number}: inconsistent number of CSV fields")
                continue
            sample_id = (row.get("sample_id") or "").strip()
            split = (row.get("split") or "").strip().lower()
            raw_path = (row.get("path") or "").strip()
            if not sample_id:
                errors.append(f"row {number}: empty sample_id")
            elif sample_id in seen_ids:
                errors.append(f"row {number}: duplicate sample_id {sample_id!r}")
            seen_ids.add(sample_id)
            if split not in SPLITS:
                errors.append(f"row {number}: invalid split {split!r}")
            counts[split] += 1
            if not raw_path:
                errors.append(f"row {number}: empty path")
            path = (root / raw_path).resolve()
            normalized = str(path)
            if normalized in seen_paths:
                errors.append(f"row {number}: duplicate path {raw_path!r}")
            seen_paths.add(normalized)
            path_to_splits[normalized].add(split)
            group = (row.get("group_id") or "").strip()
            if args.require_groups and not group:
                errors.append(f"row {number}: group_id is required")
            if group:
                groups_covered += 1
                group_to_splits[group].add(split)
            declared_hash = (row.get("sha256") or "").strip().lower()
            if declared_hash:
                if not SHA256_RE.fullmatch(declared_hash):
                    errors.append(f"row {number}: invalid sha256")
            content_hash = declared_hash if SHA256_RE.fullmatch(declared_hash) else ""
            for column in args.slice_column:
                if column in fields:
                    slices[column][split][row[column].strip() or "<empty>"] += 1
            if args.check_files or args.hash_files:
                if not path.is_file():
                    errors.append(f"row {number}: file not found: {path}")
                elif args.hash_files:
                    try:
                        content_hash = digest(path)
                        if declared_hash and content_hash != declared_hash:
                            errors.append(f"row {number}: sha256 mismatch for {path}")
                    except OSError as exc:
                        errors.append(f"row {number}: cannot hash input: {exc}")
                        content_hash = ""
                label = row.get("label_path", "").strip()
                if label and not (root / label).is_file():
                    errors.append(f"row {number}: label file not found: {root / label}")
            if content_hash:
                hashes_covered += 1
                hash_to_splits[content_hash].add(split)
                hash_counts[content_hash] += 1
    if not rows:
        errors.append("manifest contains no samples")
    if groups_covered < rows:
        warnings.append(f"group leakage check incomplete: {groups_covered}/{rows} samples have group_id")
    if hashes_covered < rows:
        warnings.append(f"exact content check incomplete: {hashes_covered}/{rows} samples have a hash")
    for key, split_set in path_to_splits.items():
        if len(split_set) > 1:
            errors.append(f"path crosses splits: {key!r} -> {sorted(split_set)}")
    for key, split_set in group_to_splits.items():
        if len(split_set) > 1:
            errors.append(f"group crosses splits: {key!r} -> {sorted(split_set)}")
    for key, split_set in hash_to_splits.items():
        if len(split_set) > 1:
            errors.append(f"content hash crosses splits: {key!r} -> {sorted(split_set)}")
        elif hash_counts[key] > 1:
            warnings.append(f"duplicate content within one split may need review: {key!r}")
    not_performed = ["image/video decoding", "annotation semantics/geometry", "near-duplicate detection", "visual quality review"]
    if not (args.check_files or args.hash_files):
        not_performed.append("file and label-path existence")
    if not args.hash_files:
        not_performed.append("SHA-256 computation/verification (declared hashes are unverified)")
    result = {
        "manifest": str(args.manifest), "rows": rows, "split_counts": dict(counts),
        "slice_counts": {key: {split: dict(count) for split, count in value.items()} for key, value in slices.items()},
        "checks": {"files": bool(args.check_files or args.hash_files), "hashes": bool(args.hash_files),
                    "groups_required": bool(args.require_groups)},
        "checks_not_performed": not_performed,
        "errors": errors, "warnings": warnings,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(json.dumps({"errors": [str(exc)]}, ensure_ascii=False))
        sys.exit(1)

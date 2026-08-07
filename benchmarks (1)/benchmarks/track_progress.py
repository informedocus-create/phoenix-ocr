#!/usr/bin/env python3
"""
Track benchmark dataset collection progress.

Usage:
  # Log a new document
  python3 track_progress.py add --file receipts/starbucks_001.jpg \
      --category receipts --source "own scan" --license "own document" \
      --ground-truth yes --notes "faded thermal print"

  # See progress toward the 50-100 target
  python3 track_progress.py status
"""
import csv
import argparse
import os
from datetime import date
from collections import Counter

MANIFEST = os.path.join(os.path.dirname(__file__), "manifest.csv")
CATEGORIES = [
    "receipts", "invoices", "books", "newspapers", "forms",
    "business_cards", "handwriting", "low_quality", "rotated",
]
TARGET_MIN, TARGET_MAX = 50, 100


def read_manifest():
    if not os.path.exists(MANIFEST):
        return []
    with open(MANIFEST, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_entry(args):
    rows = read_manifest()
    rows.append({
        "filename": args.file,
        "category": args.category,
        "source": args.source,
        "license_or_permission": args.license,
        "has_ground_truth": args.ground_truth,
        "date_added": date.today().isoformat(),
        "notes": args.notes or "",
    })
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "filename", "category", "source", "license_or_permission",
            "has_ground_truth", "date_added", "notes",
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Logged: {args.file} -> {args.category}")


def status(_args):
    rows = read_manifest()
    counts = Counter(r["category"] for r in rows)
    gt_counts = Counter(r["category"] for r in rows if r["has_ground_truth"] == "yes")
    total = len(rows)

    print(f"\nTotal documents logged: {total}  (target: {TARGET_MIN}-{TARGET_MAX})\n")
    print(f"{'category':<16}{'count':<8}{'w/ ground truth':<18}{'status'}")
    print("-" * 60)
    for cat in CATEGORIES:
        c = counts.get(cat, 0)
        gt = gt_counts.get(cat, 0)
        flag = "OK" if c >= 6 else "NEEDS MORE"  # ~6/category floor for 50-100 total across 9 folders
        print(f"{cat:<16}{c:<8}{gt:<18}{flag}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Log a new document")
    p_add.add_argument("--file", required=True)
    p_add.add_argument("--category", required=True, choices=CATEGORIES)
    p_add.add_argument("--source", required=True, help="e.g. 'own scan', 'SROIE dataset', 'FUNSD dataset'")
    p_add.add_argument("--license", required=True, help="e.g. 'own document', 'research use - SROIE license'")
    p_add.add_argument("--ground-truth", choices=["yes", "no"], default="no")
    p_add.add_argument("--notes", default="")
    p_add.set_defaults(func=add_entry)

    p_status = sub.add_parser("status", help="Show collection progress")
    p_status.set_defaults(func=status)

    args = parser.parse_args()
    args.func(args)

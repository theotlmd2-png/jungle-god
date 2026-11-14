"""Blacklist: every company already contacted, so you never apply twice to the same place.

Merged sources:
  - tracker.txt              names copied from the WTTJ tracker (welcometothejungle.com/fr/me/application-tracker)
  - batch-*/applications.json  every application prepared by the skill, on any site
  - extra.txt                manual additions (applications made elsewhere, rejections by email), one name per line

Usage: python scripts/blacklist.py --root applications
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import norm, read_json, write_json

SLUG_RE = re.compile(r"/companies/([^/]+)/")


def names_from_batches(root: Path) -> tuple[set[str], set[str]]:
    names, slugs = set(), set()
    for path in root.glob("batch-*/applications*.json"):
        for entry in read_json(path, {}).values():
            if not isinstance(entry, dict) or entry.get("status", "").startswith("skipped"):
                continue
            names.add(norm(entry.get("company")))
            match = SLUG_RE.search(entry.get("url", ""))
            if match:
                slugs.add(match.group(1))
    return names, slugs


def names_from_file(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {norm(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def build(root: Path) -> dict:
    batch_names, slugs = names_from_batches(root)
    names = batch_names | names_from_file(root / "tracker.txt") | names_from_file(root / "extra.txt")
    names.discard("")
    return {"names": sorted(names), "slugs": sorted(slugs)}


def is_blocked(blacklist: dict, slug: str, name: str) -> bool:
    """Block on exact slug, exact name, or a known name of 5+ letters contained in the other."""
    n, s = norm(name), norm(slug)
    if slug in blacklist.get("slugs", []):
        return True
    for known in blacklist.get("names", []):
        if known in (n, s) or (len(known) >= 5 and (known in n or known in s)):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path("applications"))
    args = parser.parse_args()
    blacklist = build(args.root)
    write_json(args.root / "blacklist.json", blacklist)
    print(f"[OK] {len(blacklist['names'])} companies, {len(blacklist['slugs'])} slugs -> {args.root / 'blacklist.json'}")


if __name__ == "__main__":
    main()

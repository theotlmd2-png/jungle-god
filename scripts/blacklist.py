"""Liste noire : les entreprises déjà contactées, pour ne jamais postuler deux fois au même endroit.

Sources fusionnées :
  - tracker.txt : noms copiés depuis le suivi WTTJ (welcometothejungle.com/fr/me/application-tracker)
  - lots/*/lettres*.json : chaque candidature préparée par le skill
  - extra.txt : ajouts à la main (candidatures hors WTTJ, refus par mail), un nom par ligne

Usage : python scripts/blacklist.py --root candidatures
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import norm, read_json, write_json

SLUG_RE = re.compile(r"/companies/([^/]+)/")


def names_from_lots(root: Path) -> tuple[set[str], set[str]]:
    names, slugs = set(), set()
    for path in root.glob("lot-*/lettres*.json"):
        for entry in read_json(path, {}).values():
            if not isinstance(entry, dict):
                continue
            if entry.get("statut", "").startswith("écartée"):
                continue
            names.add(norm(entry.get("entreprise")))
            match = SLUG_RE.search(entry.get("url", ""))
            if match:
                slugs.add(match.group(1))
    return names, slugs


def names_from_file(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {norm(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def build(root: Path) -> dict:
    lot_names, slugs = names_from_lots(root)
    names = lot_names | names_from_file(root / "tracker.txt") | names_from_file(root / "extra.txt")
    names.discard("")
    return {"names": sorted(names), "slugs": sorted(slugs)}


def is_blocked(blacklist: dict, slug: str, name: str) -> bool:
    """Bloque sur slug exact, nom exact, ou nom de 5 lettres et plus contenu dans l'autre."""
    n, s = norm(name), norm(slug)
    if slug in blacklist.get("slugs", []):
        return True
    for known in blacklist.get("names", []):
        if known in (n, s) or (len(known) >= 5 and (known in n or known in s)):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path("candidatures"))
    args = parser.parse_args()
    blacklist = build(args.root)
    write_json(args.root / "blacklist.json", blacklist)
    print(f"[OK] {len(blacklist['names'])} entreprises, {len(blacklist['slugs'])} slugs -> {args.root / 'blacklist.json'}")


if __name__ == "__main__":
    main()

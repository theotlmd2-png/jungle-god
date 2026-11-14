"""Keyless sweep of Welcome to the Jungle: reads the public job pages ("/fr/pages/emploi-<job>"),
the same pages search engines index, page after page, with no account and no key.

Each job page lists about 20 listings per page over ~11 pages, for the whole of France. The listing
slug ends with its city (e.g. "..._la-defense"), so listings outside the user's area and obvious
title mismatches are dropped before any listing is opened. details.py then reads each listing.

Usage:
  python scripts/sweep.py --list-pages mecanique          # find the job pages that fit a profile
  python scripts/sweep.py --config criteria.toml --out applications/batch-2026-11-14/hits.json
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from blacklist import is_blocked
from common import JOB_URL, USER_AGENT, SetupError, _open, fail, load_toml, norm, read_json, write_json

PAGES_URL = "https://www.welcometothejungle.com/fr/pages/{page}"
INDEX_PAGE = "offres-emploi-par-metier"
KEY_RE = re.compile(r"/fr/companies/([a-z0-9-]+)/jobs/([A-Za-z0-9_-]+)")
PAGE_RE = re.compile(r"/fr/pages/(emploi-[a-z0-9-]+)")
MAX_PAGES = 15
NO_MATCH = r"(?!x)x"


def fetch_html(url: str, retries: int = 3) -> str:
    """Plain GET of a public page, with back-off."""
    last = ""
    for attempt in range(retries):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
        try:
            with _open(request, 30) as response:
                if response.status == 200:
                    return response.read().decode("utf-8", "replace")
                last = f"HTTP {response.status}"
        except urllib.error.HTTPError as exc:
            last = f"HTTP {exc.code}"
            if exc.code == 404:
                break
        except (urllib.error.URLError, TimeoutError) as exc:
            last = str(exc)
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url}: {last}")


def list_pages(word: str) -> list[str]:
    """Job pages from WTTJ's index whose name contains the word (accents ignored)."""
    pages = sorted(set(PAGE_RE.findall(fetch_html(PAGES_URL.format(page=INDEX_PAGE)))))
    wanted = norm(word)
    return [p for p in pages if wanted in norm(p)]


def page_name(title: str) -> str:
    """'Ingénieur bureau d'études' -> 'emploi-ingenieur-bureau-d-etudes' (WTTJ's naming)."""
    import unicodedata
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    return "emploi-" + re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")


def probe(titles: list[str]) -> list[tuple[str, int]]:
    """Check which guessed job pages exist and how many listings their first page shows."""
    results = []
    for title in titles:
        page = page_name(title)
        try:
            count = len(set(KEY_RE.findall(fetch_html(PAGES_URL.format(page=page), retries=1))))
        except RuntimeError:
            count = 0
        results.append((page, count))
        time.sleep(1.0)
    return results


def slug_city(slug: str) -> str:
    """City token of a listing slug: the part right after the first underscore."""
    parts = slug.split("_")
    return norm(parts[1]) if len(parts) > 1 else ""


def slug_words(slug: str) -> str:
    return slug.split("_")[0].replace("-", " ")


def keep(slug: str, cities: set[str], exclude: re.Pattern) -> bool:
    city = slug_city(slug)
    if city and cities and not any(city.startswith(c) or c.startswith(city) for c in cities):
        return False
    return not exclude.search(slug_words(slug))


def sweep_page(page: str, family: str, cities: set[str], exclude: re.Pattern, found: dict, stats: dict) -> None:
    seen_here: set[str] = set()
    for number in range(1, MAX_PAGES + 1):
        try:
            html = fetch_html(PAGES_URL.format(page=page) + (f"?page={number}" if number > 1 else ""))
        except RuntimeError as exc:
            print(f"[WARN] {page} p{number}: {exc}", file=sys.stderr)
            stats["errors"] += 1
            return
        keys = {f"{org}/{slug}" for org, slug in KEY_RE.findall(html)} - seen_here
        if not keys:
            return
        seen_here |= keys
        for key in keys:
            stats["raw"] += 1
            org, slug = key.split("/", 1)
            if key in found:
                continue
            if not keep(slug, cities, exclude):
                stats["out_of_scope"] += 1
                continue
            found[key] = {"org": org, "slug": slug, "url": JOB_URL.format(org=org, slug=slug),
                          "family": family, "page": page}
        time.sleep(1.0)


def run(config: dict, root: Path) -> tuple[dict, dict]:
    search = config["search"]
    cities = {norm(c) for c in search.get("cities", [])}
    blacklist = read_json(root / "blacklist.json", {})
    handled = {k for p in root.glob("batch-*/applications*.json") for k in read_json(p, {})}
    found: dict = {}
    stats = {"raw": 0, "out_of_scope": 0, "blocked": 0, "errors": 0}
    for family in config["families"]:
        exclude = re.compile(family.get("title_exclude") or NO_MATCH, re.I)
        for page in family.get("wttj_pages", []):
            sweep_page(page, family["name"], cities, exclude, found, stats)
    kept = {}
    for key, row in found.items():
        if key in handled or is_blocked(blacklist, row["org"], ""):
            stats["blocked"] += 1
        else:
            kept[key] = row
    if not kept and stats["errors"] and not stats["raw"]:
        raise SetupError("Every page failed to load: check the connection and the page names (--list-pages).")
    return kept, stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list-pages", metavar="WORD", help="list job pages from WTTJ's index containing this word")
    parser.add_argument("--probe", nargs="+", metavar="TITLE",
                        help="job titles to test as pages (the index is incomplete), e.g. \"ingénieur mécanique\"")
    parser.add_argument("--config", type=Path, default=Path("criteria.toml"))
    parser.add_argument("--root", type=Path, default=Path("applications"))
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    try:
        if args.list_pages:
            pages = list_pages(args.list_pages)
            print("\n".join(pages) if pages else f"[INFO] no page with '{args.list_pages}' in the index: try --probe")
            return
        if args.probe:
            for page, count in probe(args.probe):
                print(f"{'[OK]  ' if count else '[NONE]'} {page} ({count} listings on page 1)")
            return
        if not args.out:
            fail("--out is required for a sweep")
        kept, stats = run(load_toml(args.config), args.root)
    except (SetupError, RuntimeError) as exc:
        fail(str(exc))
    write_json(args.out, kept)
    print(f"[OK] {stats['raw']} listings seen, {stats['out_of_scope']} out of area or title, "
          f"{stats['blocked']} already contacted or handled, {len(kept)} kept -> {args.out}")


if __name__ == "__main__":
    main()

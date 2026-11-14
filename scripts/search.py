"""Keyword sweep of WTTJ listings through the site's public search index.

Each family in criteria.toml has its own keywords and title filters. The script keeps recent listings
in the chosen cities (or fully remote), minus companies already contacted.

Usage:
  python scripts/search.py --config criteria.toml --days 14 --out applications/batch-2026-11-14/hits.json
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import date, timedelta
from pathlib import Path

from blacklist import is_blocked
from common import JOB_URL, SetupError, algolia_credentials, fail, http_json, load_toml, read_json, write_json

ATTRIBUTES = ["name", "slug", "organization", "offices", "published_at", "experience_level",
              "salary_minimum", "salary_maximum", "remote", "contract_type"]
HITS_PER_PAGE = 100
MAX_PAGES = 10  # Algolia caps a query at 1,000 results
NO_MATCH = r"(?!x)x"


def query_page(creds: tuple[str, str, str], query: str, page: int, filters: str) -> dict:
    app, key, index = creds
    return http_json(
        f"https://{app}-dsn.algolia.net/1/indexes/{index}/query",
        body={"query": query, "hitsPerPage": HITS_PER_PAGE, "page": page,
              "filters": filters, "attributesToRetrieve": ATTRIBUTES},
        headers={"X-Algolia-Application-Id": app, "X-Algolia-API-Key": key,
                 "Referer": "https://www.welcometothejungle.com/"},
    )


def to_row(raw: dict) -> dict:
    org = raw.get("organization") or {}
    return {
        "org": org.get("slug", ""), "company": org.get("name", ""), "slug": raw.get("slug", ""),
        "title": raw.get("name", ""), "published": (raw.get("published_at") or "")[:10],
        "cities": sorted({o.get("city") for o in raw.get("offices") or [] if o.get("city")}),
        "experience": raw.get("experience_level"), "remote": raw.get("remote"),
        "salary": [raw.get("salary_minimum"), raw.get("salary_maximum")],
        "url": JOB_URL.format(org=org.get("slug", ""), slug=raw.get("slug", "")),
    }


def in_area(cities: list[str], wanted: set[str]) -> bool:
    """Exact city match; 'Paris' also matches districts such as 'Paris 9e'."""
    return bool(set(cities) & wanted) or ("Paris" in wanted and any(c.startswith("Paris") for c in cities))


def keep(row: dict, wanted: set[str], accept_remote: bool, include: re.Pattern, exclude: re.Pattern, since: date) -> bool:
    if not row["published"] or date.fromisoformat(row["published"]) < since:
        return False
    if not in_area(row["cities"], wanted) and not (accept_remote and row["remote"] == "fulltime"):
        return False
    return bool(include.search(row["title"])) and not exclude.search(row["title"])


def sweep(config: dict, since: date, blacklist: dict, creds) -> tuple[dict, dict]:
    search = config["search"]
    wanted = set(search["cities"])
    accept_remote = search.get("accept_full_remote", True)
    filters = search.get("algolia_filter", "offices.country_code:FR AND contract_type:full_time")
    found, blocked, failures, total = {}, {}, 0, 0
    for family in config["families"]:
        include = re.compile(family["title_include"], re.I)
        exclude = re.compile(family.get("title_exclude") or NO_MATCH, re.I)
        for query in family["keywords"]:
            total += 1
            for page in range(MAX_PAGES):
                try:
                    result = query_page(creds, query, page, filters)
                except RuntimeError as exc:
                    print(f"[WARN] {query} p{page}: {exc}", file=sys.stderr)
                    failures += page == 0
                    break
                hits = result.get("hits", [])
                rows = [to_row(raw) for raw in hits]
                for row in rows:
                    key = f"{row['org']}/{row['slug']}"
                    if key in found:
                        found[key]["keywords"].append(query)
                    elif keep(row, wanted, accept_remote, include, exclude, since):
                        if is_blocked(blacklist, row["org"], row["company"]):
                            blocked[key] = row
                        else:
                            found[key] = {**row, "family": family["name"], "keywords": [query]}
                oldest = min((r["published"] for r in rows if r["published"]), default="")
                # the index is sorted by date: no need to page past the window
                if len(hits) < HITS_PER_PAGE or (oldest and date.fromisoformat(oldest) < since):
                    break
                time.sleep(0.3)
            time.sleep(0.2)
    if total and failures == total:
        raise SetupError("Every query failed: check your connection and credentials (references/setup.md).")
    return found, blocked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=Path("criteria.toml"))
    parser.add_argument("--days", type=int, default=14, help="maximum listing age in days")
    parser.add_argument("--since", type=date.fromisoformat, help="start date (overrides --days)")
    parser.add_argument("--blacklist", type=Path, default=Path("applications/blacklist.json"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    since = args.since or (date.today() - timedelta(days=args.days))
    try:
        found, blocked = sweep(load_toml(args.config), since, read_json(args.blacklist, {}), algolia_credentials())
    except SetupError as exc:
        fail(str(exc))
    ordered = dict(sorted(found.items(), key=lambda kv: kv[1]["published"], reverse=True))
    write_json(args.out, ordered)
    write_json(args.out.with_name(args.out.stem + "_blocked.json"), blocked)
    print(f"[OK] {len(found)} listings since {since}; {len(blocked)} skipped (already contacted) -> {args.out}")


if __name__ == "__main__":
    main()

"""Balayage des offres WTTJ par mots-clés via l'index de recherche public du site.

Chaque famille de criteres.toml a ses requêtes et ses filtres de titre. Le script garde les offres
récentes, dans les villes voulues (ou en full remote), hors entreprises déjà contactées.

Usage :
  python scripts/search.py --config criteres.toml --days 14 --out candidatures/lot-2026-11-14/hits.json
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import date, timedelta
from pathlib import Path

from blacklist import is_blocked
from common import SetupError, algolia_credentials, fail, http_json, load_toml, read_json, write_json, JOB_URL

ATTRIBUTES = ["name", "slug", "organization", "offices", "published_at", "experience_level",
              "salary_minimum", "salary_maximum", "remote", "contract_type"]
HITS_PER_PAGE = 100
MAX_PAGES = 10  # Algolia plafonne à 1000 résultats par requête


def query_page(creds: tuple[str, str, str], query: str, page: int, filters: str) -> dict:
    app, key, index = creds
    return http_json(
        f"https://{app}-dsn.algolia.net/1/indexes/{index}/query",
        body={"query": query, "hitsPerPage": HITS_PER_PAGE, "page": page,
              "filters": filters, "attributesToRetrieve": ATTRIBUTES},
        headers={"X-Algolia-Application-Id": app, "X-Algolia-API-Key": key, "Referer": "https://www.welcometothejungle.com/"},
    )


def to_row(raw: dict) -> dict:
    org = raw.get("organization") or {}
    return {
        "org": org.get("slug", ""), "entreprise": org.get("name", ""), "slug": raw.get("slug", ""),
        "poste": raw.get("name", ""), "publiee": (raw.get("published_at") or "")[:10],
        "villes": sorted({o.get("city") for o in raw.get("offices") or [] if o.get("city")}),
        "experience": raw.get("experience_level"), "remote": raw.get("remote"),
        "salaire": [raw.get("salary_minimum"), raw.get("salary_maximum")],
        "url": JOB_URL.format(org=org.get("slug", ""), slug=raw.get("slug", "")),
    }


def keep(row: dict, cities: set[str], accept_remote: bool, include: re.Pattern, exclude: re.Pattern, since: date) -> bool:
    if not row["publiee"] or date.fromisoformat(row["publiee"]) < since:
        return False
    in_city = bool(set(row["villes"]) & cities) or any("Paris" in c for c in row["villes"] if "Paris" in cities)
    if not in_city and not (accept_remote and row["remote"] == "fulltime"):
        return False
    return bool(include.search(row["poste"])) and not exclude.search(row["poste"])


def sweep(config: dict, since: date, blacklist: dict, creds) -> tuple[dict, dict]:
    search = config["recherche"]
    cities = set(search["villes"])
    accept_remote = search.get("accepter_full_remote", True)
    filters = search.get("filtre_algolia", "offices.country_code:FR AND contract_type:full_time")
    found, blocked, failures, total = {}, {}, 0, 0
    for family in config["familles"]:
        include = re.compile(family["titre_inclure"], re.I)
        exclude = re.compile(family.get("titre_exclure", r"$^"), re.I)
        for query in family["requetes"]:
            total += 1
            for page in range(MAX_PAGES):
                try:
                    result = query_page(creds, query, page, filters)
                except RuntimeError as exc:
                    print(f"[ATTENTION] {query} p{page} : {exc}", file=sys.stderr)
                    failures += page == 0
                    break
                hits = result.get("hits", [])
                rows = [to_row(raw) for raw in hits]
                oldest = min((r["publiee"] for r in rows if r["publiee"]), default="")
                for row in rows:
                    key = f"{row['org']}/{row['slug']}"
                    if key in found or not keep(row, cities, accept_remote, include, exclude, since):
                        if key in found:
                            found[key]["requetes"].append(query)
                        continue
                    if is_blocked(blacklist, row["org"], row["entreprise"]):
                        blocked[key] = row
                        continue
                    found[key] = {**row, "famille": family["nom"], "requetes": [query]}
                # index trié par date : inutile de paginer au-delà de la fenêtre
                if len(hits) < HITS_PER_PAGE or (oldest and date.fromisoformat(oldest) < since):
                    break
                time.sleep(0.3)
            time.sleep(0.2)
    if total and failures == total:
        raise SetupError("Toutes les requêtes ont échoué : vérifie la connexion et les identifiants (references/setup.md).")
    return found, blocked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=Path("criteres.toml"))
    parser.add_argument("--days", type=int, default=14, help="âge maximal des offres en jours")
    parser.add_argument("--since", type=date.fromisoformat, help="date de début (prioritaire sur --days)")
    parser.add_argument("--blacklist", type=Path, default=Path("candidatures/blacklist.json"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    try:
        creds = algolia_credentials()
        config = load_toml(args.config)
    except SetupError as exc:
        fail(str(exc))
    since = args.since or (date.today() - timedelta(days=args.days))
    try:
        found, blocked = sweep(config, since, read_json(args.blacklist, {}), creds)
    except SetupError as exc:
        fail(str(exc))
    ordered = dict(sorted(found.items(), key=lambda kv: kv[1]["publiee"], reverse=True))
    write_json(args.out, ordered)
    write_json(args.out.with_name(args.out.stem + "_bloquees.json"), blocked)
    print(f"[OK] {len(found)} offres depuis le {since} ; {len(blocked)} écartées (déjà contactées) -> {args.out}")


if __name__ == "__main__":
    main()

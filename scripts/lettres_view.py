"""Transforme lettres.json en page HTML lisible, avec un bouton « Copier » par lettre.

Usage : python scripts/lettres_view.py candidatures/lot-2026-11-14/lettres.json
Ouvre ensuite le fichier .html produit dans le navigateur (jamais le .json brut).
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

PAGE = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Lettres — {title}</title>
<style>
body{{font:16px/1.6 -apple-system,system-ui,sans-serif;max-width:820px;margin:40px auto;padding:0 20px;color:#1a1a1a;background:#fafaf7}}
article{{background:#fff;border:1px solid #e5e5e0;border-radius:12px;padding:24px 28px;margin:24px 0}}
h2{{margin:0 0 4px;font-size:20px}} .meta{{color:#666;font-size:14px;margin-bottom:16px}}
.statut{{display:inline-block;padding:2px 10px;border-radius:99px;background:#eef;font-size:13px}}
pre{{white-space:pre-wrap;font:inherit;margin:0}} button{{float:right;padding:6px 14px;border-radius:8px;border:1px solid #ccc;background:#fff;cursor:pointer}}
</style></head><body><h1>{title}</h1><p>{count} lettres</p>{articles}
<script>document.querySelectorAll('button').forEach(b=>b.onclick=()=>{{navigator.clipboard.writeText(b.nextElementSibling.nextElementSibling.nextElementSibling.innerText);b.textContent='Copié';}})</script>
</body></html>"""

ARTICLE = """<article><button>Copier</button><h2>{entreprise} — {poste}</h2>
<div class="meta"><a href="{url}">{url}</a> · CV : {cv} · <span class="statut">{statut}</span></div><pre>{lettre}</pre></article>"""


def render(letters: dict, title: str) -> str:
    esc = lambda v: html.escape(str(v or ""))
    articles = "".join(ARTICLE.format(**{k: esc(entry.get(k)) for k in ("entreprise", "poste", "url", "cv", "statut", "lettre")})
                       for entry in letters.values())
    return PAGE.format(title=esc(title), count=len(letters), articles=articles)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lettres", type=Path)
    args = parser.parse_args()
    letters = json.loads(args.lettres.read_text(encoding="utf-8"))
    out = args.lettres.with_suffix(".html")
    out.write_text(render(letters, args.lettres.parent.name), encoding="utf-8")
    print(f"[OK] {out}")


if __name__ == "__main__":
    main()

"""Turn a batch's applications.json into a readable HTML page: a scoreboard at the top, then one card
per application (letter, form answers, status) with a Copy button.

Usage: python scripts/review.py applications/batch-2026-11-14/applications.json
Then open the .html file (never review the raw .json).
"""
from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path

STYLE = """
:root{--bg:#f6f8f7;--card:#fff;--ink:#0f172a;--muted:#475569;--line:#e2e8f0;--ok:#15803d;--okbg:#dcfce7;--warn:#a16207;--warnbg:#fef9c3}
@media (prefers-color-scheme:dark){:root{--bg:#07110c;--card:#0d1f16;--ink:#f1f5f9;--muted:#94a3b8;--line:#1e3a2b;--ok:#86efac;--okbg:#14532d;--warn:#fde68a;--warnbg:#713f12}}
*{box-sizing:border-box}body{font:16px/1.6 -apple-system,system-ui,sans-serif;max-width:860px;margin:0 auto;padding:40px 20px;color:var(--ink);background:var(--bg)}
h1{font-size:28px;margin:0 0 4px}.sub{color:var(--muted);margin:0 0 24px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:32px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}.stat b{display:block;font-size:28px}
article{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 26px;margin:18px 0}
h2{margin:0 0 4px;font-size:19px}.meta{color:var(--muted);font-size:14px;margin-bottom:14px}.meta a{color:inherit}
.pill{display:inline-block;padding:2px 10px;border-radius:99px;font-size:13px;background:var(--warnbg);color:var(--warn)}
.pill.sent{background:var(--okbg);color:var(--ok)}
pre{white-space:pre-wrap;font:inherit;margin:0}dl{margin:14px 0 0;font-size:14px}dt{font-weight:600}dd{margin:0 0 8px;color:var(--muted)}
button{float:right;padding:6px 14px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
"""

SCRIPT = """document.querySelectorAll('button[data-copy]').forEach(b=>b.addEventListener('click',()=>{
navigator.clipboard.writeText(document.getElementById(b.dataset.copy).innerText).then(()=>{b.textContent='Copied'})}))"""


def esc(value) -> str:
    return html.escape(str(value or ""))


def card(index: int, entry: dict) -> str:
    status = entry.get("status", "")
    pill = "pill sent" if status.startswith("sent") else "pill"
    answers = "".join(f"<dt>{esc(q)}</dt><dd>{esc(a)}</dd>" for q, a in (entry.get("answers") or {}).items())
    letter = entry.get("letter") or ""
    body = (f'<button data-copy="l{index}">Copy</button><pre id="l{index}">{esc(letter)}</pre>' if letter
            else "<p class='meta'>No cover letter for this one.</p>")
    return (f"<article><h2>{esc(entry.get('company'))} — {esc(entry.get('title'))}</h2>"
            f"<div class='meta'><a href='{esc(entry.get('url'))}'>{esc(entry.get('url'))}</a> · "
            f"{esc(entry.get('route'))} · CV: {esc(entry.get('cv'))} · <span class='{pill}'>{esc(status)}</span></div>"
            f"{body}{f'<dl>{answers}</dl>' if answers else ''}</article>")


def render(applications: dict, title: str) -> str:
    entries = list(applications.values())
    statuses = Counter(e.get("status", "").split(" ")[0] or "pending" for e in entries)
    routes = Counter(e.get("route") or "?" for e in entries)
    stats = [("applications", len(entries)), ("sent", statuses.get("sent", 0)),
             ("to finish", len(entries) - statuses.get("sent", 0) - statuses.get("skipped", 0)),
             ("sites", len(routes))]
    stat_html = "".join(f"<div class='stat'><b>{n}</b>{esc(label)}</div>" for label, n in stats)
    cards = "".join(card(i, e) for i, e in enumerate(entries))
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' "
            f"content='width=device-width,initial-scale=1'><title>{esc(title)}</title><style>{STYLE}</style></head>"
            f"<body><h1>{esc(title)}</h1><p class='sub'>{esc(' · '.join(f'{k}: {v}' for k, v in routes.items()))}</p>"
            f"<div class='stats'>{stat_html}</div>{cards}<script>{SCRIPT}</script></body></html>")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("applications", type=Path)
    args = parser.parse_args()
    applications = json.loads(args.applications.read_text(encoding="utf-8"))
    out = args.applications.with_suffix(".html")
    out.write_text(render(applications, args.applications.parent.name), encoding="utf-8")
    print(f"[OK] {out}")


if __name__ == "__main__":
    main()

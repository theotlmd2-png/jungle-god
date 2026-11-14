"""Tests unitaires des fonctions pures (aucun appel réseau)."""
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from blacklist import build, is_blocked  # noqa: E402
from common import norm  # noqa: E402
from details import ats_label, clean  # noqa: E402
from lettres_view import render  # noqa: E402
from search import keep  # noqa: E402

INC, EXC = re.compile(r"\bAI\b|builder", re.I), re.compile(r"senior", re.I)


def row(**kw):
    base = {"poste": "AI Builder", "publiee": "2026-11-10", "villes": ["Paris"], "remote": None}
    return {**base, **kw}


def test_norm_strips_accents_and_symbols():
    assert norm("École Gustave !") == "ecolegustave"
    assert norm(None) == ""


def test_blocked_by_slug_name_and_substring():
    bl = {"names": ["fremantle", "abc"], "slugs": ["the-bradery"]}
    assert is_blocked(bl, "the-bradery", "X")
    assert is_blocked(bl, "fremantle-limited", "Fremantle France")
    assert not is_blocked(bl, "abcdef", "Abcdef")  # nom court : pas de correspondance partielle


def test_build_merges_sources(tmp_path):
    (tmp_path / "lot-2026-11-01").mkdir()
    (tmp_path / "lot-2026-11-01" / "lettres.json").write_text(
        '{"a": {"entreprise": "Acme", "url": "https://x/fr/companies/acme/jobs/y", "statut": "envoyée"},'
        ' "b": {"entreprise": "Skip", "url": "", "statut": "écartée : 5 ans"}}', encoding="utf-8")
    (tmp_path / "tracker.txt").write_text("Doctrine\n\n", encoding="utf-8")
    result = build(tmp_path)
    assert result == {"names": ["acme", "doctrine"], "slugs": ["acme"]}


def test_keep_filters():
    since = date(2026, 11, 1)
    assert keep(row(), {"Paris"}, True, INC, EXC, since)
    assert not keep(row(poste="Senior AI Builder"), {"Paris"}, True, INC, EXC, since)
    assert not keep(row(publiee="2026-10-01"), {"Paris"}, True, INC, EXC, since)
    assert not keep(row(villes=["Lyon"]), {"Paris"}, True, INC, EXC, since)
    assert keep(row(villes=["Lyon"], remote="fulltime"), {"Paris"}, True, INC, EXC, since)
    assert keep(row(villes=["Paris 9e"]), {"Paris"}, False, INC, EXC, since)


def test_clean_and_ats():
    assert clean("<p>Bonjour&nbsp;<b>toi</b></p><p>x</p>") == "Bonjour\xa0 toi\nx"
    assert ats_label(None) == "Formulaire WTTJ"
    assert ats_label("https://boards.greenhouse.io/acme/jobs/1") == "Greenhouse"


def test_render_escapes_html():
    page = render({"k": {"entreprise": "<script>", "lettre": "a & b"}}, "lot")
    assert "&lt;script&gt;" in page and "a &amp; b" in page and "<script>" not in page.split("<script>document")[0]

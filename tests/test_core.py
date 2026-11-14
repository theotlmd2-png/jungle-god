"""Unit tests for the pure functions (no network)."""
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from blacklist import build, is_blocked  # noqa: E402
from common import norm  # noqa: E402
from details import ats_label, clean  # noqa: E402
from notify import _applescript_string  # noqa: E402
from review import render  # noqa: E402
from search import in_area, keep  # noqa: E402

INC, EXC = re.compile(r"\bAI\b|builder", re.I), re.compile(r"senior", re.I)


def row(**kw):
    return {**{"title": "AI Builder", "published": "2026-11-10", "cities": ["Paris"], "remote": None}, **kw}


def test_norm_strips_accents_and_symbols():
    assert norm("École Gustave !") == "ecolegustave"
    assert norm(None) == ""


def test_blocked_by_slug_name_and_substring():
    bl = {"names": ["fremantle", "abc"], "slugs": ["the-bradery"]}
    assert is_blocked(bl, "the-bradery", "X")
    assert is_blocked(bl, "fremantle-limited", "Fremantle France")
    assert not is_blocked(bl, "abcdef", "Abcdef")  # short names never match partially


def test_build_merges_sources_and_ignores_skipped(tmp_path):
    batch = tmp_path / "batch-2026-11-01"
    batch.mkdir()
    (batch / "applications.json").write_text(
        '{"a": {"company": "Acme", "url": "https://x/fr/companies/acme/jobs/y", "status": "sent 2026-11-01"},'
        ' "b": {"company": "Skip", "url": "", "status": "skipped: 5 years"}}', encoding="utf-8")
    (tmp_path / "tracker.txt").write_text("Doctrine\n\n", encoding="utf-8")
    assert build(tmp_path) == {"names": ["acme", "doctrine"], "slugs": ["acme"]}


def test_area_and_keep():
    since = date(2026, 11, 1)
    assert in_area(["Paris 9e"], {"Paris"}) and not in_area(["Lyon"], {"Paris"})
    assert keep(row(), {"Paris"}, True, INC, EXC, since)
    assert not keep(row(title="Senior AI Builder"), {"Paris"}, True, INC, EXC, since)
    assert not keep(row(published="2026-10-01"), {"Paris"}, True, INC, EXC, since)
    assert not keep(row(cities=["Lyon"]), {"Paris"}, True, INC, EXC, since)
    assert keep(row(cities=["Lyon"], remote="fulltime"), {"Paris"}, True, INC, EXC, since)


def test_clean_and_ats():
    assert clean("<p>Bonjour&nbsp;<b>toi</b></p><p>x</p>") == "Bonjour\xa0 toi\nx"
    assert ats_label(None) == "WTTJ form"
    assert ats_label("https://boards.greenhouse.io/acme/jobs/1") == "Greenhouse"


def test_review_escapes_and_counts():
    page = render({"k": {"company": "<script>", "letter": "a & b", "status": "sent 2026-11-14"},
                   "j": {"company": "B", "status": "letter ready"}}, "batch")
    body = page.split("<script>document")[0]
    assert "&lt;script&gt;" in body and "a &amp; b" in body and "<script>" not in body
    assert "<b>2</b>applications" in page and "<b>1</b>sent" in page


def test_applescript_quoting():
    assert _applescript_string('say "hi" \\') == '"say \\"hi\\" \\\\"'

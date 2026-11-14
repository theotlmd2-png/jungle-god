"""Convertit un CV (ou une lettre) HTML en PDF A4 avec Chrome ou Chromium en mode headless.

Un profil Chrome temporaire est utilisé : sans lui, le Chrome headless peut entrer en conflit avec
la session Chrome ouverte (et couper l'extension Claude in Chrome).

Usage : python scripts/cv_pdf.py cv/cv-ia.html [--out cv/cv-ia.pdf]
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from common import fail

CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
)


def find_chrome() -> str | None:
    for candidate in CANDIDATES:
        if Path(candidate).exists():
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    return None


def to_pdf(source: Path, out: Path) -> None:
    chrome = find_chrome()
    if not chrome:
        fail("Chrome ou Chromium introuvable. Installe Google Chrome, ou imprime le HTML en PDF à la main.")
    with tempfile.TemporaryDirectory() as profile:
        cmd = [chrome, "--headless=new", "--disable-gpu", f"--user-data-dir={profile}",
               "--no-pdf-header-footer", f"--print-to-pdf={out.resolve()}", source.resolve().as_uri()]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0 or not out.exists():
        fail(f"Échec de la conversion : {result.stderr.strip()[:400]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    if not args.html.exists():
        fail(f"Fichier introuvable : {args.html}")
    out = args.out or args.html.with_suffix(".pdf")
    to_pdf(args.html, out)
    print(f"[OK] {out}")


if __name__ == "__main__":
    main()

"""Shared helpers: configuration, polite HTTP calls, name normalisation."""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import time
import tomllib
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_INDEX = "wttj_jobs_production_fr_published_at_desc"
JOB_API = "https://api.welcometothejungle.com/api/v1/organizations/{org}/jobs/{slug}"
JOB_URL = "https://www.welcometothejungle.com/fr/companies/{org}/jobs/{slug}"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Safari/605.1.15"
SYSTEM_CA_BUNDLES = ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt", "/etc/pki/tls/certs/ca-bundle.crt")


class SetupError(RuntimeError):
    """Missing or invalid configuration, with a human-readable message."""


def fail(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    sys.exit(code)


def load_env(path: Path = Path(".env")) -> None:
    """Load a simple .env file without overriding variables already set."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def algolia_credentials() -> tuple[str, str, str]:
    """WTTJ's public search credentials, fetched by the user (see references/setup.md)."""
    load_env()
    app = os.environ.get("WTTJ_ALGOLIA_APP", "").strip()
    key = os.environ.get("WTTJ_ALGOLIA_KEY", "").strip()
    index = os.environ.get("WTTJ_ALGOLIA_INDEX", DEFAULT_INDEX).strip()
    if not app or not key:
        raise SetupError("WTTJ_ALGOLIA_APP and WTTJ_ALGOLIA_KEY are missing. Copy .env.example to .env "
                         "and fill them in (see references/setup.md).")
    return app, key, index


def load_toml(path: Path) -> dict:
    if not path.exists():
        raise SetupError(f"File not found: {path}. Start from templates/{path.stem}.example.toml.")
    with path.open("rb") as handle:
        return tomllib.load(handle)


_ssl_context: ssl.SSLContext | None = None


def _candidate_contexts() -> list[ssl.SSLContext]:
    """Default store, then certifi, then system stores (some Homebrew Pythons ship a broken store)."""
    contexts = [ssl.create_default_context()]
    try:
        import certifi  # optional
        contexts.append(ssl.create_default_context(cafile=certifi.where()))
    except (ImportError, AttributeError, OSError):
        pass
    contexts += [ssl.create_default_context(cafile=p) for p in SYSTEM_CA_BUNDLES if Path(p).exists()]
    return contexts


def _open(request: urllib.request.Request, timeout: int):
    """Open the request with the first certificate store that works, then remember it."""
    global _ssl_context
    if _ssl_context is not None:
        return urllib.request.urlopen(request, timeout=timeout, context=_ssl_context)
    last: Exception | None = None
    for context in _candidate_contexts():
        try:
            response = urllib.request.urlopen(request, timeout=timeout, context=context)
            _ssl_context = context
            return response
        except urllib.error.URLError as exc:
            if not isinstance(exc.reason, ssl.SSLCertVerificationError):
                raise
            last = exc
    raise SetupError(f"No valid certificate store ({last}). Try: pip install certifi")


def http_json(url: str, *, body: dict | None = None, headers: dict | None = None,
              retries: int = 3, timeout: int = 30) -> dict:
    """GET or POST JSON with progressive back-off; raises RuntimeError once retries are exhausted."""
    data = json.dumps(body).encode() if body is not None else None
    all_headers = {"User-Agent": USER_AGENT, "Accept": "application/json", **(headers or {})}
    if data is not None:
        all_headers["Content-Type"] = "application/json"
    last_error = ""
    for attempt in range(retries):
        request = urllib.request.Request(url, data=data, headers=all_headers)
        try:
            with _open(request, timeout) as response:
                if response.status == 202:  # WTTJ burst protection: slow down
                    last_error = "HTTP 202 (rate limited)"
                else:
                    return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}"
            if exc.code in (401, 403, 404):
                break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = str(exc)
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url}: {last_error}")


def norm(text: str | None) -> str:
    """Comparable name: no accents, lowercase, letters and digits only."""
    ascii_text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", ascii_text.lower())


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1), encoding="utf-8")

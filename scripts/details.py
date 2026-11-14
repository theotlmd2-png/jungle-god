"""Full listings: missions, profile wanted, hiring process, salary, application route and form questions.

Reads a list of "org/slug" keys (one per line) or the JSON produced by search.py, then calls WTTJ's
public listing API, one listing per second.

Usage:
  python scripts/details.py --keys applications/batch-2026-11-14/keys.txt --out applications/batch-2026-11-14/details.json
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
from pathlib import Path

from datetime import date, timedelta

from common import JOB_API, JOB_URL, http_json, load_toml, norm, write_json

NO_MATCH = r"(?!x)x"

ATS_LABELS = (("lever.co", "Lever"), ("greenhouse", "Greenhouse"), ("workable", "Workable"), ("ashbyhq", "Ashby"),
              ("teamtailor", "Teamtailor"), ("smartrecruiters", "SmartRecruiters"), ("recruitee", "Recruitee"),
              ("myworkdayjobs", "Workday (account required)"), ("werecruit", "WeRecruit"), ("jobteaser", "JobTeaser"))


def clean(raw: str | None) -> str:
    text = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>", "\n", raw or "")
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    lines = (re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)


def ats_label(apply_url: str | None) -> str:
    if not apply_url:
        return "WTTJ form"
    return next((label for needle, label in ATS_LABELS if needle in apply_url), "External site")


def wttj_questions(job: dict) -> list[dict]:
    out = []
    for q in job.get("ats_questions") or []:
        fmt = q.get("format") or {}
        out.append({"question": ((q.get("question") or {}).get("title") or "").strip(),
                    "required": bool(q.get("required")), "type": fmt.get("type", "TEXT"),
                    "options": [o.get("name", "") for o in fmt.get("options") or []]})
    return out


def greenhouse_questions(apply_url: str | None) -> list[dict]:
    match = re.search(r"greenhouse\.io/([^/]+)/jobs/(\d+)", apply_url or "")
    if not match:
        return []
    board, job_id = match.groups()
    try:
        data = http_json(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs/{job_id}?questions=true")
    except RuntimeError:
        return []
    return [{"question": q.get("label", "").strip(), "required": bool(q.get("required")),
             "type": ",".join(sorted({f.get("type", "") for f in q.get("fields", [])})),
             "options": [v.get("label", "") for f in q.get("fields", []) for v in f.get("values", [])]}
            for q in data.get("questions", [])]


def fetch(key: str) -> dict:
    org, slug = key.split("/", 1)
    job = http_json(JOB_API.format(org=org, slug=slug)).get("job", {})
    apply_url = job.get("apply_url")
    fields = job.get("application_fields") or []
    organization = job.get("organization") or {}
    return {
        "company": organization.get("name", org),
        "title": job.get("name", ""),
        "url": JOB_URL.format(org=org, slug=slug),
        "published": (job.get("published_at") or "")[:10],
        "experience": job.get("experience_level"),
        "education": job.get("education_level"),
        "salary": [job.get("salary_minimum"), job.get("salary_maximum"), job.get("salary_period")],
        "remote": job.get("remote"),
        "contract": job.get("contract_type"),
        "cities": sorted({o.get("city") for o in job.get("offices") or [] if o.get("city")}),
        "language": job.get("language"),
        "route": ats_label(apply_url),
        "apply_url": apply_url,
        "required_files": [f["name"] for f in fields if f.get("mode") == "mandatory"],
        "questions": wttj_questions(job) or greenhouse_questions(apply_url),
        "missions": clean(job.get("description")),
        "profile": clean(job.get("profile")),
        "process": clean(job.get("recruitment_process")),
        "about": clean(organization.get("description"))[:1500],
    }


def in_scope(detail: dict, criteria: dict, since: date) -> str:
    """Empty string if the listing fits the criteria, else the reason it does not."""
    search = criteria.get("search", {})
    if detail["published"] and date.fromisoformat(detail["published"]) < since:
        return "too old"
    contracts = search.get("contracts", [])
    if contracts and detail["contract"] and detail["contract"] not in contracts:
        return f"contract {detail['contract']}"
    wanted = {norm(c) for c in search.get("cities", [])}
    remote_ok = search.get("accept_full_remote", False) and detail["remote"] == "fulltime"
    if wanted and not remote_ok and not ({norm(c) for c in detail["cities"]} & wanted):
        return "out of area: " + ", ".join(detail["cities"])
    for family in criteria.get("families", []):
        include = re.compile(family.get("title_include") or ".", re.I)
        exclude = re.compile(family.get("title_exclude") or NO_MATCH, re.I)
        if include.search(detail["title"]) and not exclude.search(detail["title"]):
            return ""
    return "title"


def read_keys(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return list(json.loads(text).keys())
    return [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--keys", type=Path, required=True, help="keys.txt (one org/slug per line) or hits.json")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--delay", type=float, default=1.0, help="pause between listings, in seconds")
    parser.add_argument("--criteria", type=Path, help="criteria.toml: keep only listings in scope")
    parser.add_argument("--days", type=int, default=0, help="with --criteria: maximum listing age in days")
    args = parser.parse_args()

    criteria = load_toml(args.criteria) if args.criteria else None
    since = date.today() - timedelta(days=args.days) if args.days else date.min
    details, dropped, errors = {}, {}, []
    for key in read_keys(args.keys):
        try:
            detail = fetch(key)
        except (RuntimeError, ValueError) as exc:
            errors.append(f"{key}: {exc}")
        else:
            reason = in_scope(detail, criteria, since) if criteria else ""
            if reason:
                dropped[key] = reason
            else:
                details[key] = detail
        time.sleep(args.delay)
    write_json(args.out, details)
    if dropped:
        write_json(args.out.with_name(args.out.stem + "_dropped.json"), dropped)
    for line in errors:
        print(f"[FAILED] {line}", file=sys.stderr)
    print(f"[OK] {len(details)} listings kept, {len(dropped)} out of scope, {len(errors)} failed -> {args.out}")


if __name__ == "__main__":
    main()

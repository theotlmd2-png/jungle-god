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

from common import JOB_API, JOB_URL, http_json, write_json

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
    args = parser.parse_args()

    details, errors = {}, []
    for key in read_keys(args.keys):
        try:
            details[key] = fetch(key)
        except (RuntimeError, ValueError) as exc:
            errors.append(f"{key}: {exc}")
        time.sleep(args.delay)
    write_json(args.out, details)
    for line in errors:
        print(f"[FAILED] {line}", file=sys.stderr)
    print(f"[OK] {len(details)} listings read, {len(errors)} failed -> {args.out}")


if __name__ == "__main__":
    main()

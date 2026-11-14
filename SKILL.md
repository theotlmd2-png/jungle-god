---
name: jungle-god
description: Job-hunting pipeline for Welcome to the Jungle (WTTJ) and the career sites and ATS behind it. On first run, interviews the user (target job, area, proofs, standard form answers, rules), builds their CV if needed and gets a model cover letter approved. Then, for each batch, sweeps hundreds of listings by keyword, reads every shortlisted listing in full and drops the ones that do not fit, writes one tailored letter per listing from verified facts only, fills the application forms in Chrome, notifies after each one, and keeps a blacklist so nobody gets the same application twice. Use when the user talks about finding a job, a CDI, an internship or apprenticeship, applying, applications, CV or résumé, cover letters, WTTJ or Welcome to the Jungle, or says "find me jobs", "new batch", "apply" (in any language, e.g. « trouve-moi des offres », « postule »).
---

# Jungle God

The idea: **a lot of applications, each one right.** The machine does the volume (sweep, triage,
writing, filling forms). The human keeps the decisions that matter: the truth of their profile,
their rules, the GO on the shortlist.

Always talk to the user in their language. Letters and form answers follow the listing's language.

```
          ┌───────────────── first run only ─────────────────┐
          │ 0. Onboarding: situation → CV → proofs → kit     │
          │    → rules → approved model letter → criteria    │
          └────────────────────────┬─────────────────────────┘
                                   ▼
 1. Sweep ──▶ 2. Triage ──▶ 3. Shortlist ──▶ GO ──▶ 4. Letters ──▶ 5. Apply ──▶ 6. Recap
 search.py    details.py     table          human   applications    Chrome +     review.py
                                                    .json           notify.py    blacklist.py
     ▲                                                                                │
     └───────────────────── companies already contacted are excluded ◀────────────────┘
```

## Two layers of rules
- **The core** (end of this file): pipeline order, file formats, zero invention, human GO, blacklist.
  Same for everyone. Cannot be turned off.
- **Adjustable rules**: `rules.toml` in the working folder, written during onboarding from
  `templates/rules.example.toml`. Each person keeps, changes or disables what they want.
  **Reread `rules.toml` at the start of every batch.** When a reference gives a default, `rules.toml` wins.

When the user states a new durable preference ("no more sales roles", "max 4 per company type"), write
it to `rules.toml` or `profile.md › Learned preferences` and say so in one line.

## Landmarks
- `SK=~/.claude/skills/jungle-god`: scripts, references, templates.
- Working folder, default `~/job-hunt`: `.env`, `profile.md`, `rules.toml`, `criteria.toml`, `cv/`,
  `applications/`. **Always run the scripts from this folder.**
- One batch = `applications/batch-YYYY-MM-DD/`.

## Step 0 — Onboarding (when `profile.md` is missing or says "Onboarding: not done")
1. Technical setup: `references/setup.md`. Do it yourself as far as possible.
2. Interview and build: `references/onboarding.md`, blocks A to G: situation, CV (read, improved or
   built from `templates/cv.html`), proofs, **Application kit** (so third-party forms can be filled
   without stopping), rules, **model letter approved on a real listing**, search criteria.
3. If the user is in a hurry: blocks A, B, D and F, defaults elsewhere, and say so.

## Step 1 — Sweep
```bash
python $SK/scripts/blacklist.py --root applications
python $SK/scripts/search.py --days 14 --out applications/batch-YYYY-MM-DD/hits.json
```
- Window: since the last batch if recent, else `max_listing_age_days`.
- Over 300 results: tighten title filters. Under 20: broaden keywords or the window, or see `references/channels.md`.
- Report raw volume, listings dropped by the blacklist, split by family.

## Step 2 — Triage (the heart of it)
`references/triage.md` with the thresholds from `rules.toml [triage]`. Title pass on `hits.json` → `keys.txt`, then:
```bash
python $SK/scripts/details.py --keys applications/batch-YYYY-MM-DD/keys.txt --out applications/batch-YYYY-MM-DD/details.json
```
Read each listing IN FULL. A listing passes because its missions match the proofs in `profile.md`,
not because it contains a keyword.

## Step 3 — Shortlist and GO
The table from `references/triage.md`, skipped listings included with their reason. Then wait for the GO.
**Nothing is written or sent before the GO.**

## Step 4 — Letters
`references/letters.md` + `rules.toml [letter]`, **starting from the approved model letter**. Answers ready
for every form question, from the listing and the Application kit. CV picked by family. Everything goes to
`applications.json`, then `review.py`, then open the HTML. If `letter.enabled = false`, prepare the form answers only.

## Step 5 — Apply
`references/apply.md` in the chosen `sending.mode`; `references/channels.md` for ATS, career pages,
other boards and spontaneous applications. After **each** application: update `status`, desktop
notification if enabled, and one line in the chat saying what was done and where.

## Step 6 — Recap
`review.py` scoreboard opened, chat summary (sent, per site, left to the user, running total), `blacklist.py`.
If `follow_up.gmail`, read replies. Several rejections within 48 h mean a CV screen: offer to rework the CV, not the letters.

## The core (non-negotiable, whatever the rules)
1. **Zero invention.** No fact, number, customer, date or tool that is not in `profile.md`. When in doubt, ask.
2. **Pipeline in order**: no letter without triage, no submission without GO.
3. **Blacklist** kept up to date: never the same application twice to the same company.
4. **Stable formats**: `hits.json`, `keys.txt`, `details.json`, `applications.json` (see `templates/`),
   so any later session can resume a batch.
5. **Network politeness**: keep the delays between requests, no sweeping in a loop, one batch a day at most.
6. **Personal data stays local**: `profile.md`, `rules.toml`, CVs and `applications/` are never committed or published.
7. **Stop and hand back** on account passwords, CAPTCHA, payment, ID document, or doubt.

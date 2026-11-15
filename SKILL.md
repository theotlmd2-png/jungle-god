---
name: jungle-god
description: Job-hunting pipeline for Welcome to the Jungle (WTTJ) and the career sites and ATS behind it. On first run, interviews the user (target job, area, proofs, standard form answers, rules), builds their CV if needed and gets a model cover letter approved. Then, for each batch, sweeps hundreds of listings by keyword, reads every shortlisted listing in full and drops the ones that do not fit, writes one tailored letter per listing from verified facts only, fills the application forms in Chrome, notifies after each one, and keeps a blacklist so nobody gets the same application twice. Use when the user talks about finding a job, a CDI, an internship or apprenticeship, applying, applications, CV or résumé, cover letters, WTTJ or Welcome to the Jungle, or says "find me jobs", "new batch", "apply" (in any language, e.g. « trouve-moi des offres », « postule »).
---

# Jungle God

The idea: **a lot of applications, each one right.** The machine does the volume (sweep, triage,
writing, filling forms). The human keeps the decisions that matter: the truth of their profile,
their rules, one GO on a ready-to-send batch.

Always talk to the user in their language. Letters and form answers follow the listing's language.

## Launch
The user types `/jungle-god` (often followed by "go"), or simply talks about their job hunt.
- `profile.md` missing or "Onboarding: not done" → greet in two lines (what the skill does, about
  20 minutes of setup once), then **ask the first open question right away**: what job they are looking
  for, and where, in their own words. No file, no browser, no technical step before the person has talked.
- Onboarding done and a batch already prepared (`applications.json` with letters ready, nothing sent yet)
  → open straight on that batch's **ready check** (Step 4), no greeting paragraph, no extra question.
- Onboarding done, nothing prepared → propose the next action: a new batch since the last one, or
  finishing the applications left in progress.
Never assume anything about the user's situation (seniority, contract, country, job) before they say it.

```
          ┌───────────────── first run only ─────────────────┐
          │ 0. Onboarding: situation → CV → proofs → kit     │
          │    → rules → approved model letter → criteria    │
          └────────────────────────┬─────────────────────────┘
                                   ▼
 1. Sweep ──▶ 2. Triage ──▶ 3. Letters ──▶ 4. Ready check ──▶ GO ──▶ 5. Apply ──▶ 6. Recap
  sweep.py    details.py     applications   one message        human   Chrome +     review.py
                             .json          CV ✓ letters ✓...          notify.py    blacklist.py
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
1. **A conversation, not a form.** Interview per `references/onboarding.md`, blocks A to G: situation,
   CV first (imported, or built during the conversation, 1 to 3 CVs per target market after web research,
   revealed at the end: `references/cv.md`), proofs, **Application kit** (so third-party
   forms can be filled without stopping), rules, **model letter approved on a real listing**, criteria.
2. Technical setup (`references/setup.md`) happens **silently in the background**, only when first needed
   (just before the first sweep, in block F). Never open with it, never make the user wait on it.
3. If the user is in a hurry: blocks A, B, D and F, defaults elsewhere, and say so.

## Step 1 — Sweep (behind the scenes, no key, no browser)
```bash
python $SK/scripts/blacklist.py --root applications
python $SK/scripts/sweep.py --out applications/batch-YYYY-MM-DD/hits.json
```
`sweep.py` reads WTTJ's public job pages listed under `wttj_pages` in `criteria.toml` (found at onboarding
with `--probe` / `--list-pages`), drops listings outside the user's area or with an excluded title, and
listings already contacted. Nothing to configure for the user.
- Optional fast mode: a user who pasted WTTJ's search credentials in `.env` can use `search.py`
  (keyword search over the whole index). Never extract those credentials by script.
- Report raw volume, out of scope, already contacted, kept.

## Step 2 — Triage (the heart of it)
`references/triage.md` with the thresholds from `rules.toml [triage]`. Read every kept listing, filtered on
contract, area, title and age:
```bash
python $SK/scripts/details.py --keys applications/batch-YYYY-MM-DD/hits.json --criteria criteria.toml \
  --days <max_listing_age_days> --out applications/batch-YYYY-MM-DD/details.json
```
Read each listing IN FULL. A listing passes because its missions match the proofs in `profile.md`,
not because it contains a keyword.

## Step 3 — Letters (straight away, no stop)
Right after triage, without asking: `references/letters.md` + `rules.toml [letter]`, **starting from the
approved model letter**. One letter per kept listing, answers ready for every form question (from the
listing and the Application kit), CV picked by family. Everything goes to `applications.json`. Writing is
local and harmless; the GO guards what leaves the machine.

## Step 4 — Ready check, then ONE GO
One short message, the only stop of the batch, in the user's language. Format in `references/triage.md`
› Ready check. A checklist first (CV ✓, letters ✓ N/N, form answers ✓, blacklist ✓, anything missing ✗),
then the shortlist table (one line per listing, letter included), then skipped listings in one line each,
then a single question: GO for the whole batch, or GO except some numbers. Letters are NOT pasted in full;
the user can ask "show me letter 3" and gets it in a quote block, corrected in the chat if needed.
After the GO, run Step 5 to the end without asking again (stop only per core rule 7).

## Step 5 — Apply
1. **Open every GO listing at once** in Chrome, one tab each, in shortlist order, and tell the user
   "N tabs open, I'm going through them one by one". This is the moment the user sees the batch for real.
2. Then go **tab by tab, in order**: follow the apply button to the real form (WTTJ or the ATS),
   fill it per `references/apply.md` in the chosen `sending.mode`, check every field, submit only if the
   mode and the GO allow it, then move to the next tab. `references/channels.md` covers ATS, career
   pages, other boards and spontaneous applications.
3. After **each** application: update `status`, desktop notification if enabled, and one line in the
   chat saying what was done and where.

## Step 6 — Recap
`review.py` scoreboard opened, chat summary (sent, per site, left to the user, running total), `blacklist.py`.
If `follow_up.gmail`, read replies. Several rejections within 48 h mean a CV screen: offer to rework the CV, not the letters.

## The core (non-negotiable, whatever the rules)
1. **Zero invention.** No fact, number, customer, date or tool that is not in `profile.md`. When in doubt, ask.
2. **Pipeline in order**: no letter without triage, nothing sent without the GO on the ready check.
3. **Blacklist** kept up to date: never the same application twice to the same company.
4. **Stable formats**: `hits.json`, `keys.txt`, `details.json`, `applications.json` (see `templates/`),
   so any later session can resume a batch.
5. **Network politeness**: keep the delays between requests, no sweeping in a loop, one batch a day at most.
6. **Personal data stays local**: `profile.md`, `rules.toml`, CVs and `applications/` are never committed or published.
7. **Stop and hand back** on account passwords, CAPTCHA, payment, ID document, or doubt.

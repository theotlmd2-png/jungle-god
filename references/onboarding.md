# Onboarding: the first run

Goal: fit the skill to THIS person without bending the pipeline. At the end, the working folder holds
`profile.md` (with a complete Application kit), `rules.toml`, `criteria.toml`, at least one CV as a PDF,
and an **approved model letter**. Target: 15 to 25 minutes. Speak the user's language throughout.

## How to ask
- In blocks of 2 to 4 questions with AskUserQuestion when available: proposed choices, recommended one first.
  Otherwise in plain text, one block at a time.
- Never ask what you can read yourself (CV, LinkedIn, portfolio, GitHub, listings).
- After each block, restate what you understood in one line.
- Skipped question → the default from `rules.example.toml` applies; say so.

## Block A — Situation
1. Target job(s)? Propose 3 to 5 close titles inferred from what they say.
2. Where? City, radius, remote accepted or required.
3. Contract: permanent, fixed-term, freelance, internship, apprenticeship? (adjust `algolia_filter`)
4. Real experience in this job, in years, and honest English level.
5. Pace: how many applications per week? (→ `batch_size`) How urgent?

## Block B — Material
- **Existing CV**: ask for the file path, read it, extract the facts into `profile.md`. Point out in three
  bullets what hurts it (no numbers, no links, vague title, unexplained gaps) and offer to redo it.
  Redo it only with their OK.
- **No CV**: offer to build one (see "Building the CV" below).
- Links: LinkedIn, portfolio, GitHub, App Store, website. Read them if accessible.
- Several target jobs: offer one CV per family (same base, different title and proof order).

## Block C — Proofs
For each experience or project, get at least ONE proof: a fact and a result.
- "What did you build, launch or improve there? With what result?"
- "A number, even small, that shows it?" (if there is none, none is invented)
- "What must I never write or exaggerate?" → `Truths never to bend`
- "Any project you never want cited?" → `never_mention`

## Block D — Application kit (what makes third-party sites autonomous)
Every ATS asks the same dozen things. Collect them once so Claude never has to stop mid-form.
Go through the `Application kit` section of `profile.md` and fill it, grouping questions:
1. Contact and identity: legal name, email for applications, phone, address or city only.
2. Work: right to work / visa, notice period, earliest start, relocation, travel, driving licence.
3. Money: expected salary (short and long answer), current salary (or "prefer not to say").
4. Forms: degree and year, years of experience as forms ask it, "how did you hear about us",
   diversity questions policy, references.
5. Accounts: existing accounts on job sites, whether Claude may create new ones (`forms.accounts`),
   and the rule that the **user always types passwords**.
6. Standard short answers in French and English: "Why you?", "Biggest achievement", "A weakness".
   "Why us?" is always written per company.

## Block E — Rules
Show the defaults from `rules.example.toml` as a short table (rule, default, what it changes), then ask
what to change. The questions that really vary between people:
- How many years of required experience are you willing to target? (`max_years_required`)
- A letter for every listing, or CV only? (`letter.enabled`)
- Formal or informal tone? (`informal`)
- Who clicks Submit: me after your GO, you after I fill, or texts only? (`sending.mode`)
- Which channels besides WTTJ? (`channels`)
- Desktop notification after each application? (`notify.desktop`)

Write `rules.toml` from the template with their choices.

## Block F — Model letter (the key moment)
1. Run a small sweep (`search.py --days 7`) and pick ONE listing that fits the profile very well.
2. Write the letter per `references/letters.md` and `rules.toml`, show it through `review.py`.
3. Ask for precise feedback: tone, length, what sounds fake, what is missing.
4. Iterate until approved, then paste it into `profile.md › Approved model letter`, with the feedback
   turned into rules (`banned_phrases`, `gap_sentence`…).
5. Every later letter starts from this base: same tone, same structure, content specific to each listing.

## Block G — Search criteria
Write `criteria.toml`: one family per target job, 15 to 60 keywords (French and English titles, tools,
jargon, synonyms), title include/exclude filters from block A. Run a control sweep and show the volume
per family; adjust when a family is empty or flooded.

## End of onboarding
- Replace `Onboarding: not done` with `Onboarding: done YYYY-MM-DD` at the top of `profile.md`. Next time,
  the skill goes straight to the sweep.
- Five-line summary: jobs, area, rules changed from the defaults, CVs available, next action.
- "Change my rules" or "redo my onboarding" reopens the relevant block at any time.

## Building the CV
Start from `templates/cv.html` (one A4 page, plain, ATS-readable):
1. Collect: target title, 3 to 5 experiences or projects with one proof each, real skills and tools,
   education, languages, links. Photo only if wanted (common in France, discouraged elsewhere).
2. Write `cv/cv-<family>.html` by replacing the template blocks. Title = the target job, not "looking for a job".
3. `python $SK/scripts/cv_pdf.py cv/cv-<family>.html`, check it fits one page, `open` it.
4. Iterate on feedback, then copy the facts into `profile.md`.
Rules: zero invention, action verbs, one number per line when one exists, no skill gauges.

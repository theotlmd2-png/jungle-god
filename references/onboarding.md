# Onboarding: the first run

Goal: fit the skill to THIS person without bending the pipeline. At the end, the working folder holds
`profile.md` (with a complete Application kit), `rules.toml`, `criteria.toml`, at least one CV as a PDF,
and an **approved model letter**. Target: 15 to 25 minutes. Speak the user's language throughout.

## How to ask
- **Be direct and fast.** Short spoken questions that each cover a theme ("Your studies? Your jobs? Your
  passions?"), no preamble, no explaining why you ask. Onboarding should feel like 15 minutes, not an interview.
- **Talk, in the chat, like a person.** Open questions first, one or two at a time, in the user's words
  ("Tell me what you're looking for, even if it's vague"). Follow up on what they say instead of
  marching through a list; one answer often covers several questions below.
- No multiple-choice dialog for questions about who they are (job, story, proofs): it feels like an
  admin form. Choice dialogs are fine later, for closed settings (block E rules), and only if the user
  seems to like them.
- Never ask what you can read yourself (CV, LinkedIn, portfolio, GitHub, listings).
- After each block, restate what you understood in one line, so they can correct it.
- Skipped question → the neutral default from `rules.example.toml` applies; say so.
- Technical setup (`references/setup.md`) is done in the background when first needed, never at the start.

## Block A — Situation
1. Target job(s)? Propose 3 to 5 close titles inferred from what they say.
2. Where? City, radius, remote accepted or required.
3. Contract: permanent, fixed-term, freelance, internship, apprenticeship? (adjust `algolia_filter`)
4. Real experience in this job, in years, and the languages they can work in, with an honest level.
5. Pace: how many applications per week? (→ `batch_size`) How urgent?
6. What makes their profile unusual (career change, long experience, self-taught, return to work…)
   and what they absolutely do not want (→ `deal_breakers`).

## Block B — Material: CV first
Early, right after the first answers: "Do you have a CV? Drop it here, even an old one."
Follow `references/cv.md`: read and extract it if there is one; otherwise build it **during the
conversation**, from every answer of blocks A to D. Ask for links (LinkedIn, portfolio, GitHub) too and
read them. As markets become visible, note them: up to three CVs will be revealed at the end.

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
6. Standard short answers, in each language they apply in: "Why you?", "Biggest achievement", "A weakness".
   "Why us?" is always written per company.

## Block E — Rules
The template holds neutral values only. Fill each rule from the answers so far, show the result as a short
table (rule, value, what it changes), then ask what to change. The questions that really vary between people:
- What level of required experience fits you, from how many years to how many? (`min_years_required`, `max_years_required`)
- Skip listings that require a degree you do not have, or try anyway? (`skip_if_degree_required`)
- Tone of the letters: formal or more direct? (`tone`, `opening`). Every application sends the CV **and**
  a letter by default; only turn letters off (`letter.enabled = false`) if the user asks for CV-only.
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
Write `criteria.toml`: cities, contracts, and one family per target job with its title include/exclude
filters from block A. For each family, find the WTTJ job pages that cover it:
`python $SK/scripts/sweep.py --probe "<title 1>" "<title 2>" …` (try 5 to 15 likely titles, in French) and
`--list-pages <word>`. Put the pages that exist in `wttj_pages`; WTTJ's index is incomplete, so always probe.
`keywords` only serve the optional fast mode. Run a control sweep and show the volume per family; adjust
when a family is empty or flooded.

## End of onboarding
- **The reveal** (`references/cv.md` §6): "With your profile, I built N CVs, here they are. Do we target
  these markets?" Their answer sets the families in `criteria.toml`.
- Replace `Onboarding: not done` with `Onboarding: done YYYY-MM-DD` at the top of `profile.md`. Next time,
  the skill goes straight to the sweep.
- Five-line summary: jobs, area, rules changed from the defaults, CVs available, next action.
- "Change my rules" or "redo my onboarding" reopens the relevant block at any time.

## Building the CVs
See `references/cv.md`: precise questions over several turns, 1 to 3 target markets, web research of what
works in each, one CV per market, render checked, then **the reveal at the end of onboarding**.

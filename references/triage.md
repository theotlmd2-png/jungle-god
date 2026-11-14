# Triage: the hard criteria

> Thresholds below are defaults: `rules.toml [triage]` always wins.

This is the step that makes the difference. A sweep brings back hundreds of listings and most are false
positives: the title fits, the listing asks for something else. **Five right listings beat sixteen
approximate ones.**

## Two passes
1. **Title pass** on `hits.json`: drop what the title already gives away (seniority, neighbouring job,
   foreign country, internship). Keep 20 to 40 candidates and write their keys to `keys.txt`.
2. **Listing pass** on `details.json`: read `missions` + `profile` + `process` IN FULL. That is where
   the real requirements hide ("5 years minimum", "engineering school", "fluent German").

## Skip when
- Years of experience required exceed `max_years_required` (watch the text, not only the badge:
  a third of "junior" listings ask for 3 to 5 years in the body).
- A degree the profile lacks is written as mandatory (if `skip_if_degree_required`).
- The core skill is one the profile does not have (hand-coding, advanced SQL, Figma, media buying…).
- A language is required above the profile's real level, or not in `languages`.
- The title lies: a "Product Builder" who is really PM + designer + developer; a "Growth" role that is 100 % paid ads.
- The job is somewhere other than the card says ("Paris" on WTTJ, Frankfurt in the text).
- The company was already contacted (the script filters, but check subsidiaries and brand names).
- Duplicate: two roles in the same company → keep only the closest one.

## Prefer
- Openness signals: "atypical profile", "self-taught", "junior welcome", "first experience", "show us your projects".
- A core of the role that matches the **proofs** in `profile.md`, not just the keywords.
- Listings less than 14 days old.

## Stretch
A listing one requirement above the profile can stay, marked "stretch", within `stretch_max_percent`.
Never two gaps on the same listing.

## Shortlist format
One table, one row per listing, best fit first, in the user's language:

| # | Company | Role | Posted | Exp. | Salary | Route | Why it fits | Risk |
|---|---|---|---|---|---|---|---|---|

- "Why it fits": the decisive signal from the listing, 15 words max.
- "Risk": the missing requirement, without sugar-coating.
- "Route": WTTJ form, or the external ATS (Teamtailor, Greenhouse, Lever, Workday…), or another board.
- Then list the skipped listings, one line each with the reason, so the user can rescue one.

Then ask for the GO: per listing, or for the whole batch. Respect `batch_size` and `quota`.

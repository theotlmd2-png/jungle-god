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

Every threshold comes from the user's `rules.toml`. There is no "right" level: a senior and a career
changer get opposite shortlists from the same sweep, and both are correct.

## Skip when
- Required experience is outside `min_years_required` / `max_years_required` (0 = no limit). Read the
  text, not only the badge: the level shown on the card and the one written in the body often differ.
- A degree the profile lacks is written as mandatory, if `skip_if_degree_required`.
- The core skill of the role is one the profile does not have.
- A language is required above the profile's real level, or is not in `languages`.
- It hits one of the user's `deal_breakers`.
- The title does not match the content (the role is really another job under a trendy name).
- The job is somewhere other than the card says (one city on the card, another in the text).
- The company was already contacted (the script filters, but check subsidiaries and brand names).
- Duplicate: two roles in the same company → keep only the closest one.

## Prefer
- A core of the role that matches the **proofs** in `profile.md`, not just the keywords.
- Signals that the listing is open to this specific profile (noted at onboarding: what the user brings
  that is unusual, and how listings tend to phrase it).
- Recent listings, within `max_listing_age_days`.

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

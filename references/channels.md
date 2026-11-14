# Beyond WTTJ: other sites and channels

WTTJ is the sweep engine, but a large share of applications happens elsewhere: the listing redirects
to an ATS, the company has its own career page, or the same role is on another board. The author's own
run: 200+ applications, a good part of them outside WTTJ. Enabled channels: `rules.toml [channels]`.

## Principle: autonomous, but never blind
Onboarding fills the **Application kit** in `profile.md` precisely so that Claude can complete an unknown
form alone. On any site:
1. Read the whole form before typing (all steps, if it is a multi-step wizard).
2. Map every field to the kit, the batch's `answers`, or the letter.
3. A field with no source → ask once, save the answer in the kit, continue.
4. Report right after, in one line, what was done on that site (see `apply.md`).

## ATS behind a WTTJ listing
`details.py` gives `route` and `apply_url`. Greenhouse questions are fetched ahead of time. For the others,
open the form, read its questions, prepare the answers, then fill it.

| ATS | Notes |
|---|---|
| Greenhouse, Lever, Ashby, Workable, Teamtailor, Recruitee | No account. Often in English. Custom questions. |
| Workday, Taleo, SuccessFactors, iCIMS | Account required: follow `forms.accounts`. Multi-step, slow. Check every page. |
| Welcome Kit / WTTJ native | Two file inputs (photo, then CV). |

## Other boards (`other_boards`)
- **Company career pages**: always worth checking when a WTTJ listing looks old; the role is often still open there.
- **Indeed, HelloWork, APEC, JobTeaser, LinkedIn**: search there with the same keywords. Apply only through
  forms that need no login, or with the user's own logged-in session. Never create accounts without
  `forms.accounts` allowing it.
- **LinkedIn**: the user's logged-in browser only. Low pace. No automated connection requests or messages.
- Same triage, same letter method, same blacklist: one listing found elsewhere = one entry in
  `applications.json` with its real `route`.

## Spontaneous applications (`spontaneous`)
For a company that fits but has no open role: find the right contact (careers page, "jobs@" address,
hiring manager on the company site), write a short email with the letter method, and create a **draft**
(Gmail MCP if connected). Never send an email without an explicit GO on that email.

## Regional or niche markets
When WTTJ is thin (outside big cities, specific sectors), say so with numbers ("4 relevant listings in 30 days")
and propose the next channel instead of lowering the triage bar.

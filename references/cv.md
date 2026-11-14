# CVs: built during the conversation, one per target market

The CV is not a form to fill. It grows while the user talks, and at the end of onboarding it is revealed:
"With your profile, I built 1, 2 or 3 CVs. Here they are. Do we target these markets?"

## 1. First: is there a CV?
Ask early, in block B: "Do you have a CV? Drop the file here (PDF, Word, a link), even an old one."
- **Yes** → read it fully, extract every fact into `profile.md`, then only ask about what is missing or
  vague. Keep its good parts; it will still be rebuilt in the formats below.
- **No** → say "No problem, I'll build it with you as we talk", and from then on every answer feeds it.

## 2. Direct questions, fast
Short, plain, spoken questions that cover a whole theme at once, the way a friend would ask:
"What did you do after high school? Which studies, which school?", "Your jobs or internships, from the
first one?", "Your passions, what you do outside work?". Two or three per message, no preamble, no
lecture on why you ask. The whole CV interview should take about ten minutes. Dig deeper only where a
strong proof is hiding (a result, a project, a number). What a strong CV needs:
- **Identity**: name, phone, email, city, LinkedIn or portfolio (asked once, near the end, not first).
- **Each experience**: company exact name, role, start and end month/year, city, team or service,
  2 to 4 concrete missions, tools used, and **one result** (a number, a decision, a delivery). If there is no
  number, ask what changed thanks to them; never invent one.
- **Education**: degree, school, year, specialisation, notable project or thesis.
- **Skills**: software with honest level, methods, certifications, languages with real level.
- **Gaps and side paths**: travel, career break, side projects, volunteering: what they did and learned.
  A gap explained in one line beats a hidden gap.
- **Interests**: only those that say something (team sport, a certification like diving levels, a build project).

## 3. Find the markets (1 to 3)
From what they say, identify up to three markets the profile can credibly target, e.g. the core job, a
neighbouring sector, a role that uses the same skills differently. Say it in one line as soon as it
becomes visible ("With your lab experience, R&D and testing roles could fit too"), and confirm later.

## 4. Research what works, per market
For each market, search the web (WebSearch) for what recruiters in that sector and country expect from a
CV at that level, e.g. "CV ingénieur mécanique junior France recruteur", "CV customer success manager
exemple 2026". Look for: section order, length, photo or not, title style, how results are written,
what gets a CV binned. Note 3 to 5 takeaways per market in `profile.md › CV research`, with sources.
Use the findings, never copy a CV.

## 5. Build
- Start from `templates/cv.html` (sidebar layout, one accent colour) and adapt it to the research:
  section order, single or two columns, photo slot, density. One file per market:
  `cv/cv-<market>.html` → `python $SK/scripts/cv_pdf.py cv/cv-<market>.html`.
- Same facts in every CV, different **title, accroche, order of proofs and keywords** per market.
- Language of the market (French CV for French listings unless the sector works in English).
- **Check each render yourself** before showing it (screenshot at 794×1123, or read the PDF): one page,
  no empty band, nothing cut, aligned columns. Missing facts stay in [brackets], visibly.

## 6. The reveal
At the end of onboarding, not before:
"With your profile, I built N CVs:" then for each one, the market, the title, why it fits in one line, and
open the PDFs (`open cv/*.pdf`). Then ask: "Do we target these markets? Anything to change?"
The answer sets the families in `criteria.toml` (one family per kept market, with its CV).

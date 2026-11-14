# Letters and form answers

> Defaults below: `rules.toml [letter]` and `[forms]` win. Always start from the **approved model letter** in `profile.md`.

First screenings are often CV-only, sometimes within hours. A letter is not a life story: in ten
seconds it must show the listing was read and that there is a proof for each expectation.

## Method: start from WHAT THEY EXPECT
1. Extract the 2 or 3 central expectations from `missions` and `profile`, in their own words.
2. **One proof per expectation**, taken from `profile.md`: a fact and a true number.
3. If there is a gap, say it honestly in `gap_sentence` form, with what the person comes to learn.
4. End on drive and desire, never on a reservation.

## Format
- `paragraphs` short paragraphs, 10 to 15 lines in total. `opening` first, in the `tone` set at onboarding.
- First paragraph: their stake, their customers' or their product's, not "I".
- `single_link`: one link per application, at the end. If the form already has a portfolio or LinkedIn
  field carrying it, remove it from the letter.
- Signature: first and last name.
- Plain text pasted into the form field. A PDF only if the form demands one (`cv_pdf.py` works for letters too).
- Language: the listing's, unless `language` says otherwise.

## Never
- Invent anything: a customer, a number, a date ("last week"), a deliverable, a tool. Not in `profile.md` = does not exist.
- Inflate a side project ("my clients" when there were none).
- Use `banned_phrases` or anything in `never_mention`.
- Reuse a letter: each first paragraph must be impossible to send to another company.

## Form answers
- Answer EVERY question (if `answer_every_question`), required or not, tailored to the company.
- 2 to 4 sentences, first person, a number when it is true.
- Standard fields (salary, notice, right to work, address, "how did you hear about us"…): take them from
  the **Application kit** in `profile.md`. Missing → ask once, then save the answer there for next time.
- A tool never used: say so honestly and name the equivalent actually practised.
- Sensitive questions: per `sensitive_questions`.

## Storage
All applications of a batch go to `applications/batch-YYYY-MM-DD/applications.json`
(format: `templates/applications.example.json`). Then **show every letter in full in the chat**, one after
the other: `### Company — Role`, one line with the risk, the letter in a quote block, then the prepared
form answers. The user reviews and corrects in the chat. Never send them to an HTML page or the raw JSON
for review; `review.py` is only the end-of-batch scoreboard.

## Corrections
When the user corrects ONE rule ("just apply the link rule"), fix that rule and nothing else. Do not rewrite
the batch. If the correction is durable, add it to `profile.md › Learned preferences` or `rules.toml`.

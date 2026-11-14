# Applying with Claude in Chrome

> Sending mode, consents and accounts come from `rules.toml [sending]` and `[forms]`.

Load the `mcp__claude-in-chrome__*` tools first (one ToolSearch call). If the extension is not connected,
open the listings with `open -a "Google Chrome" <url>` and hand the user the texts to paste (`texts_only` mode).

## Rules
- **Sequential, one window, in the foreground.** One tab per listing, one after the other. Several agents
  filling forms in parallel ends in chaos: mixed tabs, double submissions.
- Before clicking Submit, check every field with JavaScript: name, email, phone, CV file, letter, answers.
- **Right file, right field.** WTTJ forms have two `input[type=file]`: profile photo first, then CV.
  Target `input[name="resume"]`, never the first one found.
- CV: the PDF of the family stated in `applications.json`, never another.
- Answers: from `applications.json`, then the **Application kit** in `profile.md`. Never improvise a fact.
- Consents, terms, newsletters: tick what is mandatory to apply, per `mandatory_consents`. Never tick optional ones.
- Submit only in `claude_sends_after_go` mode, after the GO on the batch. In `claude_fills_user_sends`,
  fill, check, then tell the user which tab is ready.

## Mandatory stops (hand back to the user)
- Account creation, if `accounts = "ask"` or `"user_creates"` (Workday, Taleo, SuccessFactors…). Never
  choose or store a password: the user types it.
- CAPTCHA, email or SMS verification.
- Payment, ID document, or any request that looks off.
- A question with no answer in the profile and no safe default.
- No Submit button found: do not click around, report it.

## After each application: make it visible
1. Check the confirmation page or banner.
2. Update `status` in `applications.json`: `sent YYYY-MM-DD`, `filled not sent`, `blocked: <reason>`,
   `skipped: <reason>`; append to `log` what was done on which site.
3. If `notify.desktop`:
   ```bash
   python $SK/scripts/notify.py "Sent: <Company> — <Role>" "via <route> · <n> questions answered · <i>/<total>"
   ```
4. One line in the chat, right after the fact: `✓ Acme — AI Builder · Greenhouse · 6 questions · CV ai · 7/12`.
   For third-party sites, say what happened there ("created no account, answered the 4 screening questions,
   uploaded cv-ai.pdf").

## End of batch: the recap
- Regenerate `review.py` (scoreboard: applications, sent, to finish, sites) and open it.
- In the chat: sent count, per-site breakdown, what the user must finish themselves (email verification
  link, account), and the running total since the start (`applications/batch-*/applications.json`).
- Run `blacklist.py` so these companies disappear from the next sweeps.

## Known traps
- Tiny Chrome window (Stage Manager): bring it to the front and resize before acting.
- Teamtailor, Ashby and Greenhouse forms are often in English: answer in English.
- WTTJ may show the head office city, not the job's: the listing text wins.
- A redirect to an ATS can drop the WTTJ answers: refill everything on the ATS.

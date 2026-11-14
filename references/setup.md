# Setup (10 minutes, once)

Do everything you can yourself. Only hand over what needs the user's own hands (CV files, logging in).

## 1. Working folder
The user's data lives outside the skill, in a folder of their own (default `~/job-hunt`):

```bash
mkdir -p ~/job-hunt/cv ~/job-hunt/applications && cd ~/job-hunt
SK=~/.claude/skills/jungle-god
cp $SK/.env.example .env
cp $SK/templates/criteria.example.toml criteria.toml
cp $SK/templates/rules.example.toml rules.toml
cp $SK/templates/profile.example.md profile.md
```

Python 3.11+ is enough, with no dependency. **Google Chrome with the Claude in Chrome extension is required**:
it is where the applications are opened and filled, in front of the user. Safari cannot be driven.

## 2. Optional: fast keyword search
`sweep.py` needs no key: it reads WTTJ's public job pages. `search.py` is an optional fast mode that
searches WTTJ's whole index by keyword; it needs the site's public search credentials in `.env`.
Offer it only to users who ask for more coverage. The user reads them once in Chrome DevTools: open
https://www.welcometothejungle.com/fr/jobs, `Cmd+Option+I` → **Network**, search anything on the site,
filter on `algolia`, open a request, copy `x-algolia-application-id` and `x-algolia-api-key` from
**Request Headers**. Write them into `.env` yourself. Never extract them by script: header values are
redacted for Claude in Chrome, and scripted extraction is treated as unauthorized access.

## 3. Smoke test
```bash
python $SK/scripts/sweep.py --probe "ingénieur mécanique"
```
Expected: `[OK] emploi-ingenieur-mecanique (20 listings on page 1)`. On a certificate error, the script already falls back to the
system store; if it still fails, `pip install certifi`.

## 4. Starting blacklist
If the user has applied before, collect those companies so they are never contacted twice.

- **WTTJ**: open https://www.welcometothejungle.com/fr/me/application-tracker (logged in), scroll to the
  bottom, read the page and write one company name per line in `applications/tracker.txt`. The page
  markup changes over time: read it rather than relying on a fixed selector.
- **Everything else** (other boards, emails, rejections): one name per line in `applications/extra.txt`.
  If Gmail is connected, search for application confirmations and rejections to fill it.

```bash
python $SK/scripts/blacklist.py --root applications
```

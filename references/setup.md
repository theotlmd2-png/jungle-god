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

Python 3.11+ is enough, with no dependency. Google Chrome is used for PDFs and for applying.

## 2. WTTJ search credentials
welcometothejungle.com searches an Algolia index with an application id and a **public, search-only key**,
sent by every visitor's browser. To find them:

1. Open https://www.welcometothejungle.com/fr/jobs in Chrome, then DevTools (`Cmd+Option+I`), **Network** tab.
2. Type a keyword in the site's search bar.
3. Filter requests on `algolia` and open one:
   - `x-algolia-application-id` → `WTTJ_ALGOLIA_APP`
   - `x-algolia-api-key` → `WTTJ_ALGOLIA_KEY`
   - the index name in the URL (`/indexes/<name>/`) should end with `published_at_desc`
4. Paste the values into `.env`.

With the Claude in Chrome extension, do it for the user: open the page, type a search, then read the
requests with `read_network_requests`. If the sweep ever returns 403, the key changed: do it again.

## 3. Smoke test
```bash
python $SK/scripts/search.py --days 3 --out applications/test/hits.json
```
Expected: `[OK] N listings since ...`. On a certificate error, the script already falls back to the
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

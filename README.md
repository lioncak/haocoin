# haocoin

Shared gym points tracker for three people. No build step, no dependencies.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The app |
| `data.txt` | Data source (booking site's transaction log) |
| `tools/sanitize.py` | Strips real names before writing `data.txt` |
| `names.local.json` | Real name → nickname map (gitignored) |

## Updating data

**Manual:**
```bash
pbpaste | python3 tools/sanitize.py && git commit -am "update" && git push
```

**Automated** (`tools/sync_local.sh`, local-only — the login uses OAuth, so the
session cookie stays on this machine, never in a cloud secret):

```bash
python3 -m venv .venv
.venv/bin/pip install playwright
.venv/bin/playwright install chromium
```
Export a logged-in session cookie (e.g. via the Cookie-Editor extension) to
`tools/goodtime_cookies.local.json`, then:
```bash
bash tools/sync_local.sh          # test it once
cp tools/com.haocoin.sync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.haocoin.sync.plist   # daily schedule
```
Logs at `tools/sync.local.log`. The script fails loudly (no commit) if the
cookie expires or the scrape returns nothing.

## Logic

- Per-person quota = total points ÷ number of people
- Remaining = quota − net points used (bookings minus refunds)
- Cancelled classes don't count as attended; late cancellations refund half
- Expiry is the latest `YYYY-MM-DD ~ YYYY-MM-DD` in the log

## Local preview

```bash
python3 -m http.server 8765
```

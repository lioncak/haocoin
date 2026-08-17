#!/bin/bash
# 在本機排程（launchd）跑：抓 17FIT 點數紀錄 → 換暱稱 → 有變動才 commit + push。
# cookie 全程留在這台機器上，不碰 GitHub Secrets、不碰任何雲端環境。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PY="$ROOT/.venv/bin/python3"   # 獨立 venv，裝 playwright 用（Homebrew 的系統 python3 擋掉了 pip install）
COOKIE_FILE="tools/goodtime_cookies.local.json"

if [ ! -f "$COOKIE_FILE" ]; then
  echo "[$(date '+%F %T')] 找不到 $COOKIE_FILE——先把 Cookie-Editor 匯出的 JSON 存成這個檔案。" >&2
  exit 1
fi
if [ ! -f names.local.json ]; then
  echo "[$(date '+%F %T')] 找不到 names.local.json，sanitize.py 沒有它跑不動。" >&2
  exit 1
fi
if [ ! -x "$PY" ]; then
  echo "[$(date '+%F %T')] 找不到 $PY——先建立 venv：python3 -m venv .venv && .venv/bin/pip install playwright && .venv/bin/playwright install chromium" >&2
  exit 1
fi

export GOODTIME_COOKIES
GOODTIME_COOKIES="$(cat "$COOKIE_FILE")"

echo "[$(date '+%F %T')] 開始抓資料"

# 不要直接用 pipe（scrape | sanitize）——之前踩過一次坑：scrape 那邊崩潰、
# 印出空字串，pipe 的失敗訊號沒有可靠傳到後面，sanitize 收到空輸入還是
# 乖乖寫了「0 筆」蓋掉 data.txt。這裡自己顯式檢查 exit code + 是否有輸出，
# 兩層都過了才餵給 sanitize.py（sanitize.py 自己現在也擋空輸入/0 筆了，
# 這裡是雙重保險，不是重複）。
set +e
RAW="$("$PY" tools/scrape_goodtime.py)"
SCRAPE_STATUS=$?
set -e

if [ "$SCRAPE_STATUS" -ne 0 ] || [ -z "$RAW" ]; then
  echo "[$(date '+%F %T')] 抓資料失敗（exit $SCRAPE_STATUS），不繼續往下跑，data.txt 沒有被動到" >&2
  exit 1
fi

echo "$RAW" | "$PY" tools/sanitize.py

if git diff --quiet -- data.txt; then
  echo "[$(date '+%F %T')] data.txt 沒變化，不用 commit"
  exit 0
fi

git add data.txt
git -c user.name="好幣同步機器人" -c user.email="sync-bot@users.noreply.github.com" \
    commit -m "自動同步好幣點數 $(date '+%Y-%m-%d')"
git push
echo "[$(date '+%F %T')] 已推上去"

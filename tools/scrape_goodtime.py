#!/usr/bin/env python3
"""抓 goodtime.17fit.com 的點數交易紀錄，輸出成跟手動複製一樣的原始格式。

這支不處理登入——17FIT 用 LINE 登入，沒辦法在無人值守的排程裡重跑一次
OAuth。做法是重用一組已經登入過的 session cookie（存在 GOODTIME_COOKIES
這個環境變數/GitHub Secret 裡），cookie 過期了就會直接失敗、不會偷偷寫出
空白或錯誤的資料——寧可讓排程紅字失敗通知你，也不要靜靜地把 data.txt 弄壞。

用法：
    GOODTIME_COOKIES='[{"name":"...","value":"...","domain":"goodtime.17fit.com","path":"/"}, ...]' \
      python3 tools/scrape_goodtime.py > raw.txt

cookie 怎麼拿：瀏覽器裝 Cookie-Editor 擴充套件，登入好 17FIT 後在
goodtime.17fit.com 頁面點擴充套件圖示 → Export → 複製整段 JSON，
存進 GitHub repo 的 Secret（Settings → Secrets → Actions），
名字就叫 GOODTIME_COOKIES。

這支只印出原始文字到 stdout，跟你現在手動複製貼上的格式一樣——
下一步一樣是 `python3 tools/sanitize.py`，兩支不用合併，職責分開。
"""

import json
import os
import re
import sys

MEMBERSHIP_URL = "https://goodtime.17fit.com/my-account/membership?contract_type=valid"
LOGIN_MARKERS = ("請先登入", "Please Login", "/account?success_url")


def load_cookies():
    raw = os.environ.get("GOODTIME_COOKIES")
    if not raw:
        sys.exit("找不到 GOODTIME_COOKIES 環境變數——這支不處理登入，cookie 要自己先準備好。")
    try:
        cookies = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.exit(f"GOODTIME_COOKIES 不是合法的 JSON：{e}")

    # Cookie-Editor 匯出的欄位比 Playwright 要的多也不完全同名，這裡做個轉換，
    # 使用者不用自己手動改格式。
    out = []
    for c in cookies:
        if not c.get("name") or "value" not in c:
            continue
        item = {
            "name": c["name"],
            "value": c["value"],
            "domain": c.get("domain") or "goodtime.17fit.com",
            "path": c.get("path") or "/",
        }
        same_site = (c.get("sameSite") or "").lower()
        if same_site in ("lax", "strict", "none"):
            item["sameSite"] = same_site.capitalize()
        if isinstance(c.get("expirationDate"), (int, float)):
            item["expires"] = c["expirationDate"]
        out.append(item)

    if not out:
        sys.exit("GOODTIME_COOKIES 解析出來是空的，檢查一下匯出的內容。")
    return out


def norm(s):
    """把儲存格內部的換行/多個空白收成一個空白，日期跟原因欄都需要這個。"""
    return re.sub(r"\s+", " ", (s or "").strip())


def scrape():
    # Playwright 只在跑這支的時候才需要，本機沒裝也不影響其他 tools/*.py
    from playwright.sync_api import sync_playwright

    cookies = load_cookies()
    lines = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        context.add_cookies(cookies)
        page = context.new_page()

        page.goto(MEMBERSHIP_URL, wait_until="networkidle")

        body_text = page.inner_text("body")
        if any(marker in body_text or marker in page.url for marker in LOGIN_MARKERS):
            browser.close()
            sys.exit(
                "被導回登入頁了，GOODTIME_COOKIES 已經過期——"
                "重新登入一次、重新匯出 cookie、更新 GitHub Secret。"
            )

        # 「+Details」是 Vue 元件，點開才會渲染交易紀錄表格；可能不只一組方案。
        detail_toggles = page.get_by_text(re.compile(r"^\+?\s*Details$"))
        count = detail_toggles.count()
        if count == 0:
            browser.close()
            sys.exit(
                "頁面上找不到「Details」——可能是頁面改版了，"
                "把這次失敗的錯誤訊息貼給我，我要更新選取邏輯。"
            )
        for i in range(count):
            detail_toggles.nth(i).click()
        page.wait_for_timeout(800)  # 展開動畫 + 資料渲染

        # 逐一檢查頁面上每個 <table>，欄位表頭同時有 Date/Reason/Change
        # 才當作交易紀錄表（總覽卡片那個 table 表頭不是這個組合，會被跳過）。
        tables = page.locator("table")
        found_records_table = False
        for ti in range(tables.count()):
            table = tables.nth(ti)
            header_text = norm(table.inner_text())
            if not ("Date" in header_text and "Reason" in header_text and "Change" in header_text):
                continue
            found_records_table = True
            rows = table.locator("tbody tr")
            for ri in range(rows.count()):
                cells = rows.nth(ri).locator("td")
                if cells.count() < 4:
                    continue
                date = norm(cells.nth(0).inner_text())
                reason = norm(cells.nth(1).inner_text())
                change = norm(cells.nth(2).inner_text())
                user = norm(cells.nth(3).inner_text())
                if not re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", date):
                    continue  # 不是資料列（可能是合併儲存格的裝飾列），跳過
                lines.append(f"{date}\t{reason}\t{change}\t{user}")

        browser.close()

    # 2026-08-17 實測抓到過同一批真實資料被完整重複 3 次（117 筆裡只有 39 筆不重複，
    # 剛好整除，不是巧合）——原因待查（可能是「Details」按鈕或表格在頁面上不只比對到一份），
    # 但不管根因是什麼，同一筆交易本來就不可能逐字完全重複兩次，
    # 這裡直接照完整那行的內容去重、保留第一次出現的順序，比賭我猜對 DOM 結構更可靠。
    before = len(lines)
    seen = set()
    deduped = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            deduped.append(line)
    if before != len(deduped):
        print(f"去重：{before} 筆 → {len(deduped)} 筆（丟掉 {before - len(deduped)} 筆逐字重複的）", file=sys.stderr)
    lines = deduped

    if not found_records_table:
        sys.exit(
            "有找到「Details」按鈕、點開了，但頁面上沒有 Date/Reason/Change 表頭的表格——"
            "多半是畫面結構改了，把這次的錯誤訊息貼給我。"
        )
    if not lines:
        sys.exit("表格找到了，但一筆資料都沒解析出來——這比整個失敗更可疑，先不要覆蓋 data.txt，貼錯誤訊息給我看。")

    return lines


def main():
    lines = scrape()
    sys.stdout.write("\n".join(lines) + "\n")
    print(f"抓到 {len(lines)} 筆紀錄", file=sys.stderr)


if __name__ == "__main__":
    main()

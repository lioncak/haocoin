# 好幣

三個人一起買的運動點數，各自還剩多少。手機開起來像 app，可以加到主畫面。

## 檔案

| 檔案 | 作用 |
| --- | --- |
| `index.html` | 整個 app，沒有相依套件 |
| `data.txt` | 資料來源，就是網站 Details 表格原封不動的內容 |
| `tools/sanitize.py` | 把真名換成暱稱後寫進 `data.txt` |
| `names.local.json` | 真名 → 暱稱對照表，**不進 git** |

## 更新資料

### 手動（一直都可以這樣做）

從訂課網站（goodtime.17fit.com）的 Details 表格整段複製，然後：

```bash
pbpaste | python3 tools/sanitize.py && git commit -am "update" && git push
```

推上去之後網頁會自己讀到新的 `data.txt`，不用改任何程式。

臨時要看還沒推上去的資料，也可以在 app 的「資料」分頁直接貼，會存在自己手機裡，
按「回到同步資料」就會切回 `data.txt`。

### 自動（本機排程，`tools/sync_local.sh`）

17FIT 用 LINE 登入，沒辦法讓排程自己重跑一次 OAuth，所以走的是「重用登入過的
session cookie」這條路，不是帳密自動登入。**cookie 這種東西等於能直接操作帳號，
故意不放進 GitHub（就算是加密的 Secret）**——全部留在這台機器上，排程用 macOS
內建的 launchd，不碰任何雲端環境。cookie 過期了腳本會直接失敗（不會生出
空白/錯誤的 `data.txt`），到時候重新登入匯出一次就好：

1. 建一個獨立 venv 裝 Playwright（Homebrew 的系統 python3 會擋直接 `pip install`）：
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install playwright
   .venv/bin/playwright install chromium
   ```
2. 瀏覽器裝 **Cookie-Editor** 擴充套件，登入好 17FIT，在 `goodtime.17fit.com`
   任一頁點擴充套件圖示 → Export → 複製整段 JSON，存成
   `tools/goodtime_cookies.local.json`（`.local.json` 結尾的檔名已經在
   `.gitignore` 裡，不會進 git）。
3. 先手動跑一次確認會不會過：
   ```bash
   bash tools/sync_local.sh
   ```
4. 沒問題的話裝成排程（`tools/com.haocoin.sync.plist` 裡的路徑已經寫死成
   這台機器的路徑，換機器要改）：
   ```bash
   cp tools/com.haocoin.sync.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.haocoin.sync.plist
   ```
   預設每天早上 11 點跑一次，改 plist 裡的 `Hour`/`Minute` 可以調時間。
   **電腦當下沒開機/沒醒著就不會跑**，這是本機排程的取捨，不是 bug。
5. 要停用：`launchctl unload ~/Library/LaunchAgents/com.haocoin.sync.plist`
6. 執行紀錄在 `tools/sync.local.log`（同樣被 gitignore 擋掉，不會進 git）。

`tools/scrape_goodtime.py` 只負責把 17FIT 頁面上的表格轉成跟手動複製一樣的
原始文字，真正的暱稱替換還是交給 `tools/sanitize.py`，職責沒有合併——這支
本身不管是本機跑還是雲端跑都一樣，跟執行環境無關。

## 它怎麼算的

- 每人額度 = 總點數 ÷ 人數（人數從紀錄裡自動抓）
- 剩餘 = 額度 − 淨用掉的點數（預約扣的減掉取消退的）
- 取消掉的課不算「已上」；遲退只退一半，差額算在那個人身上
- 效期直接讀紀錄裡最新一筆 `YYYY-MM-DD ~ YYYY-MM-DD`

## 本機預覽

```bash
python3 -m http.server 8765
```

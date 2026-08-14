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

從訂課網站的 Details 表格整段複製，然後：

```bash
pbpaste | python3 tools/sanitize.py && git commit -am "update" && git push
```

推上去之後網頁會自己讀到新的 `data.txt`，不用改任何程式。

臨時要看還沒推上去的資料，也可以在 app 的「資料」分頁直接貼，會存在自己手機裡，
按「回到同步資料」就會切回 `data.txt`。

## 它怎麼算的

- 每人額度 = 總點數 ÷ 人數（人數從紀錄裡自動抓）
- 剩餘 = 額度 − 淨用掉的點數（預約扣的減掉取消退的）
- 取消掉的課不算「已上」；遲退只退一半，差額算在那個人身上
- 效期直接讀紀錄裡最新一筆 `YYYY-MM-DD ~ YYYY-MM-DD`

## 本機預覽

```bash
python3 -m http.server 8765
```

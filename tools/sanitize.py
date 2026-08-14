#!/usr/bin/env python3
"""把原始好幣紀錄換成暱稱版，輸出成 data.txt。

用法：
    python3 tools/sanitize.py raw.txt            # 寫進 data.txt
    pbpaste | python3 tools/sanitize.py          # 直接吃剪貼簿

對照表放在 names.local.json（不會進 git）。沒對到的名字會直接報出來，
避免不小心把真名推上公開的 repo。
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP_FILE = ROOT / "names.local.json"
OUT_FILE = ROOT / "data.txt"

# 一行紀錄的最後一欄是使用者，抓 "<±N> Point" 後面的東西
TAIL = re.compile(r"([+\-−–]\s?\d+)\s*Point\s*(.*)$")


def load_map():
    if not MAP_FILE.exists():
        sys.exit(f"找不到 {MAP_FILE.name}，請先建立 {{\"真名\": \"暱稱\"}} 的對照表。")
    return json.loads(MAP_FILE.read_text(encoding="utf-8"))


def sanitize(text, mapping):
    out, unknown = [], set()
    for line in text.splitlines():
        stripped = line.rstrip()
        m = TAIL.search(stripped)
        if m and m.group(2).strip():
            name = m.group(2).strip()
            if name in mapping:
                stripped = stripped[: m.start(2)] + mapping[name]
            else:
                unknown.add(name)
        out.append(stripped)
    return "\n".join(out).rstrip() + "\n", unknown


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    text = pathlib.Path(src).read_text(encoding="utf-8") if src else sys.stdin.read()

    mapping = load_map()
    result, unknown = sanitize(text, mapping)

    if unknown:
        sys.exit(
            "以下名字不在對照表裡，先補進 names.local.json 再跑一次："
            + "、".join(sorted(unknown))
        )

    OUT_FILE.write_text(result, encoding="utf-8")
    rows = sum(1 for line in result.splitlines() if "Point" in line)
    print(f"寫入 {OUT_FILE}（{rows} 筆點數紀錄）")


if __name__ == "__main__":
    main()

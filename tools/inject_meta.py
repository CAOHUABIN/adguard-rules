#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为输出规则文件注入/更新 ABPP 元数据头，使 AdGuard iOS / AdGuard Home 订阅详情页
正确显示：标题、版本、更新时间、官网、规则数（规则数由 App 自动统计）。
只替换 Title/Description/Version/Last modified/Expires/Homepage 这几个字段，
保留文件头部原有的其它说明行（统计、来源清单等）。

用法:
  inject_meta.py <file> <title> <description> [--hosts]
"""
import sys, datetime, zoneinfo

TZ = zoneinfo.ZoneInfo("Asia/Bangkok")
REPO = "https://github.com/CAOHUABIN/adguard-rules"

KEYS = ("Title", "Description", "Version", "Last modified", "Expires", "Homepage")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    is_hosts = "--hosts" in sys.argv
    path, title, desc = args[0], args[1], args[2]

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # 找到第一个非头部行（规则正文开始）
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s == "" or s.startswith("!") or s.startswith("#") or s.startswith("[Adblock Plus"):
            i += 1
        else:
            break
    header = lines[:i]
    body = lines[i:]

    # 去掉已有同名元数据行（保留其它说明行）
    kept = []
    for ln in header:
        t = ln.strip()
        if t.startswith("[Adblock Plus"):
            continue
        if t.startswith(("!", "#")):
            key = t[1:].strip().split(":", 1)[0]
            if key in KEYS:
                continue
        kept.append(ln)

    now = datetime.datetime.now(TZ)
    version = f"{now.year}.{now.month}.{now.day}.{now.hour:02d}{now.minute:02d}"
    iso = now.isoformat(timespec="seconds")
    c = "#" if is_hosts else "!"

    new_header = [] if is_hosts else ["[Adblock Plus 2.0]"]
    new_header += [
        f"{c} Title: {title}",
        f"{c} Description: {desc}",
        f"{c} Version: {version}",
        f"{c} Last modified: {iso}",
        f"{c} Expires: 1 day (update frequency)",
        f"{c} Homepage: {REPO}",
        f"{c}",
    ]
    # 保留原有的统计/来源说明行
    new_header += kept

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_header + body) + "\n")
    print(f"[inject] {path}: Version={version}")


if __name__ == "__main__":
    main()

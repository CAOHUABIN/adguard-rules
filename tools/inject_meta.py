#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为输出规则文件注入 ABPP 元数据头，使 AdGuard iOS / AdGuard Home 订阅详情页
正确显示：标题、版本、更新时间、官网、规则数（规则数由 App 自动统计）。

用法:
  inject_meta.py <file> <title> <description> [--hosts]
会自动剥离文件原有的头部注释行，再写入标准 ABPP 头。
"""
import sys, re, datetime, zoneinfo

TZ = zoneinfo.ZoneInfo("Asia/Bangkok")
REPO = "https://github.com/CAOHUABIN/doubao-adguard-rules"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    is_hosts = "--hosts" in sys.argv
    path, title, desc = args[0], args[1], args[2]

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # 剥离原有头部：注释行（! / #）、Adblock Plus 声明行、空行
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s == "" or s.startswith("!") or s.startswith("#") or s.startswith("[Adblock Plus"):
            i += 1
        else:
            break
    body = lines[i:]
    # 去掉 body 开头多余空行
    while body and body[0].strip() == "":
        body.pop(0)

    now = datetime.datetime.now(TZ)
    version = f"{now.year}.{now.month}.{now.day}.{now.hour:02d}{now.minute:02d}"
    iso = now.isoformat(timespec="seconds")
    c = "#" if is_hosts else "!"

    header = [] if is_hosts else ["[Adblock Plus 2.0]"]
    header += [
        f"{c} Title: {title}",
        f"{c} Description: {desc}",
        f"{c} Version: {version}",
        f"{c} Last modified: {iso}",
        f"{c} Expires: 1 day (update frequency)",
        f"{c} Homepage: {REPO}",
        f"{c}",
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(header + body) + "\n")
    print(f"[inject] {path}: Version={version} LastModified={iso}")


if __name__ == "__main__":
    main()

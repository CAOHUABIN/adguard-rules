#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""国内网络专用 Safari 精简拦截规则。
只用中文/国内来源（AdGuard Chinese / EasyList China / CJX / anti-AD），
提取 Safari 内容拦截器支持的主机名规则（||domain^），按来源收录数优先
截取 CAP 条，适配 iPhone AdGuard Safari 保护的单列表上限。
"""
import os, re

ROOT = "/home/user/Doubao/chats/38450599647723266/adguard_rules"
RAW = os.path.join(ROOT, "raw")
OUT = os.path.join(ROOT, "output")
CAP = 49000  # Safari 单内容拦截器规则上限约 50000，留余量

CN_FILES = ["adguard_chinese.txt", "easylistchina.txt", "cjx_rule.txt", "dns_antiad.txt"]

counts = {}  # domain -> set of sources

def add(d, src):
    d = d.rstrip('.').lower()
    if re.fullmatch(r"[a-z0-9\-\.]+\.[a-z]{2,}", d):
        counts.setdefault(d, set()).add(src)

def skip(line):
    if '##' in line or '#@' in line or '#$' in line or '#?' in line or '#%' in line:
        return True
    if '$' in line or line.startswith('/') or line.startswith('@@'):
        return True
    return False

for fn in CN_FILES:
    p = os.path.join(RAW, fn)
    if not os.path.exists(p):
        continue
    for line in open(p, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line or line.startswith(('!', '[', '#')) or skip(line):
            continue
        m = re.fullmatch(r"\|\|([a-z0-9\-\.]+)\^", line)
        if m:
            add(m.group(1), fn)
            continue
        if re.fullmatch(r"[a-z0-9\-\.]+\.[a-z]{2,}", line):  # 纯域名行
            add(line, fn)

total = len(counts)
items = sorted(counts.items(), key=lambda kv: (-len(kv[1]), kv[0]))
selected = items[:CAP]

outp = os.path.join(OUT, "safari_cn_rules.txt")
with open(outp, "w", encoding="utf-8") as f:
    f.write("[Adblock Plus 2.0]\n")
    f.write("! Title: 国内网络 Safari 精简拦截规则（主机名版）\n")
    f.write("! 只含 Safari 支持的主机名规则 ||域名^，不含进阶语法\n")
    f.write("! 来源: AdGuard Chinese / EasyList China / CJX / anti-AD\n")
    f.write(f"! 覆盖域名: {len(selected)}/{total}（按来源收录数优先截取）\n!\n")
    for d, srcs in selected:
        f.write(f"||{d}^\n")
print(f"[写出] {outp}  总域名 {total}，选用 {len(selected)}（最高覆盖数 {max(len(s) for _,s in selected)}）")

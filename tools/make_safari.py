#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从本地已下载的 16 个来源生成 Safari 友好的精简拦截规则。
只保留 Safari 内容拦截器支持的主机名规则（||domain^），去掉进阶语法
（正则、$ 修饰、元素隐藏、@@ 例外等），并按“被多少个来源收录”优先截取
CAP 条，适配 Safari 单规则列表上限。
"""
import os, re

ROOT = "/home/user/Doubao/chats/38450599647723266/adguard_rules"
RAW = os.path.join(ROOT, "raw")
OUT = os.path.join(ROOT, "output")
CAP = 49000  # Safari 单内容拦截器规则上限约 50000，留余量

AD_FILES = ["adguard_base.txt","adguard_tracking.txt","adguard_social.txt",
            "adguard_mobile.txt","adguard_annoyances.txt","adguard_dns.txt",
            "adguard_url_tracking.txt","adguard_chinese.txt","easylist.txt",
            "easyprivacy.txt","easylistchina.txt","cjx_rule.txt"]
DNS_FILES = ["dns_stevenblack.txt","dns_hagezi_pro.txt","dns_antiad.txt",
             "dns_1hosts_lite.txt"]

counts = {}  # domain -> set of sources

def add(d, src):
    d = d.rstrip('.').lower()
    if re.fullmatch(r"[a-z0-9\-\.]+\.[a-z]{2,}", d):
        counts.setdefault(d, set()).add(src)

def skip(line):
    # 跳过元素隐藏 / 高级语法 / 正则 / 例外等 Safari 不友好的行
    if '##' in line or '#@' in line or '#$' in line or '#?' in line or '#%' in line:
        return True
    if '$' in line or line.startswith('/') or line.startswith('@@'):
        return True
    return False

for fn in AD_FILES:
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

for fn in DNS_FILES:
    p = os.path.join(RAW, fn)
    if not os.path.exists(p):
        continue
    for line in open(p, encoding="utf-8", errors="replace"):
        line = line.strip().lower()
        if not line or line.startswith(('#', '!')):
            continue
        parts = line.split()
        d = None
        if len(parts) >= 2 and parts[0] in ('0.0.0.0', '127.0.0.1', '::'):
            d = parts[1]
        elif len(parts) == 1 and re.fullmatch(r"[a-z0-9\-\.]+\.[a-z]{2,}", parts[0]):
            d = parts[0]
        if d:
            add(d, fn)

total = len(counts)
# 按来源覆盖数降序（多源一致=高置信），再按字母序保证稳定
items = sorted(counts.items(), key=lambda kv: (-len(kv[1]), kv[0]))
selected = items[:CAP]

outp = os.path.join(OUT, "safari_rules.txt")
with open(outp, "w", encoding="utf-8") as f:
    f.write("[Adblock Plus 2.0]\n")
    f.write("! Title: Doubao Safari 精简拦截规则（主机名版）\n")
    f.write("! 只含 Safari 支持的主机名规则 ||域名^，不含进阶语法\n")
    f.write(f"! 覆盖域名: {len(selected)}/{total}（按来源收录数优先截取）\n!\n")
    for d, srcs in selected:
        f.write(f"||{d}^\n")
print(f"[写出] {outp}  总域名 {total}，选用 {len(selected)}（最高覆盖数 {max(len(s) for _,s in selected)}）")

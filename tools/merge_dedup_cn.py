#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""国内网络专用拦截规则：合并去重多个中文/国内来源，输出 AdGuard 规则与 DNS 域名清单。
聚焦国内站点场景，不含国际全量列表，体积更小、更贴合国内网络、降低对国内正常服务的误伤。"""
import os, re

RAW = "/home/user/Doubao/chats/38450599647723266/adguard_rules/raw"
OUT = "/home/user/Doubao/chats/38450599647723266/adguard_rules/output"

# 国内网络核心来源：(文件名, 名称, 订阅URL, 类别)
CN_SOURCES = [
    ("adguard_chinese.txt", "AdGuard Chinese filter（官方中文过滤）", "https://filters.adtidy.org/extension/ublock/filters/224.txt", "中文/官方"),
    ("easylistchina.txt",   "EasyList China（EasyList 国内补充）",     "https://raw.githubusercontent.com/easylist/easylistchina/master/easylistchina.txt", "中文"),
    ("cjx_rule.txt",        "乘风广告过滤规则（CJX）",                "https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt", "中文"),
    ("dns_antiad.txt",      "anti-AD（中文广告+跟踪）",               "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt", "中文/DNS"),
]

SKIP = {"localhost", "localhost.localdomain", "local", "broadcasthost", "ip6-localhost",
        "ip6-loopback", "ip6-localnet", "ip6-mcastprefix", "ip6-allnodes", "ip6-allrouters",
        "ip6-allhosts", "0.0.0.0", "127.0.0.1", "255.255.255.255", "::", "::1", "fe80::1", "ff02::1"}

VALID_DOMAIN = re.compile(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?){1,}$")
HOSTS_IP = re.compile(r"^(?:0\.0\.0\.0|127\.0\.0\.1|::1?|::|255\.255\.255\.255|0\.0\.0\.1)\s+([^\s#]+)")
ADP_DOMAIN = re.compile(r"^\|\|([a-z0-9][a-z0-9\-]*(\.[a-z0-9][a-z0-9\-]*)+)\^?(?:\$.*)?$")

def is_comment(line):
    s = line.strip()
    return (not s) or s.startswith("!") or s.startswith("[Adblock Plus") or s.startswith("[Adblock+") or s.startswith("#")

def clean(dom):
    d = dom.strip().strip(".").lower()
    if ":" in d:
        d = d.split(":")[0].strip(".")
    return d

def main():
    rule_set = set()
    per_source = []
    for fname, name, url, cat in CN_SOURCES:
        path = os.path.join(RAW, fname)
        n_total = n_rules = 0
        if not os.path.exists(path):
            print(f"[跳过] 文件缺失: {fname}")
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for raw_line in f:
                line = raw_line.rstrip("\n").rstrip("\r").strip()
                n_total += 1
                if is_comment(line) or not line:
                    continue
                n_rules += 1
                rule_set.add(line)
        per_source.append((name, url, cat, n_total, n_rules))
        print(f"[载入] {name}: 总行={n_total} 规则行={n_rules}")

    rules = sorted(rule_set)
    total_rules = len(rules)
    print(f"\n国内规则合并去重后唯一规则数: {total_rules}")

    # ---------- 1) 国内 AdGuard 全格式规则 ----------
    header = []
    header.append("[Adblock Plus 2.0]")
    header.append("! Title: Doubao 国内网络专用拦截规则（AdGuard 格式）")
    header.append("! Version: 2026-11-03")
    header.append("! 说明: 专为国内网络环境整理，合并去重以下中文/国内来源。聚焦国内站点广告与跟踪拦截，")
    header.append("!       不含国际全量列表，体积更小、误伤更低。适用于 AdGuard / AdGuard Home / uBlock Origin / Adblock Plus。")
    header.append("! 来源清单（合并前原始规则数）：")
    for name, url, cat, n_total, n_rules in per_source:
        header.append(f"!   [{cat}] {name} ({n_rules} 条): {url}")
    header.append(f"! 合并去重后唯一规则总数: {total_rules}")
    header.append("!")
    out_ag = os.path.join(OUT, "adguard_cn_rules.txt")
    with open(out_ag, "w", encoding="utf-8") as f:
        f.write("\n".join(header) + "\n")
        f.write("\n".join(rules) + "\n")
    print(f"[写出] 国内 AdGuard 规则: {out_ag} ({total_rules} 条)")

    # ---------- 2) DNS 域名清单 ----------
    domain_set = set()
    dns_full_set = set()
    re_dns_hosts = re.compile(r"^\s*(?:0\.0\.0\.0|127\.0\.0\.1|::1|::|255\.255\.255\.255)\s+([^\s#]+)\s*$")
    for r in rules:
        m = re_dns_hosts.match(r)
        if m:
            d = clean(m.group(1))
            if d and VALID_DOMAIN.match(d) and d not in SKIP:
                domain_set.add(d); dns_full_set.add(r)
            continue
        m = ADP_DOMAIN.match(r)
        if m:
            d = clean(m.group(1))
            if d and VALID_DOMAIN.match(d) and d not in SKIP:
                domain_set.add(d); dns_full_set.add(r)
            continue
        if VALID_DOMAIN.match(r.lower()):
            domain_set.add(r.lower()); dns_full_set.add(r)

    domains = sorted(domain_set)
    total_domains = len(domains)
    print(f"国内 DNS 唯一域名数: {total_domains}")

    # 纯域名
    out_plain = os.path.join(OUT, "dns_cn_blocklist.txt")
    with open(out_plain, "w", encoding="utf-8") as f:
        f.write("# Title: Doubao 国内网络 DNS 拦截清单（纯域名）\n")
        f.write("# 说明: 一行一个域名，兼容 AdGuard Home / Pi-hole / AdGuard DNS / dnsmasq\n")
        f.write(f"# 唯一域名数: {total_domains}\n#\n")
        f.write("\n".join(domains) + "\n")
    print(f"[写出] {out_plain}")

    # hosts 格式
    out_hosts = os.path.join(OUT, "dns_cn_blocklist_hosts.txt")
    with open(out_hosts, "w", encoding="utf-8") as f:
        f.write("# Title: Doubao 国内网络 DNS 拦截清单（hosts 格式）\n")
        f.write(f"# 唯一域名数: {total_domains}\n# 兼容 hosts / AdGuard Home hosts / Pi-hole\n#\n")
        for d in domains:
            f.write(f"0.0.0.0 {d}\n")
    print(f"[写出] {out_hosts}")

    # AdGuard DNS 格式
    out_ag_dns = os.path.join(OUT, "dns_cn_blocklist_adguard.txt")
    with open(out_ag_dns, "w", encoding="utf-8") as f:
        f.write("[Adblock Plus 2.0]\n")
        f.write("! Title: Doubao 国内网络 DNS 拦截清单（AdGuard 格式）\n")
        f.write(f"! 唯一域名数: {total_domains}\n")
        f.write("! 适用于 AdGuard / AdGuard Home DNS 过滤订阅\n!\n")
        for d in domains:
            f.write(f"||{d}^\n")
    print(f"[写出] {out_ag_dns}")

    # ---------- 3) 国内规则 Markdown 说明 ----------
    lines = []
    lines.append("# 国内网络专用拦截规则（Doubao）")
    lines.append("")
    lines.append("专为**国内网络环境**整理的轻量拦截规则，聚焦国内站点广告与跟踪拦截，合并去重，不含国际全量列表。")
    lines.append("")
    lines.append("生成日期：2026-11-03 ｜ 唯一规则：**%d** 条 ｜ 唯一域名：**%d** 个" % (total_rules, total_domains))
    lines.append("")
    lines.append("## 来源清单")
    lines.append("")
    lines.append("| 类别 | 规则列表 | 原始规则数 | 订阅地址 |")
    lines.append("|---|---|---:|---|")
    for name, url, cat, n_total, n_rules in per_source:
        lines.append(f"| {cat} | {name} | {n_rules} | {url} |")
    lines.append("")
    lines.append("## 生成文件")
    lines.append("")
    lines.append("- **adguard_cn_rules.txt**：国内 AdGuard 全格式规则（含域名/URL/元素隐藏），AdGuard / uBlock Origin / Adblock Plus 通用。")
    lines.append("- **dns_cn_blocklist.txt**：纯域名清单，一行一个，Pi-hole / AdGuard Home / dnsmasq / AdGuard DNS。")
    lines.append("- **dns_cn_blocklist_hosts.txt**：hosts 格式（0.0.0.0 domain）。")
    lines.append("- **dns_cn_blocklist_adguard.txt**：AdGuard DNS 订阅格式（||domain^）。")
    lines.append("")
    lines.append("## 说明")
    lines.append("")
    lines.append("- 定位为国内轻量方案：只含中文/国内针对性来源，规避国际全量列表对国内正常服务（统计、CDN、App 组件）的误伤。")
    lines.append("- 若同时需要国际站点拦截，建议叠加国际通用列表（如 EasyList）或使用仓库内全量合并规则 adguard_rules_merged.txt。")
    lines.append("- AdRules（hacamer）因当前仓库路径不可达（raw 404 / API 限流 / 主页 robots 拦截）本轮未纳入，可在 AdGuard 中手动订阅补充。")
    lines.append("")
    out_md = os.path.join(OUT, "README_CN.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[写出] 说明文档: {out_md}")

if __name__ == "__main__":
    main()

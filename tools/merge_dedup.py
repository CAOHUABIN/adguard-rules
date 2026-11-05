#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AdGuard 规则合并去重工具：把多个来源的拦截规则合并、去重，输出通用规则文件与 DNS 域名规则文件。"""
import os, re, sys

RAW = "/home/user/Doubao/chats/38450599647723266/adguard_rules/raw"
OUT = "/home/user/Doubao/chats/38450599647723266/adguard_rules/output"

# 来源：(文件名, 名称, 订阅URL, 类别)
SOURCES = [
    ("adguard_base.txt",        "AdGuard Base filter（基础广告过滤）",        "https://filters.adtidy.org/extension/ublock/filters/2.txt",   "广告"),
    ("adguard_tracking.txt",    "AdGuard Tracking Protection（跟踪防护）",     "https://filters.adtidy.org/extension/ublock/filters/3.txt",   "隐私"),
    ("adguard_social.txt",      "AdGuard Social Media（社交媒体）",            "https://filters.adtidy.org/extension/ublock/filters/4.txt",   "社交"),
    ("adguard_mobile.txt",      "AdGuard Mobile Ads（移动端广告）",           "https://filters.adtidy.org/extension/ublock/filters/11.txt",  "广告"),
    ("adguard_annoyances.txt",  "AdGuard Annoyances（干扰元素）",             "https://filters.adtidy.org/extension/ublock/filters/14.txt",  "干扰"),
    ("adguard_dns.txt",         "AdGuard DNS filter（DNS广告过滤）",          "https://filters.adtidy.org/extension/ublock/filters/15.txt",  "广告"),
    ("adguard_url_tracking.txt","AdGuard URL Tracking（URL跟踪参数清除）",    "https://filters.adtidy.org/extension/ublock/filters/17.txt",  "隐私"),
    ("adguard_chinese.txt",     "AdGuard Chinese filter（中文过滤）",          "https://filters.adtidy.org/extension/ublock/filters/224.txt", "中文"),
    ("easylist.txt",            "EasyList（国际广告）",                       "https://easylist-downloads.adblockplus.org/easylist.txt",      "广告"),
    ("easyprivacy.txt",         "EasyPrivacy（国际隐私/跟踪）",               "https://easylist-downloads.adblockplus.org/easyprivacy.txt",  "隐私"),
    ("easylistchina.txt",       "EasyList China（中文广告）",                 "https://raw.githubusercontent.com/easylist/easylistchina/master/easylistchina.txt", "中文"),
    ("cjx_rule.txt",            "乘风广告过滤规则（CJX）",                    "https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt", "中文"),
    ("official_adguard_dns_ios.txt", "AdGuard DNS filter（iOS 专用版）",       "https://filters.adtidy.org/dns/filter_1_ios.txt",            "广告"),
    ("heidai_dns.txt",          "217heidai AdBlock DNS（合并去重 DNS）",       "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt", "广告"),
    ("heidai_dns_lite.txt",     "217heidai AdBlock DNS Lite（国内 DNS）",      "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdnslite.txt", "中文"),
    ("heidai_filters.txt",      "217heidai AdBlock Filter（全格式合并）",      "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockfilters.txt", "广告"),
    ("heidai_filters_lite.txt", "217heidai AdBlock Filter Lite（国内全格式）", "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockfilterslite.txt", "中文"),
]

def is_comment(line):
    s = line.strip()
    return (not s) or s.startswith("!") or s.startswith("[Adblock Plus") or s.startswith("[Adblock+")

def main():
    rule_set = set()
    per_source = {}
    for fname, name, url, cat in SOURCES:
        path = os.path.join(RAW, fname)
        n_total = 0
        n_rules = 0
        if not os.path.exists(path):
            print(f"[跳过] 文件缺失: {fname}")
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for raw_line in f:
                line = raw_line.rstrip("\n").rstrip("\r")
                n_total += 1
                if is_comment(line):
                    continue
                # 去掉行内空白
                line = line.strip()
                if not line:
                    continue
                n_rules += 1
                rule_set.add(line)
        per_source[fname] = (name, url, cat, n_total, n_rules)
        print(f"[载入] {name}: 总行={n_total} 规则行={n_rules}")

    rules = sorted(rule_set)
    print(f"\n合并去重后唯一规则数: {len(rules)}")

    # ---------- 通用 AdGuard 规则文件（全格式） ----------
    header = []
    header.append("[Adblock Plus 2.0]")
    header.append("! Title: AdGuard 全格式拦截规则（合并去重）")
    header.append("! Version: 2026-10-31")
    header.append("! 说明: 由以下来源合并并精确去重生成，适用于 AdGuard / AdGuard Home / uBlock Origin / Adblock Plus 等")
    header.append("! ----------------------------------------------------------------------")
    header.append("! 来源清单（合并前原始规则数）：")
    for fname, (name, url, cat, n_total, n_rules) in per_source.items():
        header.append(f"!   [{cat}] {name} ({n_rules} 条): {url}")
    header.append(f"! ----------------------------------------------------------------------")
    header.append(f"! 合并去重后唯一规则总数: {len(rules)}")
    header.append("!")

    out_full = os.path.join(OUT, "adguard_rules_merged.txt")
    with open(out_full, "w", encoding="utf-8") as f:
        f.write("\n".join(header) + "\n")
        f.write("\n".join(rules) + "\n")
    print(f"[写出] 通用规则文件: {out_full} ({len(rules)} 条)")

    # ---------- DNS 域名规则文件（AdGuard Home / DNS 过滤） ----------
    # 仅保留 DNS 域名形式规则：||domain^  或 hosts 形式(0.0.0.0 domain / 127.0.0.1 domain / 裸域名)
    domain_set = set()
    dns_full_set = set()
    re_dns_hosts = re.compile(r"^\s*(?:0\.0\.0\.0|127\.0\.0\.1|::1|::|0\.0\.0\.0|255\.255\.255\.255)\s+([^\s#]+)\s*$")
    re_abp_domain = re.compile(r"^\|\|([a-z0-9][a-z0-9\-.]*\.[a-z]{2,63})\^.*$")
    for r in rules:
        m = re_dns_hosts.match(r)
        if m:
            d = m.group(1).lower()
            domain_set.add(d)
            dns_full_set.add(r)
            continue
        m = re_abp_domain.match(r)
        if m:
            domain_set.add(m.group(1).lower())
            dns_full_set.add(r)
            continue
    # 纯裸域名行
    re_plain = re.compile(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?)+$")
    for r in rules:
        if re_plain.match(r.lower()):
            domain_set.add(r.lower())
            dns_full_set.add(r)

    out_dns = os.path.join(OUT, "adguard_dns_only.txt")
    with open(out_dns, "w", encoding="utf-8") as f:
        f.write("# Title: DNS 域名规则（从全格式规则提取）\n")
        f.write("# 说明: 仅含域名级规则，适用于 AdGuard Home / AdGuard DNS 过滤模式\n")
        f.write(f"# 唯一域名数: {len(domain_set)}\n")
        f.write("# 来源: 同 adguard_rules_merged.txt 的 12 个列表合并去重\n")
        f.write("#\n")
        f.write("\n".join(sorted(dns_full_set)) + "\n")
    print(f"[写出] DNS域名规则文件: {out_dns} (域名规则 {len(dns_full_set)} 条 / 唯一域名 {len(domain_set)})")

    # ---------- 汇总报告（Markdown） ----------
    lines = []
    lines.append("# AdGuard 拦截规则合并去重汇总")
    lines.append("")
    lines.append("生成日期：2026-10-31 ｜ 合并去重后唯一规则数：**%d** 条 ｜ 唯一域名：%d 个" % (len(rules), len(domain_set)))
    lines.append("")
    lines.append("## 一、合并来源清单")
    lines.append("")
    lines.append("| 类别 | 规则列表 | 原始规则数 | 订阅地址 |")
    lines.append("|---|---|---:|---|")
    for fname, (name, url, cat, n_total, n_rules) in per_source.items():
        lines.append(f"| {cat} | {name} | {n_rules} | {url} |")
    lines.append("")
    lines.append("## 二、生成的文件")
    lines.append("")
    lines.append("- **adguard_rules_merged.txt**：全格式规则（含域名、URL、元素隐藏、脚本等），可用于 AdGuard 桌面端/App、uBlock Origin、Adblock Plus。")
    lines.append("- **adguard_dns_only.txt**：域名级规则，适用于 AdGuard Home / AdGuard DNS 过滤模式。")
    lines.append("")
    lines.append("## 三、注意事项")
    lines.append("")
    lines.append("- 本合并文件为静态快照，各来源会持续更新。建议优先直接订阅上表各列表（自动更新），或定期重新生成本合并文件。")
    lines.append("- 规则过多（数十万条）可能影响低配置设备性能；AdGuard Home / 路由器场景建议用 DNS 域名版本。")
    lines.append("- EasyList 官方源 easylist.to 在本环境访问受限，已改用 Adblock Plus 官方镜像 easylist-downloads.adblockplus.org，内容一致。")
    lines.append("- 未纳入：AdRules（hacamer）、CJX Annoyance 列表 等因仓库路径变动未能自动获取，可在 AdGuard 中手动订阅补充。")
    lines.append("")
    out_md = os.path.join(OUT, "README.md")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[写出] 汇总报告: {out_md}")

if __name__ == "__main__":
    main()

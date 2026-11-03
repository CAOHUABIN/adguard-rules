#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从生成的规则文件头部读取统计信息，重新生成完整 README（覆盖写入，避免重复追加）。"""
import os, re

OUT = "/home/user/Doubao/chats/38450599647723266/adguard_rules/output"

def header_kv(path, key):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("!") or line.startswith("#"):
                    if key in line:
                        m = re.search(r":\s*([\d,]+)", line)
                        if m:
                            return m.group(1)
    except Exception:
        pass
    return "?"

def main():
    # 读取合并规则文件的来源清单与总数
    sources = []
    total_rules = "?"
    with open(os.path.join(OUT, "adguard_rules_merged.txt"), "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("! 合并去重后唯一规则总数"):
                m = re.search(r":\s*([\d]+)", line)
                if m:
                    total_rules = m.group(1)
            m = re.match(r"!\s+\[([^\]]+)\]\s+(.+?)\s+\((\d+)\s+条\):\s*(\S+)", line.strip())
            if m:
                sources.append((m.group(1), m.group(2), m.group(3), m.group(4)))

    # 读取 DNS 域名数
    dns_count = "?"
    with open(os.path.join(OUT, "dns_blocklist.txt"), "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("# 唯一域名数"):
                m = re.search(r":\s*([\d]+)", line)
                if m:
                    dns_count = m.group(1)

    # 读取国内网络专用规则统计（若存在）
    cn_rules = cn_dns = None
    cn_path_rules = os.path.join(OUT, "adguard_cn_rules.txt")
    cn_path_dns = os.path.join(OUT, "dns_cn_blocklist.txt")
    if os.path.exists(cn_path_rules):
        for line in open(cn_path_rules, encoding="utf-8"):
            if line.startswith("! 合并去重后唯一规则总数"):
                m = re.search(r":\s*([\d]+)", line)
                if m:
                    cn_rules = m.group(1)
                    break
    if os.path.exists(cn_path_dns):
        for line in open(cn_path_dns, encoding="utf-8"):
            if line.startswith("# 唯一域名数"):
                m = re.search(r":\s*([\d]+)", line)
                if m:
                    cn_dns = m.group(1)
                    break

    L = []
    L.append("# Doubao AdGuard 拦截规则合集（自动更新）")
    L.append("")
    L.append("多源合并去重生成的 AdGuard 拦截规则与 DNS 拦截清单，每日自动重新拉取来源、合并去重并推送更新。")
    L.append("")
    L.append(f"- 全格式广告过滤规则：**{total_rules}** 条（adguard_rules_merged.txt）")
    L.append(f"- DNS 拦截域名：**{dns_count}** 个（dns_blocklist*.txt）")
    if cn_rules is not None:
        L.append(f"- 国内网络专用规则：**{cn_rules}** 条 / **{cn_dns}** 个域名（adguard_cn_rules.txt 等）")
    L.append("")
    L.append("## 订阅地址（AdGuard / AdGuard Home 直接添加）")
    L.append("")
    L.append("| 用途 | 订阅地址 |")
    L.append("|---|---|")
    L.append("| DNS 拦截（AdGuard `||域名^` 格式，推荐） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/dns_blocklist_adguard.txt |")
    L.append("| DNS 拦截（一行一个域名，最通用） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/dns_blocklist.txt |")
    L.append("| DNS 拦截（hosts 格式） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/dns_blocklist_hosts.txt |")
    L.append("| 全格式广告过滤规则 | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/adguard_rules_merged.txt |")
    L.append("| Safari 精简拦截规则（主机名版，约 4.9 万条） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/safari_rules.txt |")
    L.append("| 以上任一链接的 CDN 加速版（把 raw.githubusercontent.com 换成 cdn.jsdelivr.net/gh） | 见下方 |")
    L.append("")
    L.append("CDN 加速版示例：`https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_blocklist_adguard.txt`")
    L.append("")
    L.append("## 国内网络专用规则（轻量，聚焦国内站点）")
    L.append("")
    L.append("由 AdGuard Chinese filter + EasyList China + 乘风(CJX) + anti-AD 合并去重生成，专为国内网络环境整理，不含国际全量列表，体积更小、误伤更低。")
    L.append("")
    L.append("| 用途 | 订阅地址 |")
    L.append("|---|---|")
    L.append("| 国内 DNS 拦截（AdGuard `||域名^` 格式） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/dns_cn_blocklist_adguard.txt |")
    L.append("| 国内 DNS 拦截（一行一个域名） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/dns_cn_blocklist.txt |")
    L.append("| 国内 DNS 拦截（hosts 格式） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/dns_cn_blocklist_hosts.txt |")
    L.append("| 国内全格式广告过滤规则 | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/adguard_cn_rules.txt |")
    L.append("")
    L.append("> 需要同时拦截国际站点广告时，建议叠加全量规则或国际通用列表。")
    L.append("")
    L.append("## 合并来源")
    L.append("")
    L.append("| 类别 | 规则列表 | 规则数 | 订阅地址 |")
    L.append("|---|---|---:|---|")
    for cat, name, cnt, url in sources:
        L.append(f"| {cat} | {name} | {cnt} | {url} |")
    L.append("")
    L.append("## 说明")
    L.append("")
    L.append("- 本仓库每日自动更新（重新拉取各来源 → 合并去重 → 推送）。")
    L.append("- 全格式文件较大（数十万条），低配置设备建议用 DNS 域名版。")
    L.append("- 生成脚本见 tools/ 目录，可自行复现。")
    L.append("")
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"[写出] README.md（规则 {total_rules}，DNS {dns_count}，来源 {len(sources)}）")

if __name__ == "__main__":
    main()

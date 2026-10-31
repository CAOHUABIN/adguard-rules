#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DNS 过滤规则整合：从多个 DNS 拦截源提取域名，统一规范化、去重，输出多种格式。"""
import os, re

RAW = "/home/user/Doubao/chats/38450599647723266/adguard_rules/raw"
OUT = "/home/user/Doubao/chats/38450599647723266/adguard_rules/output"

# DNS 拦截来源：(文件, 名称, 官方地址)
DNS_SOURCES = [
    ("adguard_dns_only.txt",    "AdGuard 12列表提取的DNS域名（含 AdGuard DNS filter）", "见 adguard_rules_merged.txt"),
    ("dns_stevenblack.txt",     "StevenBlack hosts（广告+恶意软件）",              "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"),
    ("dns_hagezi_pro.txt",      "HaGeZi Multi PRO（广告/跟踪/钓鱼/恶意）",         "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt"),
    ("dns_antiad.txt",          "anti-AD（中文广告+跟踪）",                        "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt"),
    ("dns_1hosts_lite.txt",     "1Hosts Lite（广告/跟踪/诈骗）",                   "https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/hosts.txt"),
]

# 跳过这些保留名/IP
SKIP = {"localhost", "localhost.localdomain", "local", "broadcasthost", "ip6-localhost",
        "ip6-loopback", "ip6-localnet", "ip6-mcastprefix", "ip6-allnodes", "ip6-allrouters",
        "ip6-allhosts", "0.0.0.0", "127.0.0.1", "255.255.255.255", "::", "::1", "fe80::1", "ff02::1"}

VALID_DOMAIN = re.compile(r"^[a-z0-9]([a-z0-9\-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]*[a-z0-9])?){1,}$")
HOSTS_IP = re.compile(r"^(?:0\.0\.0\.0|127\.0\.0\.1|::1?|::|255\.255\.255\.255|0\.0\.0\.1)\s+([^\s#]+)")
ADP_DOMAIN = re.compile(r"^\|\|([a-z0-9][a-z0-9\-]*(\.[a-z0-9][a-z0-9\-]*)+)\^?(?:\$.*)?$")

def clean(dom):
    d = dom.strip().strip(".").lower()
    if ":" in d:  # 去端口
        d = d.split(":")[0].strip(".")
    return d

def extract_from_hosts(path, domain_set):
    """hosts 格式：IP 域名"""
    n = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = HOSTS_IP.match(line)
            if not m:
                continue
            d = clean(m.group(1))
            if d and VALID_DOMAIN.match(d) and d not in SKIP and not re.match(r"^\d+\.\d+\.\d+\.\d+$", d):
                domain_set.add(d); n += 1
    return n

def extract_from_adblock(path, domain_set):
    """adblock 格式：||domain^  或裸域名"""
    n = 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("!") or line.startswith("#") or line.startswith("[Adblock"):
                continue
            if line.startswith("@@") or "##" in line or "#@#" in line or "#$#" in line or line.startswith("||") is False and line.startswith("|") and not line.startswith("||"):
                continue
            # 跳过非域名规则
            if line.startswith("||"):
                m = ADP_DOMAIN.match(line)
                if not m:
                    continue
                d = clean(m.group(1))
            elif VALID_DOMAIN.match(line):
                d = clean(line)
            else:
                continue
            if d not in SKIP:
                domain_set.add(d); n += 1
    return n

def main():
    all_domains = set()
    per_source = []
    for fname, name, url in DNS_SOURCES:
        path = os.path.join(RAW, fname) if fname != "adguard_dns_only.txt" else os.path.join(OUT, fname)
        if not os.path.exists(path):
            print(f"[跳过] 缺失: {fname}")
            continue
        before = len(all_domains)
        if fname in ("dns_stevenblack.txt", "dns_1hosts_lite.txt", "adguard_dns_only.txt"):
            n = extract_from_hosts(path, all_domains)
            # adguard_dns_only 可能含 adblock 行，也走 adblock 提取补充
            if fname == "adguard_dns_only.txt":
                extract_from_adblock(path, all_domains)
        else:
            n = extract_from_adblock(path, all_domains)
        added = len(all_domains) - before
        print(f"[载入] {name}: 提取域名 {added} 个（去重后累计 {len(all_domains)}）")
        per_source.append((name, url, added))

    domains = sorted(all_domains)
    total = len(domains)
    print(f"\nDNS 整合后唯一域名总数: {total}")

    # 1) 纯域名列表（一行一个，通用）
    out_plain = os.path.join(OUT, "dns_blocklist.txt")
    with open(out_plain, "w", encoding="utf-8") as f:
        f.write("# Title: Doubao DNS 拦截清单（合并去重）\n")
        f.write("# 说明: 一行一个域名，兼容 AdGuard Home 自定义过滤、Pi-hole、AdGuard DNS、dnsmasq 等\n")
        f.write(f"# 唯一域名数: {total}\n")
        f.write("# 来源:\n")
        for name, url, added in per_source:
            f.write(f"#   - {name}（新增 {added}）: {url}\n")
        f.write("#\n")
        f.write("\n".join(domains) + "\n")
    print(f"[写出] {out_plain}")

    # 2) hosts 格式（0.0.0.0 domain）
    out_hosts = os.path.join(OUT, "dns_blocklist_hosts.txt")
    with open(out_hosts, "w", encoding="utf-8") as f:
        f.write("# Title: Doubao DNS 拦截清单（hosts 格式）\n")
        f.write(f"# 唯一域名数: {total}\n")
        f.write("# 兼容 hosts 文件 / AdGuard Home hosts / Pi-hole（导入格式 hosts）\n#\n")
        for d in domains:
            f.write(f"0.0.0.0 {d}\n")
    print(f"[写出] {out_hosts}")

    # 3) AdGuard 原生格式（||domain^）
    out_ag = os.path.join(OUT, "dns_blocklist_adguard.txt")
    with open(out_ag, "w", encoding="utf-8") as f:
        f.write("[Adblock Plus 2.0]\n")
        f.write("! Title: Doubao DNS 拦截清单（AdGuard 格式）\n")
        f.write(f"! 唯一域名数: {total}\n")
        f.write("! 适用于 AdGuard / AdGuard Home DNS 过滤订阅\n!\n")
        for d in domains:
            f.write(f"||{d}^\n")
    print(f"[写出] {out_ag}")

    # 4) 更新 README 中的 DNS 章节
    md = os.path.join(OUT, "README.md")
    with open(md, "a", encoding="utf-8") as f:
        f.write("\n## 四、DNS 过滤规则整合\n")
        f.write("\n整合后的 DNS 拦截清单（唯一域名 **%d** 个）：\n" % total)
        f.write("\n| 来源 | 新增域名 | 官方地址 |\n|---|---:|---|\n")
        for name, url, added in per_source:
            f.write(f"| {name} | {added} | {url} |\n")
        f.write("\n生成文件：\n")
        f.write("- **dns_blocklist.txt**：一行一个域名（最通用，AdGuard Home 自定义过滤 / Pi-hole / AdGuard DNS 通用）。\n")
        f.write("- **dns_blocklist_hosts.txt**：hosts 格式（0.0.0.0 域名），用于 hosts 文件替换或 AdGuard Home hosts 导入。\n")
        f.write("- **dns_blocklist_adguard.txt**：AdGuard 原生 `||domain^` 格式，可直接作为 DNS 过滤订阅。\n")
    print("[写出] README.md 更新")

if __name__ == "__main__":
    main()

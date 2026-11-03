# 国内网络专用拦截规则（Doubao）

专为**国内网络环境**整理的轻量拦截规则，聚焦国内站点广告与跟踪拦截，合并去重，不含国际全量列表。

生成日期：2026-11-03 ｜ 唯一规则：**111860** 条 ｜ 唯一域名：**95865** 个

## 来源清单

| 类别 | 规则列表 | 原始规则数 | 订阅地址 |
|---|---|---:|---|
| 中文/官方 | AdGuard Chinese filter（官方中文过滤） | 20078 | https://filters.adtidy.org/extension/ublock/filters/224.txt |
| 中文 | EasyList China（EasyList 国内补充） | 17022 | https://raw.githubusercontent.com/easylist/easylistchina/master/easylistchina.txt |
| 中文 | 乘风广告过滤规则（CJX） | 1168 | https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt |
| 中文/DNS | anti-AD（中文广告+跟踪） | 95638 | https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt |

## 生成文件

- **adguard_cn_rules.txt**：国内 AdGuard 全格式规则（含域名/URL/元素隐藏），AdGuard / uBlock Origin / Adblock Plus 通用。
- **dns_cn_blocklist.txt**：纯域名清单，一行一个，Pi-hole / AdGuard Home / dnsmasq / AdGuard DNS。
- **dns_cn_blocklist_hosts.txt**：hosts 格式（0.0.0.0 domain）。
- **dns_cn_blocklist_adguard.txt**：AdGuard DNS 订阅格式（||domain^）。

## 订阅地址（jsDelivr CDN，国内可直接访问）

| 用途 | 订阅地址 |
|---|---|
| 国内 DNS 拦截（AdGuard `||域名^` 格式，推荐） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_cn_blocklist_adguard.txt |
| 国内 DNS 拦截（一行一个域名） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_cn_blocklist.txt |
| 国内 DNS 拦截（hosts 格式） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_cn_blocklist_hosts.txt |
| 国内全格式广告过滤规则 | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/adguard_cn_rules.txt |

> 海外/备用（GitHub raw）：`https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/<文件名>`

## 说明

- 定位为国内轻量方案：只含中文/国内针对性来源，规避国际全量列表对国内正常服务（统计、CDN、App 组件）的误伤。
- 若同时需要国际站点拦截，建议叠加国际通用列表（如 EasyList）或使用仓库内全量合并规则 adguard_rules_merged.txt。
- AdRules（hacamer）因当前仓库路径不可达（raw 404 / API 限流 / 主页 robots 拦截）本轮未纳入，可在 AdGuard 中手动订阅补充。


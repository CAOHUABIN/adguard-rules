# Doubao AdGuard 拦截规则合集（自动更新）

多源合并去重生成的 AdGuard 拦截规则与 DNS 拦截清单，每日自动重新拉取来源、合并去重并推送更新。

- 全格式广告过滤规则：**670508** 条（adguard_rules_merged.txt）
- DNS 拦截域名：**547291** 个（dns_blocklist*.txt）

## 订阅地址（AdGuard / AdGuard Home 直接添加）

| 用途 | 订阅地址 |
|---|---|
| DNS 拦截（AdGuard `||域名^` 格式，推荐） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/dns_blocklist_adguard.txt |
| DNS 拦截（一行一个域名，最通用） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/dns_blocklist.txt |
| DNS 拦截（hosts 格式） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/dns_blocklist_hosts.txt |
| 全格式广告过滤规则 | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/adguard_rules_merged.txt |
| Safari 精简拦截规则（主机名版，约 4.9 万条） | https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/safari_rules.txt |
| 以上任一链接的 CDN 加速版（把 raw.githubusercontent.com 换成 cdn.jsdelivr.net/gh） | 见下方 |

CDN 加速版示例：`https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_blocklist_adguard.txt`

## 合并来源

| 类别 | 规则列表 | 规则数 | 订阅地址 |
|---|---|---:|---|
| 广告 | AdGuard Base filter（基础广告过滤） | 131461 | https://filters.adtidy.org/extension/ublock/filters/2.txt |
| 隐私 | AdGuard Tracking Protection（跟踪防护） | 386044 | https://filters.adtidy.org/extension/ublock/filters/3.txt |
| 社交 | AdGuard Social Media（社交媒体） | 16490 | https://filters.adtidy.org/extension/ublock/filters/4.txt |
| 广告 | AdGuard Mobile Ads（移动端广告） | 7969 | https://filters.adtidy.org/extension/ublock/filters/11.txt |
| 干扰 | AdGuard Annoyances（干扰元素） | 59699 | https://filters.adtidy.org/extension/ublock/filters/14.txt |
| 广告 | AdGuard DNS filter（DNS广告过滤） | 186422 | https://filters.adtidy.org/extension/ublock/filters/15.txt |
| 隐私 | AdGuard URL Tracking（URL跟踪参数清除） | 2724 | https://filters.adtidy.org/extension/ublock/filters/17.txt |
| 中文 | AdGuard Chinese filter（中文过滤） | 20850 | https://filters.adtidy.org/extension/ublock/filters/224.txt |
| 广告 | EasyList（国际广告） | 76840 | https://easylist-downloads.adblockplus.org/easylist.txt |
| 隐私 | EasyPrivacy（国际隐私/跟踪） | 53676 | https://easylist-downloads.adblockplus.org/easyprivacy.txt |
| 中文 | EasyList China（中文广告） | 17780 | https://raw.githubusercontent.com/easylist/easylistchina/master/easylistchina.txt |
| 中文 | 乘风广告过滤规则（CJX） | 1169 | https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt |

## 说明

- 本仓库每日自动更新（重新拉取各来源 → 合并去重 → 推送）。
- 全格式文件较大（数十万条），低配置设备建议用 DNS 域名版。
- 生成脚本见 tools/ 目录，可自行复现。


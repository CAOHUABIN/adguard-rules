# Doubao AdGuard 拦截规则合集（自动更新）

多源合并去重生成的 AdGuard 拦截规则与 DNS 拦截清单，每日自动重新拉取来源、合并去重并推送更新。

- 全格式广告过滤规则：**692085** 条（adguard_rules_merged.txt）
- DNS 拦截域名：**577262** 个（dns_blocklist*.txt）
- 国内网络专用规则：**111860** 条 / **95865** 个域名（adguard_cn_rules.txt 等）

## 订阅地址（AdGuard / AdGuard Home 直接添加）

> 以下均为 **jsDelivr CDN 加速地址，国内可直接访问**（GitHub raw 在国内常无法访问，仅作海外备用）。

| 用途 | 订阅地址 |
|---|---|
| DNS 拦截（AdGuard `||域名^` 格式，推荐） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_blocklist_adguard.txt |
| DNS 拦截（一行一个域名，最通用） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_blocklist.txt |
| DNS 拦截（hosts 格式） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_blocklist_hosts.txt |
| Safari 精简拦截规则（主机名版，约 4.9 万条） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/safari_rules.txt |

> **注意**：全格式广告过滤规则 `adguard_rules_merged.txt`（约 25MB）超过 jsDelivr 单文件 20MB 上限，**国内 CDN 不可用**。国内用户请用上方 DNS 域名版；确需全格式时海外走 GitHub raw：`https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/adguard_rules_merged.txt`。

海外/备用（GitHub raw）：`https://raw.githubusercontent.com/CAOHUABIN/doubao-adguard-rules/main/<文件名>`

## 国内网络专用规则（轻量，聚焦国内站点）

由 AdGuard Chinese filter + EasyList China + 乘风(CJX) + anti-AD 合并去重生成，专为国内网络环境整理，不含国际全量列表，体积更小、误伤更低。

| 用途 | 订阅地址 |
|---|---|
| 国内 DNS 拦截（AdGuard `||域名^` 格式） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_cn_blocklist_adguard.txt |
| 国内 DNS 拦截（一行一个域名） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_cn_blocklist.txt |
| 国内 DNS 拦截（hosts 格式） | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_cn_blocklist_hosts.txt |
| 国内全格式广告过滤规则 | https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/adguard_cn_rules.txt |

> 需要同时拦截国际站点广告时，建议叠加全量规则或国际通用列表。

## 合并来源

| 类别 | 规则列表 | 规则数 | 订阅地址 |
|---|---|---:|---|
| 广告 | AdGuard Base filter（基础广告过滤） | 132269 | https://filters.adtidy.org/extension/ublock/filters/2.txt |
| 隐私 | AdGuard Tracking Protection（跟踪防护） | 406659 | https://filters.adtidy.org/extension/ublock/filters/3.txt |
| 社交 | AdGuard Social Media（社交媒体） | 16514 | https://filters.adtidy.org/extension/ublock/filters/4.txt |
| 广告 | AdGuard Mobile Ads（移动端广告） | 7975 | https://filters.adtidy.org/extension/ublock/filters/11.txt |
| 干扰 | AdGuard Annoyances（干扰元素） | 59758 | https://filters.adtidy.org/extension/ublock/filters/14.txt |
| 广告 | AdGuard DNS filter（DNS广告过滤） | 188228 | https://filters.adtidy.org/extension/ublock/filters/15.txt |
| 隐私 | AdGuard URL Tracking（URL跟踪参数清除） | 2736 | https://filters.adtidy.org/extension/ublock/filters/17.txt |
| 中文 | AdGuard Chinese filter（中文过滤） | 20873 | https://filters.adtidy.org/extension/ublock/filters/224.txt |
| 广告 | EasyList（国际广告） | 77391 | https://easylist-downloads.adblockplus.org/easylist.txt |
| 隐私 | EasyPrivacy（国际隐私/跟踪） | 53678 | https://easylist-downloads.adblockplus.org/easyprivacy.txt |
| 中文 | EasyList China（中文广告） | 17800 | https://raw.githubusercontent.com/easylist/easylistchina/master/easylistchina.txt |
| 中文 | 乘风广告过滤规则（CJX） | 1169 | https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt |

## 说明

- 本仓库每日自动更新（重新拉取各来源 → 合并去重 → 推送）。
- 全格式文件较大（数十万条），低配置设备建议用 DNS 域名版。
- 生成脚本见 tools/ 目录，可自行复现。


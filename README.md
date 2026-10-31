# AdGuard 拦截规则合并去重汇总

生成日期：2026-10-31 ｜ 合并去重后唯一规则数：**511666** 条 ｜ 唯一域名：210333 个

> **去重效果**：12 个来源合并前原始规则共 **796,615** 条 → 精确去重后 **511,666** 条，共去除重复规则 **284,949** 条（约 35.8%），去重校验通过（重复行数为 0）。

## 一、合并来源清单

| 类别 | 规则列表 | 原始规则数 | 订阅地址 |
|---|---|---:|---|
| 广告 | AdGuard Base filter（基础广告过滤） | 131027 | https://filters.adtidy.org/extension/ublock/filters/2.txt |
| 隐私 | AdGuard Tracking Protection（跟踪防护） | 222865 | https://filters.adtidy.org/extension/ublock/filters/3.txt |
| 社交 | AdGuard Social Media（社交媒体） | 16490 | https://filters.adtidy.org/extension/ublock/filters/4.txt |
| 广告 | AdGuard Mobile Ads（移动端广告） | 7969 | https://filters.adtidy.org/extension/ublock/filters/11.txt |
| 干扰 | AdGuard Annoyances（干扰元素） | 59684 | https://filters.adtidy.org/extension/ublock/filters/14.txt |
| 广告 | AdGuard DNS filter（DNS广告过滤） | 185993 | https://filters.adtidy.org/extension/ublock/filters/15.txt |
| 隐私 | AdGuard URL Tracking（URL跟踪参数清除） | 2724 | https://filters.adtidy.org/extension/ublock/filters/17.txt |
| 中文 | AdGuard Chinese filter（中文过滤） | 20839 | https://filters.adtidy.org/extension/ublock/filters/224.txt |
| 广告 | EasyList（国际广告） | 76411 | https://easylist-downloads.adblockplus.org/easylist.txt |
| 隐私 | EasyPrivacy（国际隐私/跟踪） | 53675 | https://easylist-downloads.adblockplus.org/easyprivacy.txt |
| 中文 | EasyList China（中文广告） | 17769 | https://raw.githubusercontent.com/easylist/easylistchina/master/easylistchina.txt |
| 中文 | 乘风广告过滤规则（CJX） | 1169 | https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt |

## 二、生成的文件

- **adguard_rules_merged.txt**：全格式规则（含域名、URL、元素隐藏、脚本等），可用于 AdGuard 桌面端/App、uBlock Origin、Adblock Plus。
- **adguard_dns_only.txt**：域名级规则，适用于 AdGuard Home / AdGuard DNS 过滤模式。

## 三、注意事项

- 本合并文件为静态快照，各来源会持续更新。建议优先直接订阅上表各列表（自动更新），或定期重新生成本合并文件。
- 规则过多（数十万条）可能影响低配置设备性能；AdGuard Home / 路由器场景建议用 DNS 域名版本。
- EasyList 官方源 easylist.to 在本环境访问受限，已改用 Adblock Plus 官方镜像 easylist-downloads.adblockplus.org，内容一致。
- 未纳入：AdRules（hacamer）、CJX Annoyance 列表 等因仓库路径变动未能自动获取，可在 AdGuard 中手动订阅补充。


## 四、DNS 过滤规则整合

整合后的 DNS 拦截清单（唯一域名 **546201** 个）：

| 来源 | 新增域名 | 官方地址 |
|---|---:|---|
| AdGuard 12列表提取的DNS域名（含 AdGuard DNS filter） | 209951 | 见 adguard_rules_merged.txt |
| StevenBlack hosts（广告+恶意软件） | 71143 | https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts |
| HaGeZi Multi PRO（广告/跟踪/钓鱼/恶意） | 122795 | https://raw.githubusercontent.com/hagezi/dns-blocklists/main/adblock/pro.txt |
| anti-AD（中文广告+跟踪） | 9368 | https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-easylist.txt |
| 1Hosts Lite（广告/跟踪/诈骗） | 132944 | https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/hosts.txt |

生成文件：
- **dns_blocklist.txt**：一行一个域名（最通用，AdGuard Home 自定义过滤 / Pi-hole / AdGuard DNS 通用）。
- **dns_blocklist_hosts.txt**：hosts 格式（0.0.0.0 域名），用于 hosts 文件替换或 AdGuard Home hosts 导入。
- **dns_blocklist_adguard.txt**：AdGuard 原生 `||domain^` 格式，可直接作为 DNS 过滤订阅。

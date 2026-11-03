# 订阅规则速查（共 4 条）

全部为 **jsDelivr CDN 地址，国内可直接访问**；每日自动按上游更新，**地址保持不变**。

---

## 1. 最全 · 国内外 DNS 拦截（57.7 万域名）
```
https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_blocklist_adguard.txt
```

## 2. 最全 · 国内外 Safari 拦截（4.9 万条）
```
https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/safari_rules.txt
```

## 3. 最全 · 国内 DNS 拦截（9.6 万域名）
```
https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/dns_cn_blocklist_adguard.txt
```

## 4. 最全 · 国内 Safari 拦截（4.9 万条）
```
https://cdn.jsdelivr.net/gh/CAOHUABIN/doubao-adguard-rules@main/safari_cn_rules.txt
```

---

## 怎么用（AdGuard）

| 拦截层 | 拦什么 | 添加位置 | 用哪条 |
|---|---|---|---|
| **DNS 层** | 整个系统 / 所有 App 的广告域名 | AdGuard → 保护 → DNS 保护 → 过滤器 → 添加 | 1 或 3 |
| **Safari 层** | 浏览器内的网页广告 | AdGuard → 保护 → Safari 保护 → 过滤器 → 添加 | 2 或 4 |

- **国内+国外最全** → 用 1 / 2
- **仅国内、更贴合国内网络、误伤更低** → 用 3 / 4

> 说明：DNS 版拦的是"域名解析"这一层；Safari 版拦浏览器里内嵌的广告元素，两者互补。按需各取一条即可，无需重复添加。

# Where to find deals / 去哪找羊毛

Rule: aggregators and communities are only for **leads**; verification always goes back to the **official page**. Skip offers the user's region can't use. Restrict searches to the last few days (add the current month/year or use the search tool's time filter) — old news is everywhere.
原则：聚合站和社区只负责发现线索，**核对一定回到官方页面**。用户地区用不了的跳过。搜索限定最近几天，旧闻很多。

Search in the language of the source: Chinese communities with Chinese keywords, English ones with English keywords.
按来源的语言搜索：中文社区用中文关键词，英文社区用英文关键词。

## Ready-made verified source / 现成的已核对数据源

| Source 来源 | What 内容 | How 用法 |
|---|---|---|
| cc羊毛减 https://wool.eshop.us.ci | Deal posts from X (mostly Chinese), each re-checked against the original post; AI plans, free credits, crypto cards, US cards, banks, promos / X 上的羊毛帖，每条回原帖核对过 | Public RSS 公开 RSS: `python3 scripts/feeds.py https://wool.eshop.us.ci/rss.xml`; MCP at `/api/mcp` (free token on the site, no sign-up) gives category/keyword/deadline queries / 接 MCP 可按类别、关键词、截止时间查 |

## AI plans & free credits / AI 订阅与免费额度

- Official: pricing pages, official blogs/changelogs, official X accounts (OpenAI, Anthropic, Google AI, xAI, Mistral, Midjourney, Suno, Cursor, Perplexity…) / 官方定价页、博客、更新日志、官方 X
- Developer credits: cloud AI credits (Google AI Studio, AWS, Azure), startup programs / 云平台 AI 额度、创业计划
- Communities 社区: Reddit r/ChatGPT, r/ClaudeAI, r/LocalLLaMA, r/singularity; Hacker News; linux.do, V2EX
- Queries 搜索词: `"free credits" OR "free tier" <product>`, `<product> student discount`, `<产品> 免费 额度 限时`

## Crypto: airdrops, testnets, points, exchange promos / Crypto：空投、测试网、积分、交易所活动

- Official: exchange announcement/promo pages (Binance, OKX, Bybit, Bitget, Coinbase…), project blogs, official X, official Discord announcement channels / 交易所公告页、项目官方渠道
- Leads 线索: DeFiLlama airdrops page, project docs' points/rewards pages
- **Highest-risk category / 风险最高**: official domains only; wallet signatures, token approvals, "pay gas to claim" are risks; never import a seed phrase anywhere / 只认官方域名；签名、授权、"先付 gas 领空投"一律当风险；不要在任何页面导入助记词

## Crypto cards (U卡)

- Official: issuer site, fee page, promo page / 发卡方官网、费率页、活动页
- Leads 线索: X, linux.do, official Telegram channels
- Always state: issuance fee, monthly fee, top-up fee, KYC or not, supported regions / 写清开卡费、月费、充值费、是否实名、支持地区

## Banks & bank cards / 海外银行与银行卡

- US 美国: Doctor of Credit (doctorofcredit.com), r/churning, r/personalfinance, banks' promotions pages
- UK 英国: r/beermoney, r/UKPersonalFinance, bank sites
- HK / SG / MY 香港、新加坡、马来西亚: banks' promotions pages
- Always state: account requirements, deposit, holding period, early-closure fees, local address/tax ID needs / 写清开户条件、入金、持有期、提前销户罚则、是否需要当地地址或税号

## VPS & cloud / VPS 与云服务

- Official: free-tier pages (Oracle, AWS, GCP, Azure, Cloudflare), student and startup programs / 各云平台 free tier、学生和创业计划
- Communities 社区: LowEndTalk, LowEndBox, NodeSeek, hostloc
- Always state: forever-free vs trial, card required, overage billing / 写清永久免费还是试用、是否绑卡、超额是否扣费

## Software & digital services / 软件与数字服务

- GitHub Student Developer Pack, JetBrains free licenses
- Epic Games Store weekly free games, r/FreeGameFindings
- Giveaways / lifetime deals: official pages first; AppSumo-style buyouts are `cost_type=paid` / 限免、终身会员以官方页面为准，AppSumo 类属于付费

## Risk leads (record as `category=risk`) / 风险线索

Rug pulls, withdrawal problems, ban waves, phishing sites, "free giveaway" scams, trap terms. Sources: each category's communities and official security notices.
跑路、提现困难、封号潮、钓鱼网站、免费送诈骗、条款陷阱。来源：各类社区和官方安全公告。

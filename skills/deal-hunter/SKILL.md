---
name: deal-hunter
description: 羊毛猎手 Deal Hunter — find deals across the web, verify each on the official page, de-duplicate and track them, and auto-claim them in a browser the user is already signed in to. Covers free AI credits and plan discounts, crypto airdrops/points/exchange promos, crypto cards (U卡), bank and card sign-up bonuses, free VPS/cloud tiers, and software giveaways. Use when the user says "find deals", "any freebies today", "free Claude/GPT/Gemini credits", "claim it for me", "deal digest", "what's expiring", or 找羊毛、薅羊毛、今天有什么免费的、帮我领一下、羊毛日报、哪些快到期了.
---

# 羊毛猎手 · Deal Hunter

**Language / 语言**：Reply in the user's language. If the user writes in Chinese, answer in Chinese; otherwise answer in English (or the user's language). Pass `--lang zh` or `--lang en` to `ledger.py digest` to match.
用户用什么语言，你就用什么语言回复；生成日报时给 `ledger.py digest` 加对应的 `--lang zh` 或 `--lang en`。

Goal: the user never has to browse for deals. You **discover → verify → classify → de-duplicate → record → claim → archive**.
目标：用户不用每天自己刷，你负责 **发现 → 核对 → 分类 → 去重 → 记账 → 领取 → 归档**。

Files in this skill / 本 skill 的文件：
- `references/sources.md` — where to look for each category / 每类去哪找、怎么搜
- `references/claiming.md` — browser sign-in per platform, claim flow, stop rules / 各平台浏览器怎么登录、领取流程、停止条件
- `scripts/ledger.py` — local ledger: de-dupe, auto-archive, claim log, digest (Python stdlib only) / 本地账本
- `scripts/feeds.py` — read any RSS/Atom feed as JSON / 读 RSS、Atom 源

## 0. First run / 第一次使用

Run `python3 scripts/ledger.py config`. If not configured, ask the user and save with `ledger.py config --set key=value`:
运行 `python3 scripts/ledger.py config`，没配置过就问用户下面几项并保存：

- `interests` — categories to watch (default all: `ai,crypto,ucard,bank,vps,software,other`) / 关心哪些类别
- `regions` — where the user lives and which countries' phone numbers / IDs they have (rules out ineligible deals) / 所在地区、有哪些国家的手机号和证件
- `auto_claim` — `off` (find only) · `free_only` (auto-claim only truly free, no card, no KYC) · `ask` (ask every time, default) / 只找不领 · 只自动领真正免费的 · 每条先问（默认）
- `accounts` — accounts already signed in to the browser (Google, GitHub, X…) / 浏览器里已登录的账号
- `lang` — `zh` or `en`, the user's language / 用户语言

Data lives in `~/.deal-hunter/` (override with `DEAL_HUNTER_HOME`), **on the user's machine only**. If you cannot run Python, keep a table with the same fields in the conversation, project or platform memory, and apply the same de-dupe and archive rules.
账本和配置在 `~/.deal-hunter/`，**只存在用户本机**。不能运行 Python 时，就在对话、项目或平台记忆里维护同样字段的一张表，按同样规则去重和归档。

## 1. Discover / 发现

Search per `references/sources.md`, only the user's categories. First run `ledger.py list --status active --brief` to see what is already tracked.
按 `references/sources.md` 搜索用户关心的类别；先运行 `ledger.py list --status active --brief`，避免重复。

## 2. Verify (most important) / 核对（最重要）

Open the **official page** (promo page, official announcement, official blog or official account post) for every item and confirm:
每一条都要**打开官方页面**确认：

- The offer exists and has not ended / 活动存在、还没结束
- Deadline — only if officially stated; otherwise leave it empty, **never guess** / 截止时间只取官方写明的，**不要猜**
- Regions, eligibility, hidden conditions (new users only, invite code, US phone, KYC…) / 地区、资格、隐藏条件
- `cost_type`, exactly one / 成本类型，必选一个：
  `free` truly free 真正免费 · `trial` free trial that bills or needs a card 免费试用 · `deposit` needs a deposit 要充值入金 · `volume` needs trading volume 要交易量 · `invite` needs an invite 要邀请 · `paid` discount on a paid product 付费折扣
- Value — `value_usd` only if the official page gives an amount; otherwise explain in `value_note`, don't estimate / 官方给了金额才写，不估算

Items seen only second-hand (forums, reposts, aggregators) with no official source get `verified=false` and are shown as "unverified / 待核实". **Never invent deals or present rumours as fact.**
只在二手来源看到、找不到官方出处的，标 `verified=false`，展示为「待核实」。**绝不编造优惠，也不把传闻写成事实。**

## 3. Record / 记账

```bash
echo '[{...}, {...}]' | python3 scripts/ledger.py add
```

Fields: `ledger.py add --help`. Required: `title`, `category`, `official_url`, `cost_type`, `sources`. The same offer (same official URL, or same vendor + title) is merged, not duplicated. Expired items are archived automatically on every run. Write `title`/`offer` in the user's language.
必填字段同上；同一活动自动合并来源；过期自动归档。`title`、`offer` 用用户的语言写。

## 4. Claim / 领取

Read `references/claiming.md` first. In short / 先读 `references/claiming.md`，要点：

- Work out which browser you have: a platform cloud computer or cloud browser (Grok Bot, Muse, ChatGPT Work…: ask the user to **take over** and sign in themselves; the session persists), or the user's local browser (Claude in Chrome or similar extensions, Playwright MCP with a persistent profile, computer use). With none, list the steps instead of claiming.
  先判断手上是哪种浏览器：平台自带的云电脑或云端浏览器（Grok Bot、Muse、ChatGPT Work 等，需要登录时请用户**接管**后自己登录，登录会保留），还是用户本机的浏览器。都没有就只列步骤，不自动领。
- Only the user's own signed-in accounts, one account per person, **one claim per offer**. / 只用用户自己的账号，**一个活动领一份**。
- With `auto_claim=free_only`, auto-claim only `cost_type=free`, `verified=true`, eligible region, no card/KYC/wallet. / `free_only` 只自动领真正免费、已核对、地区符合、不绑卡不实名的。
- **Always stop and hand over** for: payment, card binding, deposits, KYC/ID upload, personal identity data, SMS/email codes, CAPTCHAs, auto-renewal terms, wallet connect/sign. / 付款、绑卡、充值、实名、证件、验证码、人机验证、自动续费、连接钱包签名——**一律停下交给用户**。
- Then `ledger.py claim <id> --result "what was received / where it stopped"`. / 领完记录结果。

## 5. Report / 汇报

`python3 scripts/ledger.py digest --lang zh|en` produces the digest by module:
生成按模块分组的日报：

A New today 今日新发现 · B Top value 高价值排行 · C AI · D Crypto · E Banks & cards 银行与卡 · F VPS & cloud VPS 与云 · G Ending within 48h 即将截止 · H Archive count 已结束档案

Each item shows title, category, offer, value, cost type, conditions, regions, deadline, official link, sources, last verified, risks. `risk` items (scams, rug pulls, phishing, trap terms) go under "⚠️ Risk alerts / 风险提醒". If there are many, show A and G first and ask before expanding.
每条都包含上述字段；风险类单独列出；条目多时先给 A 和 G。

## 6. Scheduling / 定时运行

If the user wants it "every 2 hours / 每 2 小时": when the platform supports scheduled tasks (Claude scheduled tasks, cron, `/loop`…), schedule "run deal-hunter: discover → verify → record → claim per auto_claim → report only new high-value or ending-within-48h items". Otherwise tell the user to just say "find deals / 找羊毛" each time.
平台支持定时任务就按上面的流程设好；不支持就告诉用户每次说一句即可。

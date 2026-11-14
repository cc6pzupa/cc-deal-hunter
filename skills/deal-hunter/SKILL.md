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

Don't open with a questionnaire — start working. / 不要先问一串问题，直接开工。

1. **Detect signed-in accounts yourself.** If you have a browser, open google.com, github.com and x.com and check whether each shows the user as signed in. Save what you find: `ledger.py config --set accounts=google,github`.
   **自己检查已登录的账号。** 有浏览器就打开 google.com、github.com、x.com，看是不是已经登录，结果存进 `accounts`。
2. **Ask once, only if it matters.** Tell the user in one line what you found and, if Google isn't signed in, ask whether to take over and sign in now or carry on (login-only items will wait on the "Waiting for you" list). Then start.
   **最多问一句。** 一行告诉用户查到了什么；Google 没登录的话，问一句现在要不要接管登录，还是先跑（要登录的会进「待你处理」）。然后开始。
3. Language: answer in the language the user wrote in, and save it (`--set lang=zh|en`). / 用户用什么语言就用什么语言，顺手存下来。

Defaults, no need to ask / 默认值，不用问：all categories 全部类别 · `auto_claim=free_only` (truly free ones are claimed straight away; everything else goes on the waiting list / 真正免费的直接领，其他进待处理). The user can change them any time by saying so, e.g. "only AI and VPS" or "ask before each claim". / 用户随时一句话就能改，比如「只要 AI 和 VPS」「每条领之前问我」。

Data lives in `~/.deal-hunter/` (override with `DEAL_HUNTER_HOME`), **on the user's machine only**. If you cannot run Python, keep a table with the same fields in the conversation, project or platform memory, and apply the same de-dupe and archive rules.
账本和配置在 `~/.deal-hunter/`，**只存在用户本机**。不能运行 Python 时，就在对话、项目或平台记忆里维护同样字段的一张表，按同样规则去重和归档。

## 1. Discover / 发现

Search per `references/sources.md`, only the user's categories. First run `ledger.py list --status active --brief` to see what is already tracked.
按 `references/sources.md` 搜索用户关心的类别；先运行 `ledger.py list --status active --brief`，避免重复。

## 2. Verify (most important) / 核对（最重要）

Open the **official page** (promo page, official announcement, official blog or official account post) for every item and confirm:
每一条都要**打开官方页面**确认：

- The offer exists and has not ended / 活动存在、还没结束
- Deadline — as officially stated; leave it empty if none / 截止时间按官方写的，没写就留空
- Regions, eligibility, hidden conditions (new users only, invite code, US phone, KYC…) / 地区、资格、隐藏条件
- `cost_type`, exactly one / 成本类型，必选一个：
  `free` truly free 真正免费 · `trial` free trial that bills or needs a card 免费试用 · `deposit` needs a deposit 要充值入金 · `volume` needs trading volume 要交易量 · `invite` needs an invite 要邀请 · `paid` discount on a paid product 付费折扣
- Value — `value_usd` only if the official page gives an amount; otherwise describe it in `value_note` / 官方给了金额才写，否则在 `value_note` 里说明

Items seen only second-hand (forums, reposts, aggregators) with no official source get `verified=false` and are shown as "unverified / 待核实". Record only what you found.
只在二手来源看到、找不到官方出处的，标 `verified=false`，展示为「待核实」。只写查到的事实。

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
- Use the user's own signed-in account; one claim per offer. / 用用户自己的账号，一个活动领一份。
- With `auto_claim=free_only` (default), claim `cost_type=free`, `verified=true` items with no card/KYC/wallet straight away. / `free_only`（默认）真正免费、已核对、不绑卡不实名的直接领。
- **Keep the batch moving.** When an item needs something only the user can do — sign-in, card binding, payment, deposit, KYC/ID, SMS/email code, CAPTCHA, wallet connect/sign, terms to accept, or the site blocks automation — park it with `ledger.py hold <id> --reason login|card|payment|kyc|code|captcha|wallet|terms|blocked|other --note "where it stopped"` and **move on to the next item**.
  **整批不停。** 遇到需要用户本人处理的（登录、绑卡、付款、充值、实名、验证码、人机验证、钱包签名、条款确认、网站拦截自动操作），用 `ledger.py hold` 放进「待你处理」，**接着领下一条**。
- After the whole batch, show the "🙋 Waiting for you / 待你处理" list grouped by reason (the digest puts it at the top). Sign-ins are batched: the user takes over once, signs in to all those sites, then says "continue claiming / 继续领" — run `ledger.py list --status pending` and retry each.
  整批跑完再把「待你处理」按原因分组给用户（日报会放在最上面）。要登录的合并成一次：用户接管一次、把这些网站都登录好，说「继续领」，你再运行 `ledger.py list --status pending` 逐条重试。
- Successful claims: `ledger.py claim <id> --result "what was received"` (this also clears a hold). / 领到了就记录，同时会从待处理里移除。

## 5. Report / 汇报

`python3 scripts/ledger.py digest --lang zh|en` produces the digest by module:
生成按模块分组的日报：

A New today 今日新发现 · B Top value 高价值排行 · C AI · D Crypto · E Banks & cards 银行与卡 · F VPS & cloud VPS 与云 · G Ending within 48h 即将截止 · H Archive count 已结束档案

Each item shows title, category, offer, value, cost type, conditions, regions, deadline, official link, sources, last verified, risks. `risk` items (scams, rug pulls, phishing, trap terms) go under "⚠️ Risk alerts / 风险提醒". If there are many, show A and G first and ask before expanding.
每条都包含上述字段；风险类单独列出；条目多时先给 A 和 G。

## 6. Scheduling / 定时运行

If the user wants it "every 2 hours / 每 2 小时": when the platform supports scheduled tasks (Claude scheduled tasks, cron, `/loop`…), schedule "run deal-hunter: discover → verify → record → claim per auto_claim → report only new high-value or ending-within-48h items". Otherwise tell the user to just say "find deals / 找羊毛" each time.
平台支持定时任务就按上面的流程设好；不支持就告诉用户每次说一句即可。

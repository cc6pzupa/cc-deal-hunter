---
name: deal-hunter
description: 羊毛猎手 Deal Hunter — find deals across the web, verify each on the official page, de-duplicate and track them, and auto-claim them in a browser the user is already signed in to. Covers free AI credits and plan discounts, crypto airdrops/points/exchange promos, crypto cards (U卡), bank and card sign-up bonuses, free VPS/cloud tiers, and software giveaways. Use when the user says "find deals", "any freebies today", "free Claude/GPT/Gemini credits", "claim it for me", "deal digest", "what's expiring", or 找羊毛、薅羊毛、今天有什么免费的、帮我领一下、羊毛日报、哪些快到期了.
---

# 羊毛猎手 · Deal Hunter

**Language / 语言**：Reply in the user's language. If the user writes in Chinese, answer in Chinese; otherwise answer in English (or the user's language). Pass `--lang zh` or `--lang en` to `ledger.py digest` to match.
用户用什么语言，你就用什么语言回复；生成日报时给 `ledger.py digest` 加对应的 `--lang zh` 或 `--lang en`。

Goal: the user never has to browse for deals. You **discover → verify → classify → de-duplicate → record → claim → archive**, on a schedule (every 2 hours by default).
目标：用户不用每天自己刷，你负责 **发现 → 核对 → 分类 → 去重 → 记账 → 领取 → 归档**，并且定时自动跑（默认每 2 小时）。

Files in this skill / 本 skill 的文件：
- `references/sources.md` — where to look for each category / 每类去哪找、怎么搜
- `references/claiming.md` — browser sign-in per platform, claim flow, stop rules / 各平台浏览器怎么登录、领取流程、停止条件
- `scripts/ledger.py` — local ledger: de-dupe, auto-archive, claim log, digest (Python stdlib only) / 本地账本
- `scripts/dashboard.html` — board template used by `ledger.py dashboard` / 看板模板
- `scripts/feeds.py` — read any RSS/Atom feed as JSON / 读 RSS、Atom 源

## 0. First run / 第一次使用

Don't open with a questionnaire — start working. / 不要先问一串问题，直接开工。

1. **Check Google first.** Open https://accounts.google.com . If the user isn't signed in, **bring up the sign-in right away — don't ask**: on a cloud computer start a take-over on that page; in a local browser leave the page open and send the user the link to sign in. Once signed in, carry on.
   **开局先查 Google。** 打开 https://accounts.google.com ，没登录就**直接弹出登录，不用问**：云电脑上直接发起接管；本机浏览器就把登录页开着、把链接发给用户。登录好就继续。
2. Glance at github.com and x.com too and save what's signed in: `ledger.py config --set accounts=google,github`. Don't stop for those — sites that need them go on the waiting list. / 顺手看一下 github.com、x.com，把已登录的存进 `accounts`；这两个没登录不用停，要用到的活动进「待你处理」。
3. Language: answer in the language the user wrote in, and save it (`--set lang=zh|en`). / 用户用什么语言就用什么语言，顺手存下来。

Defaults, no need to ask / 默认值，不用问：all categories 全部类别 · `auto_claim=free_only` (truly free ones are claimed straight away; everything else goes on the waiting list / 真正免费的直接领，其他进待处理). The user can change them any time by saying so, e.g. "only AI and VPS" or "ask before each claim". / 用户随时一句话就能改，比如「只要 AI 和 VPS」「每条领之前问我」。

Data lives in `~/.deal-hunter/` (override with `DEAL_HUNTER_HOME`), **on the user's machine only**. If you cannot run Python, keep a table with the same fields in the conversation, project or platform memory, and apply the same de-dupe and archive rules.
账本和配置在 `~/.deal-hunter/`，**只存在用户本机**。不能运行 Python 时，就在对话、项目或平台记忆里维护同样字段的一张表，按同样规则去重和归档。

## 0.5 Build the board / 建看板

Right after the Google check — before searching — set up the user's **deal board**. Everything you find and claim lands on it, and you refresh it after every run.
查完 Google 登录、开始搜之前，先给用户**建一个羊毛看板**。之后找到的、领到的都放上去，每跑一轮刷新一次。

What it shows / 看板内容：
- **Stat tiles / 统计**：Active 进行中 · New today 今日新增 · Ending within 48h 48 小时内截止 · Waiting for you 待你处理 · Unverified 待核实 · Claimed 已领 · Confirmed value $ 已确认价值
- **Tabs / 分栏**：🙋 Waiting for you 待你处理 (default when not empty / 有内容时默认打开) · A New today 今日新发现 · B Top value 高价值 · C AI · D Crypto · E Banks & cards 银行与卡 · F VPS & cloud VPS 与云 · G Ending soon 即将截止 · H Archive 已结束 · ⚠️ Risk 风险 · All 全部
- **Search / 搜索** over title, offer, sources / 按名称、内容、来源搜
- **Card per deal / 每条一张卡片**：category, cost type, unverified / claimed / waiting-reason tags; value; title linking to the official page; offer; deadline, regions, sources, last verified; conditions; risks; for waiting items, where it stopped and the page to resume / 分类、成本类型、待核实/已领/待处理原因标签；价值；标题链到官方页；内容；截止、地区、来源数、核对时间；条件；风险；待处理的写停在哪一步和继续页面

How to build it on each platform / 各平台怎么建：
- The board is **in Chinese by default** with a 中文/EN toggle; use English only if the user asks. / 看板**默认中文**，右上角可切换英文；用户要求才默认英文。
- **Can run Python / 能运行 Python**：`python3 scripts/ledger.py dashboard` writes a prebuilt, self-contained HTML board to `~/.deal-hunter/dashboard.html`; open it in the browser and give the user the path. Re-run after every batch. / 生成单文件 HTML 看板，用浏览器打开并把路径告诉用户；每跑完一轮重新生成。
- **Muse**：create a dedicated Space as the board (Spaces build trackers and boards), with the tiles, tabs and card fields above; update it in the background after each run. / 建一个专门的 Space 当看板，按上面的统计、分栏、卡片字段做；每轮后台更新。
- **Grok Bot / ChatGPT Work / other cloud computers / 其他云电脑**：build the board as a page on the cloud computer (copy the layout of `scripts/dashboard.html`, fill its `DATA` with the items) or in the platform's canvas/document feature; keep it open and refresh it after each run. / 在云电脑上做成网页（照 `scripts/dashboard.html` 的布局，把数据填进 `DATA`），或用平台的画布/文档功能；保持打开，每轮刷新。

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
- **Email verification codes: get them yourself.** When a site emails a code or a confirmation link, open https://mail.google.com in the same browser (the user's Google is signed in), find the newest message from that site, and enter the code or open the link. Use the platform's Gmail connector instead if it has one. Only if nothing arrives within a couple of minutes, park it as `code`.
  **邮箱验证码自己去取。** 网站发了邮箱验证码或确认链接，就在同一个浏览器打开 https://mail.google.com （Google 已登录），找到这个网站最新的那封邮件，填验证码或点确认链接；平台有 Gmail 连接器就用连接器。等几分钟还没收到，才放进待处理（`code`）。
- **Keep the batch moving.** When an item needs something only the user can do — sign-in, card binding, payment, deposit, KYC/ID, SMS code, CAPTCHA, wallet connect/sign, terms to accept, or the site blocks automation — park it with `ledger.py hold <id> --reason login|card|payment|kyc|code|captcha|wallet|terms|blocked|other --note "where it stopped"` and **move on to the next item**.
  **整批不停。** 遇到需要用户本人处理的（登录、绑卡、付款、充值、实名、短信验证码、人机验证、钱包签名、条款确认、网站拦截自动操作），用 `ledger.py hold` 放进「待你处理」，**接着领下一条**。
- After the whole batch, show the "🙋 Waiting for you / 待你处理" list grouped by reason (the digest puts it at the top). Sign-ins are batched: the user takes over once, signs in to all those sites, then says "continue claiming / 继续领" — run `ledger.py list --status pending` and retry each.
  整批跑完再把「待你处理」按原因分组给用户（日报会放在最上面）。要登录的合并成一次：用户接管一次、把这些网站都登录好，说「继续领」，你再运行 `ledger.py list --status pending` 逐条重试。
- Successful claims: `ledger.py claim <id> --result "what was received"` (this also clears a hold). / 领到了就记录，同时会从待处理里移除。

## 5. Report / 汇报

After each run, refresh the board (`ledger.py dashboard`), then reply with a short digest — `python3 scripts/ledger.py digest --lang zh|en`:
每轮跑完先刷新看板，再回一份简短日报：

A New today 今日新发现 · B Top value 高价值排行 · C AI · D Crypto · E Banks & cards 银行与卡 · F VPS & cloud VPS 与云 · G Ending within 48h 即将截止 · H Archive count 已结束档案

Each item shows title, category, offer, value, cost type, conditions, regions, deadline, official link, sources, last verified, risks. `risk` items (scams, rug pulls, phishing, trap terms) go under "⚠️ Risk alerts / 风险提醒". If there are many, show A and G first and ask before expanding.
每条都包含上述字段；风险类单独列出；条目多时先给 A 和 G。

## 6. Schedule it — by default / 定时运行（默认开启）

This is a recurring job, not a one-off. At the end of the first run, **create the schedule yourself without asking**: every 2 hours, using the platform's own scheduler — Grok Bot / ChatGPT Work scheduled tasks, Muse Space background updates, Claude scheduled tasks or `/loop`, or cron where you have a shell. Tell the user in one line that it's on and how to change or stop it ("every 4 hours", "only mornings", "stop").
这是一个定时任务，不是跑一次就完。第一轮跑完，**不用问，直接设好定时**：每 2 小时一次，用平台自己的定时功能（Grok Bot / ChatGPT Work 的定时任务、Muse Space 的后台更新、Claude 的定时任务或 `/loop`，有 shell 就用 cron）。用一句话告诉用户已开启，以及怎么改或关（"改成 4 小时一次""只在早上跑""停掉"）。

Each scheduled run / 每次定时运行：discover → verify → record → claim per `auto_claim` → refresh the board → **notify only** when there are new high-value items, items ending within 48h, or new "Waiting for you" items; stay silent otherwise.
发现 → 核对 → 记账 → 按 `auto_claim` 领取 → 刷新看板 → **只在**有新的高价值活动、48 小时内截止、或新的待你处理时才提醒，其余时候不打扰。

Cron example (local) / 本机 cron 示例：`0 */2 * * * <agent CLI> "run deal-hunter"` — use whatever non-interactive command the user's agent provides. / 换成用户所用 agent 的非交互命令。

If the platform has no scheduler at all, say so once and tell the user to say "find deals / 找羊毛" when they want a run. / 平台完全没有定时功能，就说一次，让用户想跑的时候说一句。

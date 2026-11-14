# 羊毛猎手 · Deal Hunter

**中文** | [English](#english)

一个给 AI 用的 skill：**全网找羊毛 → 回官方页核对 → 分类去重 → 用你自己登录的浏览器自动领 → 过期归档 → 出日报。** 你用什么语言跟 AI 说话，它就用什么语言回复。

覆盖 AI 订阅和免费额度、Crypto 空投/积分/交易所活动、U卡、海外银行与银行卡、VPS 与云、软件限免。

## 最快的用法：把这个仓库链接直接丢给 AI

```
帮我装上这个 skill：https://github.com/cc6pzupa/cc-deal-hunter
```

> **给 AI 看的安装说明 / For AI agents**：skill 在 `skills/deal-hunter/`（含 `SKILL.md`）。能装 skill 就把整个文件夹复制到你的 skills 目录，然后按 `SKILL.md` 的「第一次使用」问用户设置；不能装 skill 就读取 [`PROMPT.md`](PROMPT.md) 里用户语言的那一段，当作本次对话（或 Space、项目）的长期指令执行。The skill is in `skills/deal-hunter/`. If you support skills, copy that folder into your skills directory and run its first-time setup; if not, follow the block in the user's language in [`PROMPT.md`](PROMPT.md) as standing instructions.

## 一行命令安装

**Claude Code**（在 Claude Code 里输入）：
```
/plugin install deal-hunter --marketplace cc6pzupa/cc-deal-hunter
```
较老的 Claude Code 版本分两步：`/plugin marketplace add cc6pzupa/cc-deal-hunter`，再 `/plugin install deal-hunter@deal-hunter`。

**Codex、Gemini CLI、Cursor 等支持 Agent Skills 的工具**（需要 Node.js，用 [skills CLI](https://github.com/vercel-labs/skills)）：
```bash
npx skills add cc6pzupa/cc-deal-hunter          # 交互式选择装到哪个工具
npx skills add cc6pzupa/cc-deal-hunter -g -y    # 全局安装，跳过询问
```

**不用任何工具**（装到 Claude Code 的个人 skills 目录）：
```bash
git clone --depth 1 https://github.com/cc6pzupa/cc-deal-hunter /tmp/cc-deal-hunter && cp -r /tmp/cc-deal-hunter/skills/deal-hunter ~/.claude/skills/
```

**Claude 网页 / App**：下载 [deal-hunter.zip](https://wool.eshop.us.ci/skill/deal-hunter.zip)，在 设置 → Skills 里上传。

**Grok Bot、Muse、ChatGPT Work 等不能装 skill 的**：复制 [`PROMPT.md`](PROMPT.md) 里的中文版发给它，建议放进专门的 Space 或项目。

## 自动领取怎么登录

登录**永远由你本人完成**，AI 只做登录之后的操作：

- **内置云电脑的 AI**（Grok Bot、Muse、ChatGPT Work）：需要登录时，AI 会请你接管浏览器，你自己输密码、做两步验证；登录之后会一直保留在云电脑里。
- **本机浏览器**（Claude in Chrome 等扩展、Playwright MCP 加持久化配置目录、桌面控制）：用的就是你电脑上已经登录的账号，登录态不离开你的电脑。

要登录、付款、绑卡、充值、实名认证、验证码、人机验证、连接钱包、签名授权的，AI 不替你做，也**不会卡住**：放进「🙋 待你处理」清单，接着领下一条。整批跑完按原因分组给你，要登录的你接管一次全部登好，说「继续领」就行。一人一份，不注册小号，不绕过网站的机器人检测。详见 [`claiming.md`](skills/deal-hunter/references/claiming.md)。

建议准备一个专门用来薅羊毛的账号，不要在云电脑里登录主力邮箱、银行或交易所主账号。

## 里面有什么

```
skills/deal-hunter/
  SKILL.md                  主流程（中英双语）：发现 → 核对 → 记账 → 领取 → 汇报 → 定时
  references/sources.md     各类别去哪找、怎么搜
  references/claiming.md    各平台浏览器怎么登录、领取流程、停止条件
  scripts/ledger.py         本地账本：去重、过期归档、领取记录、待你处理清单、A–H 日报（--lang zh|en，只用 Python 标准库）
  scripts/feeds.py          读任意 RSS / Atom 源
PROMPT.md                   一段话版（中文版 + English），给不能装 skill 的 AI
.claude-plugin/             Claude Code 插件市场配置
```

账本和设置保存在你本机的 `~/.deal-hunter/`，不会上传到任何地方。

## 数据源

已核对的现成数据源：[cc羊毛减](https://wool.eshop.us.ci)——X 上的中文羊毛帖，每条都回原帖核对过，提供 RSS 和 MCP。其他来源（官方公告、Reddit、Doctor of Credit、LowEndTalk、NodeSeek、linux.do 等）见 [`sources.md`](skills/deal-hunter/references/sources.md)。

## 许可

[PolyForm Noncommercial 1.0.0](LICENSE.md)：个人学习、研究、自用以及非营利用途可以免费使用和修改；**禁止任何商业用途**（包括拿去收费、打包售卖、放进付费产品或服务）。商业授权请联系 [cc羊毛减](https://wool.eshop.us.ci)。

## 免责声明

本项目只整理公开信息并按你的指令操作你自己的账号。优惠、返利、开户、空投类信息不构成投资或消费建议；参与前请自行核实条款和风险，遵守各平台规则。

---

## English

[中文](#羊毛猎手--deal-hunter) | **English**

An AI skill that **finds deals across the web → verifies each on the official page → classifies and de-duplicates → claims them in a browser you're already signed in to → archives expired ones → writes a digest.** It replies in whatever language you use.

Covers free AI credits and plan discounts, crypto airdrops/points/exchange promos, crypto cards, overseas bank and card sign-up bonuses, free VPS/cloud tiers, and software giveaways.

### Quickest way: give your AI this repo link

```
Install this skill: https://github.com/cc6pzupa/cc-deal-hunter
```

### One-line install

**Claude Code** (type inside Claude Code):
```
/plugin install deal-hunter --marketplace cc6pzupa/cc-deal-hunter
```
Older Claude Code versions: `/plugin marketplace add cc6pzupa/cc-deal-hunter`, then `/plugin install deal-hunter@deal-hunter`.

**Codex, Gemini CLI, Cursor and other Agent Skills tools** (needs Node.js, uses the [skills CLI](https://github.com/vercel-labs/skills)):
```bash
npx skills add cc6pzupa/cc-deal-hunter          # choose which tool interactively
npx skills add cc6pzupa/cc-deal-hunter -g -y    # global install, no prompts
```

**No tools** (into Claude Code's personal skills folder):
```bash
git clone --depth 1 https://github.com/cc6pzupa/cc-deal-hunter /tmp/cc-deal-hunter && cp -r /tmp/cc-deal-hunter/skills/deal-hunter ~/.claude/skills/
```

**Claude (web / app):** download [deal-hunter.zip](https://wool.eshop.us.ci/skill/deal-hunter.zip) and upload it in Settings → Skills.

**Grok Bot, Muse, ChatGPT Work and other agents without skills:** paste the English block from [`PROMPT.md`](PROMPT.md#english), ideally into a dedicated Space or project.

### How sign-in works for claiming

Signing in is **always done by you**; the AI only acts afterwards.

- **Agents with a built-in cloud computer** (Grok Bot, Muse, ChatGPT Work): when a login is needed the AI hands you the browser ("take over"); you type the password and 2FA; the session stays on that cloud computer.
- **Your local browser** (Claude in Chrome and similar extensions, Playwright MCP with a persistent profile, computer use): reuses the accounts already signed in on your machine; the session never leaves it.

Anything that needs a sign-in, payment, card, deposit, KYC, verification code, CAPTCHA, wallet connection or signature is never done for you and **never blocks the run**: it goes on a "🙋 Waiting for you" list and the agent moves on. At the end you get the list grouped by reason; take over once to sign in to all the sites, say "continue claiming", and it retries. One claim per person, no alt accounts, no bot-detection bypassing. See [`claiming.md`](skills/deal-hunter/references/claiming.md).

Use a dedicated account for deals; don't sign in to your main email, bank or exchange accounts on a cloud computer.

### What's inside

`skills/deal-hunter/` holds `SKILL.md` (bilingual workflow), `references/sources.md` (where to look), `references/claiming.md` (sign-in per platform, claim flow, stop rules), `scripts/ledger.py` (local ledger, de-dupe, auto-archive, claim log, waiting-for-you list, A–H digest with `--lang zh|en`; Python stdlib only) and `scripts/feeds.py` (RSS/Atom reader). `PROMPT.md` has the paste-in prompt in Chinese and English. Your ledger and settings stay in `~/.deal-hunter/` on your machine.

### Data sources

Ready-made verified source: [cc羊毛减](https://wool.eshop.us.ci) — deal posts from X (mostly Chinese), each re-checked against the original post, with RSS and MCP. Other sources (official announcements, Reddit, Doctor of Credit, LowEndTalk, NodeSeek, linux.do…) are listed in [`sources.md`](skills/deal-hunter/references/sources.md).

### License

[PolyForm Noncommercial 1.0.0](LICENSE.md): free for personal, research and non-profit use and modification; **no commercial use** (no charging for it, reselling it, or putting it in a paid product or service). For a commercial licence, contact [cc羊毛减](https://wool.eshop.us.ci).

### Disclaimer

This project only organises public information and operates your own accounts on your instructions. Deal, cashback, account-opening and airdrop information is not investment or purchasing advice; check the terms and risks yourself and follow each platform's rules.

# Auto-claiming / 自动领取

Claiming uses accounts already signed in to the browser — most often Google, then GitHub, X, Apple; most offers allow one-click sign-up with them. The user signs in; you take it from there.
自动领取用浏览器里已经登录好的账号（最常见 Google，其次 GitHub、X、Apple）。用户登录，之后的操作交给你。

## Step 1: which browser do you have? / 第一步：判断你手上是哪种浏览器

### A. Platform cloud computer / cloud browser / 平台自带的云电脑或云端浏览器

| Platform 平台 | Sign-in 怎么登录 | Persistence 能保持多久 |
|---|---|---|
| Grok Bot (xAI, Agent Computer) | At a login page, hand the screen to the user with **Take over**; they type the password and 2FA / 发起「Take over」，用户自己输密码、做两步验证 | Kept on the cloud disk across sessions; **all Bots on the account share this computer and its logins** / 跨会话保留，同账号所有 Bot 共用 |
| ChatGPT Work (OpenAI, cloud browser) | The user completes the site login; ChatGPT never sees the password / 用户自己完成登录 | Cookies kept in the cloud until they expire; clearable per site in settings / 保留到过期，可按网站清除 |
| Muse (Meta, built-in cloud computer) | Same: ask the user to take over the browser and sign in / 同样请用户接管浏览器登录 | Kept on the cloud computer; keep records in a dedicated Space / 保留在云电脑里，记录放进专门的 Space |
| Other agents with a cloud computer (Manus…) | Use the platform's take-over / hand-off feature / 用平台的接管功能 | Per platform docs / 以平台说明为准 |

- At the start: open https://accounts.google.com ; if not signed in, start a take-over immediately (no question) and continue once the avatar shows. / 开局打开 Google 登录页，没登录就直接发起接管，看到头像就继续。
- **Google number prompt / Google 数字确认**：on a new device Google often shows a number and asks the user to tap it on their phone. Read the number off the screen and tell the user right away ("📱 tap **47** on your phone"); continue when the page moves on; on timeout click Resend and report the new number. Same for other sites that show a number to match. / 新设备登录 Google 常会显示一个数字、要用户在手机上点同样的数字：马上把数字告诉用户（「📱 在手机上点 **47**」），通过就继续，超时点重新发送再报新数字。其他网站要求核对数字的同样处理。
- Email codes and confirmation links: open https://mail.google.com in the same browser and read the newest message from that site (or use the platform's Gmail connector). / 邮箱验证码、确认链接：同一个浏览器打开 Gmail 看这个网站最新的邮件（平台有 Gmail 连接器就用连接器）。

### B. The user's local browser / 用户本机的浏览器

| Method 方式 | Notes 说明 |
|---|---|
| Claude in Chrome and similar extensions / 浏览器扩展 | Uses the user's everyday Chrome, already signed in; nothing to set up / 直接用平时的 Chrome，什么都不用设置 |
| Playwright MCP + persistent profile / 持久化配置目录 | `{"mcpServers":{"browser":{"command":"npx","args":["@playwright/mcp@latest","--user-data-dir","~/.deal-hunter/browser-profile"]}}}` — first run: open the Google login page and **let the user sign in in the window themselves**; it stays signed in / 第一次让用户自己在窗口里登录，之后一直有效 |
| Computer use / 桌面控制 | Drive the signed-in browser on the user's desktop / 操作桌面上已登录的浏览器 |
| AI browsers / local agents (Comet, Edge Copilot mode…) | Use the user's own browser profile — same as an extension / 等同于扩展 |

### C. No browser at all / 什么浏览器都没有

Don't claim. Give the user the steps and official link for each item. / 不自动领，把步骤和官方链接整理给用户。

## Step 2: claim flow / 第二步：领取流程

1. Pick claimable items (`ledger.py list --claimable`, or apply the `auto_claim` rules yourself without the script); high value and soon-ending first. / 筛出能领的，优先高价值和快到期的。
2. Open the official link. **Check the domain first** — it must be official; if it redirects somewhere unfamiliar, stop and mark it as a risk. / **先核对域名**，跳到陌生域名就停下并标为风险。
3. When sign-in is needed, prefer "Continue with Google / GitHub" using the signed-in account; if not signed in, ask the user to take over per Step 1. / 优先「用 Google / GitHub 继续」；没登录就请用户接管登录。
4. Follow the page step by step — sign up, click claim, enter codes — and confirm a success message after each step. Sign-up forms: name and email from the Google account; every other ordinary field (birthday, gender, occupation, company, use case…) from `ledger.py config --profile` — one saved, reasonable adult profile reused everywhere. Phone: ask the user the first time, save it, reuse it. Unverified address fields: IP location + a public, non-residential place from the map, generated once and saved. / 注册表单：姓名邮箱用 Google 账号的；其他普通字段（生日、性别、职业、公司、用途…）按 `ledger.py config --profile` 里那套固定的成年人资料填，各站一致。手机号第一次问用户、存下复用；不核验的地址按 IP 位置 + 地图上的公共非住宅地点生成一次、存下复用。 When a code or confirmation link is sent by email, open https://mail.google.com , take it from the newest message from that site, and continue. / 一步步操作，每步确认有成功提示。要邮箱验证码或确认链接时，打开 Gmail 从这个网站最新的邮件里取，然后继续。
5. If you hit any of these, park the item and **move on to the next one** (the user handles them later in one go): / 遇到以下情况，放进「待你处理」，**接着领下一条**（用户之后一次性处理）：
   - payment, card binding, top-up, deposit, or an auto-renewal checkbox / 付款、绑卡、充值、入金、自动续费
   - KYC, ID upload, ID or tax numbers / 实名认证、上传证件、身份证号或税号
   - a password, an SMS code the user hasn't sent yet, an email code that hasn't arrived after a few minutes / 密码、用户还没给的短信验证码、等几分钟还没收到的邮箱验证码
   - a human check (CAPTCHA) that hasn't cleared after **3 attempts** — waiting for it to pass on its own or reloading the page; puzzle/image challenges aren't solved by you and go straight to the list / 试了 **3 次**还没过的人机验证（等它自动通过或刷新页面）；要做图片/拼图题的不自己解，直接放进清单
   - wallet connect, signatures, token approvals / 连接钱包、签名、授权代币
   - terms that need the user's judgement (data used for training, forced arbitration, long holding periods) / 需要用户自己判断的条款
   - the site blocks automation or keeps challenging the cloud browser / 网站拦截自动操作，或者反复要求验证

   Park it / 放进待处理：`ledger.py hold <id> --reason login|card|payment|kyc|code|captcha|wallet|terms|blocked|other --note "where it stopped / 停在哪一步" --url <page to resume / 从哪个页面继续>`. Without the script, add it to a "Waiting for you / 待你处理" list in the conversation with the same fields.
   "Already claimed", "not eligible" or "region not supported" are not holds: record them with `ledger.py claim <id> --failed --result "..."`. / 「已领过、不符合资格、地区不支持」不算待处理，用 `--failed` 记录。
6. Record successes: what was received, where to see it, when it expires (for trials: when billing starts and how to cancel) — `ledger.py claim <id> --result "..."`. / 领到了就记录：领到什么、在哪查看、何时过期（试用类写上何时开始扣费、怎么取消）。
7. When the batch is done, give the user the "🙋 Waiting for you / 待你处理" list grouped by reason (`ledger.py digest` puts it first). **Batch the sign-ins**: on a cloud computer, start one take-over and let the user sign in to every site on the login list; locally, ask them to sign in in their browser. When they say "continue / 继续领", run `ledger.py list --status pending` and retry each; items that still need them get held again. / 整批跑完，把「待你处理」按原因分组交给用户。**登录合并成一次**：云电脑上发起一次接管，让用户把清单上的网站都登录好；之后说「继续领」，就逐条重试，还需要用户处理的再放回清单。

## Modes / 模式

- Use the user's own account, one claim per offer. / 用用户自己的账号，一个活动领一份。
- `auto_claim=ask`: confirm each item before claiming. `free_only`: claim the truly free ones directly. / `ask` 每条先确认；`free_only` 真正免费的直接领。

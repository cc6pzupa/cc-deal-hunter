#!/usr/bin/env python3
"""Deal ledger / 羊毛账本: de-dupe, auto-archive, claim log, digest. Data in $DEAL_HUNTER_HOME (default ~/.deal-hunter). Stdlib only.

  ledger.py config [--set key=value ...]
  ledger.py add                      read one item or a list as JSON from stdin / 从 stdin 读 JSON
  ledger.py list [--category C] [--status active|expiring|pending|archived|claimed|all] [--claimable] [--brief]
  ledger.py hold ID --reason R [--note TEXT] [--url URL]   park it for the user, keep going / 放进「待你处理」，继续下一条
  ledger.py claim ID --result TEXT [--failed]
  ledger.py archive ID               archive manually (offer ended early) / 手动归档
  ledger.py digest [--days 1] [--lang zh|en]   Markdown digest / 日报
  ledger.py dashboard [--lang zh|en] [--out PATH]   HTML board, Chinese by default / 看板，默认中文 (~/.deal-hunter/dashboard.html)
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.parse

HOME = os.path.expanduser(os.environ.get("DEAL_HUNTER_HOME", "~/.deal-hunter"))
DB = os.path.join(HOME, "deals.json")
CFG = os.path.join(HOME, "config.json")

CATEGORIES = ["ai", "crypto", "ucard", "bank", "vps", "software", "other", "risk"]
LABELS = {
    "zh": {"ai": "AI", "crypto": "Crypto", "ucard": "U卡", "bank": "银行与卡", "vps": "VPS与云", "software": "软件", "other": "其他", "risk": "风险",
           "free": "真正免费", "trial": "免费试用", "deposit": "需充值/入金", "volume": "需交易量", "invite": "需邀请", "paid": "付费优惠",
           "h_login": "要登录", "h_card": "要绑卡", "h_payment": "要付款/充值", "h_kyc": "要实名/证件", "h_code": "要验证码",
           "h_captcha": "人机验证", "h_wallet": "钱包签名/授权", "h_terms": "条款要你确认", "h_blocked": "网站拦截了自动操作", "h_other": "其他"},
    "en": {"ai": "AI", "crypto": "Crypto", "ucard": "Crypto card", "bank": "Bank & cards", "vps": "VPS & cloud", "software": "Software", "other": "Other", "risk": "Risk",
           "free": "Truly free", "trial": "Free trial", "deposit": "Needs deposit", "volume": "Needs volume", "invite": "Needs invite", "paid": "Paid discount",
           "h_login": "Sign-in needed", "h_card": "Card needed", "h_payment": "Payment / top-up", "h_kyc": "KYC / ID", "h_code": "Verification code",
           "h_captcha": "CAPTCHA", "h_wallet": "Wallet sign / approve", "h_terms": "Terms need your OK", "h_blocked": "Site blocked automation", "h_other": "Other"},
}
TEXT = {
    "zh": {"unverified": " ·【待核实】", "value_na": "价值未写明", "deadline": "截止", "not_stated": "未写明", "regions": "地区", "conditions": "条件",
           "official": "官方", "sources": "来源 {n} 个", "verified_at": "核对于", "claimed": " · ✅ 已领", "title": "# 羊毛日报 · {t}",
           "stats": "进行中 {a} · 新发现 {n} · 48 小时内截止 {e} · 待核实 {u} · 已领 {c}",
           "pending": "## 🙋 待你处理（{n} 条）", "pending_hint": "按原因分组。要登录的可以一次接管浏览器把这些网站都登录好，然后说「继续领」。",
           "stopped_at": "停在",
           "A": "A 今日新发现", "B": "B 高价值排行", "C": "C AI 专区", "D": "D Crypto 专区", "E": "E 银行与卡", "F": "F VPS 与云",
           "G": "G 即将截止（48 小时内）", "risk": "## ⚠️ 风险提醒", "H": "## H 已结束档案：{n} 条（`ledger.py list --status archived` 查看）"},
    "en": {"unverified": " · [unverified]", "value_na": "value not stated", "deadline": "ends", "not_stated": "not stated", "regions": "regions", "conditions": "Conditions",
           "official": "Official", "sources": "{n} source(s)", "verified_at": "verified", "claimed": " · ✅ claimed", "title": "# Deal digest · {t}",
           "stats": "Active {a} · new {n} · ending within 48h {e} · unverified {u} · claimed {c}",
           "pending": "## 🙋 Waiting for you ({n})", "pending_hint": "Grouped by reason. For sign-ins, take over the browser once, sign in to all of these sites, then say \"continue claiming\".",
           "stopped_at": "stopped at",
           "A": "A New today", "B": "B Top value", "C": "C AI", "D": "D Crypto", "E": "E Banks & cards", "F": "F VPS & cloud",
           "G": "G Ending within 48h", "risk": "## ⚠️ Risk alerts", "H": "## H Archive: {n} item(s) (`ledger.py list --status archived`)"},
}
COST_TYPES = ["free", "trial", "deposit", "volume", "invite", "paid"]
HOLD_REASONS = ["login", "card", "payment", "kyc", "code", "captcha", "wallet", "terms", "blocked", "other"]
DEFAULT_CFG = {"interests": ["ai", "crypto", "ucard", "bank", "vps", "software", "other"],
               "auto_claim": "free_only", "accounts": [], "lang": "zh"}
FIELDS_HELP = """Fields / 字段 (* required 必填):
  *title  *category (%s)  *official_url  *cost_type (%s)  *sources [url,...]
  offer 优惠内容 · value_usd number 数字 · value_note 价值说明 · conditions 参与条件 · regions [地区]
  start / deadline  ISO time, e.g. 2026-11-20 or 2026-11-20T23:59+08:00 (omit if not officially stated / 官方没写就不填)
  steps [步骤] · risks [风险] · vendor 厂商 · verified true/false (checked on the official page / 是否回官方页核对过)
  needs [card|kyc|phone|captcha|wallet] barriers when claiming / 领取时会遇到的门槛
""" % ("|".join(CATEGORIES), "|".join(COST_TYPES))


def now():
    return dt.datetime.now(dt.timezone.utc)


def iso(t):
    return t.astimezone(dt.timezone.utc).isoformat(timespec="seconds")


def parse_time(s):
    if not s:
        return None
    s = str(s).strip().replace("Z", "+00:00")
    try:
        t = dt.datetime.fromisoformat(s)
    except ValueError:
        raise SystemExit(f"Bad time / 时间格式不对: {s} (ISO, e.g. 2026-11-20 or 2026-11-20T23:59+08:00)")
    if t.tzinfo is None:  # 只给日期/没时区: 当作当天结束, 按 UTC 算, 宁可晚归档不早归档
        t = t.replace(tzinfo=dt.timezone.utc)
        if len(s) <= 10:
            t = t.replace(hour=23, minute=59, second=59)
    return t


def load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def save(path, data):
    os.makedirs(HOME, mode=0o700, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=HOME)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def norm_url(u):
    p = urllib.parse.urlsplit(u.strip())
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query) if not re.match(r"(utm_|ref$|ref_|fbclid|gclid|aff|invite|via$)", k, re.I)]
    host = p.netloc.lower().removeprefix("www.")
    return urllib.parse.urlunsplit(("https", host, p.path.rstrip("/"), urllib.parse.urlencode(q), ""))


def norm_text(s):
    return re.sub(r"[\W_]+", "", (s or "").lower())


def keys(d):
    out = [norm_url(d["official_url"])]
    if d.get("vendor"):
        out.append("vt:" + norm_text(d["vendor"]) + "|" + norm_text(d["title"]))
    return out


def make_id(d):
    return hashlib.sha1(keys(d)[0].encode()).hexdigest()[:8]


def status(d, t=None):
    t = t or now()
    if d.get("archived"):
        return "archived"
    dl = parse_time(d.get("deadline"))
    if dl and dl < t:
        return "archived"
    if d.get("claimed"):
        return "claimed"
    if d.get("hold"):
        return "pending"
    if dl and dl < t + dt.timedelta(hours=48):
        return "expiring"
    return "active"


def auto_archive(db):
    t, n = now(), 0
    for d in db.values():
        if not d.get("archived") and status(d, t) == "archived":
            d["archived"], d["archived_at"], d["archived_why"] = True, iso(t), "deadline passed"
            n += 1
    return n


def validate(d):
    miss = [k for k in ("title", "category", "official_url", "cost_type", "sources") if not d.get(k)]
    if miss:
        raise SystemExit(f"Missing fields / 缺字段 {miss}: {d.get('title') or d}\n\n{FIELDS_HELP}")
    if d["category"] not in CATEGORIES:
        raise SystemExit(f"category must be one of / 只能是 {CATEGORIES}: {d['title']}")
    if d["cost_type"] not in COST_TYPES:
        raise SystemExit(f"cost_type must be one of / 只能是 {COST_TYPES}: {d['title']}")
    if not str(d["official_url"]).startswith(("http://", "https://")):
        raise SystemExit(f"official_url must be a full URL / 要是完整链接: {d['title']}")
    for k in ("start", "deadline"):
        if d.get(k):
            parse_time(d[k])
    if isinstance(d["sources"], str):
        d["sources"] = [d["sources"]]
    for k in ("regions", "steps", "risks", "needs"):
        if isinstance(d.get(k), str):
            d[k] = [d[k]]
    if d.get("value_usd") is not None:
        d["value_usd"] = float(d["value_usd"])
    d["verified"] = bool(d.get("verified"))


def cmd_add(a, db):
    raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit(FIELDS_HELP)
    items = json.loads(raw)
    items = items if isinstance(items, list) else [items]
    index = {k: i for i, d in db.items() for k in keys(d)}
    t, added, merged = iso(now()), [], []
    for d in items:
        validate(d)
        hit = next((index[k] for k in keys(d) if k in index), None)
        if hit:
            old = db[hit]
            old["sources"] = sorted(set(old["sources"]) | set(d["sources"]))
            # 回官方页核对过的新信息才覆盖旧的; 没核对过的二手转述只补空缺, 不改已核对的内容
            for k, v in d.items():
                if k in ("sources", "id", "found_at", "claimed", "claim_log", "verified", "official_url") or v in (None, "", []):
                    continue
                if d["verified"] or not old.get(k):
                    old[k] = v
            if d["verified"]:
                old["verified"], old["last_verified"] = True, t
            merged.append(hit)
        else:
            i = make_id(d)
            d.update(id=i, found_at=t, last_verified=t if d["verified"] else None)
            db[i] = d
            index.update({k: i for k in keys(d)})
            added.append(i)
    print(json.dumps({"added": added, "merged_into_existing": merged}, ensure_ascii=False))


def claimable(d, cfg):
    mode = cfg.get("auto_claim", "free_only")
    if mode == "off" or d["category"] == "risk" or status(d) not in ("active", "expiring"):  # pending = waiting for the user / 等用户处理
        return False
    if mode == "free_only":
        return d["cost_type"] == "free" and d["verified"] and not set(d.get("needs") or []) & {"card", "kyc", "wallet"}
    return True


def sort_key(d):
    dl = parse_time(d.get("deadline"))
    return (status(d) != "expiring", -(d.get("value_usd") or 0), dl.timestamp() if dl else 9e12)


def cmd_list(a, db, cfg):
    rows = [d for d in db.values()
            if (a.status == "all" or status(d) == a.status or (a.status == "active" and status(d) in ("expiring", "pending")))
            and (not a.category or d["category"] == a.category)
            and (not a.claimable or claimable(d, cfg))]
    rows.sort(key=sort_key)
    if a.brief:
        rows = [{"id": d["id"], "title": d["title"], "category": d["category"], "status": status(d),
                 "deadline": d.get("deadline"), "official_url": d["official_url"]} for d in rows]
    else:
        rows = [dict(d, status=status(d)) for d in rows]
    print(json.dumps(rows, ensure_ascii=False, indent=1))


def cmd_claim(a, db):
    d = db.get(a.id) or sys.exit(f"No such id / 没有这个 id: {a.id}")
    d.setdefault("claim_log", []).append({"at": iso(now()), "ok": not a.failed, "result": a.result})
    if not a.failed:
        d["claimed"] = True
        d.pop("hold", None)
    print(json.dumps({"id": a.id, "claimed": d.get("claimed", False)}, ensure_ascii=False))


def cmd_hold(a, db):
    d = db.get(a.id) or sys.exit(f"No such id / 没有这个 id: {a.id}")
    d["hold"] = {"reason": a.reason, "note": a.note or "", "url": a.url or d["official_url"], "at": iso(now())}
    d.setdefault("claim_log", []).append({"at": d["hold"]["at"], "ok": False, "result": f"hold: {a.reason} {a.note or ''}".strip()})
    print(json.dumps({"id": a.id, "status": "pending", "reason": a.reason}, ensure_ascii=False))


def fmt_time(s, T):
    t = parse_time(s)
    return t.astimezone().strftime("%m-%d %H:%M") if t else T["not_stated"]


def line(d, lang):
    L, T = LABELS[lang], TEXT[lang]
    v = f"${d['value_usd']:g}" if d.get("value_usd") else (d.get("value_note") or T["value_na"])
    out = [f"**[{L[d['category']]}] {d['title']}**" + ("" if d["verified"] else T["unverified"]), f"  {d.get('offer') or ''}".rstrip()]
    if d["category"] != "risk":
        out.append(f"  {v} · {L[d['cost_type']]} · {T['deadline']} {fmt_time(d.get('deadline'), T)}"
                   + (f" · {T['regions']} {'/'.join(d['regions'])}" if d.get("regions") else ""))
    if d.get("conditions"):
        out.append(f"  {T['conditions']}: {d['conditions']}")
    if d.get("risks"):
        out.append(f"  ⚠️ {'; '.join(d['risks'])}")
    out.append(f"  {T['official']}: {d['official_url']} · {T['sources'].format(n=len(d['sources']))} · {T['verified_at']} {fmt_time(d.get('last_verified'), T)}"
               + (T["claimed"] if d.get("claimed") else ""))
    return "\n".join(x for x in out if x.strip())


def cmd_digest(a, db, cfg):
    lang = a.lang or cfg.get("lang") or "zh"
    T = TEXT[lang]
    t = now()
    since = t - dt.timedelta(days=a.days)
    live = [d for d in db.values() if status(d, t) in ("active", "expiring", "pending", "claimed")]
    deals = [d for d in live if d["category"] != "risk"]
    new = [d for d in deals if parse_time(d["found_at"]) >= since]
    expiring = [d for d in deals if status(d, t) == "expiring"]
    sec = [("A", new, True),
           ("B", sorted([d for d in deals if d.get("value_usd")], key=lambda d: -d["value_usd"])[:10], False),
           ("C", [d for d in deals if d["category"] == "ai"], True),
           ("D", [d for d in deals if d["category"] == "crypto"], True),
           ("E", [d for d in deals if d["category"] in ("bank", "ucard")], True),
           ("F", [d for d in deals if d["category"] == "vps"], True),
           ("G", expiring, True)]
    out = [T["title"].format(t=t.astimezone().strftime("%Y-%m-%d %H:%M")),
           T["stats"].format(a=len(deals), n=len(new), e=len(expiring), u=sum(not d["verified"] for d in deals),
                             c=sum(bool(d.get("claimed")) for d in deals))]
    pending = [d for d in deals if status(d, t) == "pending"]
    if pending:
        L = LABELS[lang]
        out += ["", T["pending"].format(n=len(pending)), "", T["pending_hint"]]
        for r in HOLD_REASONS:
            grp = sorted([d for d in pending if d["hold"]["reason"] == r], key=sort_key)
            if grp:
                out += ["", f"**{L['h_' + r]}**"] + [
                    f"- [{L[d['category']]}] {d['title']} — {d['hold']['url']}"
                    + (f" · {T['deadline']} {fmt_time(d.get('deadline'), T)}" if d.get("deadline") else "")
                    + (f" · {T['stopped_at']}: {d['hold']['note']}" if d["hold"]["note"] else "") for d in grp]
    for key, rows, resort in sec:  # B is already ordered by value / B 已按价值排好
        if rows:
            rows = sorted(rows, key=sort_key) if resort else rows
            out += ["", "## " + T[key], ""] + [line(d, lang) + "\n" for d in rows[:15]]
    risk = [d for d in live if d["category"] == "risk"]
    if risk:
        out += ["", T["risk"], ""] + [line(d, lang) + "\n" for d in risk]
    out += ["", T["H"].format(n=sum(status(d, t) == "archived" for d in db.values()))]
    print("\n".join(out))


def cmd_dashboard(a, db, cfg):
    lang = a.lang or "zh"  # board opens in Chinese; it has a 中文/EN toggle / 看板默认中文，可一键切换
    t = now()
    items = [dict(d, status=status(d, t)) for d in db.values()]
    data = {"lang": lang, "generated": iso(t), "labels": LABELS, "items": items}
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard.html"), encoding="utf-8").read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")  # safe inside <script>
    out = os.path.expanduser(a.out or os.path.join(HOME, "dashboard.html"))
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(tpl.replace("/*DATA*/{}", payload, 1))
    print(json.dumps({"dashboard": out, "items": len(items)}, ensure_ascii=False))


def cmd_config(a, cfg):
    if not os.path.exists(CFG) and not a.set:
        print(json.dumps({"configured": False, "defaults": DEFAULT_CFG, "path": CFG}, ensure_ascii=False, indent=1))
        return
    for kv in a.set or []:
        k, _, v = kv.partition("=")
        if k not in DEFAULT_CFG:
            raise SystemExit(f"Unknown setting / 未知配置项 {k}: {list(DEFAULT_CFG)}")
        if k == "auto_claim" and v not in ("off", "free_only", "ask"):
            raise SystemExit("auto_claim: off | free_only | ask")
        if k == "lang" and v not in ("zh", "en"):
            raise SystemExit("lang: zh | en")
        cfg[k] = [x.strip() for x in v.split(",") if x.strip()] if isinstance(DEFAULT_CFG[k], list) else v
    if a.set:
        save(CFG, cfg)
    print(json.dumps({"configured": True, **cfg, "path": CFG}, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description="Deal ledger / 羊毛账本", formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("config")
    p.add_argument("--set", nargs="*", metavar="KEY=VALUE")
    sub.add_parser("add", description=FIELDS_HELP, formatter_class=argparse.RawDescriptionHelpFormatter)
    p = sub.add_parser("list")
    p.add_argument("--category", choices=CATEGORIES)
    p.add_argument("--status", default="active", choices=["active", "expiring", "pending", "archived", "claimed", "all"])
    p.add_argument("--claimable", action="store_true")
    p.add_argument("--brief", action="store_true")
    p = sub.add_parser("claim")
    p.add_argument("id")
    p.add_argument("--result", required=True)
    p.add_argument("--failed", action="store_true")
    p = sub.add_parser("hold", help="park an item for the user / 放进待你处理")
    p.add_argument("id")
    p.add_argument("--reason", required=True, choices=HOLD_REASONS)
    p.add_argument("--note", help="where it stopped / 停在哪一步")
    p.add_argument("--url", help="page to resume from / 从哪个页面继续")
    p = sub.add_parser("archive")
    p.add_argument("id")
    p = sub.add_parser("digest")
    p.add_argument("--days", type=float, default=1)
    p.add_argument("--lang", choices=["zh", "en"], help="default: config lang / 默认取配置")
    p = sub.add_parser("dashboard", help="write the HTML board / 生成看板")
    p.add_argument("--lang", choices=["zh", "en"])
    p.add_argument("--out", help="output path / 输出路径")
    a = ap.parse_args()

    cfg = {**DEFAULT_CFG, **load(CFG, {})}
    if a.cmd == "config":
        return cmd_config(a, cfg)
    db = load(DB, {})
    changed = auto_archive(db) > 0
    if a.cmd == "add":
        cmd_add(a, db); changed = True
    elif a.cmd == "list":
        cmd_list(a, db, cfg)
    elif a.cmd == "claim":
        cmd_claim(a, db); changed = True
    elif a.cmd == "hold":
        cmd_hold(a, db); changed = True
    elif a.cmd == "archive":
        d = db.get(a.id) or sys.exit(f"No such id / 没有这个 id: {a.id}")
        d.update(archived=True, archived_at=iso(now()), archived_why="manual")
        changed = True
        print(json.dumps({"id": a.id, "archived": True}))
    elif a.cmd == "digest":
        cmd_digest(a, db, cfg)
    elif a.cmd == "dashboard":
        cmd_dashboard(a, db, cfg)
    if changed:
        save(DB, db)


if __name__ == "__main__":
    main()

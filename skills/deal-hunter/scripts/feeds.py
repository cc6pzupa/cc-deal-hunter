#!/usr/bin/env python3
"""Read RSS / Atom feeds as JSON / 读 RSS、Atom 源. Stdlib only.

  feeds.py URL [URL ...] [--limit 20] [--days 7]
"""
import argparse
import datetime as dt
import email.utils
import json
import re
import urllib.request
import xml.etree.ElementTree as ET

UA = "deal-hunter-skill/1.0"
ATOM = "{http://www.w3.org/2005/Atom}"


def when(s):
    if not s:
        return None
    try:
        return email.utils.parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            return dt.datetime.fromisoformat(s.strip().replace("Z", "+00:00"))
        except ValueError:
            return None


def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()[:800]


def read(url, limit, since):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/atom+xml, */*"})
    with urllib.request.urlopen(req, timeout=20) as r:
        root = ET.fromstring(r.read())
    out = []
    for it in root.iter("item"):  # RSS
        out.append({"title": strip(it.findtext("title")), "url": (it.findtext("link") or "").strip(),
                    "summary": strip(it.findtext("description")), "published": it.findtext("pubDate")})
    for it in root.iter(ATOM + "entry"):  # Atom
        link = next((l.get("href") for l in it.findall(ATOM + "link") if l.get("rel") in (None, "alternate")), "")
        out.append({"title": strip(it.findtext(ATOM + "title")), "url": link,
                    "summary": strip(it.findtext(ATOM + "summary") or it.findtext(ATOM + "content")),
                    "published": it.findtext(ATOM + "published") or it.findtext(ATOM + "updated")})
    for o in out:
        t = when(o["published"])
        o["published"] = t.isoformat() if t else None
        o["_t"] = t
    out = [o for o in out if not since or not o["_t"] or o["_t"] >= since]
    for o in out:
        del o["_t"]
    return out[:limit]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--days", type=float, default=7)
    a = ap.parse_args()
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days) if a.days else None
    res = {}
    for u in a.urls:
        try:
            res[u] = read(u, a.limit, since)
        except Exception as e:  # one bad feed must not break the others / 一个源坏了不影响其他源
            res[u] = {"error": f"{type(e).__name__}: {e}"}
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

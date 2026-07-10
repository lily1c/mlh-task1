"""
writing.py — pulls articles from Substack and Medium via their public RSS feeds,
merges them, sorts newest-first, and caches the result so page loads stay fast.

Usage in app.py:
    from writing import get_articles
    articles = get_articles()   # list of dicts, newest first
"""

import re
import time
import html
from datetime import datetime, timezone

import feedparser

# ---- Configure your feeds here ---------------------------------------------
# Substack:  https://<yourname>.substack.com/feed
# Medium:    https://medium.com/feed/@<yourhandle>
FEEDS = [
    {"source": "Substack", "url": "https://aabasova.substack.com/feed"},
    {"source": "Medium",   "url": "https://medium.com/@assolabasova"},
]

# Cache so we don't hit the network on every request.
_CACHE = {"data": None, "ts": 0.0}
_CACHE_TTL = 60 * 30  # 30 minutes


def _strip_html(raw: str) -> str:
    """Turn an HTML summary into a short plain-text preview."""
    if not raw:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw)      # drop tags
    text = html.unescape(text)               # decode &amp; etc.
    text = re.sub(r"\s+", " ", text).strip()  # collapse whitespace
    return text


def _first_image(entry) -> str | None:
    """Best-effort cover image: media content, enclosure, or first <img> in body."""
    media = entry.get("media_content") or entry.get("media_thumbnail")
    if media and isinstance(media, list) and media[0].get("url"):
        return media[0]["url"]
    for enc in entry.get("enclosures", []) or []:
        if str(enc.get("type", "")).startswith("image"):
            return enc.get("href") or enc.get("url")
    body = ""
    if entry.get("content"):
        body = entry["content"][0].get("value", "")
    body = body or entry.get("summary", "")
    m = re.search(r'<img[^>]+src="([^"]+)"', body)
    return m.group(1) if m else None


def _parse_date(entry):
    """Return a timezone-aware datetime, or epoch if missing."""
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            return datetime.fromtimestamp(time.mktime(t), tz=timezone.utc)
    return datetime.fromtimestamp(0, tz=timezone.utc)


def _fetch_one(feed_cfg, max_items=8):
    out = []
    parsed = feedparser.parse(feed_cfg["url"])
    for entry in parsed.entries[:max_items]:
        preview = _strip_html(entry.get("summary", ""))
        if len(preview) > 180:
            preview = preview[:177].rstrip() + "…"
        dt = _parse_date(entry)
        out.append({
            "title": entry.get("title", "Untitled").strip(),
            "url": entry.get("link", "#"),
            "source": feed_cfg["source"],
            "preview": preview,
            "image": _first_image(entry),
            "date": dt,
            "date_display": dt.strftime("%b %d, %Y"),
        })
    return out


def get_articles(force=False):
    """Merged, newest-first list of articles across all feeds. Cached."""
    now = time.time()
    if not force and _CACHE["data"] is not None and (now - _CACHE["ts"]) < _CACHE_TTL:
        return _CACHE["data"]

    articles = []
    for cfg in FEEDS:
        try:
            articles.extend(_fetch_one(cfg))
        except Exception as e:
            # A single dead feed shouldn't blank the whole page.
            print(f"[writing] failed to fetch {cfg['url']}: {e}")

    articles.sort(key=lambda a: a["date"], reverse=True)
    _CACHE["data"] = articles
    _CACHE["ts"] = now
    return articles


if __name__ == "__main__":
    # Quick manual test against a known-good public Medium feed.
    import sys
    test_url = sys.argv[1] if len(sys.argv) > 1 else "https://medium.com/feed/@medium"
    print(f"Testing parse against: {test_url}\n")
    data = _fetch_one({"source": "Medium", "url": test_url}, max_items=3)
    for a in data:
        print(f"  • [{a['source']}] {a['title']}")
        print(f"    {a['date_display']}  |  img: {'yes' if a['image'] else 'no'}")
        print(f"    {a['preview'][:90]}...")
        print()
    print(f"Parsed {len(data)} items OK." if data else "No items parsed.")

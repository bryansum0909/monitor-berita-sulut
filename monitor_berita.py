#!/usr/bin/env python3
"""
Bot Monitor Berita Viral Manado/Sulut -> Telegram
==================================================
Script ini menarik berita dari Google News RSS dan beberapa portal berita
nasional, memfilter berita yang berkaitan dengan Manado/Sulawesi Utara dan
mengirimkannya ke Telegram.

Dirancang untuk dijalankan periodik (mis. tiap 5 menit) via GitHub Actions
atau cron lokal.

Environment variables yang dibutuhkan:
    TELEGRAM_BOT_TOKEN   - Token bot dari @BotFather
    TELEGRAM_CHAT_ID     - Chat ID tujuan (chat pribadi, group, atau channel)

Optional:
    LOOKBACK_HOURS       - Hanya kirim berita yang dipublish dalam X jam
                           terakhir (default: 6)
    MAX_NEWS_PER_RUN     - Batas maksimum berita yang dikirim per run
                           (default: 15)
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote_plus

import feedparser
import requests

# ---------------------------------------------------------------------------
# KONFIGURASI
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
STATE_PATH = ROOT / "state.json"

DEFAULT_LOOKBACK_HOURS = int(os.getenv("LOOKBACK_HOURS", "6"))
DEFAULT_MAX_PER_RUN = int(os.getenv("MAX_NEWS_PER_RUN", "15"))

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# UTIL
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    """Print dengan timestamp."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"WARN gagal baca {path.name}: {e}")
        return default


def save_json(path: Path, data) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clean_text(text: str) -> str:
    """Buang tag HTML & spasi berlebih."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def make_id(url: str) -> str:
    """Hash URL jadi ID pendek untuk state."""
    return hashlib.md5(url.encode("utf-8")).hexdigest()[:16]


def parse_date(entry) -> datetime | None:
    """Ambil tanggal publish dari entri RSS, return UTC datetime."""
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


# ---------------------------------------------------------------------------
# SUMBER BERITA
# ---------------------------------------------------------------------------

def build_google_news_url(query: str, lang: str = "id", country: str = "ID") -> str:
    """Bikin URL RSS Google News untuk query tertentu."""
    q = quote_plus(query)
    return f"https://news.google.com/rss/search?q={q}&hl={lang}&gl={country}&ceid={country}:{lang}"


def default_config() -> dict:
    """Konfigurasi default jika config.json belum ada."""
    return {
        # Kata kunci yang harus muncul di judul/ringkasan agar berita dipilih.
        # Bersifat OR (cukup salah satu cocok).
        "keywords": [
            "manado",
            "sulut",
            "sulawesi utara",
            "minahasa",
            "bitung",
            "tomohon",
            "kotamobagu",
            "bolaang mongondow",
            "sangihe",
            "talaud",
            "siau",
            "kawanua",
        ],
        # Kata kunci penanda berita "viral/trending" untuk diberi tanda khusus.
        "viral_markers": [
            "viral", "heboh", "trending", "geger", "ramai", "diserbu",
            "trending topic", "netizen", "media sosial", "viral di",
        ],
        # Query Google News (paling reliable). Tiap query = 1 feed terpisah.
        "google_news_queries": [
            "Manado",
            "Sulawesi Utara",
            "viral Manado",
            "viral Sulut",
            "berita Minahasa",
            "Bitung",
            "Tomohon",
            "Kawanua",
        ],
        # Feed RSS langsung dari portal Indonesia (akan difilter via keyword).
        "rss_feeds": [
            "https://www.antaranews.com/rss/top-news",
            "https://news.detik.com/berita/rss",
            "https://feed.liputan6.com/rss/news",
            "https://www.cnnindonesia.com/nasional/rss",
            "https://www.cnbcindonesia.com/news/rss",
            "https://rss.tempo.co/nasional",
            "https://www.suara.com/rss/news",
            "https://www.jawapos.com/nasional/rss",
        ],
    }


def ensure_config() -> dict:
    if not CONFIG_PATH.exists():
        cfg = default_config()
        save_json(CONFIG_PATH, cfg)
        log(f"config.json dibuat di {CONFIG_PATH}")
        return cfg
    return load_json(CONFIG_PATH, default_config())


# ---------------------------------------------------------------------------
# AMBIL & FILTER
# ---------------------------------------------------------------------------

def fetch_feed(url: str, timeout: int = 15):
    """Ambil feed dengan custom user-agent (beberapa portal block default UA)."""
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
        return feedparser.parse(resp.content)
    except Exception as e:
        log(f"  ! gagal fetch {url[:60]}...: {e}")
        return None


def matches_keywords(text: str, keywords: list[str]) -> bool:
    t = text.lower()
    return any(k.lower() in t for k in keywords)


def is_viral(text: str, markers: list[str]) -> bool:
    t = text.lower()
    return any(m.lower() in t for m in markers)


def collect_news(config: dict, lookback_hours: int) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
    keywords = config.get("keywords", [])
    viral_markers = config.get("viral_markers", [])
    seen_urls: set[str] = set()
    items: list[dict] = []

    feeds: list[tuple[str, str]] = []  # (label, url)
    for q in config.get("google_news_queries", []):
        feeds.append((f"GoogleNews: {q}", build_google_news_url(q)))
    for url in config.get("rss_feeds", []):
        feeds.append(("RSS", url))
    # Feed kustom user (kalau ditambahkan di config)
    for url in config.get("custom_rss_feeds", []):
        feeds.append(("Custom", url))

    log(f"Mengambil {len(feeds)} feed...")
    for label, url in feeds:
        parsed = fetch_feed(url)
        if not parsed:
            continue
        n_match = 0
        for entry in parsed.entries[:50]:  # cap per feed
            link = entry.get("link", "")
            if not link or link in seen_urls:
                continue
            title = clean_text(entry.get("title", ""))
            summary = clean_text(entry.get("summary", entry.get("description", "")))
            text = f"{title} {summary}"

            # Untuk Google News query, sudah include keyword.
            # Untuk RSS portal nasional, harus difilter via keyword Sulut.
            if label == "RSS" and not matches_keywords(text, keywords):
                continue
            if label == "Custom" and keywords and not matches_keywords(text, keywords):
                # untuk custom feed, kalau ada keyword filter terapkan
                pass  # biarkan lewat agar fleksibel

            pub = parse_date(entry)
            if pub and pub < cutoff:
                continue

            seen_urls.add(link)
            items.append({
                "id": make_id(link),
                "title": title,
                "summary": summary[:300],
                "link": link,
                "source": (entry.get("source", {}) or {}).get("title")
                          or label.replace("GoogleNews: ", ""),
                "published": pub.isoformat() if pub else None,
                "viral": is_viral(text, viral_markers),
            })
            n_match += 1
        log(f"  {label[:50]}: {n_match} cocok dari {len(parsed.entries)} entri")

    # Sort: viral dulu, lalu berdasarkan tanggal terbaru
    items.sort(key=lambda x: (not x["viral"], x["published"] or ""), reverse=False)
    items.sort(key=lambda x: (x["published"] or ""), reverse=True)
    items.sort(key=lambda x: not x["viral"])  # viral di atas
    return items


# ---------------------------------------------------------------------------
# TELEGRAM
# ---------------------------------------------------------------------------

def tg_escape(text: str) -> str:
    """Escape karakter HTML untuk Telegram parse_mode=HTML."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def format_message(item: dict) -> str:
    flag = "🔥 <b>VIRAL</b>\n" if item["viral"] else ""
    source = tg_escape(item.get("source") or "")
    title = tg_escape(item["title"])
    summary = tg_escape(item["summary"])
    link = item["link"]
    pub = ""
    if item.get("published"):
        try:
            dt = datetime.fromisoformat(item["published"])
            # konversi ke WITA (UTC+8)
            dt_local = dt.astimezone(timezone(timedelta(hours=8)))
            pub = f"\n🕒 {dt_local.strftime('%d %b %Y %H:%M')} WITA"
        except Exception:
            pass
    msg = (
        f"{flag}📰 <b>{title}</b>\n"
        f"{summary}\n\n"
        f"📌 <i>{source}</i>{pub}\n"
        f'<a href="{link}">Baca selengkapnya →</a>'
    )
    return msg


def send_telegram(token: str, chat_id: str, message: str) -> bool:
    url = TELEGRAM_API.format(token=token)
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        if r.status_code == 200:
            return True
        log(f"  ! Telegram error {r.status_code}: {r.text[:200]}")
        # rate limit: tunggu kalau 429
        if r.status_code == 429:
            try:
                retry = r.json().get("parameters", {}).get("retry_after", 5)
                time.sleep(int(retry) + 1)
            except Exception:
                time.sleep(5)
        return False
    except Exception as e:
        log(f"  ! Gagal kirim telegram: {e}")
        return False


# ---------------------------------------------------------------------------
# STATE (dedup history)
# ---------------------------------------------------------------------------

def load_state() -> dict:
    state = load_json(STATE_PATH, {"sent_ids": [], "last_run": None})
    # Pastikan struktur valid
    if "sent_ids" not in state:
        state["sent_ids"] = []
    return state


def save_state(state: dict, keep_last: int = 2000) -> None:
    # Batasi ukuran agar file tidak balon
    state["sent_ids"] = state["sent_ids"][-keep_last:]
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    save_json(STATE_PATH, state)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> int:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        log("ERROR: TELEGRAM_BOT_TOKEN dan TELEGRAM_CHAT_ID belum di-set.")
        log("Set environment variable dulu (lihat README.md).")
        return 1

    config = ensure_config()
    state = load_state()
    sent_set = set(state["sent_ids"])

    items = collect_news(config, DEFAULT_LOOKBACK_HOURS)
    log(f"Total kandidat berita: {len(items)}")

    new_items = [i for i in items if i["id"] not in sent_set]
    log(f"Berita baru (belum dikirim): {len(new_items)}")

    if not new_items:
        log("Tidak ada berita baru. Selesai.")
        save_state(state)
        return 0

    # Batasi jumlah per run agar tidak spam
    to_send = new_items[:DEFAULT_MAX_PER_RUN]
    sent = 0
    for item in to_send:
        msg = format_message(item)
        if send_telegram(token, chat_id, msg):
            state["sent_ids"].append(item["id"])
            sent += 1
            log(f"  ✓ Terkirim: {item['title'][:60]}")
            time.sleep(1.5)  # hindari rate limit Telegram
        else:
            log(f"  ✗ Gagal: {item['title'][:60]}")

    log(f"Selesai. {sent}/{len(to_send)} berita terkirim.")
    save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())

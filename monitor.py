#!/usr/bin/env python3
"""
page-change-monitor — watch web pages, get a Telegram ping when they change.

Tracks full pages or a single CSS selector (e.g. a price element).
State is kept in state.json so only *new* changes alert.

Setup:
    cp config.example.py config.py   # token, chat id, and your JOBS list
    pip install -r requirements.txt
    python monitor.py                # once, or on cron / systemd timer
"""
import hashlib
import json
import os
import re

import requests
from bs4 import BeautifulSoup

import config

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; page-change-monitor/1.0)"}


def send_telegram(text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(config.TELEGRAM_BOT_TOKEN)
    requests.post(
        url,
        json={"chat_id": config.TELEGRAM_CHAT_ID, "text": text},
        timeout=15,
    )


def fetch_text(url, selector=None):
    html = requests.get(url, headers=HEADERS, timeout=20).text
    if selector:
        el = BeautifulSoup(html, "html.parser").select_one(selector)
        return el.get_text(" ", strip=True) if el else ""
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def main():
    state = json.load(open(STATE_FILE)) if os.path.exists(STATE_FILE) else {}
    for job in config.JOBS:
        try:
            digest = hashlib.sha256(
                fetch_text(job["url"], job.get("selector")).encode()
            ).hexdigest()
        except Exception as exc:
            print("[warn] {}: {}".format(job["name"], exc))
            continue
        if state.get(job["name"]) and state[job["name"]] != digest:
            send_telegram("Change detected: {}\n{}".format(job["name"], job["url"]))
            print("[alert] {} changed".format(job["name"]))
        state[job["name"]] = digest
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print("checked {} job(s)".format(len(config.JOBS)))


if __name__ == "__main__":
    main()

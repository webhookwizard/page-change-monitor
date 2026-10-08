# 👀 page-change-monitor

> Watch any web page. Get a Telegram ping the second it changes. **Zero paid APIs.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/alerts-Telegram-26A5E4.svg)](https://telegram.org/)

## ✨ What it does

- 🌐 Tracks whole pages — or a single CSS selector (e.g. `.price`)
- 🔔 Telegram alert with page name + URL on every change
- 💾 Remembers state in `state.json`, so only *new* changes alert
- ⏰ Built for cron / systemd timers

## 🖥 Demo

```bash
$ python monitor.py
checked 2 job(s)

# ...when the watched element moves:
Telegram:  Change detected: gadget-price
           https://shop.example/item/42
```

## 🚀 Quick start

```bash
cp config.example.py config.py   # ← token, chat id, JOBS list
pip install -r requirements.txt
python monitor.py
```

`config.py`:

```python
JOBS = [
    {"name": "example", "url": "https://example.com"},
    {"name": "gadget-price",
     "url": "https://shop.example/item/42",
     "selector": ".price"},
]
```

## 💰 Running costs

$0 — Telegram Bot API is free. One run = one polite request per job (identifiable User-Agent).

## 🛠 Stack

Python · `requests` · BeautifulSoup · Telegram Bot API

---

### 📬 Want it customized?

Email alerts, screenshots on change, JS-rendered pages, multi-user routing — I build these to order.
**DM [@WebhookWizard](https://x.com/WebhookWizard)** · 50% deposit, settled in USDT.

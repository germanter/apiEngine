# 🚀 API Engine

**A minimal, automated engine that collects, validates, and serves public API data — all in one clean JSON.**

---

## SHORT CUT API LIST URLS
api.json: 
```
https://raw.githubusercontent.com/germanter/apiEngine/refs/heads/main/api.json
```

apiCmp.json:
```
https://raw.githubusercontent.com/germanter/apiEngine/refs/heads/main/apiCmp.json
```

API-Engine site:
```
https://api-engine.vercel.app/
```

## 📌 Overview

**API Engine** is an open-source project built to solve a simple but real problem:

> There is **no fast, clean, and reliable way** to explore modern public APIs in one place.

So this project does exactly that — it **collects**, **validates**, and **serves** API data in a structured format that works for both **humans 👤** and **machines 🤖**.

---

## 🧠 Core Idea

Instead of scattered API lists across blogs, outdated repos, or broken links:

* ✅ You get a **single source of truth**
* ✅ Automatically validated endpoints
* ✅ Continuously updated dataset
* ✅ Dual-format JSON optimized for different use cases

---

## 📦 Data Outputs

### 👤 `api.json` — Human-Friendly

Readable, structured, and descriptive.

```
https://raw.githubusercontent.com/germanter/apiEngine/refs/heads/main/api.json
```

---

### 🤖 `apiCmp.json` — Machine-Optimized

Compressed version of `api.json` for automation and performance.

```
https://raw.githubusercontent.com/germanter/apiEngine/refs/heads/main/apiCmp.json
```

* ~**60KB → 20KB**
* ~**3x smaller**
* Ideal for frontend apps, bots, and fast parsing

---

### 📥 `incoming.json` — Staging Layer

Temporary dataset before validation pipeline.

* Holds freshly scraped data
* Prevents bad data from reaching production

---

## ⚙️ Tech Stack

* **Python**

  * `httpx` → async requests / endpoint validation
  * `playwright` → scraping dynamic content
* **JSON** → data storage & serving
* **GitHub Actions** → automation (cron jobs)

---

## 🔄 Data Pipeline

The entire system is **fully automated**:

```
Scraper → Initial Validation → incoming.json
        → Deep Validation → api.json
        → URL Ping Check (async)
        → Compression → apiCmp.json
        → GitHub Actions → Daily Run
```

Or visually:

```
[Scrape]
   ↓
[Validate (basic)]
   ↓
[incoming.json]
   ↓
[Validate (strict)]
   ↓
[api.json]
   ↓
[Ping URLs]
   ↓
[Compress]
   ↓
[apiCmp.json]
```

---

## 🧪 Validation System

### ✅ Multi-Layer Protection

The engine prevents bad data from corrupting the dataset:

* **Basic validation**

  * JSON structure checks
  * Required fields
* **Mid-level validation**

  * Duplicate detection
  * Invalid payload filtering
* **Strict validation**

  * Ensures compatibility with `api.json`

---

## 🌐 Endpoint Status System

Every API URL is checked using an **async pinger**.

### Status Values:

| Status    | Meaning                         |
| --------- | ------------------------------- |
| `ALIVE`   | Endpoint responded successfully |
| `DEAD`    | Error response received         |
| `UNKNOWN` | Blocked or unreachable          |

---

### ⚠️ Real-World Notes

* Some APIs **block automated requests** → marked as `UNKNOWN`
* Some APIs return **error codes but still work in browser**
* The system avoids aggressive retries — no need to go rogue on 200+ endpoints

---

## 📊 Data Structure

### Standard Format (`api.json`)

```json
{
    "name": "OpenAI API",
    "desc": "Text, image, speech, embeddings models via REST API",
    "url": "https://platform.openai.com/docs/api-reference",
    "cost": "freemium",
    "auth": true,
    "category": "AI",
    "status": "ALIVE"
}
```

---

### Field Explanation

| Field      | Description                       |
| ---------- | --------------------------------- |
| `name`     | API name                          |
| `desc`     | Short description                 |
| `url`      | Documentation / endpoint          |
| `cost`     | Pricing model                     |
| `auth`     | `true` → requires API key / OAuth |
| `category` | API category                      |
| `status`   | Health status from pinger         |

---

## ⚡ Compressed Format (`apiCmp.json`)

Designed for **speed and minimal payload size**.

```json
{
    "n": "OpenAI API",
    "d": "Text, image, speech, embeddings models via REST API",
    "u": "https://platform.openai.com/docs/api-reference",
    "m": "freemium",
    "a": true,
    "c": "AI",
    "s": 1
}
```

---

### Compression Mapping

| Short | Full     | Description   |
| ----- | -------- | ------------- |
| `n`   | name     | API name      |
| `d`   | desc     | Description   |
| `u`   | url      | Endpoint      |
| `m`   | cost     | Pricing       |
| `a`   | auth     | Auth required |
| `c`   | category | Category      |
| `s`   | status   | 1 / 0 / -1    |

---

### Status Encoding

| Value | Meaning |
| ----- | ------- |
| `1`   | ALIVE   |
| `0`   | DEAD    |
| `-1`  | UNKNOWN |

---

### 📌 Special Note

`apiCmp.json` always includes:

* A **final item (`x`)**
* Contains **distinct category list**
* Useful for frontend filtering

---

## 🤖 Automation

Everything runs through a single orchestrator:

### `runner.py`

Handles:

* Scraping
* Validation
* Pinging
* Compression
* Final output generation

---

### ⏱ GitHub Actions

* Runs on **cron schedule (daily)**
* Fully autonomous pipeline
* Zero manual intervention required

---

## 🛡️ Incident Report — Apr 14, 8:09 AM (GMT+4)

> First real failure of the automated system.

* Scraper failed due to a bad data entry
* **BUT:**

  * `incoming.json` → safe
  * `api.json` → untouched

### 💡 Key Insight

> Validation layers successfully prevented dataset corruption.

This proved that:

* The system is **resilient**
* Bad data **cannot poison production JSON**
* Failures are **contained and recoverable**

---

## 🌍 Live Preview

* 🔗 **API Engine Website**
  https://api-engine.vercel.app/

---

## 🎯 Use Cases

* 🔍 Discover APIs quickly
* ⚡ Build tools needing API datasets
* 🤖 Feed bots / automation systems
* 📊 Frontend filtering via categories
* 🧪 Testing API availability

---

## 🚧 Limitations

* Some endpoints block automated requests
* Some APIs return misleading status codes
* Not all APIs guarantee long-term stability

---

## 🧩 Philosophy

This project is intentionally:

* **Simple**
* **Fast**
* **Practical**

No over-engineering. No unnecessary complexity.

Just:

> **Clean data. Reliable pipeline. Useful output.**

---

## 🤝 Contributing

Contributions are welcome — especially:

* Adding new APIs
* Improving validation logic
* Enhancing scraper reliability

---

## 📄 License

MIT License — use it freely.

---

## 💬 Final Words

This project started from a simple frustration — and turned into a **fully automated API discovery engine**.

If you’ve ever struggled to find reliable APIs…

**This is built for you.**

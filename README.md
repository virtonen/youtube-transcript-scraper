# YouTube Transcript Scraper

## Download All YouTube Channel Transcripts in One Click

A simple, **API-key–only** Python script that downloads every available transcript from a single YouTube channel and combines them into one text file for downstream NLP, search, or archival.

> **Author**: Vladislav Virtonen
> **Year**: 2025

---

## ✨ Features

| Feature                  | Details                                                 |
| ------------------------ | ------------------------------------------------------- |
| **No OAuth**             | Works with a lightweight YouTube Data API v3 key.       |
| **Channel-wide**         | Iterates through **all** public videos on a channel.    |
| **Titles included**      | Each transcript section is headed with the video title. |
| **Plain text output**    | Easy to index, grep, or feed into LLMs.                 |
| **Minimal dependencies** | Only two pip installs.                                  |

---

Need every caption or subtitle from a YouTube channel **without copying them one by one**?  
This tool automates the entire process: point it at any channel, and it downloads **all available transcripts at once**—manual or auto-generated—ready for NLP, archives, or personal study.
---

## 📂 Repository Contents

```
├── youtube_transcript_downloader.py   # Main script (fully documented)
└── README.md                          # You are here
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/<yourusername>/youtube-transcript-scraper.git
cd youtube-transcript-scraper
pip install -r requirements.txt  # or see “Dependencies” below
python youtube_transcript_downloader.py
```

After the script finishes you will find:

```
all_transcripts.txt
```

Each section looks like:

```
========== [Title] ==========

[transcript] ...
```

---

## 🔑 Prerequisites

| Item                        | Notes                                  |
| --------------------------- | -------------------------------------- |
| **Python ≥ 3.8**            | Tested on 3.8–3.12                     |
| **YouTube Data API v3 key** | Free in Google Cloud Console           |
| **Channel ID**              | Begins with **UC**… (see next section) |

### 1 · Obtain an API Key

1. Open **Google Cloud Console** → `APIs & Services` → **New Project**.
2. In *API Library*, enable **YouTube Data API v3**.
3. Go to *Credentials* → **Create Credentials** → **API Key**.
4. (Optional) Restrict it to “YouTube Data API v3” only.

### 2 · Find the Channel ID

Method A – Fast Online
: Paste `https://www.youtube.com/@channel` into any online “YouTube Channel ID Finder”.

Method B – Manual (no third-party tools)

1. Open the channel page in Chrome/Firefox.
2. **Right-click → View Page Source**.
3. Press **`Ctrl/Cmd + F`** and search for

   ```
   "channelId":
   ```
4. Copy the value that looks like `UCxxxxxxxxxxxxxxxxxxxxxx`.

---

## ⚙️ Configuration & Execution

Open `youtube_transcript_downloader.py` and fill in:

```python
API_KEY   = "YOUR_API_KEY_HERE"
CHANNEL_ID = "UCxxxxxxxxxxxxxxxxxxxxxx"
```

Then run:

```bash
python youtube_transcript_downloader.py
```

The script will:

1. List every video on the channel (50 per page, auto-paginated).
2. Fetch the transcript (manual or auto-generated) via **youtube-transcript-api**.
3. Write them to `all_transcripts.txt`, with clear title headers.

---

## 🪄 Dependencies

```bash
pip install google-api-python-client youtube-transcript-api
```

*(Alternatively use `pip install -r requirements.txt` if you add one.)*

---

## 😎 Contributing / Forking

Feel free to fork and PR:

* Add JSON/CSV export
* Push transcripts to Google Drive or S3
* Rate-limit handling for very large channels
* Language fallback chains

---

## 📜 License

MIT License – see `LICENSE` if added.

---

## 🙏 Acknowledgements

* **google-api-python-client** – official YouTube Data API wrapper.
* **youtube-transcript-api** – elegant caption fetcher by @jdepoix.

Happy scraping! 🎬📝

[![downloads transcripts](https://img.shields.io/badge/YouTube-Transcript_Downloader-blue)](#)


#!/usr/bin/env python3
"""
youtube_transcript_downloader.py
--------------------------------
Download **all available transcripts** from a single YouTube channel,
then combine them into one text file with clear section headers that
show the video titles.

Requirements
------------
pip install google-api-python-client youtube-transcript-api

Usage
-----
1. Create a Google Cloud project and enable “YouTube Data API v3”.
2. Generate an **API key** (no OAuth needed) and paste it below.
3. Paste the **channel ID** (begins with “UC…”) for the channel you want.
4. Run:  python youtube_transcript_downloader.py
   – A file called ``all_transcripts.txt`` will be created in the same folder.

Notes
-----
* Only videos with transcripts (manual or auto-generated) are included.
* Each transcript is stored under a header like:
      ========== [Title] ==========
* API quota usage: ~100 units per 100 videos.
"""

from __future__ import annotations

from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List, Optional

# ---------------------------------------------------------------------------
# 🔧 User-supplied settings – **EDIT THESE TWO LINES** before running
# ---------------------------------------------------------------------------
API_KEY: str = ""          # ← paste your YouTube Data API v3 key here
CHANNEL_ID: str = ""       # ← paste the “UC…” channel ID here
# ---------------------------------------------------------------------------


# Create a YouTube API client using the simple API-key flow
youtube = build("youtube", "v3", developerKey=API_KEY)


def get_all_video_ids(channel_id: str) -> List[str]:
    """
    Return a list of every video ID published by the given channel.

    Parameters
    ----------
    channel_id : str
        YouTube channel ID (starts with “UC…”).

    Returns
    -------
    List[str]
        Video IDs in newest-first order.
    """
    video_ids: List[str] = []
    next_page: Optional[str] = None

    while True:
        resp = (
            youtube.search()
            .list(
                channelId=channel_id,
                part="id",
                order="date",
                maxResults=50,        # API maximum per page
                pageToken=next_page,
            )
            .execute()
        )

        # Filter only “youtube#video” (skip playlists, etc.)
        video_ids.extend(
            item["id"]["videoId"]
            for item in resp["items"]
            if item["id"]["kind"] == "youtube#video"
        )

        next_page = resp.get("nextPageToken")
        if not next_page:  # reached last page
            break

    return video_ids


def get_video_title(video_id: str) -> str:
    """
    Fetch the human-readable title for a single video.

    Returns a fallback string if the API fails (rare).
    """
    try:
        response = (
            youtube.videos()
            .list(part="snippet", id=video_id)
            .execute()
        )
        return response["items"][0]["snippet"]["title"]
    except Exception as err:
        print(f"[WARN] Could not get title for {video_id}: {err}")
        return f"Video ID: {video_id}"


def download_transcript(video_id: str, languages: List[str] | None = None) -> Optional[str]:
    """
    Download the transcript for one YouTube video.

    Parameters
    ----------
    video_id : str
        Video ID to fetch.
    languages : List[str] | None
        Preferred language codes.  Defaults to English only.

    Returns
    -------
    str | None
        Transcript text if available, else ``None``.
    """
    if languages is None:
        languages = ["en"]

    try:
        # This call works for both manual and auto-generated captions
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        return "\n".join(segment["text"] for segment in transcript)
    except Exception as err:
        print(f"[INFO] No transcript for {video_id}: {err}")
        return None


def main() -> None:
    """Orchestrate the download and file writing."""
    if not API_KEY or not CHANNEL_ID:
        raise ValueError("Please supply both API_KEY and CHANNEL_ID in the settings section.")

    video_ids = get_all_video_ids(CHANNEL_ID)
    print(f"Found {len(video_ids)} videos. Fetching transcripts...\n")

    with open("all_transcripts.txt", "w", encoding="utf-8") as outfile:
        for vid in video_ids:
            transcript_text = download_transcript(vid)
            if transcript_text:
                title = get_video_title(vid)
                header = f"\n\n========== {title} ==========\n\n"
                outfile.write(header)
                outfile.write(transcript_text)
                print(f"✅ Saved transcript for: {title}")
            else:
                print(f"❌ Skipped {vid} (no transcript)")

    print("\nFinished! Transcripts saved to all_transcripts.txt")


if __name__ == "__main__":
    main()

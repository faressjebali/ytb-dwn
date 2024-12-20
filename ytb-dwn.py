#!/usr/bin/env python3

"""
YouTube Music Downloader
Author: Fares jebali
Email: fjbeli39@gmail.com
Description: A CLI tool to download music from YouTube using yt-dlp.
"""

import os
import sys
import subprocess

try:
    import yt_dlp
except ImportError:
    print("yt_dlp not found. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

def youtube_search(query):
    """Search for a video on YouTube using yt-dlp."""
    ydl_opts = {
        'quiet': True,
        'default_search': 'ytsearch1',
        'simulate': True,
        'force_generic_extractor': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            return info['entries'][0]['webpage_url']
        return info['webpage_url']

def download_audio(video_url):
    music_folder = os.path.expanduser('~/Music')
    os.makedirs(music_folder, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(music_folder, '%(title)s.%(ext)s'),
        'extractaudio': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def main():
    print("Welcome to YouTube Music Downloader!")
    query = input("Enter a song name to download: ")
    video_url = youtube_search(query)
    if video_url:
        print(f"Downloading from: {video_url}")
        download_audio(video_url)
        print("Download completed!")

if __name__ == "__main__":
    main()

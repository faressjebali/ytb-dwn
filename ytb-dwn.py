#!/usr/bin/env python3

"""
YouTube Music Downloader
Author: Fares Jebali
Email: fjbeli39@gmail.com
Description: A CLI tool to download music from YouTube using yt-dlp.
"""

import os
import sys
import subprocess
import time

try:
    import yt_dlp
except ImportError:
    print("yt_dlp not found. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

def youtube_search(query):
    """Search for videos on YouTube using yt-dlp and return multiple results."""
    ydl_opts = {
        'quiet': True,  # Suppress output
        'no_warnings': True,  # Disable warnings
        'default_search': 'ytsearch10',  # Fetch top 10 results
        'simulate': True,
        'force_generic_extractor': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if 'entries' in info:
            results = []
            for entry in info['entries']:
                results.append({
                    'title': entry.get('title'),
                    'url': entry.get('webpage_url'),
                    'duration': entry.get('duration'),
                })
            return results
    return []

def display_results(results):
    """Display search results for the user."""
    print("\n--- Search Results ---")
    for i, result in enumerate(results, start=1):
        duration = result['duration']
        minutes = duration // 60 if duration else 0
        seconds = duration % 60 if duration else 0
        print(f"{i}. {result['title']} ({minutes:02}:{seconds:02}) - {result['url']}")

def download_audio(video_url):
    """Download audio from a YouTube URL."""
    music_folder = os.path.expanduser('~/Music')
    os.makedirs(music_folder, exist_ok=True)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(music_folder, '%(title)s.%(ext)s'),
        'extractaudio': True,
        'quiet': True,  # Suppress yt-dlp output
        'no_warnings': True,  # Suppress yt-dlp warnings
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def loading_bar(query):
    """Display a simple loading animation."""
    print(f'\nSearching for "{query}"', end="")
    for _ in range(3):
        time.sleep(0.5)  # Pause for half a second
        print(".", end="", flush=True)  # Print dots dynamically
    print("\nPlease wait...")

def main():
    print("Welcome to YouTube Music Downloader!")
    print("\nSelect an option:")
    print("1. Search for a song by name")
    print("2. Provide a YouTube URL for download")

    while True:
        try:
            choice = int(input("\nEnter your choice (1 or 2): ").strip())
            if choice not in [1, 2]:
                print("\nInvalid choice. Please enter 1 or 2.")
            else:
                break  # Break out of the loop if a valid choice is entered
        except ValueError:
            print("\nInvalid input. Please enter a number (1 or 2).")

    if choice == 1:
        # Search by song name
        query = input("\nEnter a song name to search: ").strip()
        loading_bar(query)
        results = youtube_search(query)
        
        if results:
            display_results(results)
            try:
                choice = int(input("\nEnter the number of the video to download (0 to cancel): ").strip())
                if choice == 0:
                    print("\nDownload canceled.")
                    return
                selected_video = results[choice - 1]
                print(f"\nDownloading: {selected_video['title']}")
                download_audio(selected_video['url'])
                print("\nDownload completed!")
            except (ValueError, IndexError):
                print("\nInvalid choice. Exiting.")
        else:
            print("\nNo results found. Please try again with a different search term.")

    elif choice == 2:
        # Download by URL
        video_url = input("\nEnter the YouTube URL of the song to download: ").strip()
        print(f"\nDownloading the song from {video_url}...")
        download_audio(video_url)
        print("\nDownload completed!")

    else:
        print("\nInvalid choice. Exiting.")

if __name__ == "__main__":
    main()


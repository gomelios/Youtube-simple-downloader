# 📥 YouTube Simple Downloader (GUI)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Active-green?style=for-the-badge)

A simple and efficient desktop application built with Python to download videos, music, and full playlists from YouTube and YouTube Music.


## 🚀 Features

* **User-Friendly Interface:** Built with `tkinter`, offering a clean GUI without the need for command-line usage.
* **Multiple Formats:**
    * 🎵 **MP3:** High-quality audio extraction with automatic conversion.
    * 🎬 **MP4:** Downloads the best available video and audio streams and merges them for high-definition output.
* **Full Support:** Handles single video links, YouTube Music albums, and entire Playlists.
* **Smart Downloads:**
    * **Progress Bar:** Real-time visual tracking of the download status.
    * **Skip Existing:** Automatically detects if a file already exists in the destination folder and skips it to save time and bandwidth.
    * **Resumable:** Attempts to resume interrupted downloads.
* **Multithreading:** The interface remains responsive and does not freeze while downloads are in progress.

## 🛠️ Tech Stack

* **Python 3.x**
* **Tkinter** (Native GUI Library)
* **yt-dlp** (Advanced command-line media downloader)
* **FFmpeg** (Multimedia framework for processing and conversion)

## 📋 Prerequisites

Before running the application, you **must** have FFmpeg installed on your system.

### Installing FFmpeg:
* **Windows:** Download the build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract it, and add the `bin` folder to your System PATH variables.
* **Linux:** `sudo apt install ffmpeg`
* **macOS:** `brew install ffmpeg`

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/gomelios/Youtube-simple-downloader
    cd Youtube-simple-downloader
    ```

2.  **Install dependencies:**
    ```bash
    pip install yt-dlp
    ```

## ▶️ How to Use

1.  Run the application script:
    ```bash
    python downloader.py
    ```

2.  **Paste the URL:** Supports Video, Playlist, or YouTube Music links.
3.  **Select Destination:** Choose the folder where files will be saved.
4.  **Choose Format:** Select MP3 (Audio) or MP4 (Video).
5.  **Download:** Click the button and wait for the magic!

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📝 License

This project is for **educational purposes only**. Please respect copyright laws and YouTube's Terms of Service.

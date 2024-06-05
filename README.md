# telegramDownloader

## README

# Telegram Media Downloader Bot

This is a Telegram bot that downloads media and videos from YouTube, Instagram, Facebook, and Twitter/X. Users can send a link to the bot, and it will download the video from the specified platform and send it back to the user.

## Features

- Detects the media platform from the provided URL.
- Downloads videos from YouTube, Instagram, Facebook, and Twitter/X.
- Sends the downloaded video back to the user in the chat.
- Supports links from major social media platforms.

## Prerequisites

- Python 3.6 or later
- `telebot` library
- `yt-dlp` library
- `pytube` library

## Installation

1. Clone the repository or download the code.
2. Install the required libraries:

   ```bash
   pip install pyTelegramBotAPI yt-dlp pytube
   ```

3. Replace the placeholder token with your actual bot token from BotFather:

   ```python
   TOKEN = 'YOUR_TOKEN_HERE'
   ```

## Usage

1. Start the bot by running the script:

   ```bash
   python bot.py
   ```

2. Open Telegram and start a chat with your bot.
3. Send the `/start` command to receive a welcome message.
4. Send a valid URL from YouTube, Instagram, Facebook, or Twitter/X.
5. The bot will download the video and send it back to you.

## Code Explanation

### Detect Media Platform

The function `detect_media_platform` takes a URL as input and returns the name of the platform (YouTube, Instagram, Facebook, Twitter/X) based on the URL pattern.

### Download Video

The function `download_video` takes a URL and platform name as input, downloads the video, and returns the path to the downloaded video.

- For YouTube, it uses the `pytube` library.
- For other platforms, it uses the `yt-dlp` library.

### Bot Initialization

The bot is initialized with the provided token using the `telebot` library. It has handlers for the `/start` command and for processing any message containing a URL.

### Handling Messages

When a message is received, the bot:
1. Detects the media platform from the URL.
2. Sends a message indicating that the video is being downloaded.
3. Downloads the video.
4. Sends the downloaded video back to the user.
5. Deletes the video file from the local storage to save space.

## Example Usage

```python
import telebot
import re
import os
import yt_dlp
from pytube import YouTube

def detect_media_platform(url: str) -> str:
    youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu\.be)(\.com)?/.*')
    instagram_pattern = re.compile(r'(https?://)?(www\.)?instagram\.com/.*')
    facebook_pattern = re.compile(r'(https?://)?(www\.)?facebook\.com/.*')
    twitter_pattern = re.compile(r'(https?://)?(www\.)?(twitter|x)\.com/.*')

    if youtube_pattern.match(url):
        return "YouTube"
    elif instagram_pattern.match(url):
        return "Instagram"
    elif facebook_pattern.match(url):
        return "Facebook"
    elif twitter_pattern.match(url):
        return "Twitter/X"
    else:
        return "Unknown"

def download_video(url: str, platform: str) -> str:
    output_path = "downloads"
    os.makedirs(output_path, exist_ok=True)

    if platform == "YouTube":
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        stream.download(output_path)
        return os.path.join(output_path, stream.default_filename)
    else:
        ydl_opts = {'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s')}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            video_ext = info_dict.get('ext', None)
            return os.path.join(output_path, f"{video_title}.{video_ext}")

# Replace 'YOUR_TOKEN_HERE' with your actual bot token
TOKEN = 'YOUR_TOKEN_HERE'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Please provide your link!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    platform = detect_media_platform(url)
    if platform == "Unknown":
        bot.reply_to(message, "Unsupported or unknown URL. Please provide a valid link from YouTube, Instagram, Facebook, or Twitter/X.")
    else:
        bot.reply_to(message, f"Downloading video from {platform}...")
        video_path = download_video(url, platform)
        with open(video_path, 'rb') as video:
            bot.send_video(message.chat.id, video)
        os.remove(video_path)

if __name__ == "__main__":
    bot.polling()
```

### Additional Information

- **GIF Creation**: If you need to create a GIF for your bot, you can use the images generated in the discussions and combine them using an online GIF maker or software like Photoshop or GIMP.
- **BotPic**: To set a profile picture for your bot, use BotFather in Telegram.

If you have any questions or need further assistance, feel free to reach out!

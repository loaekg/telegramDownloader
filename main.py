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
TOKEN = 'INSERT_UR_TOKEN'
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

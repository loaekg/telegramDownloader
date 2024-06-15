import telebot
import re
import os
import yt_dlp
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def get_next_filename(output_path: str, prefix: str, extension: str = '.mp4') -> str:

    index = 1
    while True:
        filename = f"{prefix}{index}{extension}"
        if not os.path.exists(os.path.join(output_path, filename)):
            return os.path.join(output_path, filename)
        index += 1

def download_mp4(url: str) -> str:

    output_path = "downloads"
    os.makedirs(output_path, exist_ok=True)
    file_path = get_next_filename(output_path, 'video', '.mp4') 
    ydl_opts = {
        'outtmpl': file_path,  
        'format': 'bestvideo+bestaudio/best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    normalized_path = os.path.normpath(file_path)  
    logging.info(f"MP4 downloaded: {normalized_path}")
    return normalized_path


TOKEN = 'Token'
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
        try:
            bot.reply_to(message, f"Downloading video from {platform}...")
            video_path = download_mp4(url)
            logging.info(f"Normalized path for sending: {video_path}")
            with open(video_path, 'rb') as video:
                normalized_video_path = os.path.normpath(video_path)
                logging.info(f"Sending video from normalized path: {normalized_video_path}")
                bot.send_video(message.chat.id, video)
            os.remove(normalized_video_path)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            bot.reply_to(message, f"An error occurred while downloading the video: {e}")

if __name__ == "__main__":
    bot.polling()

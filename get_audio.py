import os
import yt_dlp as youtube_dl
import re

def sanitize_filename(filename):
    sanitized = re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')
    return sanitized

def download_audio_from_youtube(youtube_url, output_path='.', cookies_file='cookies.txt'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],

        'cookiefile': cookies_file,
        'nocheckcertificate': True,
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        title = info_dict.get('title', 'audio')
        sanitized_title = sanitize_filename(title)
        ydl_opts['outtmpl'] = os.path.join(output_path, f"{sanitized_title}.%(ext)s")

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return os.path.join(output_path, sanitized_title + '.mp3')

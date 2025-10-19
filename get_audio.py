import os
import yt_dlp as youtube_dl
import re

def sanitize_filename(filename):
    sanitized = re.sub(r'[^a-zA-Z0-9_\-]', '_', filename)
    sanitized = re.sub(r'_+', '_', sanitized).strip('_')
    return sanitized

def download_audio_from_youtube(ydl_opts, ytdlp_info_dict):
    youtube_url = ytdlp_info_dict.get("webpage_url")
    title = ytdlp_info_dict.get("title", "audio")

    sanitized_title = sanitize_filename(title)
    output_path = "."

    os.makedirs(output_path, exist_ok=True)

    ydl_opts['outtmpl'] = os.path.join(output_path, f"{sanitized_title}.%(ext)s")

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return os.path.join(output_path, sanitized_title + '.mp3')

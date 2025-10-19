import os
import yt_dlp as youtube_dl

def get_ytdlp_info(ydl_opts, youtube_url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)

    return info_dict

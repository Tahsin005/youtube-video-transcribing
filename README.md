# YouTube Video Transcription

Simple Streamlit app that downloads audio from a YouTube video and transcribes it using OpenAI Whisper.

- Web UI: [app.py](app.py) — main Streamlit app.
- Audio download: [`get_audio.download_audio_from_youtube`](get_audio.py) in [get_audio.py](get_audio.py).
- Filename sanitization: [`get_audio.sanitize_filename`](get_audio.py) in [get_audio.py](get_audio.py).
- Transcription: [`get_transcript.transcribe_audio_to_text`](get_transcript.py) in [get_transcript.py](get_transcript.py).
- Requirements: [requirements.txt](requirements.txt)
- Optional: raw extractor output example: [video_info_from_ytdlp.txt](video_info_from_ytdlp.txt)
- Cookies file (ignored by git): [cookies.txt](cookies.txt)

## Features
- Paste a YouTube URL in the UI and click "Transcribe".
- Downloads best audio as MP3 (via yt-dlp + ffmpeg).
- Uses Whisper (`small` model by default) to produce a plain-text transcription.

## Prerequisites
- Python 3.8+
- ffmpeg installed and available on PATH
- Recommended: virtual environment
- (Optional) cookies.txt for private/age-restricted videos — file is already listed in .gitignore.

## Quick start

1. Clone repository
```bash
git clone git@github.com:Tahsin005/youtube-video-transcribing.git
cd youtube-video-transcribing
```

2. Create & activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

3. Install Python dependencies
```bash
pip install -r requirements.txt
```

4. Install ffmpeg (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```
(For other OSes, install from https://ffmpeg.org/)

5. Run the app
```bash
streamlit run app.py
```
Open the local Streamlit URL shown in the terminal, paste a YouTube link and click "Transcribe".

## Files of interest
- `app.py` — Streamlit UI and orchestration
- `get_audio.py` — downloads and sanitizes audio filenames
- `get_transcript.py` — runs Whisper transcription
- `requirements.txt` — Python deps
- `cookies.txt` — optional (not committed) for restricted videos

## Notes & troubleshooting
- If Whisper fails to load models or you want faster results, change the model name in [get_transcript.py](get_transcript.py).
- If download fails for age-restricted or private videos, provide a `cookies.txt` exported from your browser (project already references [cookies.txt](cookies.txt)).
- Ensure ffmpeg is on PATH; yt-dlp uses it to convert/extract audio.
- Large Whisper models require significant RAM / GPU. Use `small` or `base` for local CPU runs.

## Preview

<div align="center">
  <img src="https://github.com/Tahsin005/youtube-video-transcribing/blob/main/assets/img-v2-1.png" alt="readme image" />
</div>
<div align="center">
  <img src="https://github.com/Tahsin005/youtube-video-transcribing/blob/main/assets/img-v2-2.png" alt="readme image" />
</div>
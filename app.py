import datetime
import requests
from io import BytesIO
import streamlit as st
import os
import time
from get_ytdlp_info import get_ytdlp_info
from get_audio import download_audio_from_youtube
from get_transcript import transcribe_audio_to_text

# ---------------------- Page Setup ----------------------
st.set_page_config(
    page_title="YouTube Video Transcription",
    layout="centered"
)

# Font Awesome for icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
""", unsafe_allow_html=True)

# ---------------------- Custom CSS ----------------------
st.markdown("""
<style>
    body {
        background-color: #0e1117;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .subtext {
        text-align: center;
        color: #aaa;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .video-card {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    .video-meta {
        font-size: 0.95rem;
        line-height: 1.7;
        color: #ddd;
    }
    .video-meta strong {
        color: #fff;
    }
    .video-meta a {
        color: #2ea3f2;
        text-decoration: none;
    }
    .video-meta i {
        color: #aaa;
        margin-right: 6px;
    }
    .step-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
        color: #ccc;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- Main Title ----------------------
st.markdown('<h1 class="main-title">YouTube Video Transcription</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Download audio, view details, and get accurate AI transcriptions — all in one click.</p>', unsafe_allow_html=True)

# ---------------------- URL Input ----------------------
youtube_url = st.text_input("Enter YouTube URL here 🔗", placeholder="https://www.youtube.com/watch?v=...")

start_button = st.button("Start Transcription", use_container_width=True)

# ---------------------- Processing ----------------------
if start_button and youtube_url:
    try:
        progress = st.progress(0)

        # ---------------------- Step 1: Fetch Info ----------------------
        st.markdown('<div class="step-title">Step 1 — Fetch Video Info</div>', unsafe_allow_html=True)
        with st.spinner("Fetching video metadata..."):
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'cookiefile': "cookies.txt",
                'nocheckcertificate': True,
                'outtmpl': os.path.join(".", '%(title)s.%(ext)s'),
            }
            info = get_ytdlp_info(ydl_opts, youtube_url)
            time.sleep(0.5)
        progress.progress(40)
        st.success("Video info fetched successfully!")

        # Format upload date
        raw_date = info.get('upload_date')
        formatted_date = "N/A"
        if raw_date and len(raw_date) == 8:
            try:
                formatted_date = datetime.datetime.strptime(raw_date, "%Y%m%d").strftime("%B %d, %Y")
            except:
                formatted_date = raw_date

        # ---------------------- Video Details ----------------------
        st.markdown("### <i class='fa-solid fa-circle-info'></i> Video Details", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])

        with col1:
            if "thumbnail" in info:
                thumb_url = info["thumbnail"]
                st.image(thumb_url, use_container_width=True)

                # Download Thumbnail
                try:
                    response = requests.get(thumb_url)
                    if response.status_code == 200:
                        image_bytes = BytesIO(response.content)
                        title_for_file = (
                            info.get('title', 'thumbnail')
                            .replace(" ", "_")
                            .replace("/", "_")
                        )
                        st.download_button(
                            "📥 Download Thumbnail",
                            data=image_bytes,
                            file_name=f"{title_for_file}_thumbnail.jpg",
                            mime="image/jpeg",
                            use_container_width=True
                        )
                except:
                    st.warning("Could not download thumbnail.")

        with col2:
            st.markdown(f"""
            <div class="video-card">
                <div class="video-meta">
                    <p><i class="fa-solid fa-clapperboard"></i><strong>Title:</strong> {info.get('fulltitle', 'N/A')}</p>
                    <p><i class="fa-solid fa-user"></i><strong>Channel:</strong> <a href="{info.get('uploader_url', '#')}" target="_blank">{info.get('channel', 'N/A')}</a></p>
                    <p><i class="fa-solid fa-calendar"></i><strong>Uploaded:</strong> {formatted_date}</p>
                    <p><i class="fa-solid fa-clock"></i><strong>Duration:</strong> {info.get('duration_string', 'N/A')}</p>
                    <p><i class="fa-solid fa-thumbs-up"></i><strong>Likes:</strong> {info.get('like_count', 0):,}</p>
                    <p><i class="fa-solid fa-users"></i><strong>Subscribers:</strong> {info.get('channel_follower_count', 0):,}</p>
                    <p><i class="fa-solid fa-globe"></i><strong>Visibility:</strong> {info.get('availability', 'N/A')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ---------------------- Step 2: Download Audio ----------------------
        st.markdown('<div class="step-title">Step 2 — Downloading Audio</div>', unsafe_allow_html=True)
        with st.spinner("Downloading high-quality audio..."):
            audio_path = download_audio_from_youtube(ydl_opts, info)
            time.sleep(0.5)
        progress.progress(80)
        st.success("Audio downloaded successfully!")

        if os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                st.download_button(
                    label="🎧 Download Audio File",
                    data=f,
                    file_name=os.path.basename(audio_path),
                    mime="audio/mpeg",
                    use_container_width=True
                )

        # ---------------------- Step 3: Transcription ----------------------
        st.markdown('<div class="step-title">Step 3 — Generating Transcription</div>', unsafe_allow_html=True)
        with st.spinner("Transcribing audio using AI..."):
            transcription = transcribe_audio_to_text(audio_path)
            time.sleep(0.5)
        progress.progress(100)
        st.success("Transcription completed successfully!")

        with st.expander("View Full Transcription", expanded=True):
            st.text_area("Transcribed Text", transcription, height=300)

    except Exception as e:
        st.error(f"Error: {str(e)}")

# ---------------------- Idle State ----------------------
else:
    st.markdown("###Ready to Transcribe?")
    st.info("""
    Paste a **YouTube video URL** above and click **Start Transcription**.
    The app will:
    1. Fetch video info
    2. Download the audio
    3. Generate the transcription automatically
    """)

    st.markdown("#### Example URL:")
    st.code("https://www.youtube.com/watch?v=dQw4w9WgXcQ", language="text")

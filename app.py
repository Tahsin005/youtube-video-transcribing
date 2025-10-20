import datetime
import requests
from io import BytesIO
import streamlit as st
import os
from get_ytdlp_info import get_ytdlp_info
from get_audio import download_audio_from_youtube
from get_transcript import transcribe_audio_to_text

st.set_page_config(page_title="YouTube Video Transcription", layout="centered")
st.title("🎧 YouTube Video Transcription")

# Input
youtube_url = st.text_input("Enter YouTube URL:")

if st.button("Transcribe"):
    if youtube_url:
        try:
            # yt-dlp options
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

            # get video info
            with st.spinner("🔍 Fetching video information... Please wait"):
                ytdlp_info_dict = get_ytdlp_info(ydl_opts, youtube_url)

            raw_date = ytdlp_info_dict.get('upload_date')
            formatted_date = "N/A"
            if raw_date and len(raw_date) == 8:
                try:
                    formatted_date = datetime.strptime(raw_date, "%Y%m%d").strftime("%B %d, %Y")
                except:
                    formatted_date = raw_date

            # show metadata
            st.subheader("📄 Video Information")
            col1, col2 = st.columns([1, 2])
            with col1:
                if "thumbnail" in ytdlp_info_dict:
                    thumbnail_url = ytdlp_info_dict["thumbnail"]
                    st.image(thumbnail_url, use_container_width=True)

                    # downloadable thumbnail
                    try:
                        response = requests.get(thumbnail_url)
                        if response.status_code == 200:
                            image_bytes = BytesIO(response.content)
                            # Generate filename with video title
                            title_for_file = (
                                ytdlp_info_dict.get('title', 'thumbnail')
                                .replace(" ", "_")
                                .replace("/", "_")
                            )
                            st.download_button(
                                label="📥 Download Thumbnail",
                                data=image_bytes,
                                file_name=f"{title_for_file}_thumbnail.jpg",
                                mime="image/jpeg"
                            )
                    except Exception:
                        st.warning("⚠️ Could not download thumbnail.")
            with col2:
                st.markdown(f"**🎬  Title:** {ytdlp_info_dict.get('fulltitle', 'N/A')}")
                st.markdown(f"**👤  Channel:** [{ytdlp_info_dict.get('channel', 'N/A')}]({ytdlp_info_dict.get('uploader_url', '#')})")
                st.markdown(f"**📅  Upload Date:** {formatted_date}")
                st.markdown(f"**🕒  Duration:** {ytdlp_info_dict.get('duration_string', 'N/A')}")
                st.markdown(f"**👍  Likes:** {ytdlp_info_dict.get('like_count', 'N/A'):,}")
                st.markdown(f"**👥  Subscribers:** {ytdlp_info_dict.get('channel_follower_count', 'N/A'):,}")
                st.markdown(f"**🌐  Visibility:** {ytdlp_info_dict.get('availability', 'N/A')}")

            # download audio
            with st.spinner("🎧 Downloading audio from YouTube..."):
                audio_file_path = download_audio_from_youtube(ydl_opts, ytdlp_info_dict)

            # check and show download button
            if os.path.exists(audio_file_path):
                with open(audio_file_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Audio File",
                        data=f,
                        file_name=os.path.basename(audio_file_path),
                        mime="audio/mpeg",
                    )

                # transcribe
                st.subheader("📝 Transcription")
                with st.spinner("🎤 Transcribing audio... Please wait, this may take a moment ⏳"):
                    transcription = transcribe_audio_to_text(audio_file_path)

                st.success("✅ Transcription completed!")
                st.write(transcription)

                # subtitles
                if ytdlp_info_dict.get("subtitles"):
                    st.subheader("📜 Available Subtitles")
                    for lang, subs in ytdlp_info_dict["subtitles"].items():
                        st.markdown(f"### 🌍 {lang.upper()}")
                        for sub in subs:
                            ext = sub.get("ext", "unknown")
                            url = sub.get("url", "#")
                            name = sub.get("name", "Subtitle")
                            st.markdown(
                                f"- [{name} ({ext.upper()})]({url})",
                                unsafe_allow_html=True
                            )
                else:
                    st.info("No subtitles found for this video.")
            else:
                st.error(f"Error: File {audio_file_path} does not exist.")

        except Exception as e:
            st.error(f"Error: {e}")

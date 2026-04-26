import streamlit as st
import yt_dlp
import os
import tempfile
import glob

# Page configuration
st.set_page_config(page_title="YouTube Pro Downloader", layout="centered")

# UI Styling and Headers
st.title("YouTube Pro Downloader")
st.markdown("Download your favorite YouTube content as **MP3 Audio** or **MP4 Video**.")

# URL Input field
url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

# Format Selection Radio Buttons
download_format = st.radio(
    "Choose your format:",
    ["MP3 (Audio Only)", "MP4 (Video and Audio)"],
    index=0,
    horizontal=True
)

if st.button("Prepare Download"):
    if not url:
        st.warning("Please enter a valid URL first!")
    else:
        try:
            with st.spinner("Processing... This may take a while for high-quality content."):
                # Create a temporary directory to handle the download/conversion process
                with tempfile.TemporaryDirectory() as tmp_dir:

                    # Configuration for MP3 (Audio Only)
                    if download_format == "MP3 (Audio Only)":
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'restrictfilenames': True,
                        }
                        mime_type = "audio/mpeg"
                        final_ext = "mp3"

                    # Configuration for MP4 (Video and Audio)
                    else:
                        ydl_opts = {
                            # Fetches best video and best audio then merges them into an MP4 container
                            'format': 'bestvideo[vcodec^=avc1][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                            'restrictfilenames': True,
                        }
                        mime_type = "video/mp4"
                        final_ext = "mp4"

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        # Extract metadata and trigger the download
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'youtube_download')

                        # Locate the processed file within the temporary directory using glob
                        search_pattern = os.path.join(tmp_dir, f"*.{final_ext}")
                        files = glob.glob(search_pattern)

                        if files:
                            target_file = files[0]
                            # Read the file in binary mode and provide the download button
                            with open(target_file, "rb") as f:
                                st.download_button(
                                    label=f"Download {final_ext.upper()}",
                                    data=f,
                                    file_name=f"{title}.{final_ext}",
                                    mime=mime_type,
                                    use_container_width=True
                                )
                            st.success(f"Ready: **{title}**")
                        else:
                            st.error("The file could not be found after processing.")

        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.divider()
st.info("**Note:** High-quality MP4/MP3 processing requires `ffmpeg` installed on the host system.")
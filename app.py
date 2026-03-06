import streamlit as st

st.set_page_config(page_title="Vox AI Tool", page_icon="🎙️", layout="wide")

st.title("🎙️ Vox AI Tool")
st.write("AI Voice • Subtitle • Script Generator")

tool = st.sidebar.selectbox(
"Choose AI Tool",
[
"Voice to Text",
"Video Subtitle Generator",
"Text to AI Voice",
"AI Script Generator"
]
)

if tool == "Voice to Text":

    st.header("🎤 Voice to Text")

    audio_file = st.file_uploader("Upload Audio", type=["mp3","wav","m4a"])

    if audio_file:
        st.audio(audio_file)
        st.success("Audio uploaded successfully")

if tool == "Video Subtitle Generator":

    st.header("🎬 Video Subtitle Generator")

    video_file = st.file_uploader("Upload Video", type=["mp4","mov"])

    if video_file:
        st.video(video_file)
        st.success("Video uploaded successfully")

if tool == "Text to AI Voice":

    st.header("🔊 Text to AI Voice")

    text = st.text_area("Enter text")

    voice = st.selectbox(
        "Choose Voice",
        ["Male","Female","Narrator"]
    )

    if st.button("Generate Voice"):
        st.success("Voice generation starting...")

if tool == "AI Script Generator":

    st.header("✍️ AI Script Generator")

    topic = st.text_input("Enter topic")

    if st.button("Generate Script"):
        st.success("AI generating script...")
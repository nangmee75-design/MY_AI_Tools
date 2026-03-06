import streamlit as st

# PAGE CONFIG
st.set_page_config(page_title="Vox AI Tool", page_icon="🎤", layout="wide")

st.title("🎤 Vox AI Tool")
st.write("AI Tools for Content Creators")

# -------------------------
# API KEY SAVE SYSTEM
# -------------------------

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

st.sidebar.header("🔑 API Settings")

api_input = st.sidebar.text_input("Enter API Key", type="password")

if st.sidebar.button("Save API Key"):
    st.session_state.api_key = api_input
    st.sidebar.success("API Key Saved!")

if st.session_state.api_key:
    st.sidebar.success("API Key Active ✅")

# -------------------------
# MENU
# -------------------------

tool = st.sidebar.selectbox(
    "Choose Tool",
    [
        "Home",
        "Voice to Text",
        "Video Subtitle",
        "AI Movie Recap",
        "TikTok Hook Generator",
        "AI Script Generator",
        "Voice Clone",
        "Subtitle Style Maker"
    ]
)

# -------------------------
# HOME PAGE
# -------------------------

if tool == "Home":
    st.header("Welcome to Vox AI Tool")

    st.write("""
This website provides AI tools for creators.

Tools included:
- Voice to Text
- Video Subtitle Generator
- AI Movie Recap Tool
- TikTok Viral Hook Generator
- AI Script Generator
- Voice Clone Upload
- Subtitle Style Maker
""")

# -------------------------
# VOICE TO TEXT
# -------------------------

if tool == "Voice to Text":

    st.header("🎤 Voice to Text")

    audio = st.file_uploader("Upload audio file", type=["mp3","wav","m4a"])

    if audio:
        st.success("Audio uploaded successfully")
        st.info("AI transcription will appear here")

# -------------------------
# VIDEO SUBTITLE
# -------------------------

if tool == "Video Subtitle":

    st.header("🎬 Video Subtitle Generator")

    video = st.file_uploader("Upload video file", type=["mp4","mov"])

    if video:
        st.success("Video uploaded")
        st.info("Subtitle generation will appear here")

# -------------------------
# AI MOVIE RECAP
# -------------------------

if tool == "AI Movie Recap":

    st.header("🎥 AI Movie Recap Tool")

    video = st.file_uploader("Upload movie clip", type=["mp4"])

    if video:
        st.success("Video uploaded")
        st.write("AI will generate movie recap script here")

# -------------------------
# TIKTOK HOOK
# -------------------------

if tool == "TikTok Hook Generator":

    st.header("🔥 TikTok Viral Hook Generator")

    topic = st.text_input("Enter video topic")

    if st.button("Generate Hook"):

        hook = f"You won't believe what happened in this {topic} story!"
        st.success(hook)

# -------------------------
# AI SCRIPT GENERATOR
# -------------------------

if tool == "AI Script Generator":

    st.header("✍️ AI Script Generator")

    topic = st.text_input("Enter your video topic")

    if st.button("Generate Script"):

        script = f"""
Intro:
Today we are talking about {topic}.

Story:
This topic is very interesting and many people want to know about it.

Ending:
That's the story about {topic}. Don't forget to follow for more!
"""

        st.text_area("Generated Script", script, height=250)

# -------------------------
# VOICE CLONE
# -------------------------

if tool == "Voice Clone":

    st.header("🎙️ AI Voice Clone")

    voice = st.file_uploader("Upload voice sample", type=["mp3","wav"])

    if voice:
        st.success("Voice sample uploaded")
        st.info("Voice cloning process will happen here")

# -------------------------
# SUBTITLE STYLE
# -------------------------

if tool == "Subtitle Style Maker":

    st.header("🎬 Subtitle Style Maker")

    subtitle = st.text_area("Paste your subtitle text")

    style = st.selectbox(
        "Choose subtitle style",
        [
            "TikTok Style",
            "Movie Style",
            "YouTube Style"
        ]
    )

    if st.button("Apply Style"):

        st.write("Preview:")
        st.write(subtitle)
        st.success(f"Style applied: {style}")
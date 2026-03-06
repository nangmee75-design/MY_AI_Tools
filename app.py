import streamlit as st
import moviepy.editor as mp
import google.generativeai as genai
import edge_tts
import asyncio
import os
import datetime

# --- ဝက်ဘ်ဆိုက် မျက်နှာပြင် စတင်ခြင်း ---
st.set_page_config(page_title="VoxAI Tools", layout="wide", page_icon="🚀")
st.title("🤖 Vox AI Tool")
st.write("AI Tools for Video Creators")
# --- App ဘာသာစကား ရွေးချယ်ရန် (Language Toggle) ---
if 'app_lang' not in st.session_state:
    st.session_state['app_lang'] = 'MM'

with st.sidebar:
    menu = st.selectbox(
"Choose Tool",
[
"Home",
"Movie Recap Script",
"Voice to Text",
"Video to Subtitle",
"Text to AI Voice"
]
)
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        if st.button("🇲🇲 မြန်မာ"): st.session_state['app_lang'] = 'MM'
    with lang_col2:
        if st.button("🇬🇧 English"): st.session_state['app_lang'] = 'EN'

# --- ဘာသာစကား အဘိဓာန် (Translations Dictionary) ---
UI = {
    "MM": {
        "title": "🚀 VoxAI Studio",
        "menu_title": "🛠️ လုပ်ဆောင်ချက် ရွေးချယ်ပါ",
        "m1": "🎥 ဗီဒီယိုမှ စာထုတ်ရန် (Video to Text)",
        "m2": "🌍 ဘာသာပြန်ရန် (Translate)",
        "m3": "🎙️ AI အသံသွင်းရန် (Text to Voice)",
        "m4": "📝 စာတန်းထိုးထုတ်ရန် (Create SRT)",
        "api_req": "🔑 Google Gemini API Key ထည့်ရန်:",
        "api_err": "❌ ကျေးဇူးပြု၍ ဘေးဘောင်တွင် API Key အရင်ထည့်ပါ။",
        "copy_hint": "👇 အောက်ပါဘောက်စ်၏ ညာဘက်အပေါ်ထောင့်ရှိ 'Copy' ခလုတ်ကိုနှိပ်၍ ကူးယူပါ။"
    },
    "EN": {
        "title": "🚀 VoxAI Studio",
        "menu_title": "🛠️ Select Feature",
        "m1": "🎥 Video to Text",
        "m2": "🌍 Translate",
        "m3": "🎙️ Text to Voice",
        "m4": "📝 Create SRT Subtitles",
        "api_req": "🔑 Enter Google Gemini API Key:",
        "api_err": "❌ Please enter your API Key in the sidebar first.",
        "copy_hint": "👇 Click the 'Copy' icon at the top right of the box below."
    }
}

lang = st.session_state['app_lang']
t = UI[lang]

# --- Sidebar Menu ---
with st.sidebar:
    st.title(t["menu_title"])
    menu = st.radio("", (t["m1"], t["m2"], t["m3"], t["m4"]))
    st.divider()
    google_api_key = st.text_input(t["api_req"], type="password")
    st.markdown("[Get Free API Key Here](https://aistudio.google.com/app/apikey)")

st.title(t["title"])

# ==========================================
# Feature 1: Video to Text
# ==========================================
if menu == t["m1"]:
    st.header(t["m1"])
    uploaded_file = st.file_uploader("Upload Video/Audio (Limit: 500MB)", type=["mp4", "mov", "mp3", "wav"])
    
    btn_text = "✨ စာသားထုတ်ပါ" if lang == 'MM' else "✨ Extract Text"
    if uploaded_file and st.button(btn_text):
        if not google_api_key:
            st.error(t["api_err"])
        else:
            try:
                with st.spinner("Processing... Please wait" if lang == 'EN' else "အလုပ်လုပ်နေပါသည်..."):
                    file_ext = uploaded_file.name.split('.')[-1]
                    temp_filename = f"temp_input.{file_ext}"
                    with open(temp_filename, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    audio_filename = temp_filename
                    if file_ext in ['mp4', 'mov']:
                        video = mp.VideoFileClip(temp_filename)
                        audio_filename = "temp_audio.mp3"
                        video.audio.write_audiofile(audio_filename, logger=None)
                    
                    genai.configure(api_key=google_api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash") # Updated Model
                    
                    audio_file = genai.upload_file(audio_filename)
                    prompt = "Listen to this audio and transcribe the exact words spoken in its original language. Output only the text."
                    result = model.generate_content([audio_file, prompt])
                    
                    st.success("✅ Success!" if lang == 'EN' else "✅ အောင်မြင်ပါသည်!")
                    st.info(t["copy_hint"])
                    st.code(result.text, language="markdown") # COPY BUTTON အလိုလိုပေါ်ပါမည်
                    
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# Feature 2: Translate
# ==========================================
elif menu == t["m2"]:
    st.header(t["m2"])
    text_to_translate = st.text_area("Text to translate:" if lang == 'EN' else "ဘာသာပြန်လိုသော စာသားကို ထည့်ပါ:", height=150)
    
    target_lang = st.selectbox("Target Language:",["မြန်မာ (Burmese)", "English", "Korean", "Japanese", "Thai", "Chinese"])
    
    btn_text = "✨ ဘာသာပြန်ပါ" if lang == 'MM' else "✨ Translate"
    if st.button(btn_text):
        if not google_api_key:
            st.error(t["api_err"])
        elif not text_to_translate:
            st.warning("Enter text first!" if lang == 'EN' else "စာသား အရင်ထည့်ပါ။")
        else:
            try:
                with st.spinner("Translating..." if lang == 'EN' else "ဘာသာပြန်နေပါသည်..."):
                    genai.configure(api_key=google_api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    prompt = f"Translate the following text to {target_lang}. Output ONLY the translation.\n\n{text_to_translate}"
                    result = model.generate_content(prompt)
                    
                    st.success("✅ Success!" if lang == 'EN' else "✅ ဘာသာပြန်ဆိုပြီးပါပြီ!")
                    st.info(t["copy_hint"])
                    st.code(result.text, language="markdown") # COPY BUTTON
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# Feature 3: Text to Voice (Multiple Voices)
# ==========================================
elif menu == t["m3"]:
    st.header(t["m3"])
    text_to_speak = st.text_area("Text to read:" if lang == 'EN' else "အသံထွက်ဖတ်ခိုင်းလိုသော စာကို ထည့်ပါ:", height=150)
    
    # Expanded Voices
    voices = {
        "🇲🇲 Myanmar (Boy - Thiha)": "my-MM-ThihaNeural", 
        "🇲🇲 Myanmar (Girl - Nilar)": "my-MM-NilarNeural",
        "🇬🇧 English (US - Guy)": "en-US-GuyNeural",
        "🇬🇧 English (US - Jenny)": "en-US-JennyNeural",
        "🇬🇧 English (UK - Ryan)": "en-GB-RyanNeural",
        "🇬🇧 English (UK - Sonia)": "en-GB-SoniaNeural",
        "🇰🇷 Korean (Boy - InJoon)": "ko-KR-InJoonNeural", 
        "🇰🇷 Korean (Girl - SunHi)": "ko-KR-SunHiNeural",
        "🇯🇵 Japanese (Boy - Keita)": "ja-JP-KeitaNeural", 
        "🇯🇵 Japanese (Girl - Nanami)": "ja-JP-NanamiNeural"
    }
    selected_voice = st.selectbox("Select Voice / အသံအမျိုးအစား ရွေးချယ်ပါ:", list(voices.keys()))
    
    async def generate_audio(text, voice, filename):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

    btn_text = "✨ အသံထုတ်ပါ" if lang == 'MM' else "✨ Generate Voice"
    if st.button(btn_text):
        if not text_to_speak:
            st.warning("Enter text first!" if lang == 'EN' else "စာသား အရင်ထည့်ပါ။")
        else:
            with st.spinner("Generating AI Voice..." if lang == 'EN' else "AI အသံ ဖန်တီးနေပါသည်..."):
                try:
                    voice_id = voices[selected_voice]
                    output_file = "ai_voice_output.mp3"
                    asyncio.run(generate_audio(text_to_speak, voice_id, output_file))
                    
                    st.success("✅ Voice Generated!" if lang == 'EN' else "✅ AI Voice ရပါပြီ!")
                    st.audio(output_file)
                except Exception as e:
                    st.error(f"Error: {e}")

# ==========================================
# Feature 4: Create SRT
# ==========================================
elif menu == t["m4"]:
    st.header(t["m4"])
    st.info("Hit Enter for each new line. / စာကြောင်း တစ်ကြောင်းချင်းစီကို Enter ခေါက်ပြီး ရိုက်ထည့်ပါ။")
    
    srt_text_input = st.text_area("Text / စာသားများ:", height=200)
    
    btn_text = "✨ SRT ဖိုင် ဖန်တီးပါ" if lang == 'MM' else "✨ Create SRT File"
    if st.button(btn_text):
        if not srt_text_input:
            st.warning("Enter text first!" if lang == 'EN' else "စာသား အရင်ထည့်ပါ။")
        else:
            with st.spinner("Creating SRT..." if lang == 'EN' else "SRT ဖိုင် တည်ဆောက်နေပါသည်..."):
                lines = srt_text_input.strip().split('\n')
                srt_content = ""
                current_time = datetime.timedelta(seconds=0)
                
                for i, line in enumerate(lines):
                    if line.strip():
                        start_time_str = str(current_time) + ",000"
                        if len(start_time_str.split(':')[0]) == 1: start_time_str = "0" + start_time_str
                        current_time += datetime.timedelta(seconds=3)
                        end_time_str = str(current_time) + ",000"
                        if len(end_time_str.split(':')[0]) == 1: end_time_str = "0" + end_time_str
                        srt_content += f"{i+1}\n{start_time_str} --> {end_time_str}\n{line.strip()}\n\n"
                
                st.success("✅ SRT Created!" if lang == 'EN' else "✅ အောင်မြင်ပါသည်!")
                st.info(t["copy_hint"])
                st.code(srt_content, language="markdown") # COPY BUTTON
                
                st.download_button(
                    label="📥 Download SRT File" if lang == 'EN' else "📥 SRT ဖိုင်ကို Download ဆွဲရန်",
                    data=srt_content,
                    file_name="subtitles.srt",
                    mime="text/plain"
                )
                uploaded_file = st.file_uploader(
    "Upload Video",
    type=["mp4", "mov", "avi"],
    accept_multiple_files=False
)

if uploaded_file is not None:
    st.video(uploaded_file)
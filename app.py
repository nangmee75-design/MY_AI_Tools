import streamlit as st
import moviepy.editor as mp
import google.generativeai as genai
import edge_tts
import asyncio
import os
import datetime

# --- ဝက်ဘ်ဆိုက် မျက်နှာပြင် အကျယ်ကြီးဖြစ်အောင် လုပ်ခြင်း ---
st.set_page_config(page_title="My AI Tools", layout="wide")

# --- ဘေးဘောင် (Sidebar) တွင် Menu ရွေးရန်နေရာ ဖန်တီးခြင်း ---
with st.sidebar:
    st.title("🛠️ AI Tools Menu")
    menu = st.radio(
        "လုပ်ဆောင်မည့် စနစ်ကို ရွေးချယ်ပါ:",
        ("၁။ ဗီဒီယိုမှ စာထုတ်ရန်", 
         "၂။ စာသားကို ဘာသာပြန်ရန်", 
         "၃။ စာသားမှ အသံပြောင်းရန်", 
         "၄။ စာတန်းထိုးဖိုင် ထုတ်ရန်")
    )
    st.divider()
    st.header("🔑 Google API Key ထည့်ရန်")
    google_api_key = st.text_input("Gemini API Key:", type="password")
    st.markdown("[API Key မရှိသေးရင် ဒီမှာယူပါ](https://aistudio.google.com/app/apikey)")

# ==========================================
# Feature 1: Video to Text (ဗီဒီယိုမှ စာထုတ်ခြင်း)
# ==========================================
if menu == "၁။ ဗီဒီယိုမှ စာထုတ်ရန်":
    st.header("🎥 ဗီဒီယိုမှ စာသားထုတ်ယူခြင်း (Video to Text)")
    uploaded_file = st.file_uploader("Video သို့မဟုတ် Audio ဖိုင်ကို တင်ပါ", type=["mp4", "mov", "mp3", "wav"])
    
    if uploaded_file and st.button("✨ စာသားထုတ်ပါ"):
        if not google_api_key:
            st.error("ဘေးဘောင်မှာ API Key အရင်ထည့်ပါ။")
        else:
            try:
                with st.spinner("အလုပ်လုပ်နေပါသည်... အချိန်အနည်းငယ် ကြာနိုင်ပါသည်။"):
                    file_ext = uploaded_file.name.split('.')[-1]
                    temp_filename = f"temp_input.{file_ext}"
                    with open(temp_filename, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    audio_filename = temp_filename
                    if file_ext in ['mp4', 'mov']:
                        st.info("Video မှ အသံ ခွဲထုတ်နေပါသည်...")
                        video = mp.VideoFileClip(temp_filename)
                        audio_filename = "temp_audio.mp3"
                        video.audio.write_audiofile(audio_filename, logger=None)
                    
                    st.info("AI မှ စကားပြောများကို စာသားအဖြစ် ပြောင်းနေပါသည်...")
                    genai.configure(api_key=google_api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    
                    audio_file = genai.upload_file(audio_filename)
                    prompt = "Listen to this audio and transcribe the exact words spoken. Output only the text."
                    result = model.generate_content([audio_file, prompt])
                    
                    st.success("✅ အောင်မြင်ပါသည်!")
                    st.text_area("ရရှိလာသော စာသားများ:", result.text, height=200)
                    
            except Exception as e:
                st.error(f"အမှားဖြစ်နေပါသည်: {e}")

# ==========================================
# Feature 2: Translate (ဘာသာပြန်ခြင်း)
# ==========================================
elif menu == "၂။ စာသားကို ဘာသာပြန်ရန်":
    st.header("🌍 စာသားများကို ဘာသာပြန်ခြင်း (Text Translation)")
    text_to_translate = st.text_area("ဘာသာပြန်လိုသော စာသားကို ဤနေရာတွင် ထည့်ပါ:", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        target_lang = st.selectbox("ပြောင်းလိုသော ဘာသာစကား:",["မြန်မာ (Burmese)", "English", "Korean", "Japanese", "Thai"])
    
    if st.button("✨ ဘာသာပြန်ပါ"):
        if not google_api_key:
            st.error("ဘေးဘောင်မှာ API Key အရင်ထည့်ပါ။")
        elif not text_to_translate:
            st.warning("ဘာသာပြန်မည့် စာသား အရင်ထည့်ပါ။")
        else:
            try:
                with st.spinner("ဘာသာပြန်နေပါသည်..."):
                    genai.configure(api_key=google_api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    prompt = f"Translate the following text to {target_lang}. Output ONLY the translation.\n\n{text_to_translate}"
                    result = model.generate_content(prompt)
                    
                    st.success("✅ ဘာသာပြန်ဆိုပြီးပါပြီ!")
                    st.text_area(f"{target_lang} သို့ ဘာသာပြန်ရလဒ်:", result.text, height=150)
            except Exception as e:
                st.error(f"အမှားဖြစ်နေပါသည်: {e}")

# ==========================================
# Feature 3: Text to Voice (အသံသွင်းခြင်း)
# ==========================================
elif menu == "၃။ စာသားမှ အသံပြောင်းရန်":
    st.header("🎙️ စာသားကို AI အသံဖြင့် ဖတ်ခိုင်းခြင်း (Text to Speech)")
    text_to_speak = st.text_area("အသံထွက်ဖတ်ခိုင်းလိုသော စာကို ဤနေရာတွင် ထည့်ပါ:", height=150)
    
    voices = {
        "Myanmar - Boy": "my-MM-ThihaNeural", "Myanmar - Girl": "my-MM-NilarNeural",
        "English - Boy": "en-US-ChristopherNeural", "English - Girl": "en-US-AriaNeural"
    }
    selected_voice = st.selectbox("အသံအမျိုးအစား ရွေးချယ်ပါ:", list(voices.keys()))
    
    async def generate_audio(text, voice, filename):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filename)

    if st.button("✨ အသံထုတ်ပါ"):
        if not text_to_speak:
            st.warning("စာသား အရင်ထည့်ပါ။")
        else:
            with st.spinner("AI အသံ ဖန်တီးနေပါသည်..."):
                try:
                    voice_id = voices[selected_voice]
                    output_file = "ai_voice_output.mp3"
                    asyncio.run(generate_audio(text_to_speak, voice_id, output_file))
                    
                    st.success("✅ AI Voice ရပါပြီ!")
                    st.audio(output_file)
                except Exception as e:
                    st.error(f"အမှားဖြစ်နေပါသည်: {e}")

# ==========================================
# Feature 4: Create SRT (စာတန်းထိုးဖိုင်ထုတ်ခြင်း)
# ==========================================
elif menu == "၄။ စာတန်းထိုးဖိုင် ထုတ်ရန်":
    st.header("📝 စာသားများမှ စာတန်းထိုး (SRT) ဖိုင် ပြုလုပ်ခြင်း")
    st.info("စာကြောင်း တစ်ကြောင်းချင်းစီကို Enter ခေါက်ပြီး တစ်ကြောင်းစီ ရိုက်ထည့်ပါ။ AI မှ အချိန် (Timestamps) များကို အလိုအလျောက် ခန့်မှန်းပြီး SRT ဖိုင် ထုတ်ပေးပါမည်။")
    
    srt_text_input = st.text_area("စာသားများ ထည့်ရန်:", height=200)
    
    if st.button("✨ SRT ဖိုင် ဖန်တီးပါ"):
        if not srt_text_input:
            st.warning("စာသား အရင်ထည့်ပါ။")
        else:
            with st.spinner("SRT ဖိုင် တည်ဆောက်နေပါသည်..."):
                lines = srt_text_input.strip().split('\n')
                srt_content = ""
                current_time = datetime.timedelta(seconds=0)
                
                for i, line in enumerate(lines):
                    if line.strip():
                        start_time_str = str(current_time) + ",000"
                        if len(start_time_str.split(':')[0]) == 1:
                            start_time_str = "0" + start_time_str
                            
                        current_time += datetime.timedelta(seconds=3)
                        
                        end_time_str = str(current_time) + ",000"
                        if len(end_time_str.split(':')[0]) == 1:
                            end_time_str = "0" + end_time_str
                            
                        srt_content += f"{i+1}\n{start_time_str} --> {end_time_str}\n{line.strip()}\n\n"
                
                st.success("✅ SRT စာတန်းထိုးဖိုင် အောင်မြင်စွာ တည်ဆောက်ပြီးပါပြီ!")
                st.text_area("SRT ရလဒ်:", srt_content, height=200)
                
                st.download_button(
                    label="📥 SRT ဖိုင်ကို Download ဆွဲရန် နှိပ်ပါ",
                    data=srt_content,
                    file_name="subtitles.srt",
                    mime="text/plain"
                )
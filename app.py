import streamlit as st
from gtts import gTTS
import base64
import google.generativeai as genai

# --- 1. KONFIGURASI API KEY ---
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. FUNGSI SUARA (Manual Klik) ---
def buat_audio(teks):
    try:
        teks_bersih = teks.replace("*", "").replace("#", "")
        tts = gTTS(text=teks_bersih[:500], lang='id')
        tts.save("respon.mp3")
        with open("respon.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            return f'data:audio/mp3;base64,{b64}'
    except:
        return None

# --- 3. TAMPILAN FULL SCREEN ---
st.set_page_config(page_title="SY-Core AI Universal", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .block-container { max-width: 95% !important; }
    .stChatFloatingInputContainer { bottom: 20px; }
    /* Gaya untuk header */
    .header-text { color: #00ffcc; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='header-text'>🌐 SY-Core AI Universal</h1>", unsafe_allow_html=True)
st.write(f"<center>Developer: <b>Slamet Yulianto</b></center>", unsafe_allow_html=True)
st.write("---")

# Riwayat Percakapan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Chat
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Jika ini jawaban AI, tampilkan tombol speaker di pojok kanan bawah jawaban
        if message["role"] == "assistant":
            col_text, col_spk = st.columns([0.9, 0.1])
            with col_spk:
                if st.button("🔊", key=f"spk_{i}"):
                    audio_base64 = buat_audio(message["content"])
                    if audio_base64:
                        st.markdown(f'<audio src="{audio_base64}" autoplay></audio>', unsafe_allow_html=True)

# Input Pesan
prompt = st.chat_input("Ketik pesan kamu di sini...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner('SY-Core sedang memproses...'):
        try:
            response = model.generate_content(prompt)
            jawaban = response.text
            
            st.session_state.messages.append({"role": "assistant", "content": jawaban})
            # Trigger refresh untuk menampilkan tombol speaker baru
            st.rerun()
            
        except Exception as e:
            st.error(f"Terjadi kendala: {e}")

st.write("---")
st.caption("<center>© 2026 SY-Core Project</center>", unsafe_allow_html=True)

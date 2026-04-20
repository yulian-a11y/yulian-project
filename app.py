import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# --- API KEY (100% GRATIS) ---
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

# Setting Halaman Full Screen
st.set_page_config(page_title="SY-Core AI", layout="wide")

st.markdown("""
    <style>
    .block-container { max-width: 98% !important; padding: 1rem; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi - Paksa pakai versi standar
try:
    genai.configure(api_key=API_KEY)
    # Gunakan nama model yang paling umum agar tidak 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Koneksi Gagal: {e}")

# Fungsi Suara
def bicara(teks):
    try:
        tts = gTTS(text=teks[:300], lang='id')
        tts.save("s.mp3")
        with open("s.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay></audio>', unsafe_allow_html=True)
    except: pass

st.title("🌐 SY-Core AI Universal")
st.write("Sistem: **Aktif** | Developer: **Slamet Yulianto**")
st.write("---")

if "m" not in st.session_state: st.session_state.m = []

# Tampilkan Chat Full
for i, msg in enumerate(st.session_state.m):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            if st.button("🔊 Putar", key=f"s_{i}"): bicara(msg["content"])

# Input Chat
p = st.chat_input("Tanya apa saja...")

if p:
    st.session_state.m.append({"role": "user", "content": p})
    with st.chat_message("user"): st.write(p)
    
    with st.spinner("Berpikir..."):
        try:
            # Panggilan langsung tanpa embel-embel
            r = model.generate_content(p)
            st.session_state.m.append({"role": "assistant", "content": r.text})
            st.rerun()
        except Exception as e:
            st.error("Koneksi sedang disegarkan. Klik 'Manage App' -> 'Reboot' jika terus berlanjut.")

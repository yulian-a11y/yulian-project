import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# --- KONFIGURASI API (100% GRATIS) ---
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

# Setting Halaman Melebar (Full Screen)
st.set_page_config(page_title="SY-Core AI", layout="wide")

# CSS Khusus untuk Tampilan Full
st.markdown("""
    <style>
    .block-container { max-width: 98% !important; padding: 1rem; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi AI
genai.configure(api_key=API_KEY)

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
st.write("Developer: **Slamet Yulianto** | Status: **Online & Gratis**")
st.write("---")

if "m" not in st.session_state: st.session_state.m = []

# Tampilan Chat Full
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
            # Gunakan model gemini-pro yang paling stabil
            model = genai.GenerativeModel('gemini-pro')
            r = model.generate_content(p)
            st.session_state.m.append({"role": "assistant", "content": r.text})
            st.rerun()
        except Exception as e:
            st.error(f"Koneksi sedikit terganggu, silakan coba lagi.")

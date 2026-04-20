import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# --- 1. SETTING DASAR ---
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

# Tampilan Full Screen (Melebar)
st.set_page_config(page_title="SY-Core AI", layout="wide")

st.markdown("""
    <style>
    .block-container { max-width: 98% !important; padding: 1rem; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INISIALISASI MESIN (JALUR STABIL v1) ---
try:
    genai.configure(api_key=API_KEY)
    # Trik: Menggunakan 'gemini-1.5-flash' dengan awalan 'models/' 
    # Ini cara paling ampuh untuk akun gratis agar tidak 404
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Sistem gagal mulai: {e}")

# Fungsi Suara
def bicara(teks):
    try:
        teks_bersih = teks.replace("*", "").replace("#", "")
        tts = gTTS(text=teks_bersih[:500], lang='id')
        tts.save("r.mp3")
        with open("r.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay></audio>', unsafe_allow_html=True)
    except: pass

# --- 3. ANTARMUKA CHAT ---
st.title("🌐 SY-Core AI Universal")
st.write(f"Developer: **Slamet Yulianto** | Status: **Gratis**")
st.write("---")

if "chat" not in st.session_state:
    st.session_state.chat = []

# Tampilkan history chat secara luas
for i, m in enumerate(st.session_state.chat):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button("🔊 Putar", key=f"s_{i}"):
                bicara(m["content"])

# Input Chat
p = st.chat_input("Tanya apa saja ke SY-Core...")

if p:
    st.session_state.chat.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.write(p)
    
    with st.spinner("SY-Core sedang berpikir..."):
        try:
            # Panggilan paling aman untuk akun gratis
            r = model.generate_content(p)
            st.session_state.chat.append({"role": "assistant", "content": r.text})
            st.rerun()
        except Exception as e:
            # Jika 'flash' masih tidak ditemukan, kita paksa pakai 'gemini-pro'
            try:
                model_alt = genai.GenerativeModel('models/gemini-pro')
                r = model_alt.generate_content(p)
                st.session_state.chat.append({"role": "assistant", "content": r.text})
                st.rerun()
            except Exception as e2:
                st.error("Server Google sedang sibuk. Coba lagi dalam 1 menit.")

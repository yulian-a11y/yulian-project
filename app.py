import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# --- KONFIGURASI GRATIS ---
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

st.set_page_config(page_title="SY-Core AI", layout="wide")

# Styling agar Full Screen
st.markdown("""
    <style>
    .block-container { max-width: 98% !important; padding: 1rem; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi AI Jalur Gratis
try:
    genai.configure(api_key=API_KEY)
    # Kita pakai gemini-1.5-flash tapi dengan cara panggil yang benar agar tetap gratis
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Error: {e}")

# Fungsi Suara
def bicara(teks):
    try:
        tts = gTTS(text=teks[:500], lang='id')
        tts.save("r.mp3")
        with open("r.mp3", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay></audio>', unsafe_allow_html=True)
    except: pass

st.title("🌐 SY-Core AI Universal")
st.write("Status: **Gratis & Aktif** | Developer: **Slamet Yulianto**")

if "m" not in st.session_state: st.session_state.m = []

for i, msg in enumerate(st.session_state.m):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            if st.button("🔊", key=f"s_{i}"): bicara(msg["content"])

p = st.chat_input("Tanya apa saja...")
if p:
    st.session_state.m.append({"role": "user", "content": p})
    with st.chat_message("user"): st.write(p)
    
    with st.spinner("Berpikir..."):
        try:
            # Panggilan paling dasar (100% Free)
            r = model.generate_content(p)
            st.session_state.m.append({"role": "assistant", "content": r.text})
            st.rerun()
        except Exception as e:
            # Jika masih error 404, kita paksa ganti ke model cadangan gratis
            model = genai.GenerativeModel('gemini-pro')
            r = model.generate_content(p)
            st.session_state.m.append({"role": "assistant", "content": r.text})
            st.rerun()

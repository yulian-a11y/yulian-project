import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# --- 1. SETTING UTAMA ---
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

# Konfigurasi Tampilan Full Screen
st.set_page_config(page_title="SY-Core AI", layout="wide")

# CSS agar tampilan lega dan modern
st.markdown("""
    <style>
    .block-container { max-width: 98% !important; padding: 1rem; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. KONEKSI LANGSUNG ---
# Kita gunakan nama model tanpa embel-embel 'models/' atau 'v1beta'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

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

# --- 3. ANTARMUKA ---
st.title("🌐 SY-Core AI Universal")
st.write(f"Developer: **Slamet Yulianto** | Jalur: **Gratis**")
st.write("---")

if "chat" not in st.session_state:
    st.session_state.chat = []

for i, m in enumerate(st.session_state.chat):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button("🔊 Putar", key=f"s_{i}"):
                bicara(m["content"])

p = st.chat_input("Tanya apa saja ke SY-Core...")

if p:
    st.session_state.chat.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.write(p)
    
    with st.spinner("SY-Core sedang merespon..."):
        try:
            # Gunakan jalur paling stabil 'gemini-1.5-flash-latest'
            r = model.generate_content(p)
            st.session_state.chat.append({"role": "assistant", "content": r.text})
            st.rerun()
        except Exception as e:
            st.error(f"Sistem sedang sinkronisasi. Coba ketik ulang pertanyaanmu sekali lagi.")
            # Jika error, coba paksa ke model paling basic
            model = genai.GenerativeModel('gemini-pro')

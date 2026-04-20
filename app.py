import streamlit as st
from gtts import gTTS
import base64
import google.generativeai as genai

# --- 1. SETTING API KEY GRATIS ---
# Gunakan kunci AIza yang kamu temukan tadi
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM" 
genai.configure(api_key=API_KEY)

# Menggunakan model 'gemini-1.5-flash' (Ini yang paling cepat dan gratis)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. FUNGSI SUARA ---
def bicara(teks):
    try:
        # Bersihkan teks agar suara robot enak didengar
        teks_bersih = teks.replace("*", "").replace("#", "")
        tts = gTTS(text=teks_bersih[:500], lang='id')
        tts.save("suara.mp3")
        with open("suara.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay></audio>', unsafe_allow_html=True)
    except:
        pass

# --- 3. TAMPILAN ANTARMUKA FULL SCREEN ---
st.set_page_config(page_title="SY-Core AI", layout="wide")

st.markdown("""
    <style>
    .block-container { max-width: 98% !important; padding-top: 1rem; }
    .stApp { background-color: #0b0d10; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 SY-Core AI Universal")
st.write(f"Sistem Aktif | Developer: **Slamet Yulianto**")
st.write("---")

# Memory Chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tampilkan Chat
for i, chat in enumerate(st.session_state.chat_history):
    with st.chat_message(chat["role"]):
        st.write(chat["content"])
        if chat["role"] == "assistant":
            # Tombol speaker di pojok kanan
            if st.button("🔊 Putar Suara", key=f"btn_{i}"):
                bicara(chat["content"])

# Input Chat
user_query = st.chat_input("Tulis pesan di sini...")

if user_query:
    # Simpan pesan user
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    # Ambil jawaban dari AI Gratis
    with st.spinner("SY-Core sedang merespon..."):
        try:
            # Panggilan paling simpel agar tidak error 404
            response = model.generate_content(user_query)
            jawaban = response.text
            
            st.session_state.chat_history.append({"role": "assistant", "content": jawaban})
            st.rerun()
        except Exception as e:
            st.error("Gagal terhubung ke server. Pastikan API Key benar.")

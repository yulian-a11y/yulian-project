import streamlit as st
from gtts import gTTS
import base64
import google.generativeai as genai

# --- 1. KONFIGURASI MESIN (STABIL) ---
# Gunakan API Key kamu yang sudah benar tadi
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM" 
genai.configure(api_key=API_KEY)

# Memanggil model tanpa v1beta agar tidak error 404
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. FUNGSI SUARA (KLIK BARU BUNYI) ---
def buat_suara(teks):
    try:
        # Bersihkan simbol agar suara robot tidak mengeja simbol
        teks_bersih = teks.replace("*", "").replace("#", "").replace("-", " ")
        tts = gTTS(text=teks_bersih[:500], lang='id')
        tts.save("respon.mp3")
        with open("respon.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            return f'data:audio/mp3;base64,{b64}'
    except:
        return None

# --- 3. TAMPILAN ANTARMUKA FULL SCREEN ---
# 'layout="wide"' membuat tampilan memenuhi seluruh lebar layar
st.set_page_config(page_title="SY-Core AI Universal", page_icon="🌐", layout="wide")

# CSS Khusus untuk membuat tampilan benar-benar "Full" dan Modern
st.markdown("""
    <style>
    /* Menghilangkan margin samping agar full screen */
    .block-container {
        max-width: 98% !important;
        padding-top: 1rem !important;
        padding-bottom: 5rem !important;
    }
    /* Warna latar belakang dan teks */
    .stApp {
        background-color: #0e1117;
    }
    /* Kotak Chat Assistant agar lebih lebar */
    .stChatMessage {
        width: 100% !important;
    }
    /* Styling Header */
    .main-header {
        font-size: 40px;
        color: #00ffcc;
        text-align: center;
        text-shadow: 2px 2px #000;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🌐 SY-Core AI Universal</h1>", unsafe_allow_html=True)
st.write(f"<center>Sistem Kecerdasan Buatan | Pengembang: <b>Slamet Yulianto</b></center>", unsafe_allow_html=True)
st.write("---")

# Penyimpanan Percakapan (Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Chat secara Full
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        # Tampilan teks jawaban
        st.markdown(msg["content"])
        
        # Tombol Speaker di pojok kanan bawah setiap jawaban AI
        if msg["role"] == "assistant":
            col_t, col_btn = st.columns([0.94, 0.06])
            with col_btn:
                if st.button("🔊", key=f"voice_{i}", help="Klik untuk mendengar suara"):
                    audio_data = buat_suara(msg["content"])
                    if audio_data:
                        st.markdown(f'<audio src="{audio_data}" autoplay></audio>', unsafe_allow_html=True)

# Input Pesan (Tampilan Melayang di Bawah)
prompt = st.chat_input("Ketik pesan kamu di sini, Slamet...")

if prompt:
    # 1. Tambahkan pesan user ke layar
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Proses jawaban dari AI
    with st.spinner('SY-Core sedang memproses data...'):
        try:
            response = model.generate_content(prompt)
            jawaban_ai = response.text
            
            # Tambahkan jawaban AI ke riwayat
            st.session_state.messages.append({"role": "assistant", "content": jawaban_ai})
            
            # Refresh otomatis untuk memunculkan tombol speaker
            st.rerun()
            
        except Exception as e:
            st.error(f"Sistem mengalami kendala: {e}")

# Footer bawah
st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background-color: #0e1117;'>
        <p style='color: grey; font-size: 12px;'>© 2026 SY-Core Project | Ditenagai oleh Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)

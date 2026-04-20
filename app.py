import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# --- 1. SETTING UTAMA ---
# Ganti dengan API Key milikmu jika yang di bawah ini tidak jalan
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

# Konfigurasi halaman agar LEBAR (Full Screen)
st.set_page_config(page_title="SY-Core AI", layout="wide")

# CSS untuk mempercantik dan melebarkan kotak chat
st.markdown("""
    <style>
    .block-container { max-width: 98% !important; padding: 1rem; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. KONEKSI KE GOOGLE (DIPERKUAT) ---
@st.cache_resource
def inisialisasi_ai():
    try:
        genai.configure(api_key=API_KEY)
        # Menggunakan model paling stabil untuk akun gratis
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Gagal inisialisasi: {e}")
        return None

model = inisialisasi_ai()

# --- 3. FUNGSI SUARA ---
def putar_suara(teks):
    try:
        # Bersihkan teks agar suara robot tidak aneh
        teks_bersih = teks.replace("*", "").replace("#", "")
        tts = gTTS(text=teks_bersih[:500], lang='id')
        tts.save("respon.mp3")
        with open("respon.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay></audio>', unsafe_allow_html=True)
    except:
        st.warning("Gagal memutar suara.")

# --- 4. ANTARMUKA (UI) ---
st.title("🌐 SY-Core AI Universal")
st.write(f"Status: **Online** | Developer: **Slamet Yulianto**")
st.write("---")

# Memory Chat agar percakapan tidak hilang saat refresh
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat yang sudah ada
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            if st.button("🔊 Suara", key=f"btn_{i}"):
                putar_suara(msg["content"])

# Kotak Input Chat (Full Width)
user_input = st.chat_input("Tanya apa saja...")

if user_input:
    # Simpan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Proses jawaban AI
    if model:
        with st.spinner("SY-Core sedang berpikir..."):
            try:
                # Panggilan API yang paling stabil
                response = model.generate_content(user_input)
                jawaban = response.text
                
                # Simpan jawaban AI
                st.session_state.messages.append({"role": "assistant", "content": jawaban})
                st.rerun() # Refresh agar tombol suara muncul
            except Exception as e:
                st.error(f"Koneksi terputus: {e}")
                st.info("Saran: Coba cek apakah API Key kamu masih aktif di Google AI Studio.")

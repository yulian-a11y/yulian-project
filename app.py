import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

# --- 1. KONFIGURASI ---
# Pastikan API Key ini tidak ada spasi di awal/akhir
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

st.set_page_config(page_title="SY-Core AI", layout="wide")

# CSS untuk tampilan FULL lebar
st.markdown("""
    <style>
    .block-container { max-width: 98% !important; padding: 1rem; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INISIALISASI AI (VERSI STABIL) ---
try:
    genai.configure(api_key=API_KEY)
    # Menentukan model tanpa embel-embel v1beta secara manual
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error(f"Gagal konfigurasi: {e}")

# --- 3. FUNGSI SUARA ---
def putar_suara(teks):
    try:
        teks_bersih = teks.replace("*", "").replace("#", "")
        tts = gTTS(text=teks_bersih[:500], lang='id')
        tts.save("respon.mp3")
        with open("respon.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay></audio>', unsafe_allow_html=True)
    except:
        st.warning("Gagal memutar suara.")

# --- 4. TAMPILAN ---
st.title("🌐 SY-Core AI Universal")
st.write(f"Developer: **Slamet Yulianto**")
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            if st.button("🔊 Suara", key=f"btn_{i}"):
                putar_suara(msg["content"])

# Input Chat
user_input = st.chat_input("Tanya apa saja...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Berpikir..."):
        try:
            # Panggilan langsung tanpa parameter tambahan yang memicu v1beta
            response = model.generate_content(user_input)
            
            if response.text:
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
        except Exception as e:
            # Jika masih 404, kita beri tahu cara perbaikinya
            st.error(f"Koneksi terputus: {e}")
            if "404" in str(e):
                st.info("Saran: Coba ganti baris 'models/gemini-1.5-flash' menjadi 'models/gemini-pro' di kode app.py")

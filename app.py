import streamlit as st
from gtts import gTTS
import base64
import google.generativeai as genai

# --- 1. FUNGSI SUARA (AUDIO ENGINE) ---
def bicara(teks):
    try:
        tts = gTTS(text=teks, lang='id')
        tts.save("suara.mp3")
        with open("suara.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error("Gagal memproses suara.")

# --- 2. KONFIGURASI TAMPILAN (UI) ---
st.set_page_config(page_title="SY-Core AI Universal", page_icon="🤖", layout="centered")

# Header Utama
st.title("🤖 SY-Core AI Universal")
st.write(f"Sistem Aktif | Pengembang: **Slamet Yulianto**")
st.write("---")

# Sidebar (Profil & Status)
with st.sidebar:
    st.header("Sistem Status")
    st.success("Server: Online")
    st.info("Mode: AI Universal v1.0")
    st.write("---")
    st.write("Proyek ini adalah pusat kendali AI untuk pengembangan masa depan.")

# --- 3. LOGIKA INTERAKSI ---
st.subheader("Pusat Kendali Pesan")
user_input = st.text_input("Ketik perintah atau sapa AI kamu:", placeholder="Contoh: Halo SY-Core!")

if user_input:
    # Simulasi Respon AI (Nanti bisa dihubungkan ke API Key Gemini)
    respon_ai = f"Halo Slamet! SY-Core menerima pesan: '{user_input}'. Sistem sedang mengoptimalkan data untukmu."
    
    # Menampilkan Chat
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        st.write(respon_ai)
        # Menjalankan Suara
        bicara(respon_ai)

# Footer
st.write("---")
st.caption("© 2026 SY-Core Project | Dedicated for Future Technology")

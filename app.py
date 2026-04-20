import streamlit as st
from gtts import gTTS
import base64
import google.generativeai as genai

# --- 1. KONFIGURASI API KEY ---
# Masukkan kode AIza yang tadi kamu temukan di sini
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM" 

genai.configure(api_key=API_KEY)

# Konfigurasi Model dengan kemampuan mencari di internet (Google Search)
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=[{"google_search_retrieval": {}}]
)

# --- 2. FUNGSI UNTUK MENGHASILKAN SUARA ---
def bicara(teks):
    try:
        # Membersihkan teks dari simbol bintang (*) agar suara lebih jernih
        teks_bersih = teks.replace("*", "")
        tts = gTTS(text=teks_bersih[:500], lang='id')
        tts.save("respon.mp3")
        
        with open("respon.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            # Script ini akan memutar suara secara otomatis (autoplay)
            audio_html = f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning("Gagal memproses suara, tapi teks tetap muncul.")

# --- 3. TAMPILAN ANTARMUKA WEBSITE (UI) ---
st.set_page_config(page_title="SY-Core AI Universal", page_icon="🌐", layout="centered")

# CSS untuk mempercantik tampilan
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput>div>div>input {
        background-color: #262730;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 SY-Core AI Universal")
st.subheader("Asisten AI dengan Akses Internet & Suara")
st.write(f"Sistem Aktif | Pengembang: **Slamet Yulianto**")
st.write("---")

# Input pertanyaan dari pengguna
user_input = st.text_input("Ketik pertanyaan kamu di sini:", placeholder="Tanya apa saja, misalnya: Berita teknologi terbaru hari ini...")

if user_input:
    with st.spinner('SY-Core sedang berpikir dan mencari informasi...'):
        try:
            # Mengirim pertanyaan ke AI
            response = model.generate_content(user_input)
            jawaban = response.text
            
            # Menampilkan percakapan
            with st.chat_message("user"):
                st.write(user_input)
                
            with st.chat_message("assistant"):
                st.write(jawaban)
            
            # Memanggil fungsi suara
            bicara(jawaban)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
            st.info("Pastikan API Key kamu masih aktif di Google AI Studio.")

# Footer
st.write("---")
st.caption("© 2026 SY-Core Project | Ditenagai oleh Google Gemini & Streamlit")

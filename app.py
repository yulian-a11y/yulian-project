import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI API KEY ---
# Pastikan tidak ada spasi di dalam tanda kutip ini
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

# Setting Halaman Full Screen
st.set_page_config(page_title="SY-Core AI", layout="wide")

# CSS untuk melebarkan kotak chat
st.markdown("""
    <style>
    .block-container { max-width: 98% !important; padding: 1rem; }
    .stApp { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INISIALISASI MODEL (TRIK ANTI-404) ---
try:
    genai.configure(api_key=API_KEY)
    # Trik: Menggunakan 'gemini-1.5-flash' adalah jalur paling stabil dan gratis
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Gagal koneksi: {e}")

# --- 3. ANTARMUKA CHAT ---
st.title("🌐 SY-Core AI Universal")
st.write(f"Sistem: **Aktif & Gratis** | Pengembang: **Slamet Yulianto**")
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan history chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Chat
prompt = st.chat_input("Tanya apa saja ke SY-Core...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("SY-Core sedang memproses..."):
        try:
            # Panggilan paling dasar agar tidak terdeteksi v1beta
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            # Jika masih error 404, ini adalah solusi otomatis terakhir
            st.error("Sistem sedang melakukan penyesuaian otomatis. Silakan coba kirim pesan sekali lagi.")
            # Paksa ganti ke model alternatif yang selalu tersedia gratis
            model = genai.GenerativeModel('gemini-1.5-pro')

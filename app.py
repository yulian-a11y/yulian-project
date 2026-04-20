import streamlit as st
import google.generativeai as genai

# --- 1. CONFIG ENGINE & TAMPILAN ---
# API Key tetap gratis selama tidak input kartu kredit
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

st.set_page_config(
    page_title="SY-Core AI Universal",
    page_icon="🌐",
    layout="wide", # Membuat tampilan Full Screen
    initial_sidebar_state="collapsed"
)

# --- 2. CSS KUSTOM WEBSITE PROFESIONAL ---
st.markdown("""
    <style>
    /* Mengatur lebar halaman agar lega */
    .block-container { padding-top: 1.5rem; max-width: 95%; }
    /* Warna tema gelap premium */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    /* Menghilangkan tanda-tanda Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    /* Styling Chat Box */
    .stChatMessage { border-radius: 12px; border: 1px solid #30363d; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. KONEKSI KE GOOGLE AI ---
try:
    genai.configure(api_key=API_KEY)
    # Gunakan model Flash terbaru (Sangat cepat & Gratis)
    # System instruction memastikan AI tahu identitasnya
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Kamu adalah SY-Core AI, asisten cerdas yang dikembangkan oleh Slamet Yulianto. Jawablah dengan singkat, padat, cerdas, dan gunakan bahasa yang sama dengan pengguna."
    )
except Exception as e:
    st.error("Koneksi Engine Gagal. Silakan cek API Key.")

# --- 4. LOGIKA PERCAKAPAN ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header Tengah
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🌐 SY-Core AI Universal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Status: <b>Online</b> | Developer: <b>Slamet Yulianto</b></p>", unsafe_allow_html=True)
st.write("---")

# Menampilkan Riwayat Chat (Full Width)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Pesan di Bagian Bawah
if prompt := st.chat_input("Tanya apa saja ke SY-Core..."):
    # Simpan pesan User
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses Jawaban AI
    with st.chat_message("assistant"):
        with st.spinner("Sedang berpikir..."):
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error("Server sedang sibuk atau API Key bermasalah. Coba lagi dalam beberapa saat.")

# Tombol Reset (Di Sidebar atau bawah)
if st.sidebar.button("Hapus Semua Riwayat"):
    st.session_state.messages = []
    st.rerun()

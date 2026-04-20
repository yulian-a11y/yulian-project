import streamlit as st
import google.generativeai as genai

# --- CONFIGURASI DASAR ---
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

st.set_page_config(page_title="SY-Core Lite", layout="wide")

# Koneksi ke Otak AI
try:
    genai.configure(api_key=API_KEY)
    # Model Flash adalah yang paling ringan dan jarang sibuk
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Gagal koneksi ke server pusat.")

# Judul Sederhana
st.title("🌐 SY-Core Lite")
st.caption("Developer: Slamet Yulianto | Mode: Stabil & Ringan")

# Penyimpanan Memori Chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Menampilkan Chat
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# Input Chat
if prompt := st.chat_input("Ketik pesan di sini..."):
    # Simpan pesan User
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Respon AI
    with st.chat_message("assistant"):
        try:
            # Instruksi singkat agar AI tahu dia SY-Core
            full_prompt = f"Kamu adalah SY-Core AI buatan Slamet Yulianto. Jawablah: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.write(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Koneksi API terputus. Coba kirim ulang pesan.")

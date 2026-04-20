import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI ---
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

st.set_page_config(page_title="SY-Core AI", layout="wide")

# Inisialisasi
try:
    genai.configure(api_key=API_KEY)
    # Kita pakai gemini-pro, ini model paling stabil di dunia untuk akun gratis
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Gagal Konfigurasi: {e}")

st.title("🌐 SY-Core AI Universal")
st.write("Developer: **Slamet Yulianto**")
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Tanya apa saja...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Berpikir..."):
        try:
            # Panggilan paling simpel tanpa parameter apa pun
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"Akses Ditolak Google: {e}")
            st.info("Slamet, coba buat API Key baru di Google AI Studio. Klik 'Create API key in new project'.")

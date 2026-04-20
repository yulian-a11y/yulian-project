import streamlit as st
import google.generativeai as genai

# Konfigurasi Paling Dasar
st.set_page_config(page_title="SY-Core AI", layout="wide")
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"

# Koneksi Langsung (Tanpa System Instruction dulu agar stabil)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

st.title("🌐 SY-Core AI Universal")
st.write("Developer: **Slamet Yulianto**")
st.write("---")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tampilkan Chat
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Input
if p := st.chat_input("Tanya sesuatu..."):
    st.session_state.chat_history.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.markdown(p)

    try:
        # Panggilan paling simpel
        response = model.generate_content(p)
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
        st.rerun()
    except Exception as e:
        st.error(f"Google belum merespon. Tunggu 5 detik lalu ketik lagi.")

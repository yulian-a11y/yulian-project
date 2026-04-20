import streamlit as st
import google.generativeai as genai

# Konfigurasi
API_KEY = "AIzaSyDfHcDfors-zLMSk09nuKzWQEUmSSdbUaM"
st.set_page_config(page_title="SY-Core AI", layout="wide")

# CSS Full Screen
st.markdown("<style>.block-container {max-width: 98% !important;}</style>", unsafe_allow_html=True)

# Inisialisasi
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🌐 SY-Core AI Universal")
st.write("Developer: **Slamet Yulianto**")

if "m" not in st.session_state: st.session_state.m = []

for msg in st.session_state.m:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

p = st.chat_input("Tanya sesuatu...")

if p:
    st.session_state.m.append({"role": "user", "content": p})
    with st.chat_message("user"): st.write(p)
    
    try:
        r = model.generate_content(p)
        st.session_state.m.append({"role": "assistant", "content": r.text})
        st.rerun()
    except Exception as e:
        st.error(f"Ada masalah koneksi. Klik 'Manage app' lalu 'Reboot'.")

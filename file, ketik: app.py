import streamlit as st
from gtts import gTTS
import base64
import google.generativeai as genai

# 1. Fungsi Suara
def bicara(teks):
    try:
        tts = gTTS(text=teks, lang='id')
        tts.save("suara.mp3")
        with open("suara.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>"""
            st.markdown(md, unsafe_allow_html=True)
    except:
        st.warning("Gagal memutar suara. Pastikan koneksi stabil.")

# 2. Konfigurasi Halaman Universal
st.set_page_config(page_title="Yulian AI Universal", page_icon="🌍")

# 3. Sidebar (Identitas & Monetisasi)
with st.sidebar:
    st.title("🌍 Yulian Universal")
    st.info("AI cerdas untuk semua. Masukkan pertanyaan di kolom utama.")
    st.markdown("""
    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; border: 1px solid #00ff00;">
        <p style="color: #00ff00; font-size: 14px;"><b>IKLAN PRABAYAR</b></p>
        <p style="color: white; font-size: 12px;">Dukung pengembangan AI ini melalui:</p>
        <a href="https://karyakarsa.com/yulianproject" target="_blank" style="color: #ff4b4b; text-decoration: none;">👉 <b>KaryaKarsa Yulian Project</b></a>
    </div>
    """, unsafe_allow_html=True)
    st.write("---")
    st.write("👤 **Developer:** Slamet Yulianto")
    # Tempat menaruh API KEY agar AI Aktif (Ambil di Google AI Studio)
    api_key = st.text_input("Sistem Key (API):", type="password", help="Masukkan API Key Gemini untuk mengaktifkan AI")

# 4. Konten Utama
st.title("🤖 Yulian AI - Asisten Universal")
st.write("Tanyakan apa saja. AI akan menjawab dengan teks, suara, dan referensi.")

prompt = st.text_input("Apa yang ingin kamu ketahui hari ini?")

if prompt:
    if not api_key:
        st.warning("⚠️ Mohon masukkan API Key di sidebar untuk mengaktifkan kecerdasan universal.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            with st.spinner('Yulian AI sedang berpikir...'):
                response = model.generate_content(f"Jelaskan secara ringkas tentang {prompt} dalam bahasa Indonesia dan sertakan minimal 2 sumber referensi di akhir jawaban.")
                hasil_teks = response.text
                
                st.subheader("💡 Jawaban:")
                st.write(hasil_teks)
                
                # Tombol Suara
                if st.button("🔊 Dengarkan Jawaban"):
                    # Kita ambil 200 karakter pertama agar suara tidak terlalu panjang/error
                    bicara(hasil_teks[:300])
                    
        except Exception as e:
            st.error(f"Terjadi kesalahan sistem: {e}")

# 5. Footer WhatsApp untuk Bisnis/Iklan
st.write("---")
st.link_button("Pasang Iklan / Hubungi Admin", "https://wa.me/628xxxxxxxxxx")

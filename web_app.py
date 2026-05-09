import streamlit as st
import os
import sys
from dotenv import load_dotenv

# 1. Setup Path 
root_path = os.path.abspath(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

load_dotenv()

from src.retrieval.retriever import Retriever
from src.generation.generator import Generator

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SHAVIRA AI", page_icon="🤖", layout="centered")

st.title("🤖 SHAVIRA")
st.caption("Virtual Campus Assistant - Powered by RAG & OpenAI")

# --- INISIALISASI SESSION STATE ---
if "retriever" not in st.session_state:
    db_path = os.path.join(root_path, "storage", "chroma_db")
    st.session_state.retriever = Retriever(db_path=db_path)
    # Gunakan generator dari session state
    st.session_state.generator = Generator(model_name="gpt-4o-mini")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- TAMPILKAN HISTORY CHAT ---
# Loop ini akan merender ulang semua pesan yang tersimpan setiap kali script berjalan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "references" in message and message["references"]:
            with st.expander("Lihat Sumber Referensi"):
                st.markdown(message["references"])

# --- INPUT USER ---
if prompt := st.chat_input("Apa yang ingin Anda tanyakan?"):
    # 1. Tampilkan & Simpan Pesan User
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Jalankan Logika RAG
    with st.chat_message("assistant"):
        with st.spinner("Mencari di dokumen..."):
            nodes = st.session_state.retriever.search(prompt)
            
            if nodes:
                response = st.session_state.generator.generate(prompt, nodes)
                
                # Format Referensi
                ref_text = ""
                for i, node in enumerate(nodes):
                    fname = node.metadata.get('file_name', 'Unknown')
                    page = node.metadata.get('page_label', '?')
                    chunk_content = node.get_content() if hasattr(node, 'get_content') else getattr(node, 'text', 'No content')
                    
                    ref_text += f"**Sumber {i+1}: {fname} (Hal: {page})**\n"
                    ref_text += f"```text\n{chunk_content}\n```\n"
                    ref_text += "---\n"

                # Tampilkan Jawaban Assistant
                st.markdown(response)
                with st.expander("Lihat Detail Chunking & Referensi"):
                    st.markdown(ref_text)
                
                # 3. Simpan Jawaban Assistant ke History
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "references": ref_text
                })
            else:
                error_msg = "Maaf, saya tidak menemukan informasi tersebut dalam dokumen saya."
                st.warning(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # PENTING: Force rerun agar loop 'Tampilkan History' di atas menangkap pesan terbaru
    st.rerun()
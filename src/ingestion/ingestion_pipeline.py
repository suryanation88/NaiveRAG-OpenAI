import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from loader import PDFLoader
from chunking import chunk_documents
from embedder import save_to_vector_store

def run_ingestion_pipeline(data_path="data/raw"):
    print(f"\n[1/3] Memulai pemindaian direktori: {data_path}")
    
    # 1. Load & Chunk
    loader_obj = PDFLoader()
    try:
        docs_gen = loader_obj.load_directory(data_path, save_cleaned=True, cleaned_dir="data/cleaned")
        chunks_gen = chunk_documents(docs_gen, save_to_json=True, chunk_dir="data/chunk")
        
        # 2. Konversi ke List
        all_chunks = list(chunks_gen)
        print(f"[2/3] Ekstraksi selesai. Terbentuk {len(all_chunks)} chunks.")

        if len(all_chunks) > 0:
            # 3. Simpan ke Vector Store
            print("[3/3] Memasukkan data ke ChromaDB...")
            index = save_to_vector_store(all_chunks)
            print("\n[SUKSES] Database telah diperbarui dan siap digunakan!")
            return index
        else:
            print("[PERINGATAN] Tidak ada data baru yang diproses. Pastikan PDF tidak kosong.")
            return None

    except Exception as e:
        print(f"[ERROR] Pipeline gagal: {e}")
        return None

if __name__ == "__main__":
    run_ingestion_pipeline()
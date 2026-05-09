import os
import chromadb
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document as LlamaDocument
from typing import List

EMBED_MODEL_NAME = "intfloat/multilingual-e5-small"

def save_to_vector_store(documents: List[LlamaDocument], db_path: str = "storage/chroma_db"):
    if not documents:
        print("[Warning] Tidak ada dokumen untuk disimpan.")
        return None

    # 1. Pastikan direktori ada
    os.makedirs(db_path, exist_ok=True)

    # 2. Inisialisasi Chroma secara manual untuk memastikan Collection tercipta
    db = chromadb.PersistentClient(path=db_path)
    # Gunakan get_or_create agar tidak error jika dijalankan ulang
    chroma_collection = db.get_or_create_collection("campus_rag_collection")

    # 3. Hubungkan ke LlamaIndex
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. Inisialisasi model embedding
    embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)

    print(f"[INFO] Memulai proses embedding untuk {len(documents)} chunks...")
    
    # 5. Build Index
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress_bar=True
    )

    # CRITICAL: Paksa simpan ke disk
    storage_context.persist(persist_dir=db_path)
    
    print(f"[SUCCESS] {chroma_collection.count()} data tersimpan di {db_path}")
    return index
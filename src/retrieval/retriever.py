import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

class Retriever:
    def __init__(self, db_path="storage/chroma_db", model_name="text-embedding-ada-002"):
        self.embed_model = OpenAIEmbedding(model=model_name)
        self.db = chromadb.PersistentClient(path=db_path)
        self.chroma_collection = self.db.get_collection("campus_rag_collection")
        
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.index = VectorStoreIndex.from_vector_store(
            self.vector_store, 
            embed_model=self.embed_model
        )
        
    def search(self, query_str, top_k=3):
        # Mengambil potongan teks paling relevan
        retriever = self.index.as_retriever(similarity_top_k=top_k)
        return retriever.retrieve(query_str)
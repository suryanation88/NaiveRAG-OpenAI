from llama_index.llms.openai import OpenAI
from llama_index.core import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

class Generator:
    def __init__(self, model_name="gpt-4o-mini"):
        self.llm = OpenAI(model=model_name)
        
        # Template yang memaksa LLM menyebutkan sumber
        self.qa_template = PromptTemplate(
            "Anda adalah asisten akademik virtual Universitas. "
            "Gunakan informasi berikut untuk menjawab pertanyaan.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "TUGAS:\n"
            "1. Jawab pertanyaan berdasarkan konteks yang diberikan.\n"
            "2. Di akhir jawaban, buatkan bagian 'REFERENSI DOKUMEN' yang mencantumkan nama file dan nomor halaman.\n"
            "3. Jika tidak ada di konteks, katakan data tidak tersedia.\n\n"
            "Pertanyaan: {query_str}\n"
            "Jawaban:"
        )

    def generate(self, query_str, nodes):
        context_list = []
        for node in nodes:
            content = node.get_content()
            source = node.metadata.get('file_name', 'Unknown')
            page = node.metadata.get('page_label', '-')
            # Menyuntikkan informasi sumber ke dalam teks yang dibaca LLM
            context_list.append(f"[Sumber: {source}, Hal: {page}]\nIsi: {content}")
        
        context_str = "\n\n".join(context_list)
        
        final_prompt = self.qa_template.format(context_str=context_str, query_str=query_str)
        response = self.llm.complete(final_prompt)
        return response
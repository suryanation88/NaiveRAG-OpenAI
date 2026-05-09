import os
import re
import pymupdf4llm
import hashlib
import json
from pathlib import Path
from typing import Generator
from llama_index.core import Document as LlamaDocument

class PDFLoader:
    def __init__(self):
        pass

    def _clean_text(self, text: str) -> str:
        """Pembersihan teks tingkat lanjut."""
        #Hapus spasi di akhir setiap baris (trailing spaces)
        text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
        
        #Batasi baris kosong berlebih (maksimal 2 baris baru berurutan)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        #Hapus pagination 
        text = re.sub(r'(?i)(halaman|page)\s+\d+\s+(dari|of)\s+\d+', '', text)
        
        return text.strip()

    def _generate_file_id(self, path: str) -> str:
        """Membuat ID unik berdasarkan konten file untuk deteksi duplikasi."""
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()

    def load_pdf(self, path: str, save_cleaned: bool = False, cleaned_dir: str = "data/cleaned") -> Generator[LlamaDocument, None, None]:
        if not os.path.isfile(path):
            print(f"[Error] File tidak ditemukan: {path}")
            return

        file_id = self._generate_file_id(path)
        
        try:
            md_text = pymupdf4llm.to_markdown(path)
            cleaned_text = self._clean_text(md_text)

            if cleaned_text:
                metadata = {
                    "file_name": os.path.basename(path),
                    "file_id": file_id,
                    "file_path": path,
                    "category": "raw_document"
                }
                
                if save_cleaned:
                    cleaned_dir_path = Path(cleaned_dir)
                    cleaned_dir_path.mkdir(parents=True, exist_ok=True)
                    
                    source_name = Path(path).stem
                    json_filename = f"{source_name}.json"
                    
                    with open(cleaned_dir_path / json_filename, "w", encoding="utf-8") as f:
                        json.dump({
                            "text": cleaned_text,
                            "metadata": metadata
                        }, f, ensure_ascii=False, indent=2)

                yield LlamaDocument(
                    text=cleaned_text,
                    metadata=metadata
                )
        except Exception as e:
            print(f"[Fatal Error] Gagal memproses {path}: {e}")

    def load_directory(self, raw_dir: str, save_cleaned: bool = False, cleaned_dir: str = "data/cleaned") -> Generator[LlamaDocument, None, None]:
        """Generator untuk memproses seluruh folder tanpa membebani RAM."""
        if not os.path.exists(raw_dir):
            print(f"[Error] Folder {raw_dir} tidak ada.")
            return

        for filename in os.listdir(raw_dir):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(raw_dir, filename)
                print(f"[PROCESS] Mengambil data dari: {filename}")
                yield from self.load_pdf(full_path, save_cleaned=save_cleaned, cleaned_dir=cleaned_dir)
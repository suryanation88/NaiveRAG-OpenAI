# SHAVIRA AI - Virtual Campus Assistant 🤖

SHAVIRA (Simple & Helpful Virtual Assistant) adalah aplikasi **Retrieval-Augmented Generation (RAG)** yang dirancang untuk membantu mahasiswa dan civitas akademik dalam mencari informasi dari dokumen internal kampus (seperti PDF peraturan, panduan akademik, dll) secara akurat menggunakan model bahasa OpenAI.

## Fitur Utama

- **Akurasi Tinggi**: Menggunakan teknik RAG untuk memastikan jawaban hanya didasarkan pada dokumen referensi yang valid.
- **Referensi Otomatis**: Setiap jawaban mencantumkan nama file dan nomor halaman sumber informasi.
- **Pipeline Ingestion Otomatis**: Secara otomatis memproses file PDF baru dari folder `data/raw`, melakukan pembersihan, chunking, dan indexing ke ChromaDB.
- **Dua Antarmuka**: 
  - **Web UI**: Interface interaktif berbasis Streamlit.
  - **CLI (Terminal)**: Akses cepat melalui baris perintah.
- **Hybrid Storage**: Data teks yang telah dibersihkan dan di-chunk disimpan dalam folder `data/` untuk transparansi.

## Tech Stack

- **Framework**: [LlamaIndex](https://www.llamaindex.ai/)
- **Large Language Model**: OpenAI (GPT-4o-mini)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Web UI**: [Streamlit](https://streamlit.io/)
- **Parser**: PyMuPDF4LLM
- **Embeddings**: HuggingFace (sentence-transformers)

## Struktur Proyek

```text
RAG-GPT/
├── app/                # Logika aplikasi CLI
├── data/
│   ├── raw/            # Tempat menaruh file PDF asli
│   ├── cleaned/        # Hasil ekstraksi teks bersih
│   └── chunk/          # Hasil pemotongan teks (JSON)
├── src/
│   ├── ingestion/      # Pipeline pengolahan dokumen
│   ├── retrieval/      # Logika pencarian dokumen relevan
│   └── generation/     # Logika pembuatan jawaban (LLM)
├── storage/            # Database ChromaDB
├── web_app.py          # Dashboard Streamlit
├── run.py              # Entry point utama
└── requirements.txt    # Daftar dependensi
```

## Instalasi

1. **Clone Repository**:
   ```bash
   git clone https://github.com/username/RAG-GPT.git
   cd RAG-GPT
   ```

2. **Buat Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Environment**:
   Buat file `.env` di root direktori dan masukkan API Key Anda:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

## Cara Menjalankan

### 1. Ingest Data (Opsional)
Taruh file PDF Anda di folder `data/raw/`. Sistem akan otomatis melakukan ingestion saat dijalankan melalui `run.py`, atau Anda bisa menjalankan pipeline secara manual:
```bash
python src/ingestion/ingestion_pipeline.py
```

### 2. Jalankan via Web UI (Rekomendasi)
```bash
streamlit run web_app.py
```

### 3. Jalankan via Terminal (CLI)
```bash
python run.py
```

## Lisensi
Proyek ini dikembangkan untuk keperluan penelitian dan akademik. Silakan gunakan dan modifikasi sesuai kebutuhan.



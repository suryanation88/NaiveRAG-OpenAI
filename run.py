import os
from src.ingestion.ingestion_pipeline import run_ingestion_pipeline

def start():
    print("Memeriksa pembaruan dokumen...")
    run_ingestion_pipeline() 
    
    print("Menjalankan SHAVIRA...")
    os.system("python -m app.main")

if __name__ == "__main__":
    start()
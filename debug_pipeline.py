"""Script debug untuk cek kenapa pipeline masih re-embed."""
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "ingestion"))

from ingestion_pipeline import _get_chroma_count, _load_manifest, _find_new_or_changed_files

print("=== DEBUG PIPELINE ===\n")

# 1. Cek ChromaDB
count = _get_chroma_count()
print(f"1. ChromaDB count: {count}")
print(f"   -> {'OK, data ada' if count > 0 else 'KOSONG! Ini penyebab re-embed'}")

# 2. Cek Manifest
manifest = _load_manifest()
print(f"\n2. Manifest: {len(manifest)} file terdaftar")
for fname, info in manifest.items():
    print(f"   - {fname}: hash={info['hash'][:12]}...")

# 3. Cek perubahan
changed = _find_new_or_changed_files("data/raw", manifest)
print(f"\n3. File berubah/baru: {len(changed)}")
for f in changed:
    print(f"   - [{('BARU' if f['is_new'] else 'BERUBAH')}] {f['filename']}")

# 4. Kesimpulan
print("\n=== KESIMPULAN ===")
if not changed and count > 0:
    print("SEHARUSNYA SKIP! Pipeline tidak perlu re-embed.")
elif changed:
    print(f"ADA {len(changed)} FILE BERUBAH, pipeline perlu re-embed file tersebut.")
elif count == 0:
    print("CHROMADB KOSONG, pipeline perlu embed dari awal.")

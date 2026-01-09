import os, pickle
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

PDF_DIR = "data_pdfs"
OUT_DIR = "vector_db"
os.makedirs(OUT_DIR, exist_ok=True)

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
docs = []

for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        reader = PdfReader(os.path.join(PDF_DIR, file))
        for page in reader.pages:
            text = page.extract_text()
            if text and len(text) > 100:
                docs.append(text)

embs = model.encode(docs)
index = faiss.IndexFlatL2(embs.shape[1])
index.add(np.array(embs).astype("float32"))

faiss.write_index(index, f"{OUT_DIR}/index.faiss")
with open(f"{OUT_DIR}/docs.pkl", "wb") as f:
    pickle.dump(docs, f)

print("✅ ĐÃ TẠO VECTOR DATABASE")

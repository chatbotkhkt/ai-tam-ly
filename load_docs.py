import os
from pypdf import PdfReader

def load_all_docs(folder="data_pdfs"):
    texts = []
    for f in os.listdir(folder):
        if f.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder, f))
            for page in reader.pages:
                texts.append(page.extract_text())
    return "\n".join(texts)

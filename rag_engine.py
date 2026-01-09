import os
import faiss
import pickle
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

MODEL = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def load_vector_db():
    index = faiss.read_index("vector_db/index.faiss")
    with open("vector_db/docs.pkl", "rb") as f:
        docs = pickle.load(f)
    return index, docs

def retrieve_context(query, top_k=3):
    index, docs = load_vector_db()
    q_emb = MODEL.encode([query])
    D, I = index.search(np.array(q_emb).astype("float32"), top_k)
    return "\n\n".join([docs[i] for i in I[0]])

def chat_ai(question, user_context=""):
    doc_context = retrieve_context(question)

    prompt = f"""
Bạn là AI tư vấn tâm lý học đường.
Ưu tiên dùng tài liệu khoa học được cung cấp.

Thông tin người dùng:
{user_context}

Tài liệu tham khảo:
{doc_context}

Câu hỏi:
{question}

Trả lời bằng tiếng Việt, nhẹ nhàng, không phán xét.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return res.choices[0].message.content

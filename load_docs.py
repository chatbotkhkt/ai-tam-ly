import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

DATA_DIR = "data_pdfs"
DB_DIR = "vector_db"

def build_vector_store():
    documents = []

    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_DIR, file))
            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    db = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    db.persist()
    return db


def load_vector_store():
    embeddings = OpenAIEmbeddings()
    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )

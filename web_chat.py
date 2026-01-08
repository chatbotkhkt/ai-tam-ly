import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from load_docs import build_vector_store, load_vector_store
from prompt import SYSTEM_PROMPT

load_dotenv()

st.set_page_config(page_title="AI Tư vấn tâm lý", layout="wide")

st.title("🧠 AI Tư vấn tâm lý (Đọc tài liệu của bạn)")

if "db" not in st.session_state:
    st.session_state.db = None

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📄 Tài liệu PDF")

    if st.button("🔄 Tạo / Cập nhật dữ liệu"):
        with st.spinner("Đang đọc PDF và tạo vector..."):
            st.session_state.db = build_vector_store()
        st.success("✅ Đã sẵn sàng")

# Chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

user_input = st.chat_input("Bạn đang cảm thấy thế nào?")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("AI đang suy nghĩ..."):
        if st.session_state.db is None:
            db = load_vector_store()
            st.session_state.db = db
        else:
            db = st.session_state.db

        docs = db.similarity_search(user_input, k=4)
        context = "\n\n".join([d.page_content for d in docs])

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)

        prompt = f"""
{SYSTEM_PROMPT}

Dưới đây là nội dung từ tài liệu:
{context}

Câu hỏi người dùng:
{user_input}
"""

        response = llm.invoke(prompt)

    st.chat_message("assistant").markdown(response.content)
    st.session_state.messages.append(
        {"role": "assistant", "content": response.content}
    )

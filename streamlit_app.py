import streamlit as st
from openai import OpenAI
import time

# ================== CONFIG ==================
st.set_page_config(page_title="AI Tư vấn tâm lý", layout="centered")

# ================== API KEY ==================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ Chưa cấu hình OPENAI_API_KEY trong Streamlit Secrets")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ================== QUESTIONS ==================
QUESTIONS = [
    "Tôi dễ bị bực bội dễ dàng.",
    "Tôi thường nóng giận.",
    "Khi tức giận, tôi dễ nổi xung với người khác.",
    "Tôi nghĩ rằng nếu ai đó xúc phạm mình, họ đáng bị đánh lại.",
    "Tôi khó kiểm soát hành vi khi tức giận.",
    "Tôi hay la hét khi bực mình.",
    "Tôi từng làm hỏng đồ vì tức giận.",
    "Tôi thấy khó kiềm chế cảm xúc.",
    "Tôi dễ cáu gắt vì những việc nhỏ.",
    "Tôi cảm thấy hối hận sau khi nổi nóng.",
    "Tôi thường giữ cơn giận trong lòng.",
    "Tôi hay suy nghĩ tiêu cực khi tức giận.",
    "Tôi cảm thấy mất kiểm soát khi bị khiêu khích.",
    "Tôi thường phản ứng ngay khi tức giận.",
    "Tôi khó bình tĩnh lại sau cơn giận.",
    "Tôi thấy căng thẳng kéo dài.",
    "Tôi hay mất ngủ vì suy nghĩ nhiều.",
    "Tôi cảm thấy áp lực trong cuộc sống.",
    "Tôi dễ bị stress.",
    "Tôi cảm thấy khó thích nghi với thay đổi."
]

OPTIONS = [
    "Hoàn toàn không đúng",
    "Không đúng lắm",
    "Phân vân",
    "Khá đúng",
    "Rất đúng"
]

SCORE_MAP = {
    "Hoàn toàn không đúng": 1,
    "Không đúng lắm": 2,
    "Phân vân": 3,
    "Khá đúng": 4,
    "Rất đúng": 5
}

# ================== SESSION ==================
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "aq_result" not in st.session_state:
    st.session_state.aq_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================== UI ==================
st.title("🧠 AI TƯ VẤN TÂM LÝ")
st.header("PHẦN 1. TRẮC NGHIỆM HÀNH VI (AQ)")

answers = []
for i, q in enumerate(QUESTIONS):
    ans = st.radio(f"{i+1}. {q}", OPTIONS, key=f"q{i}")
    answers.append(ans)

st.divider()
st.header("✍️ PHẦN 2. CÂU HỎI TỰ LUẬN")

story = st.text_area("Hãy chia sẻ câu chuyện của bạn")
need = st.text_area("Bạn cần chúng tôi hỗ trợ gì không?")

# ================== SUBMIT ==================
if st.button("📨 GỬI KHẢO SÁT"):
    score = sum(SCORE_MAP[a] for a in answers)
    level = "Thấp" if score <= 40 else "Trung bình" if score <= 70 else "Cao"

    prompt = f"""
Bạn là chuyên gia tư vấn tâm lý.

Điểm AQ: {score} ({level})
Câu chuyện: {story}
Nhu cầu: {need}

Hãy:
- Giải thích ý nghĩa điểm AQ
- Liên hệ câu chuyện
- Đưa lời khuyên thực tế
- Không chẩn đoán y khoa
"""

    with st.spinner("🤖 AI đang phân tích..."):
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

    st.session_state.aq_result = {
        "score": score,
        "level": level,
        "content": res.choices[0].message.content
    }
    st.session_state.submitted = True

# ================== RESULT ==================
if st.session_state.submitted:
    st.divider()
    st.header("📊 KẾT QUẢ ĐÁNH GIÁ")
    st.write(f"**Điểm AQ:** {st.session_state.aq_result['score']} ({st.session_state.aq_result['level']})")
    st.success(st.session_state.aq_result["content"])

# ================== CHAT ==================
if st.session_state.submitted:
    st.divider()
    st.header("💬 Trò chuyện với AI tư vấn")

    user_msg = st.text_input("Nhập câu hỏi của bạn")

    if user_msg:
        st.session_state.chat_history.append(("Bạn", user_msg))

        chat_prompt = f"""
Bạn là AI tư vấn tâm lý.
KHÔNG nhắc lại kết quả AQ.
Chỉ trả lời câu hỏi sau:

{user_msg}
"""

        with st.spinner("AI đang suy nghĩ..."):
            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": chat_prompt}],
                temperature=0.7
            )

        ai_msg = res.choices[0].message.content
        st.session_state.chat_history.append(("AI", ai_msg))

    for role, msg in st.session_state.chat_history:
        st.markdown(f"**{role}:** {msg}")

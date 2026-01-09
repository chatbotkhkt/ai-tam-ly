import streamlit as st
from openai import OpenAI
import time

# =========================
# CẤU HÌNH
# =========================
st.set_page_config(
    page_title="AI Tư vấn tâm lý",
    layout="centered"
)

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

# =========================
# SESSION STATE
# =========================
if "aq_done" not in st.session_state:
    st.session_state.aq_done = False

if "aq_result" not in st.session_state:
    st.session_state.aq_result = ""

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# =========================
# DỮ LIỆU CÂU HỎI AQ (20 CÂU)
# =========================
questions = [
    "1. Tôi bị bực bội dễ dàng.",
    "2. Tôi thường nóng giận.",
    "3. Khi tức giận, tôi dễ nổi xung với người khác.",
    "4. Tôi nghĩ rằng nếu ai đó xúc phạm mình, họ đáng bị đánh lại.",
    "5. Tôi dễ mất bình tĩnh.",
    "6. Tôi khó kiểm soát cảm xúc khi căng thẳng.",
    "7. Tôi hay quát mắng người khác.",
    "8. Tôi cảm thấy khó chịu khi mọi việc không theo ý mình.",
    "9. Tôi thường hối hận sau khi nổi giận.",
    "10. Tôi dễ cáu gắt với người thân.",
    "11. Tôi khó giữ bình tĩnh khi bị chỉ trích.",
    "12. Tôi dễ nổi nóng trong giao tiếp.",
    "13. Tôi hay phản ứng mạnh khi bị áp lực.",
    "14. Tôi thường to tiếng khi tranh luận.",
    "15. Tôi thấy khó kiềm chế cơn giận.",
    "16. Tôi dễ bùng nổ cảm xúc.",
    "17. Tôi thường mất kiểm soát hành vi khi tức giận.",
    "18. Tôi thấy mình thiếu kiên nhẫn.",
    "19. Tôi dễ phản ứng tiêu cực.",
    "20. Tôi hay để cảm xúc chi phối hành động."
]

options = [
    "Hoàn toàn không đúng",
    "Không đúng lắm",
    "Phân vân",
    "Khá đúng",
    "Rất đúng"
]

scores = {
    "Hoàn toàn không đúng": 0,
    "Không đúng lắm": 1,
    "Phân vân": 2,
    "Khá đúng": 3,
    "Rất đúng": 4
}

# =========================
# GIAO DIỆN
# =========================
st.title("🧠 AI TƯ VẤN TÂM LÝ")
st.markdown("### PHẦN 1. TRẮC NGHIỆM HÀNH VI (AQ)")

answers = []

for q in questions:
    ans = st.radio(q, options, index=0, key=q)
    answers.append(scores[ans])

st.markdown("---")
st.markdown("### ✍️ PHẦN 2. CÂU HỎI TỰ LUẬN")

story = st.text_area("Hãy chia sẻ câu chuyện của bạn", height=120)
need = st.text_area("Bạn cần chúng tôi hỗ trợ gì không?", height=120)

# =========================
# SUBMIT
# =========================
if st.button("📤 GỬI KHẢO SÁT"):
    aq_score = sum(answers)

    if aq_score <= 20:
        level = "Thấp"
    elif aq_score <= 50:
        level = "Trung bình"
    else:
        level = "Cao"

    with st.spinner("🤖 AI đang phân tích..."):
        time.sleep(1.5)
        prompt = f"""
Bạn là chuyên gia tâm lý học đường.

Điểm AQ: {aq_score} ({level})
Câu chuyện: {story}
Nhu cầu: {need}

Hãy:
- Giải thích ý nghĩa điểm AQ
- Phân tích vấn đề
- Đưa ra 3–5 lời khuyên thực tế
- Văn phong nhẹ nhàng, dễ hiểu
"""

        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.session_state.aq_result = res.choices[0].message.content
        st.session_state.aq_done = True

# =========================
# KẾT QUẢ (HIỂN THỊ 1 LẦN)
# =========================
if st.session_state.aq_done:
    st.markdown("---")
    st.subheader("📊 KẾT QUẢ ĐÁNH GIÁ")
    st.success(st.session_state.aq_result)

# =========================
# CHAT – CHỈ DÙNG ĐỂ HỎI TIẾP
# =========================
if st.session_state.aq_done:
    st.markdown("---")
    st.subheader("💬 Trò chuyện với AI tư vấn")

    for msg in st.session_state.chat_messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Nhập câu hỏi tiếp theo...")

    if user_input:
        st.session_state.chat_messages.append(
            {"role": "user", "content": user_input}
        )

        with st.spinner("AI đang suy nghĩ..."):
            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.chat_messages
            )

        ai_reply = res.choices[0].message.content
        st.session_state.chat_messages.append(
            {"role": "assistant", "content": ai_reply}
        )

        st.rerun()

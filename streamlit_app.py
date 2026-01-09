import streamlit as st
import os
from openai import OpenAI

# =====================
# CẤU HÌNH TRANG
# =====================
st.set_page_config(
    page_title="AI Tư vấn tâm lý",
    layout="centered"
)

st.title("AI TƯ VẤN TÂM LÝ")

# =====================
# API KEY
# =====================
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# =====================
# LOAD TÀI LIỆU OCR / PDF TEXT
# =====================
def load_docs():
    text = ""
    if os.path.exists("ocr_texts"):
        for f in os.listdir("ocr_texts"):
            if f.endswith(".txt"):
                with open(os.path.join("ocr_texts", f), encoding="utf-8") as file:
                    text += file.read() + "\n"
    return text

DOC_TEXT = load_docs()[:4000]

# =====================
# CÂU HỎI AQ (20 CÂU – GIỮ NGUYÊN)
# =====================
AQ_QUESTIONS = [
    "1. Tôi bị bực bội dễ dàng.",
    "2. Tôi thường nóng giận.",
    "3. Khi tức giận, tôi dễ nói xung với người khác.",
    "4. Tôi nghĩ rằng nếu ai đó xúc phạm mình, họ đáng bị đánh lại.",
    "5. Tôi dễ mất bình tĩnh.",
    "6. Tôi hay cáu gắt.",
    "7. Tôi thường không kiềm chế được cảm xúc.",
    "8. Tôi phản ứng mạnh khi bị chê trách.",
    "9. Tôi hay đập đồ khi tức giận.",
    "10. Tôi khó bình tĩnh khi tranh cãi.",
    "11. Tôi hay quát mắng người khác.",
    "12. Tôi cảm thấy khó chịu kéo dài.",
    "13. Tôi dễ nổi nóng khi mệt.",
    "14. Tôi khó tha thứ khi bị làm tổn thương.",
    "15. Tôi thường hành động trước khi suy nghĩ.",
    "16. Tôi dễ nổi cáu khi không được như ý.",
    "17. Tôi khó kiểm soát hành vi khi căng thẳng.",
    "18. Tôi hay tức giận vì chuyện nhỏ.",
    "19. Tôi khó giữ bình tĩnh trong xung đột.",
    "20. Tôi dễ mất kiểm soát hành vi."
]

OPTIONS = [
    "Hoàn toàn không đúng",
    "Không đúng lắm",
    "Phân vân",
    "Khá đúng",
    "Rất đúng"
]

SCORE_MAP = {
    "Hoàn toàn không đúng": 0,
    "Không đúng lắm": 1,
    "Phân vân": 2,
    "Khá đúng": 3,
    "Rất đúng": 4
}

# =====================
# STATE
# =====================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "chat" not in st.session_state:
    st.session_state.chat = []

# =====================
# PHẦN 1 – TRẮC NGHIỆM AQ
# =====================
st.header("PHẦN 1. TRẮC NGHIỆM HÀNH VI (AQ)")

answers = []

for q in AQ_QUESTIONS:
    ans = st.radio(q, OPTIONS, index=0)
    answers.append(SCORE_MAP[ans])

# =====================
# PHẦN 2 – TỰ LUẬN
# =====================
st.header("PHẦN 2. CÂU HỎI TỰ LUẬN")

story = st.text_area("1. Hãy chia sẻ câu chuyện của bạn", height=120)
need = st.text_area("2. Bạn cần chúng tôi hỗ trợ gì không?", height=120)

# =====================
# TÍNH AQ
# =====================
def aq_level(score):
    if score <= 20:
        return "Thấp"
    elif score <= 40:
        return "Trung bình"
    else:
        return "Cao"

# =====================
# AI PHÂN TÍCH KẾT QUẢ
# =====================
def ai_analyze(score, level, story, need):
    prompt = f"""
Bạn là chuyên gia tư vấn tâm lý học đường.

Điểm AQ: {score} ({level})
Câu chuyện người dùng: {story}
Nhu cầu hỗ trợ: {need}

Yêu cầu:
- Giải thích vì sao điểm AQ như vậy
- Liên hệ trực tiếp với câu chuyện
- Đưa ra lời khuyên thực tế
- Không chẩn đoán y khoa
- Giọng nhẹ nhàng, động viên

Tài liệu tham khảo:
{DOC_TEXT}
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

# =====================
# GỬI KHẢO SÁT
# =====================
if st.button("📤 GỬI KHẢO SÁT"):
    st.session_state.submitted = True
    aq_score = sum(answers)
    level = aq_level(aq_score)

    st.subheader("📊 KẾT QUẢ ĐÁNH GIÁ")
    st.write(f"**Điểm AQ:** {aq_score} ({level})")

    with st.spinner("AI đang phân tích..."):
        result = ai_analyze(aq_score, level, story, need)

    st.success(result)

    st.session_state.chat.append(
        {"role": "assistant", "content": result}
    )

# =====================
# KHUNG CHAT – LUÔN Ở CUỐI
# =====================
if st.session_state.submitted:
    st.divider()
    st.header("💬 Trò chuyện với AI tư vấn")

    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f"👤 **Bạn:** {msg['content']}")
        else:
            st.markdown(f"🤖 **AI:** {msg['content']}")

    user_input = st.text_input("Nhập câu hỏi hoặc chia sẻ thêm...")

    if user_input:
        st.session_state.chat.append(
            {"role": "user", "content": user_input}
        )

        with st.spinner("AI đang suy nghĩ..."):
            follow_prompt = f"""
Tiếp tục tư vấn dựa trên:
- Điểm AQ
- Lịch sử trò chuyện
- Tài liệu tham khảo

Người dùng nói: {user_input}
"""
            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": follow_prompt}]
            )

        answer = res.choices[0].message.content
        st.session_state.chat.append(
            {"role": "assistant", "content": answer}
        )

        st.rerun()

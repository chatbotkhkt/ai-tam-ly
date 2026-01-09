import streamlit as st
from openai import OpenAI

# ================== CẤU HÌNH ==================
st.set_page_config(page_title="AI Tư vấn tâm lý", layout="centered")

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("❌ Chưa cấu hình OPENAI_API_KEY")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ================== SESSION STATE ==================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "aq_score" not in st.session_state:
    st.session_state.aq_score = 0

if "aq_level" not in st.session_state:
    st.session_state.aq_level = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ================== DỮ LIỆU AQ ==================
QUESTIONS = [
    "1. Tôi dễ bị bực bội.",
    "2. Tôi thường nóng giận.",
    "3. Khi tức giận, tôi dễ nói nặng lời.",
    "4. Tôi khó kiểm soát cảm xúc.",
    "5. Tôi hay cáu gắt với người thân.",
    "6. Tôi thấy khó bình tĩnh khi gặp áp lực.",
    "7. Tôi thường phản ứng mạnh với lời chỉ trích.",
    "8. Tôi khó kiềm chế khi không vừa ý.",
    "9. Tôi dễ nổi nóng vì chuyện nhỏ.",
    "10. Tôi hay hối hận sau khi nổi giận.",
    "11. Tôi khó tha thứ khi bị xúc phạm.",
    "12. Tôi hay giữ cảm xúc tiêu cực.",
    "13. Tôi thường suy nghĩ tiêu cực khi căng thẳng.",
    "14. Tôi khó thích nghi khi có thay đổi.",
    "15. Tôi dễ bị stress kéo dài.",
    "16. Tôi khó lấy lại bình tĩnh nhanh.",
    "17. Tôi hay lo lắng quá mức.",
    "18. Tôi cảm thấy áp lực ảnh hưởng đến cảm xúc.",
    "19. Tôi khó duy trì tinh thần tích cực.",
    "20. Tôi dễ mất kiểm soát cảm xúc."
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

# ================== GIAO DIỆN ==================
st.title("🧠 AI TƯ VẤN TÂM LÝ")
st.subheader("PHẦN 1. TRẮC NGHIỆM HÀNH VI (AQ)")

answers = []

for i, q in enumerate(QUESTIONS):
    ans = st.radio(q, OPTIONS, key=f"q{i}")
    answers.append(SCORE_MAP[ans])

story = st.text_area("📝 Hãy chia sẻ câu chuyện của bạn")
need = st.text_area("💬 Bạn cần chúng tôi hỗ trợ gì không?")

# ================== GỬI KHẢO SÁT ==================
if st.button("📤 GỬI KHẢO SÁT"):
    aq_score = sum(answers)

    if aq_score <= 25:
        level = "Thấp"
    elif aq_score <= 55:
        level = "Trung bình"
    else:
        level = "Cao"

    st.session_state.aq_score = aq_score
    st.session_state.aq_level = level
    st.session_state.submitted = True

    prompt = f"""
Bạn là chuyên gia tư vấn tâm lý.

Điểm AQ: {aq_score}
Mức AQ: {level}
Câu chuyện: {story}
Nhu cầu hỗ trợ: {need}

Hãy:
- Giải thích ý nghĩa điểm AQ
- Liên hệ với vấn đề người dùng
- Đưa ra lời khuyên nhẹ nhàng, không chẩn đoán y khoa
- Kết thúc bằng câu hỏi mở
"""

    with st.spinner("🤖 AI đang phân tích..."):
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

    st.session_state.chat_history = [
        {"role": "assistant", "content": res.choices[0].message.content}
    ]

# ================== HIỂN THỊ KẾT QUẢ ==================
if st.session_state.submitted:
    st.markdown("---")
    st.subheader("📊 KẾT QUẢ ĐÁNH GIÁ")
    st.write(f"**Điểm AQ:** {st.session_state.aq_score}")
    st.write(f"**Mức AQ:** {st.session_state.aq_level}")

    st.success(st.session_state.chat_history[0]["content"])

# ================== CHAT AI (LUÔN Ở CUỐI) ==================
if st.session_state.submitted:
    st.markdown("---")
    st.subheader("💬 Trò chuyện với AI tư vấn")

    for msg in st.session_state.chat_history[1:]:
        role = "👤 Bạn" if msg["role"] == "user" else "🤖 AI"
        st.markdown(f"**{role}:** {msg['content']}")

    user_msg = st.text_input(
        "Nhập câu hỏi của bạn",
        key="chat_input",
        placeholder="Ví dụ: tôi cảm thấy rất mệt mỏi..."
    )

    if user_msg:
        st.session_state.chat_history.append(
            {"role": "user", "content": user_msg}
        )

        with st.spinner("🤖 AI đang trả lời..."):
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.chat_history
            )

        st.session_state.chat_history.append(
            {"role": "assistant", "content": reply.choices[0].message.content}
        )

        # ✅ TỰ ĐỘNG XÓA INPUT SAU KHI CHAT
        st.session_state.chat_input = ""
        st.rerun()

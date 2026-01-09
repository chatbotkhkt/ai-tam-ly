import streamlit as st
from openai import OpenAI
import time

# ================= CONFIG =================
st.set_page_config(page_title="AI Tư vấn tâm lý", layout="centered")

# ================= API =================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("❌ Chưa cấu hình OPENAI_API_KEY")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ================= QUESTIONS =================
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
    OPTIONS[0]: 1,
    OPTIONS[1]: 2,
    OPTIONS[2]: 3,
    OPTIONS[3]: 4,
    OPTIONS[4]: 5
}

# ================= SESSION =================
for k in ["submitted", "locked", "result", "chat"]:
    if k not in st.session_state:
        st.session_state[k] = False if k != "chat" else []

# ================= UI =================
st.title("🧠 AI TƯ VẤN TÂM LÝ")
st.header("PHẦN 1. TRẮC NGHIỆM HÀNH VI (AQ)")

answers = []
for i, q in enumerate(QUESTIONS):
    answers.append(
        st.radio(f"{i+1}. {q}", OPTIONS, key=f"q{i}")
    )

st.divider()
st.header("✍️ PHẦN 2. CÂU HỎI TỰ LUẬN")
story = st.text_area("Hãy chia sẻ câu chuyện của bạn")
need = st.text_area("Bạn cần chúng tôi hỗ trợ gì không?")

# ================= SUBMIT =================
submit = st.button(
    "📨 GỬI KHẢO SÁT",
    disabled=st.session_state.locked
)

if submit and not st.session_state.submitted:
    st.session_state.locked = True  # 🔒 KHÓA NGAY

    try:
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

        st.session_state.result = {
            "score": score,
            "level": level,
            "content": res.choices[0].message.content
        }
        st.session_state.submitted = True

    except Exception as e:
        st.error("⚠️ Hệ thống đang bận, vui lòng thử lại sau")
        st.session_state.locked = False

# ================= RESULT =================
if st.session_state.submitted:
    st.divider()
    st.header("📊 KẾT QUẢ ĐÁNH GIÁ")
    st.write(f"**Điểm AQ:** {st.session_state.result['score']} ({st.session_state.result['level']})")
    st.success(st.session_state.result["content"])

# ================= CHAT =================
if st.session_state.submitted:
    st.divider()
    st.header("💬 Trò chuyện với AI tư vấn")

    msg = st.text_input("Nhập câu hỏi của bạn")

    if msg:
        st.session_state.chat.append(("Bạn", msg))

        with st.spinner("AI đang suy nghĩ..."):
            res = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": msg}],
                temperature=0.7
            )

        st.session_state.chat.append(("AI", res.choices[0].message.content))

    for r, m in st.session_state.chat:
        st.markdown(f"**{r}:** {m}")

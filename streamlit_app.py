import streamlit as st
from openai import OpenAI
from aq_scoring import score_aq

# =====================
# CẤU HÌNH
# =====================
st.set_page_config(
    page_title="AI tư vấn tâm lý",
    layout="centered"
)

st.title("AI tư vấn tâm lý")

# =====================
# OPENAI CLIENT
# =====================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =====================
# SESSION STATE
# =====================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =====================
# PHẦN 1: KHẢO SÁT AQ
# =====================
st.header("PHẦN 1. TRẮC NGHIỆM HÀNH VI (AQ)")

answers = []
options = [
    "Hoàn toàn không đúng",
    "Không đúng lắm",
    "Phân vân",
    "Khá đúng",
    "Rất đúng"
]

for i in range(1, 6):
    ans = st.radio(
        f"**Câu {i}. Tôi dễ mất bình tĩnh.**",
        options,
        key=f"q{i}"
    )
    answers.append(options.index(ans) + 1)

# =====================
# PHẦN 2: TỰ LUẬN
# =====================
st.header("PHẦN 2. CÂU HỎI TỰ LUẬN")

story = st.text_area("**1. Hãy chia sẻ câu chuyện của bạn**")
need_help = st.text_area("**2. Bạn cần chúng tôi hỗ trợ gì không?**")

# =====================
# SUBMIT
# =====================
if st.button("📨 GỬI KHẢO SÁT"):
    score, level, explain = score_aq(answers)

    st.session_state.submitted = True
    st.session_state.score = score
    st.session_state.level = level
    st.session_state.explain = explain
    st.session_state.story = story
    st.session_state.need_help = need_help

# =====================
# KẾT QUẢ + CHAT
# =====================
if st.session_state.submitted:
    st.divider()
    st.subheader("KẾT QUẢ ĐÁNH GIÁ")

    st.write(f"📊 **Điểm AQ:** {st.session_state.score} ({st.session_state.level})")
    st.write(f"🧠 **Giải thích:** {st.session_state.explain}")

    st.success("Mình sẽ đồng hành và tư vấn cho bạn ngay bây giờ.")

    st.subheader("💬 Trò chuyện với AI tư vấn")

    user_input = st.text_input("Nhập câu hỏi hoặc chia sẻ thêm...")

    if user_input:
        prompt = f"""
        Bạn là AI tư vấn tâm lý.

        Thông tin người dùng:
        - Điểm AQ: {st.session_state.score}
        - Mức độ: {st.session_state.level}
        - Câu chuyện: {st.session_state.story}
        - Mong muốn hỗ trợ: {st.session_state.need_help}

        Câu hỏi tiếp theo của người dùng:
        {user_input}

        Hãy trả lời bằng tiếng Việt, nhẹ nhàng, giải thích rõ lý do và đưa lời khuyên thực tế.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content
        st.session_state.chat_history.append((user_input, answer))

    for u, a in st.session_state.chat_history:
        st.markdown(f"**🧑 Bạn:** {u}")
        st.markdown(f"**🤖 AI:** {a}")

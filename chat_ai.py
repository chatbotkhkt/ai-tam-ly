import openai
from load_docs import load_all_docs

DOC_TEXT = load_all_docs()

def ai_giai_thich_ket_qua(api_key, aq_score, aq_level, story, need):
    openai.api_key = api_key

    prompt = f"""
Bạn là chuyên gia tư vấn tâm lý học đường.

Dữ liệu khảo sát:
- Điểm AQ: {aq_score}
- Mức độ: {aq_level}
- Câu chuyện người dùng: {story}
- Nhu cầu hỗ trợ: {need}

Yêu cầu:
1. Giải thích vì sao điểm AQ này tương ứng với mức độ trên
2. Liên hệ trực tiếp với câu chuyện người dùng
3. Giải thích bằng ngôn ngữ dễ hiểu, nhẹ nhàng
4. Không chẩn đoán y khoa
5. Kết thúc bằng câu mời người dùng tiếp tục chia sẻ

Tài liệu tham khảo khoa học:
{DOC_TEXT[:4000]}
"""

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return res.choices[0].message.content


def ai_tu_van(api_key, aq_score, aq_level, story, need, chat_history, user_msg):
    openai.api_key = api_key

    messages = [
        {
            "role": "system",
            "content": f"""
Bạn là AI tư vấn tâm lý.
Ghi nhớ:
- AQ: {aq_score} ({aq_level})
- Câu chuyện: {story}
- Nhu cầu: {need}

Ưu tiên tài liệu khoa học sau:
{DOC_TEXT[:4000]}
"""
        }
    ]

    for r, c in chat_history:
        messages.append({"role": r, "content": c})

    messages.append({"role": "user", "content": user_msg})

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.6
    )

    return res.choices[0].message.content

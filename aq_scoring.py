def calculate_aq_scores(answers):
    """
    answers: list gồm 20 số (1–5)
    """
    return sum(answers)


def aq_level(score):
    if score <= 35:
        return "Thấp – Kiểm soát cảm xúc tốt"
    elif score <= 60:
        return "Trung bình – Đôi lúc khó kiểm soát"
    elif score <= 80:
        return "Cao – Dễ bị kích động"
    else:
        return "Rất cao – Cần hỗ trợ tâm lý chuyên sâu"

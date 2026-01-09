def score_aq(answers):
    """
    answers: list[int] (1–5)
    """
    total = sum(answers)

    if total <= 40:
        level = "Thấp"
        note = "Bạn có xu hướng kiểm soát hành vi tốt."
    elif total <= 70:
        level = "Trung bình"
        note = "Bạn có dấu hiệu căng thẳng ở mức vừa."
    else:
        level = "Cao"
        note = "Bạn dễ căng thẳng, cần hỗ trợ tâm lý."

    return total, level, note

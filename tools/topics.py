def extract_topics(text: str):
    topics = []
    if "order" in text:
        topics.append("order")
    if "refund" in text:
        topics.append("refund")
    if "payment" in text:
        topics.append("payment")
    if "delivery" in text:
        topics.append("delivery")
    if not topics:
        topics.append("general")

    return {"topics": topics}

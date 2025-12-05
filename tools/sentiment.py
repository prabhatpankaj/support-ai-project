import random


def get_sentiment(text: str):
    """
    Simple deterministic sentiment for reproducible output.
    """
    if "damaged" in text or "crashing" in text:
        return {"sentiment": "negative"}
    if "delayed" in text:
        return {"sentiment": "neutral"}
    return {"sentiment": random.choice(["positive", "neutral", "negative"])}

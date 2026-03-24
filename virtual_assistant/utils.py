from datetime import datetime


def current_time_str():
    return datetime.now().strftime("%I:%M %p")


def current_date_str():
    return datetime.now().strftime("%A, %d %B %Y")


def clean_query_text(text: str) -> str:
    if not text:
        return ""

    text = text.strip().lower()

    prefixes = [
        "who is ",
        "what is ",
        "what are ",
        "define ",
        "tell me about ",
        "search web for ",
        "search for ",
        "google ",
        "look up ",
        "lookup ",
    ]

    for prefix in prefixes:
        if text.startswith(prefix):
            return text[len(prefix):].strip()

    return text.strip()


def shorten_text(text: str, max_chars: int = 320) -> str:
    if not text:
        return "I couldn't find a short answer."

    text = " ".join(text.split())

    if len(text) <= max_chars:
        return text

    trimmed = text[:max_chars].rsplit(" ", 1)[0]
    return trimmed + "..."
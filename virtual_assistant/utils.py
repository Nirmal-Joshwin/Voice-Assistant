from datetime import datetime


def current_time_str():
    return datetime.now().strftime("%I:%M %p")


def current_date_str():
    return datetime.now().strftime("%A, %d %B %Y")


def clean_query_text(text):
    triggers = ["what is", "who is", "tell me", "search"]
    for t in triggers:
        if text.startswith(t):
            return text.replace(t, "").strip()
    return text
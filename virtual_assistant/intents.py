def detect_intent(text: str) -> str:
    if not text:
        return "unknown"

    t = text.lower().strip()

    if any(word in t for word in ["exit", "quit", "goodbye", "bye", "stop app", "close app"]):
        return "exit"

    if "time" in t:
        return "time"

    if "date" in t or "today" in t:
        return "date"

    if any(phrase in t for phrase in ["hello", "hi", "hey"]):
        return "greeting"

    if "how are you" in t:
        return "how_are_you"

    if "thank you" in t or "thanks" in t:
        return "thanks"

    if "help" in t:
        return "help"

    web_triggers = [
        "who is",
        "what is",
        "what are",
        "define",
        "tell me about",
        "search web for",
        "search for",
        "google",
        "look up",
        "lookup",
    ]
    if any(t.startswith(trigger) for trigger in web_triggers):
        return "web_summary"

    return "casual"
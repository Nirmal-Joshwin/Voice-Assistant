from intents import detect_intent
from utils import current_time_str, current_date_str, clean_query_text
from web_search import get_web_summary


class Assistant:
    def __init__(self):
        self.last_response = ""
        self.last_user_text = ""

    def handle(self, text: str):
        self.last_user_text = text or ""
        intent = detect_intent(text)

        if intent == "exit":
            response = "Goodbye."
            self.last_response = response
            return response, True

        if intent == "time":
            response = f"It is {current_time_str()}."
            self.last_response = response
            return response, False

        if intent == "date":
            response = f"Today is {current_date_str()}."
            self.last_response = response
            return response, False

        if intent == "greeting":
            response = "Hello. How can I help?"
            self.last_response = response
            return response, False

        if intent == "how_are_you":
            response = "I'm doing fine. Ready when you are."
            self.last_response = response
            return response, False

        if intent == "thanks":
            response = "You're welcome."
            self.last_response = response
            return response, False

        if intent == "help":
            response = (
                "You can ask me about the time, date, definitions, "
                "or tell me to search the web for a topic."
            )
            self.last_response = response
            return response, False

        if intent == "web_summary":
            query = clean_query_text(text)
            response = get_web_summary(query)
            self.last_response = response
            return response, False

        response = (
            "I can help with time, date, and short web summaries. "
            "Try asking what something is, or say search web for a topic."
        )
        self.last_response = response
        return response, False
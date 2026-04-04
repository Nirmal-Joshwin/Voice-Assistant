from system_control import *
from file_system import *
from web_search import *
from utils import *
from llm import *
from rapidfuzz import fuzz
import re

def fuzzy(text, options):
    return any(fuzz.partial_ratio(text, opt) > 70 for opt in options)


class Assistant:
    def handle(self, text):
        text = text.lower()

        if fuzzy(text, ["exit", "quit"]):
            return "Goodbye", True

        if fuzzy(text, ["time"]):
            return current_time_str(), False

        if fuzzy(text, ["date", "today"]):
            return current_date_str(), False

        # safer logic

        import re

        if "volume" in text or "sound" in text:
            # 🔥 set volume
            num = re.search(r'\d+', text)
            if num:
                return set_volume(num.group()), False

            # decrease
            if any(w in text for w in ["down", "decrease", "lower"]):
                return decrease_volume(), False

            # increase
            if any(w in text for w in ["up", "increase", "raise"]):
                return increase_volume(), False

            # mute
            if "mute" in text:
                return mute_volume(), False
            
        if "brightness" in text:
            import re
            num = re.search(r'\d+', text)
            if num:
                return set_brightness(num.group()), False

        if fuzzy(text, ["open", "launch"]):
            return open_app(text.replace("open", "").strip()), False

        if fuzzy(text, ["list files", "show files"]):
            return list_files(), False

        if "file details" in text:
            return file_details(text.split()[-1]), False

        if "open file" in text:
            return open_file(text.split()[-1]), False

        if fuzzy(text, ["what", "who", "search", "tell"]):
            query = clean_query_text(text)
            result = get_web_summary(query)

            if result == "No result found":
                return ask_llm(query), False

            return result, False

        # fallback → LLM
        if len(text.split()) > 2:
            return ask_llm(text), False

        return "I didn't understand that.", False
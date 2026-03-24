import requests
import wikipedia
from bs4 import BeautifulSoup
from utils import shorten_text

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def wikipedia_summary(query: str):
    try:
        return wikipedia.summary(query, sentences=2, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError as e:
        options = ", ".join(e.options[:5])
        return f"That topic is ambiguous. Some options are: {options}."
    except wikipedia.exceptions.PageError:
        return None
    except Exception:
        return None


def duckduckgo_instant_answer(query: str):
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 0,
        }
        resp = requests.get(url, params=params, headers=HEADERS, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        abstract = data.get("AbstractText")
        if abstract:
            return abstract

        related = data.get("RelatedTopics", [])
        for item in related:
            if isinstance(item, dict) and item.get("Text"):
                return item["Text"]

        return None
    except Exception:
        return None


def scrape_duckduckgo_snippet(query: str):
    try:
        url = "https://html.duckduckgo.com/html/"
        resp = requests.post(url, data={"q": query}, headers=HEADERS, timeout=8)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        snippet = soup.select_one(".result__snippet")
        if snippet:
            return snippet.get_text(" ", strip=True)

        return None
    except Exception:
        return None


def get_web_summary(query: str) -> str:
    query = query.strip()
    if not query:
        return "I need something to search for."

    wiki = wikipedia_summary(query)
    if wiki:
        return shorten_text(wiki)

    ddg = duckduckgo_instant_answer(query)
    if ddg:
        return shorten_text(ddg)

    snippet = scrape_duckduckgo_snippet(query)
    if snippet:
        return shorten_text(snippet)

    return "I couldn't find a reliable short answer for that."
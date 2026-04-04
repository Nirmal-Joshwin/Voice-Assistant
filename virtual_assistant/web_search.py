import wikipedia


def get_web_summary(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "No result found"
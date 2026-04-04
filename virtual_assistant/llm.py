import requests

API_KEY = "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"

def ask_llm(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/auto",
                "messages": [
                    {"role": "user", "content": f"""
Answer the following in maximum 2 sentences.
Be direct and concise.
No extra explanation.

{prompt}
"""}
                ]
            },
            timeout=20
        )

        data = response.json()

        # 🔥 DEBUG PRINT (temporary)
        print("API RESPONSE:", data)

        if "choices" in data:
            return data["choices"][0]["message"]["content"].strip()

        return "API returned unexpected response."

    except Exception as e:
        print("ERROR:", e)
        return "LLM unavailable (API error)."
import requests

LETTA_URL = "http://127.0.0.1:8283/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are a memory-augmented research assistant. "
    "Use stored memory when relevant."
)

def process_query(query: str):

    payload = {
        "model": "letta",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    }

    response = requests.post(LETTA_URL, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

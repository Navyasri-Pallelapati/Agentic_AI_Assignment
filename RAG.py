import json
import urllib.request
from pathlib import Path


def load_document():
    candidates = [
        Path("Sample document.txt"),
        Path("sample_document.txt"),
        Path(__file__).with_name("Sample document.txt"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.read_text(encoding="utf-8")
    return "No document found."


def generate_answer(prompt):
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
    }

    try:
        import requests

        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=5,
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception:
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.load(response)
                return result.get("response", "")
        except Exception:
            return "[offline fallback] Unable to reach the local LLM service."


if __name__ == "__main__":
    document = load_document()
    question = input("Enter your question: ").strip() or "What is the document about?"
    prompt = f"""
Answer the question using only the information in the document below.
Document:
{document}
Question:
{question}
Answer:
"""
    answer = generate_answer(prompt)
    print("\nRetrieved Context:")
    print(document)
    print("\nAnswer:")
    print(answer)

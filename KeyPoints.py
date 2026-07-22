import json
import urllib.request


def generate(prompt):
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
            return f"[offline fallback] {prompt.strip()[:120]}"


if __name__ == "__main__":
    topic = input("Enter a topic: ").strip() or "Artificial Intelligence"
    summary = generate(f"Write a short summary about {topic}.")
    key_points = generate(f"Extract the important key points from this summary:\n{summary}")
    questions = generate(
        f"Create exactly three questions based on this topic and summary.\n"
        f"Topic: {topic}\n"
        f"Summary: {summary}"
    )
    print("\nSummary:")
    print(summary)
    print("\nKey Points:")
    print(key_points)
    print("\nThree Questions:")
    print(questions)
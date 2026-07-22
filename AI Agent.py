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
    task = input("Enter a task for the AI agent: ").strip() or "write a short email"
    plan = generate(f"Create a simple step-by-step plan to complete this task:\n{task}")
    result = generate(
        f"Complete the task using this plan:\n\n"
        f"Task: {task}\n\n"
        f"Plan:\n{plan}"
    )
    print("\nPlan:")
    print(plan)
    print("\nFinal Output:")
    print(result)

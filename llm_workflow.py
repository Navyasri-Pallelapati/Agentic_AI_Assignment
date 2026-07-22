"""
Assignment 1: LLM Workflow

This program:
1. Accepts user input
2. Sends the input to an LLM
3. Displays the generated response
"""

import os

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - fallback for minimal environments
    def load_dotenv():
        return False

try:
    from google import genai
except ImportError:  # pragma: no cover - fallback for minimal environments
    genai = None


# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key and genai is not None:
    try:
        client = genai.Client(api_key=api_key)
    except Exception:
        client = None


def generate_response(user_input):
    """
    Sends user input to the Gemini LLM
    and returns the generated response.
    """

    prompt = f"""
You are a helpful AI assistant.

User Question:
{user_input}

Provide a clear, accurate, and easy-to-understand answer.
"""

    if client is not None:
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception:
            pass

    return f"[offline fallback] Here is a simple answer to your question: {user_input}"


def main():

    print("=" * 60)
    print("          LLM WORKFLOW APPLICATION")
    print("=" * 60)

    user_input = input("\nEnter your question: ")

    if not user_input.strip():
        print("Please enter a valid question.")
        return

    print("\nGenerating response...\n")

    answer = generate_response(user_input)

    print("=" * 60)
    print("AI RESPONSE")
    print("=" * 60)
    print(answer)


if __name__ == "__main__":
    main()
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API credentials and configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"


def query_groq(prompt, model=MODEL, max_tokens=500):
    """
    Queries the Groq LLM API with a food/nutrition-specific system prompt.

    Args:
        prompt (str): The user prompt.
        model (str): The model to use (default: llama3-70b-8192).
        max_tokens (int): The max tokens for the output (default: 500).

    Returns:
        str: The model's response or an error message.
    """
    if not GROQ_API_KEY:
        return "❌ Missing GROQ_API_KEY. Please check your .env file."

    if not prompt.strip():
        return "⚠️ Empty prompt received."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant specialized in food, nutrition, and healthy eating."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except requests.exceptions.HTTPError as http_err:
        return f"❌ HTTPError {http_err.response.status_code}: {http_err.response.text}"
    except Exception as e:
        return f"❌ General Error: {e}"

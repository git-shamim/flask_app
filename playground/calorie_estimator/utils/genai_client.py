import os
import requests
import logging
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Constants
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama3-70b-8192"

# Only load if not already configured (helps in Cloud Run)
if not GROQ_API_KEY:
    logging.warning("⚠️ GROQ_API_KEY not set. GenAI functionality will be disabled.")


def query_groq(prompt, model=DEFAULT_MODEL, max_tokens=500, temperature=0.7):
    """
    Query the Groq LLM API with a prompt.
    Args:
        prompt (str): The user query.
        model (str): LLM model to use.
        max_tokens (int): Token cap for output.
        temperature (float): Creativity control.
    Returns:
        str: Model response or error.
    """
    if not GROQ_API_KEY:
        return "❌ Missing GROQ_API_KEY. Please configure it in Secret Manager or .env"

    if not prompt.strip():
        logging.warning("⚠️ Skipped empty prompt.")
        return "⚠️ Empty prompt received."

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
        "temperature": temperature
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        logging.error("❌ Timeout while querying Groq.")
        return "❌ Request to Groq timed out."

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"❌ HTTPError: {http_err.response.status_code} - {http_err.response.text}")
        return f"❌ HTTPError {http_err.response.status_code}: {http_err.response.text}"

    except Exception as e:
        logging.exception("❌ General error while querying Groq.")
        return f"❌ General Error: {e}"

import os
import requests
from google.cloud import secretmanager

def get_groq_api_key():
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/moonlit-mesh-387316/secrets/GROQ_API_KEY/versions/latest"
    response = client.access_secret_version(request={"name": name})
    key = response.payload.data.decode("UTF-8")
    print("🔐 Retrieved Groq API Key:", key[:6], "..." if key else "❌ None")
    return key

def ask_groq_llm(question, context):
    GROQ_API_KEY = get_groq_api_key()
    if not GROQ_API_KEY:
        raise RuntimeError("❌ Groq API Key could not be retrieved or is empty.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the given document."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ],
        "model": "mixtral-8x7b-32768"
    }

    try:
        print("📤 Sending request to Groq API...")
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )

        print("✅ Response status code:", response.status_code)

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print("📥 Groq API Response Preview:", content[:100], "...")
            return content
        else:
            print("❌ Groq API Error:", response.status_code)
            print("🧾 Error Details:", response.text)
            raise RuntimeError(f"Groq API error: {response.status_code} → {response.text}")

    except requests.exceptions.RequestException as e:
        print("🚨 Exception calling Groq API:", str(e))
        raise RuntimeError("Network or timeout error when calling Groq API.")

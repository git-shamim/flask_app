import os
from dotenv import load_dotenv
from google.cloud import secretmanager
from groq import Groq

# Load env only in local (not in Cloud Run)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not os.getenv("K_SERVICE"):  # K_SERVICE is set by Cloud Run
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

def get_api_key():
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        return api_key

    # fallback for Cloud Run using GCP Secret Manager
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv("GCP_PROJECT")
        name = f"projects/{project_id}/secrets/GROQ_API_KEY/versions/latest"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Could not load GROQ_API_KEY: {e}")

def suggest_improvements(resume_text, jd_text):
    prompt = f"""
Resume:
{resume_text}

Job Description:
{jd_text}

List 4–6 clear bullet points on what the candidate should add or improve in the resume to align with the job.
"""
    client = Groq(api_key=get_api_key())
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert resume consultant."},
            {"role": "user", "content": prompt}
        ],
        model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content

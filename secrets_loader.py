import os
from google.cloud import secretmanager

def load_secrets(local=False):
    """
    Load secrets based on environment:
    - From environment variables (.env) if local.
    - From Google Cloud Secret Manager if deployed.
    """
    if local:
        return {
            "DATABASE_URL": os.getenv("DATABASE_URL", ""),
            "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret")
        }

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise RuntimeError("❌ GOOGLE_CLOUD_PROJECT environment variable is not set.")

    client = secretmanager.SecretManagerServiceClient()
    cache = {}

    def get_secret(secret_id):
        if secret_id in cache:
            return cache[secret_id]
        try:
            name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            secret_value = response.payload.data.decode("UTF-8")
            cache[secret_id] = secret_value
            return secret_value
        except Exception as e:
            raise RuntimeError(f"❌ Failed to retrieve secret '{secret_id}': {str(e)}")

    return {
        "DATABASE_URL": get_secret("flask-database-url"),
        "SECRET_KEY": get_secret("flask-secret-key")
    }

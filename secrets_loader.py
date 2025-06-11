import os

def load_config():
    """
    Load configuration from environment variables.
    Dynamically builds the SQLALCHEMY_DATABASE_URI from its parts.
    """
    user = os.environ["DB_USER"]
    pwd  = os.environ["DB_PASS"]
    host = os.environ["DB_HOST"]
    port = os.environ.get("DB_PORT", "5432")
    name = os.environ["DB_NAME"]

    # If we're pointing at a Cloud SQL socket, use the query‐param URI form
    if host.startswith("/cloudsql"):
        uri = (
            f"postgresql+psycopg2://{user}:{pwd}@/{name}"
            f"?host={host}&port={port}"
        )
    else:
        # Standard TCP URI
        uri = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{name}"

    return {
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret"),
        "SQLALCHEMY_DATABASE_URI": uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
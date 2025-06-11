import os
import logging

def load_config():
    """
    Load configuration for Flask (Cloud Run production).
    Connects to Cloud SQL Postgres via Unix socket.
    """
    secret_key = os.getenv("SECRET_KEY", "dev-secret")
    user       = os.environ["DB_USER"]
    pwd        = os.environ["DB_PASS"]
    db_name    = os.environ["DB_NAME"]
    socket     = os.environ["DB_HOST"]
    port       = os.environ.get("DB_PORT", "5432")

    uri = (
        f"postgresql+psycopg2://{user}:{pwd}@/{db_name}"
        f"?host={socket}&port={port}"
    )
    logging.info(f"→ SQLALCHEMY_DATABASE_URI = {uri}")

    return {
        "SECRET_KEY": secret_key,
        "SQLALCHEMY_DATABASE_URI": uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

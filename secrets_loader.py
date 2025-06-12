import os
import logging
from dotenv import load_dotenv

# Always load .env when running locally
load_dotenv()

def load_config():
    """
    Load Flask config:
     - If USE_SQLITE is truthy, use local SQLite (instance/local.db).
     - Otherwise, connect to Cloud SQL Postgres via Unix socket.
    """
    secret_key = os.getenv("SECRET_KEY", "dev-secret")

    # ─── LOCAL SQLITE FALLBACK ───────────────────────────────────────────────
    if os.getenv("USE_SQLITE", "").lower() in ("1", "true", "yes"):
        project_root = os.path.dirname(os.path.abspath(__file__))
        sqlite_path = os.path.join(project_root, "instance", "local.db")
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        uri = f"sqlite:///{sqlite_path}"
        logging.info(f"→ Using local SQLite DB at {sqlite_path}")
        return {
            "SECRET_KEY": secret_key,
            "SQLALCHEMY_DATABASE_URI": uri,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }

    # ─── PRODUCTION: CLOUD SQL POSTGRES ───────────────────────────────────────
    user    = os.environ["DB_USER"]
    pwd     = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    host    = os.environ["DB_HOST"]   # e.g. /cloudsql/project:region:instance
    port    = os.environ.get("DB_PORT", "5432")

    uri = (
        f"postgresql+psycopg2://{user}:{pwd}@/{db_name}"
        f"?host={host}&port={port}"
    )
    logging.info(f"→ SQLALCHEMY_DATABASE_URI = {uri}")
    return {
        "SECRET_KEY": secret_key,
        "SQLALCHEMY_DATABASE_URI": uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

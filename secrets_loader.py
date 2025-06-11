import os
import logging
from dotenv import load_dotenv

# Only load .env when running locally (Cloud Run sets K_SERVICE)
if os.getenv("K_SERVICE") is None:
    load_dotenv()

def load_config():
    """
    Build Flask configuration:
      - Locally (USE_SQLITE=true): use instance/local.db SQLite
      - In Cloud Run: connect to Cloud SQL via Unix socket
    """
    secret_key = os.getenv("SECRET_KEY", "dev-secret")

    # ─── LOCAL SQLITE FALLBACK ───────────────────────────────────────────────
    if os.getenv("USE_SQLITE", "").lower() in ("1", "true", "yes"):
        # Determine project root and ensure instance folder exists
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
    user      = os.environ["DB_USER"]
    pwd       = os.environ["DB_PASS"]
    db_name   = os.environ["DB_NAME"]
    socket    = os.environ["DB_HOST"]      # e.g. "/cloudsql/project:region:instance"
    db_port   = os.environ.get("DB_PORT", "5432")

    uri = (
        f"postgresql+psycopg2://{user}:{pwd}@/{db_name}"
        f"?host={socket}&port={db_port}"
    )
    logging.info(f"→ SQLALCHEMY_DATABASE_URI = {uri}")
    return {
        "SECRET_KEY": secret_key,
        "SQLALCHEMY_DATABASE_URI": uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

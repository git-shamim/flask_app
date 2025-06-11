import os
import logging
from dotenv import load_dotenv

# Load local .env if present (harmless in Cloud Run)
load_dotenv()

def load_config():
    secret_key = os.getenv("SECRET_KEY", "dev-secret")

    # LOCAL SQLITE FALLBACK
    if os.getenv("USE_SQLITE", "").lower() in ("1", "true", "yes"):
        # Compute project root (dir containing this file)
        project_root = os.path.dirname(os.path.abspath(__file__))
        # Path under instance/local.db
        sqlite_path = os.path.join(project_root, "instance", "local.db")
        # Ensure the folder exists
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        # Build URI
        uri = f"sqlite:///{sqlite_path}"
        logging.info(f"→ Using local SQLite DB at {sqlite_path}")
        return {
            "SECRET_KEY": secret_key,
            "SQLALCHEMY_DATABASE_URI": uri,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }

    # PRODUCTION: CLOUD SQL POSTGRES
    user    = os.environ["DB_USER"]
    pwd     = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    socket  = os.environ["DB_HOST"]
    port    = os.environ.get("DB_PORT", "5432")
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

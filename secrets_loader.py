import os
import logging

def load_config():
    """
    Load configuration from environment variables (GCP/Cloud Run only).
    Always builds the SQLALCHEMY_DATABASE_URI to connect via the Cloud SQL socket.
    """
    # Required env vars (populated by Cloud Run + Secret Manager)
    user      = os.environ["DB_USER"]
    pwd       = os.environ["DB_PASS"]
    db_name   = os.environ["DB_NAME"]
    socket    = os.environ["DB_HOST"]      # e.g. "/cloudsql/project:region:instance"
    db_port   = os.environ.get("DB_PORT", "5432")

    # Build the “query-param” style URI for a Unix socket
    uri = (
        f"postgresql+psycopg2://{user}:{pwd}@/{db_name}"
        f"?host={socket}&port={db_port}"
    )

    # Log it once at startup so you can validate in Cloud Run logs
    logging.info(f"→ SQLALCHEMY_DATABASE_URI = {uri}")

    return {
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret"),
        "SQLALCHEMY_DATABASE_URI":   uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

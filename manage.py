import os
import logging

# Load .env so USE_SQLITE and SECRET_KEY (and any others) are available
from dotenv import load_dotenv
load_dotenv()

from flask.cli import FlaskGroup
from flask_migrate import Migrate

# Now import your app after loading env vars
from index import app  # ensures app.config picks up USE_SQLITE
from models import db

# Set up logging so you can see migration output
logging.basicConfig(level=logging.INFO)

# Initialize migrations
migrate = Migrate(app, db)

# Create the Flask CLI group
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()

from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
from secrets_loader import load_secrets
import os
from datetime import datetime

from models import db, Contact

# Load environment variables
load_dotenv()
is_local = os.environ.get("FLASK_DEBUG", "0") == "1"

# Load secrets
secrets = load_secrets(local=is_local)

# Flask app setup
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.get('SECRET_KEY', 'fallback')

if is_local:
    # Use SQLite locally
    app.config['SQLALCHEMY_DATABASE_URI'] = secrets.get('DATABASE_URL') or 'sqlite:///local.db'
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()
else:
    # Use BigQuery in Cloud Run
    from google.cloud import bigquery
    bq_client = bigquery.Client()
    bq_project = secrets['BQ_PROJECT_ID']
    bq_dataset = secrets['BQ_DATASET']
    bq_table = secrets['BQ_TABLE']
    table_id = f"{bq_project}.{bq_dataset}.{bq_table}"

# ROUTES

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/playground')
def playground():
    return render_template('playground.html')

@app.route('/dashboards')
def dashboards():
    return render_template('dashboards.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/certifications')
def certifications():
    return render_template('certifications.html')

@app.route('/hackathons')
def hackathons():
    return render_template('hackathons.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email:
        flash("Name and Email are required!", "error")
        return redirect('/#contact')

    if is_local:
        contact = Contact(name=name, email=email, message=message)
        db.session.add(contact)
        db.session.commit()
    else:
        row = [{
            "name": name,
            "email": email,
            "message": message,
            "submitted_at": datetime.utcnow().isoformat()
        }]
        errors = bq_client.insert_rows_json(table_id, row)
        if errors:
            flash("❌ Failed to submit message. Try again.", "error")
            return redirect('/#contact')

    flash("Thanks! Your message was received.", "success")
    return redirect('/#contact')

# Main entrypoint
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

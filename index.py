from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
import os
from datetime import datetime
from models import db, Contact
import logging
from secrets_loader import load_config

logging.basicConfig(level=logging.INFO)

# Load .env (for local) or rely on real environment vars in Cloud Run
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.config.update(load_config())

# Initialize the database
db.init_app(app)

# Ensure tables exists on startup
with app.app_context():
    db.create_all()

# ─── ROUTES ───────────────────────────────────────────────────────────────

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

    # Always save to Postgres via SQLAlchemy
    contact = Contact(name=name, email=email, message=message)
    db.session.add(contact)
    db.session.commit()

    flash("Thanks! Your message was received.", "success")
    return redirect('/#contact')

# Main entrypoint
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

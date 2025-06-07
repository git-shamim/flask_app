# index.py

from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
from secrets_loader import load_secrets
import os

from models import db, Contact

# Load environment variables for local development
load_dotenv()
is_local = os.environ.get("FLASK_ENV") == "development"

# Load secrets based on environment
secrets = load_secrets(local=is_local)

# Flask app configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.get('SECRET_KEY', 'fallback')
app.config['SQLALCHEMY_DATABASE_URI'] = secrets.get('DATABASE_URL') or 'sqlite:///local.db'

# Initialize database
db.init_app(app)

# Auto-create tables for local dev
@app.before_first_request
def create_tables():
    db.create_all()

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
        return redirect("/")

    contact = Contact(name=name, email=email, message=message)
    db.session.add(contact)
    db.session.commit()
    flash("Thanks! Your message was received.", "success")
    return redirect('/#contact')

# Cloud Run–friendly entrypoint
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

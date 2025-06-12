import os
import logging
from flask import Flask, render_template, request, redirect, flash
from models import db, Contact
from secrets_loader import load_config
from flask_migrate import Migrate

# Setup logging
logging.basicConfig(level=logging.INFO)

# Flask app initialization
app = Flask(__name__)
app.config.update(load_config())

# Initialize SQLAlchemy
db.init_app(app)

# ─── Migrations ─────────────────────────────────────────────────────────────
migrate = Migrate(app, db)

# Ensure tables exist on startup
with app.app_context():
    try:
        db.create_all()
        app.logger.info("Tables created or already exist")
    except Exception as e:
        app.logger.error(f"Could not create tables: {e}")

# Routes
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
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email:
        flash("Name and Email are required!", "error")
        return redirect('/#contact')

    contact = Contact(name=name, email=email, message=message)
    try:
        db.session.add(contact)
        db.session.commit()
        flash("Thanks! Your message was received.", "success")
    except Exception as exc:
        db.session.rollback()
        app.logger.error(f"Error saving contact: {exc}")
        flash("Sorry, something went wrong.", "error")

    return redirect('/#contact')

# Main entrypoint
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

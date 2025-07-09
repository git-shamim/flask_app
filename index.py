import os
import logging
import threading
import requests
from flask import Flask, render_template, request, redirect, flash
from models import db, Contact
from secrets_loader import load_config
from flask_migrate import Migrate

# ─── Setup Logging ──────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)

# ─── Flask App Initialization ───────────────────────────────────────────────
app = Flask(__name__)
app.config.update(load_config())

# ─── Database Initialization ────────────────────────────────────────────────
db.init_app(app)
migrate = Migrate(app, db)

# ─── Ensure Tables Exist ────────────────────────────────────────────────────
with app.app_context():
    try:
        db.create_all()
        app.logger.info("Tables created or already exist")
    except Exception as e:
        app.logger.error(f"Could not create tables: {e}")

# ─── App Warm-Up Function ───────────────────────────────────────────────────
def warm_up_services():
    urls = [
        "https://documentquery-bqcmvvkyzna4hszxpq2855.streamlit.app",
        "https://resume-scanner-927330113220.asia-southeast1.run.app",
        "https://food-calorie-estimator-927330113220.asia-southeast1.run.app",
        # Add more app URLs as needed
    ]
    for url in urls:
        try:
            requests.get(url, timeout=3)
            app.logger.info(f"Warmed up {url}")
        except Exception as e:
            app.logger.warning(f"Warm-up failed for {url}: {e}")

# ─── Routes ─────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    threading.Thread(target=warm_up_services).start()
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

# ─── Dynamic Playground App Route ───────────────────────────────────────────
@app.route('/playground/<project_name>')
def playground_project(project_name):
    projects = {
        "document-query": {
            "title": "Document Query Chatbot",
            "description": "Upload PDFs and ask questions using a GenAI chatbot.",
            "url": "https://documentquery-bqcmvvkyzna4hszxpq2855.streamlit.app"
        },
        "resume-scanner": {
            "title": "Resume Scanner",
            "description": "Upload your resume and job description for a match score and feedback.",
            "url": "https://resume-scanner-927330113220.asia-southeast1.run.app"
        },
        "food-calorie-estimator": {
            "title": "Food Calorie Estimator",
            "description": "Upload a food image and get calorie predictions + dietary tips.",
            "url": "https://food-calorie-estimator-927330113220.asia-southeast1.run.app"
        }
        # Add more mappings as needed
    }

    project = projects.get(project_name)
    if not project:
        return render_template("404.html"), 404

    return render_template(
        "playground_project.html",
        title=project["title"],
        description=project["description"],
        embed_url=project["url"]
    )

# ─── Entrypoint ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

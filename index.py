import os
import logging
import threading
import requests
import json
import markdown
from flask import Flask, render_template, request, redirect, flash
from flask_migrate import Migrate
from models import db, Contact
from secrets_loader import load_config
from utils.groq_llm import ask_groq_llm
from utils.document_reader import extract_text  # ✅ Unified reader (PDF, Word, Excel, Text)

# ─── Setup Logging ──────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("index")

# ─── Flask App Initialization ───────────────────────────────────────────────
app = Flask(__name__)
app.config.update(load_config())

# ─── Database Initialization ────────────────────────────────────────────────
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    try:
        db.create_all()
        logger.info("Tables created or already exist")
    except Exception as e:
        logger.error(f"Could not create tables: {e}")

# ─── App Warm-Up Function ───────────────────────────────────────────────────
def warm_up_services():
    urls = [
        "https://documentquery-bqcmvvkyzna4hszxpq2855.streamlit.app",
        "https://resume-scanner-927330113220.asia-southeast1.run.app",
        "https://food-calorie-estimator-927330113220.asia-southeast1.run.app",
    ]
    for url in urls:
        try:
            requests.get(url, timeout=3)
            logger.info(f"Warmed up {url}")
        except Exception as e:
            logger.warning(f"Warm-up failed for {url}: {e}")

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
    try:
        with open('static/data/blogs.json') as f:
            blogs_data = json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading blogs.json: {e}")
        blogs_data = []
    return render_template('blogs.html', blogs=blogs_data)

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

@app.route('/projects/<project_name>')
def project_detail(project_name):
    projects = {
        "diabetes-prediction": {
            "title": "Diabetes Risk Prediction",
            "description": "Predict whether a person is likely to have diabetes based on health metrics.",
            "details": "Uses classification algorithms with balanced datasets. Visual insights and model explanation included.",
            "embed_url": "https://deepnote.com/embed/58bfb0e4-9979-4bbb-9a8b-6f03ee38e76c"
        }
    }
    project = projects.get(project_name)
    if not project:
        return render_template("404.html"), 404
    return render_template("project_detail.html", **project)

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
    }
    project = projects.get(project_name)
    if not project:
        return render_template("404.html"), 404
    return render_template("playground_project.html", **project)

@app.route('/dashboards/<dashboard_name>')
def dashboard_view(dashboard_name):
    dashboards = {
        "search-trends-india": {
            "title": "Google Search Trends in India",
            "description": "Search interest for key business terms across Indian states.",
            "url": "https://lookerstudio.google.com/s/n1G_-CsxHI4"
        }
    }
    dashboard = dashboards.get(dashboard_name)
    if not dashboard:
        return render_template("404.html"), 404
    return render_template("dashboard_view.html", **dashboard)

@app.route('/blogs/<blog_slug>')
def blog_article(blog_slug):
    try:
        with open('static/data/blogs.json', 'r') as f:
            blogs = json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading blogs.json: {e}")
        return render_template("404.html"), 404

    blog = next((b for b in blogs if b["slug"] == blog_slug), None)
    if not blog:
        return render_template("404.html"), 404

    markdown_path = os.path.join('static', 'blogs', blog['markdown_file'])
    if not os.path.exists(markdown_path):
        app.logger.error(f"Markdown file not found: {markdown_path}")
        return render_template("404.html"), 404

    try:
        with open(markdown_path, 'r') as f:
            md_content = f.read()
            html_content = markdown.markdown(
                md_content,
                extensions=["fenced_code", "codehilite", "tables"]
            )
    except Exception as e:
        app.logger.error(f"Error reading markdown file: {e}")
        return render_template("404.html"), 404

    return render_template(
        "blog_article.html",
        title=blog["title"],
        description=blog["description"],
        content=html_content,
        medium_url=blog["medium_url"]
    )

# ─── Document Query ─────────────────────────────────────────────────────────
@app.route("/playground/document-query", methods=["GET", "POST"])
def document_query():
    answer = None
    uploaded_filenames = []

    if request.method == "POST":
        uploaded_files = request.files.getlist("documents")
        question = request.form.get("question", "").strip()
        app.logger.info(f"📥 Received question: {question}")

        uploaded_filenames = [file.filename for file in uploaded_files]
        combined_text = ""

        for file in uploaded_files:
            try:
                text = extract_text(file)
                combined_text += f"\n{text}"
                app.logger.info(f"📄 Extracted text from {file.filename}")
            except Exception as e:
                app.logger.error(f"❌ Failed reading {file.filename}: {e}")

        if not combined_text.strip():
            app.logger.warning("⚠️ No readable text found in uploaded files.")
            answer = "⚠️ None of the uploaded files contain readable text. Please try different files."
        else:
            try:
                app.logger.info("🧠 Invoking Groq with extracted context...")
                answer = ask_groq_llm(question, combined_text[:15000])
            except Exception as e:
                app.logger.error(f"❌ Groq API call failed: {e}")
                answer = "Sorry, the GenAI model could not process your request right now."

    return render_template(
        "playground/document_query.html",
        answer=answer,
        uploaded_filenames=uploaded_filenames
    )

# ─── Entrypoint ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

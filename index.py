import os
import logging
import threading
import requests
import time
import json
from flask import Flask, render_template, request, redirect, flash
from secrets_loader import load_config
import markdown
# from flask_migrate import Migrate
# from models import db, Contact

# ─── Modular Blueprints ─────────────────────────────────────────
from projects.projects_routes import projects_bp
from playground.playground_routes import playground_bp
from dashboards.dashboards_routes import dashboards_bp
from blogs.blogs_routes import blogs_bp

from playground.resume_scanner.resume_scanner_routes import resume_scanner_bp
from playground.document_query.document_query_routes import document_query_bp
from playground.calorie_estimator.calorie_estimator_routes import calorie_estimator_bp

# ─── Setup Logging ─────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("index")

# ─── Flask App Initialization ───────────────────────────────────────────────
app = Flask(__name__)
app.config.update(load_config())

# ─── Register Modular Blueprints ────────────────────────────────────────────
app.register_blueprint(projects_bp)
app.register_blueprint(playground_bp)
app.register_blueprint(dashboards_bp)
app.register_blueprint(blogs_bp)

app.register_blueprint(resume_scanner_bp)
app.register_blueprint(document_query_bp)
app.register_blueprint(calorie_estimator_bp)

# ─── Database Initialization ────────────────────────────────────────────────
# db.init_app(app)
# migrate = Migrate(app, db)
#
# with app.app_context():
#     try:
#         db.create_all()
#         logger.info("✅ Tables created or already exist.")
#     except Exception as e:
#         logger.error(f"❌ Could not create tables: {e}")

# ─── Primary Website Routes ─────────────────────────────────────────────────

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
    try:
        with open('blogs/blogs_data.json') as f:
            blogs_data = json.load(f)
    except Exception as e:
        app.logger.error(f"❌ Error loading blogs_data.json: {e}")
        blogs_data = []
    return render_template('blogs.html', blogs=blogs_data)

# @app.route('/certifications')
# def certifications():
#     return render_template('certifications.html')
#
# @app.route('/hackathons')
# def hackathons():
#     return render_template('hackathons.html')

# @app.route('/submit_contact', methods=['POST'])
# def submit_contact():
#     name = request.form.get("name", "").strip()
#     email = request.form.get("email", "").strip()
#     message = request.form.get("message", "").strip()
#
#     if not name or not email:
#         flash("Name and Email are required!", "error")
#         return redirect('/#contact')
#
#     contact = Contact(name=name, email=email, message=message)
#     try:
#         db.session.add(contact)
#         db.session.commit()
#         flash("Thanks! Your message was received.", "success")
#     except Exception as exc:
#         db.session.rollback()
#         app.logger.error(f"❌ Error saving contact: {exc}")
#         flash("Sorry, something went wrong.", "error")
#     return redirect('/#contact')


# @app.route('/blogs/<blog_slug>')
# def blog_article(blog_slug):
#     try:
#         with open('blogs/blogs_data.json', 'r') as f:
#             blogs = json.load(f)
#     except Exception as e:
#         app.logger.error(f"❌ Error loading blogs_data.json: {e}")
#         return render_template("404.html"), 404
#
#     blog = next((b for b in blogs if b["slug"] == blog_slug), None)
#     if not blog:
#         return render_template("404.html"), 404
#
#     markdown_path = os.path.join('static', 'blogs', blog['markdown_file'])
#     if not os.path.exists(markdown_path):
#         app.logger.error(f"Markdown file not found: {markdown_path}")
#         return render_template("404.html"), 404
#
#     try:
#         with open(markdown_path, 'r') as f:
#             md_content = f.read()
#             html_content = markdown.markdown(
#                 md_content,
#                 extensions=["fenced_code", "codehilite", "tables"]
#             )
#     except Exception as e:
#         app.logger.error(f"❌ Error reading markdown file: {e}")
#         return render_template("404.html"), 404
#
#     return render_template(
#         "blog_article.html",
#         title=blog["title"],
#         description=blog["description"],
#         content=html_content,
#         medium_url=blog["medium_url"]
#     )


# List of Deepnote app URLs to keep alive
deepnote_urls = [
    "https://deepnote.com/@shamim/crop-selection-d2ea5127-496f-4712-b0b9-8928b04f9e21?__run=true",
    "https://deepnote.com/@shamim/diabetes-prediction-58bfb0e4-9979-4bbb-9a8b-6f03ee38e76c?__run=true"
]

def keep_deepnote_warm():
    while True:
        for url in deepnote_urls:
            try:
                print(f"Pinging {url} ...")
                requests.get(url, timeout=15)
            except Exception as e:
                print(f"Failed to ping {url}: {e}")
        time.sleep(120)

# Start pinger thread on Flask startup
threading.Thread(target=keep_deepnote_warm, daemon=True).start()

# ─── Entrypoint ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)



import os
import logging
from flask import Flask, render_template, request, redirect, flash
from models import db, Contact
from secrets_loader import load_config

# ─── Setup Logging ──────────────────────────────────────────────────────────
# You might later configure a richer formatter or external log sink here.
logging.basicConfig(level=logging.INFO)

# ─── Flask App Initialization ───────────────────────────────────────────────
app = Flask(__name__)
app.config.update(load_config())

# ENABLE CSRF PROTECTION (optional – install Flask-WTF)
# from flask_wtf import CSRFProtect
# CSRFProtect(app)

# ─── Initialize SQLAlchemy ──────────────────────────────────────────────────
db.init_app(app)

# ─── Ensure tables exist ────────────────────────────────────────────────────
# In production you’d normally use Alembic/Flask-Migrate rather than create_all(),
# but for a simple Cloud Run setup this is fine.
with app.app_context():
    try:
        db.create_all()
        app.logger.info("Tables created or already exist")
    except Exception as e:
        app.logger.error(f"Could not create tables: {e}")

# ─── ROUTES ──────────────────────────────────────────────────────────────────
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
        # Make sure your template reads flash messages and displays them
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


# ─── ERROR HANDLERS (optional) ──────────────────────────────────────────────
# @app.errorhandler(404)
# def not_found(e):
#     return render_template('404.html'), 404
#
# @app.errorhandler(500)
# def server_error(e):
#     app.logger.error(f"Server error: {e}")
#     return render_template('500.html'), 500


# ─── Main entrypoint for local dev ───────────────────────────────────────────
if __name__ == '__main__':
    # In Cloud Run this block is ignored (Gunicorn will serve the app).
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

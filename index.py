from flask import Flask, render_template
import os

app = Flask(__name__)

# Home page (landing with tiles, banner, contact)
@app.route('/')
def home():
    return render_template('index.html')

# Inner pages (extend base.html)
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


# ✅ Single main entry point for local + Cloud Run
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Use Cloud Run's expected port
    app.run(host='0.0.0.0', port=port)        # Accessible externally

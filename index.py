from flask import Flask, render_template

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


if __name__ == '__main__':
    app.run(debug=True)

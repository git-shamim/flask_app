from flask import Blueprint, render_template, abort

playground_bp = Blueprint('playground_bp', __name__, template_folder='templates')

@playground_bp.route('/playground/<project_name>')
def playground_project(project_name):
    valid_projects = {
        "resume-scanner": "resume_scanner.html",
        "food-calorie-estimator": "calorie_estimator.html",
        "document-query": "document_query.html"
    }

    template = valid_projects.get(project_name)
    if not template:
        return abort(404)

    return render_template(f'playground/{template}')

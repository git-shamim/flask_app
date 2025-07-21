from flask import Blueprint, render_template

projects_bp = Blueprint("projects", __name__)

# Define your Deepnote project metadata here
projects_data = {
    "crop-selection": {
        "title": "Crop Selection Advisor",
        "description": "Suggest the most suitable crop based on soil and climate data.",
        "details": "Uses environmental and soil condition parameters to recommend optimal crops.",
        "iframe_url": "https://deepnote.com/app/projects-47c4/Crop-Selection-d2ea5127-496f-4712-b0b9-8928b04f9e21?utm_source=app-settings&utm_medium=product-embed&utm_campaign=data-app&utm_content=d2ea5127-496f-4712-b0b9-8928b04f9e21&__embedded=true",
        "image": "images/projects/crop-selection.jpg"
    },
    "diabetes-prediction": {
        "title": "Diabetes Risk Prediction",
        "description": "Predict diabetes risk from health indicators like age, glucose, BMI, and HbA1c.",
        "details": "Enter patient parameters to assess risk using a trained ML model.",
        "iframe_url": "https://deepnote.com/app/projects-47c4/Diabetes-Prediction-58bfb0e4-9979-4bbb-9a8b-6f03ee38e76c?utm_source=app-settings&utm_medium=product-embed&utm_campaign=data-app&utm_content=58bfb0e4-9979-4bbb-9a8b-6f03ee38e76c&__embedded=true",
        "image": "images/projects/diabetes-prediction.jpg"
    }
}


# Route to list all Deepnote projects
@projects_bp.route("/projects")
def project_list():
    return render_template("projects.html", projects=projects_data)

# Route to view an individual Deepnote project
@projects_bp.route("/projects/<slug>")
def project_detail(slug):
    project = projects_data.get(slug)
    if not project:
        return render_template("404.html"), 404
    return render_template("project_detail.html", **project)

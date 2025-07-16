from flask import Blueprint, render_template, request
from .resume_scanner_app import analyze_resume

resume_scanner_bp = Blueprint('resume_scanner_bp', __name__, template_folder='templates')

@resume_scanner_bp.route("/playground/resume-scanner", methods=["GET", "POST"])
def resume_scanner():
    result = None
    error = None

    if request.method == "POST":
        resume_file = request.files.get('resume')
        jd_file = request.files.get('jd_file')
        jd_text_input = request.form.get('jd_text_input')
        use_genai = request.form.get('use_genai') == 'on'

        try:
            result = analyze_resume(
                resume_file=resume_file,
                jd_file=jd_file,
                jd_text_input=jd_text_input,
                use_genai=use_genai
            )
            if "error" in result:
                error = result["error"]
                result = None
        except Exception as e:
            error = f"Something went wrong: {str(e)}"

    return render_template("playground/resume_scanner.html", result=result, error=error)

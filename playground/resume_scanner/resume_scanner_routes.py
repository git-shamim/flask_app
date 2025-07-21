# playground/resume_scanner/resume_scanner_routes.py

from flask import Blueprint, render_template, request, current_app
from .resume_scanner_app import analyze_resume

resume_scanner_bp = Blueprint('resume_scanner_bp', __name__, template_folder='templates')

@resume_scanner_bp.route("/playground/resume-scanner", methods=["GET", "POST"])
def resume_scanner():
    result = error = None

    if request.method == "POST":
        resume_file = request.files.get("resume")
        jd_file = request.files.get("jd_file")
        jd_text_input = request.form.get("jd_text_input", "").strip()
        use_genai = request.form.get("use_genai") == "on"

        if not resume_file or (not jd_file and not jd_text_input):
            error = "Please upload a resume and either a JD file or enter JD text."
        else:
            try:
                current_app.logger.info(f"📥 Analyzing resume using GenAI: {use_genai}")
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
                current_app.logger.error(f"❌ Resume scanner failed: {e}")
                error = "Something went wrong while analyzing the resume."

    return render_template("playground/resume_scanner.html", result=result, error=error)

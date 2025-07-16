from flask import Blueprint, render_template, request, current_app
from .document_query_app import process_document_query

document_query_bp = Blueprint('document_query_bp', __name__, template_folder='templates')

@document_query_bp.route("/playground/document-query", methods=["GET", "POST"])
def document_query():
    result = None

    if request.method == "POST":
        uploaded_files = request.files.getlist("documents")
        question = request.form.get("question", "").strip()
        current_app.logger.info(f"📥 Received question: {question}")

        result = process_document_query(uploaded_files, question, logger=current_app.logger)

    return render_template(
        "playground/document_query.html",
        answer=result.get("answer") if result else None,
        error=result.get("error") if result else None,
        uploaded_filenames=result.get("filenames") if result else []
    )

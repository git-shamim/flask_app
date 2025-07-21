# playground/document_query/document_query_routes.py

from flask import Blueprint, render_template, request, current_app
from .document_query_app import process_document_query

document_query_bp = Blueprint('document_query_bp', __name__, template_folder='templates')

@document_query_bp.route("/playground/document-query", methods=["GET", "POST"])
def document_query():
    answer = error = None
    uploaded_filenames = []

    if request.method == "POST":
        uploaded_files = request.files.getlist("documents")
        question = request.form.get("question", "").strip()

        if not uploaded_files or not question:
            error = "Please upload at least one document and enter a question."
        else:
            current_app.logger.info(f"📥 Processing question: {question} with {len(uploaded_files)} file(s)")
            result = process_document_query(uploaded_files, question, logger=current_app.logger)

            answer = result.get("answer")
            error = result.get("error")
            uploaded_filenames = result.get("filenames", [])

    return render_template(
        "playground/document_query.html",
        answer=answer,
        error=error,
        uploaded_filenames=uploaded_filenames
    )

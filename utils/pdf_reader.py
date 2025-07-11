import fitz  # PyMuPDF
import pdfplumber
from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_storage):
    file_stream = file_storage.stream

    # Try PyMuPDF
    try:
        file_stream.seek(0)
        with fitz.open(stream=file_stream.read(), filetype="pdf") as doc:
            return "\n".join(page.get_text() or "" for page in doc)
    except Exception:
        pass

    # Try pdfplumber
    try:
        file_stream.seek(0)
        with pdfplumber.open(file_stream) as doc:
            return "\n".join(page.extract_text() or "" for page in doc.pages)
    except Exception:
        pass

    # Try pdfminer.six
    try:
        file_stream.seek(0)
        return extract_text(file_stream)
    except Exception:
        pass

    return ""

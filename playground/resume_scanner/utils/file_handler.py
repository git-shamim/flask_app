import pdfplumber
import docx2txt


def extract_text_from_file(file_storage):
    """
    Extracts text content from PDF, DOCX, or TXT file-like objects.
    Supported extensions: .pdf, .docx, .txt
    """
    filename = file_storage.filename.lower()
    file_storage.stream.seek(0)  # Ensure the stream is at beginning

    try:
        if filename.endswith(".pdf"):
            with pdfplumber.open(file_storage.stream) as pdf:
                return "\n".join(page.extract_text() or "" for page in pdf.pages)

        elif filename.endswith(".docx"):
            return docx2txt.process(file_storage.stream)

        elif filename.endswith(".txt"):
            return file_storage.read().decode("utf-8")

    except Exception as e:
        # Optional: log the error for debugging
        print(f"❌ Failed to extract text from {filename}: {e}")

    return ""

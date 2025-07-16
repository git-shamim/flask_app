import pdfplumber
import docx2txt

def extract_text_from_file(file_storage):
    filename = file_storage.filename

    if filename.endswith('.pdf'):
        file_storage.stream.seek(0)  # reset stream
        with pdfplumber.open(file_storage.stream) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])

    elif filename.endswith('.docx'):
        file_storage.stream.seek(0)
        return docx2txt.process(file_storage.stream)

    elif filename.endswith('.txt'):
        file_storage.stream.seek(0)
        return file_storage.read().decode("utf-8")

    else:
        return ""

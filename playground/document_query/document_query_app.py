from .utils.document_reader import extract_text
from .utils.groq_llm import ask_groq_llm

def process_document_query(files, question, logger=None):
    combined_text = ""
    filenames = []

    for file in files:
        try:
            text = extract_text(file)
            combined_text += f"\n{text}"
            filenames.append(file.filename)
            if logger: logger.info(f"📄 Extracted from {file.filename}")
        except Exception as e:
            if logger: logger.error(f"❌ Failed to extract from {file.filename}: {e}")

    if not combined_text.strip():
        return {
            "error": "⚠️ None of the uploaded files contain readable text.",
            "filenames": filenames
        }

    try:
        if logger: logger.info("🧠 Invoking Groq API...")
        response = ask_groq_llm(question, combined_text[:15000])
        return {
            "answer": response,
            "filenames": filenames
        }
    except Exception as e:
        if logger: logger.error(f"❌ Groq API call failed: {e}")
        return {
            "error": "Sorry, the GenAI model could not process your request.",
            "filenames": filenames
        }

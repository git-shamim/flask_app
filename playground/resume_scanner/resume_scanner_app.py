import os
from dotenv import load_dotenv
from .utils.file_handler import extract_text_from_file
from .utils.fitment_evaluator import evaluate_fitment
from .utils.improvement_suggester import suggest_improvements

load_dotenv(dotenv_path=".env")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def analyze_resume(resume_file, jd_file=None, jd_text_input=None, use_genai=True):
    if not resume_file or not (jd_file or jd_text_input):
        return {"error": "Missing input files or text."}

    resume_text = extract_text_from_file(resume_file)
    jd_text = extract_text_from_file(jd_file) if jd_file else jd_text_input

    score, common_skills = evaluate_fitment(resume_text, jd_text)

    result = {
        "score": round(score, 2),
        "common_skills": common_skills,
    }

    if use_genai:
        suggestions = suggest_improvements(resume_text, jd_text)
        result["suggestions"] = suggestions

    return result

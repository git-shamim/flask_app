# utils/fitment_evaluator.py
from sentence_transformers import SentenceTransformer, util
import spacy

model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    doc = nlp(text)
    return set([token.text.lower() for token in doc if token.pos_ == 'NOUN' or token.pos_ == 'PROPN'])

def evaluate_fitment(resume_text, jd_text):
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    score = float(util.cos_sim(resume_emb, jd_emb)[0][0]) * 100

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    matched = list(resume_skills.intersection(jd_skills))

    return score, matched

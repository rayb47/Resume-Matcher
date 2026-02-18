import streamlit
import spacy
import fitz
from sentence_transformers import SentenceTransformer

import fitz  # PyMuPDF
import spacy
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from functools import lru_cache

# Abbreviations mapped to cannonical skill names
SKILL_ALIASES = {
    "css": "cascading style sheets",
    "html": "hypertext markup language",
    "js": "javascript",
    "reactjs": "react",
    "nodejs": "node",
    "ml": "machine learning",
    "nlp": "natural language processing",
}

# Noramlises skill text
def normalize_skill(skill):
    skill = skill.lower().strip()

    if skill in SKILL_ALIASES:
        return SKILL_ALIASES[skill]

    return skill

# Loads and caches skill taxonomy
@lru_cache(maxsize=1)
def load_skill_taxonomy():
    with open("skills/skills.txt", "r", encoding="utf-8") as f:
        skills = [line.strip().lower() for line in f if line.strip()]
    return skills

# Precomputes embeddings for taxonomy skills
@lru_cache(maxsize=1)
def load_skill_embeddings():
    skills = load_skill_taxonomy()
    embeddings = model.encode(skills)
    return skills, embeddings

# Validates whether a phrase is likely a skill using semantic similarity
def is_valid_skill(phrase, threshold=0.70):
    skills, skill_embeddings = load_skill_embeddings()

    phrase_emb = model.encode(phrase)

    similarities = cosine_similarity(
        [phrase_emb],
        skill_embeddings
    )[0]

    return max(similarities) >= threshold

# Loads NLP and embedding model
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Extracts text from the uploaded PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Noramlises text for comparison
def clean_text(text):
    return " ".join(text.lower().split())

# Generates embedding vectors for text
def get_embedding(text):
    return model.encode([text])

# Computes resume, job similarity score
def compute_match_score(resume_text, jd_text):
    resume_emb = get_embedding(resume_text)
    jd_emb = get_embedding(jd_text)
    score = cosine_similarity(resume_emb, jd_emb)[0][0]
    return round(score * 100, 2)

# Extracts candidate skills using NLP noun chunks + semantic validation
def extract_skills(text):
    doc = nlp(text)
    skills = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.lower().strip()

        # basic length filter
        if len(phrase.split()) > 3:
            continue

        # linguistic sanity check
        if not any(tok.pos_ in {"NOUN", "PROPN"} for tok in chunk):
            continue

        # taxonomy-based validation
        if is_valid_skill(phrase):
            skills.add(phrase)

    return skills

def missing_skills(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    return semantic_skill_analysis(resume_skills, jd_skills)

def semantic_skill_gap(resume_skills, jd_skills, threshold=0.70):
    missing_skills = []

    resume_embeddings = {
        skill: model.encode(skill)
        for skill in resume_skills
    }

    for jd_skill in jd_skills:
        jd_embedding = model.encode(jd_skill)

        similarities = []
        for resume_skill, resume_embedding in resume_embeddings.items():
            sim = cosine_similarity(
                [jd_embedding],
                [resume_embedding]
            )[0][0]
            similarities.append(sim)

        if max(similarities, default=0) < threshold:
            missing_skills.append(jd_skill)
        
        #print(jd_skill, max(similarities))


    return missing_skills

# Compares resume and JD skills
def semantic_skill_analysis(resume_skills, jd_skills, threshold=0.65):
    results = []

    resume_embeddings = {
        skill: model.encode(skill)
        for skill in resume_skills
    }

    for jd_skill in jd_skills:
        jd_emb = model.encode(jd_skill)

        best_match = None
        best_score = 0.0

        for resume_skill, resume_emb in resume_embeddings.items():
            score = cosine_similarity([jd_emb], [resume_emb])[0][0]
            if score > best_score:
                best_score = score
                best_match = resume_skill

        results.append({
            "jd_skill": jd_skill,
            "best_match": best_match,
            "score": round(best_score, 2)
        })

    return results

# Computes % of skills covered by resume
def compute_skill_match_percentage(results, threshold=0.65):
    if not results:
        return 0

    matched = [r for r in results if r["score"] >= threshold]
    return round((len(matched) / len(results)) * 100, 2)





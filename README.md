# Resume ↔ Job Description Matcher

A Streamlit app that compares a resume with a job description using NLP and semantic embeddings to estimate match quality and identify skill gaps.

This project uses **spaCy**, **Sentence Transformers**, and **cosine similarity** to evaluate how well a candidate’s resume aligns with a job description.

---

## Features

* Upload resume as PDF
* Paste job description text
* Resume ↔ JD semantic similarity score
* Skill extraction using NLP noun chunks
* Skill validation using a skill taxonomy
* Semantic skill matching
* Skill coverage percentage
* Categorized skill results:

  * Strong matches
  * Weak matches
  * Missing skills

---

## Project Structure

```
.
├── app.py
├── utils.py
├── skills/
│   └── skills.txt
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/resume-jd-matcher.git
cd resume-jd-matcher
```

Install dependencies:

```
pip install -r requirements.txt
```

Download the spaCy model:

```
python -m spacy download en_core_web_sm
```

---

## Running the App

```
streamlit run app.py
```

The app will open in your browser.

---

## Tech Stack

* Python
* Streamlit
* spaCy
* Sentence Transformers
* scikit-learn
* PyMuPDF

---

## How It Works

### Resume–JD Match Score

The app converts both the resume and job description into embeddings using the model:

```
all-MiniLM-L6-v2
```

Cosine similarity between embeddings produces the overall match score.

---

### Skill Extraction

Skills are extracted using:

* spaCy noun chunk parsing
* Part-of-speech filtering
* Semantic validation against a skill taxonomy

---

### Skill Matching

Each job description skill is compared against resume skills using embedding similarity to find the closest match.

---

## Future Improvements

Possible extensions:

* Highlight missing skills directly in resumes
* Resume rewriting suggestions
* Improved skill taxonomy
* Support for DOCX resumes
* Deployment via Streamlit Cloud or Docker
* LLM-based skill extraction
* Job description summarization

---

## License

MIT License

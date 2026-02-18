import streamlit as st
from utils import (
    extract_text_from_pdf,
    clean_text,
    compute_match_score,
    missing_skills,
    compute_skill_match_percentage,
)

# Configures Streamlit page
st.set_page_config(page_title="Resume ↔ JD Matcher", layout="centered")

st.title("📄 Resume ↔ Job Description Matcher")
st.write("Upload your resume and a job description to see how well they match.")

# Inputs
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description", height=250)

# Main analysis trigger
if st.button("🔍 Analyze Match"):

    if resume_file and jd_text.strip():
        with st.spinner("Analyzing..."):

            # Extract and normalise resume text
            resume_text = extract_text_from_pdf(resume_file)
            resume_text = clean_text(resume_text)

            # Extract and normalise job description 
            jd_text_clean = clean_text(jd_text)

            score = compute_match_score(resume_text, jd_text_clean)
            gaps = missing_skills(resume_text, jd_text_clean)
            gaps = [g for g in gaps if isinstance(g, dict)]


            strong = [g for g in gaps if g["score"] >= 0.80]
            weak = [g for g in gaps if 0.65 <= g["score"] < 0.80]
            missing = [g for g in gaps if g["score"] < 0.65]

            gaps = missing_skills(resume_text, jd_text_clean)
            skill_match_pct = compute_skill_match_percentage(gaps)


        st.subheader("📊 Match Score")
        st.metric("Resume–JD Match", f"{score}%")
        st.subheader("📊 Skill Match Score")
        st.metric("JD Skill Coverage", f"{skill_match_pct}%")


        # st.subheader("🧩 Missing / Weak Skills")
        # if gaps:
        #     for skill in gaps[:15]:
        #         st.write(f"- {skill}")
        # else:
        #     st.success("Great match! No major skill gaps detected.")

        st.subheader("🧩 Skill Match Breakdown")

        if strong:
            st.markdown("### ✅ Strong Matches")
            for s in strong:
                st.write(f"- **{s['jd_skill']}** (matched with *{s['best_match']}*, score: {s['score']})")

        if weak:
            st.markdown("### ⚠️ Partial / Weak Matches")
            for w in weak:
                st.write(
                    f"- **{w['jd_skill']}** → closest match: *{w['best_match']}* "
                    f"(similarity: {w['score']})"
                )

        if missing:
            st.markdown("### ❌ Missing Skills")
            for m in missing:
                st.write(f"- **{m['jd_skill']}** (no strong related skill found)")
        else:
            st.success("Excellent coverage — no critical skills missing.")


        # st.subheader("✍️ Resume Improvement Suggestions")
        # st.write(
        #     "• Add measurable impact (metrics, results)\n"
        #     "• Mirror key job description terminology\n"
        #     "• Add missing skills naturally into experience bullets\n"
        #     "• Prioritize relevant projects at the top"
        # )

    else:
        st.warning("Please upload a resume and paste a job description.")

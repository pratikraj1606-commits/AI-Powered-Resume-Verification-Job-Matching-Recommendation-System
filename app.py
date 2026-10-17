
import streamlit as st

from src.resume_parser import clean_resume_text, extract_skills
from src.job_matcher import recommend_jobs

from pypdf import PdfReader

st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide",
)

st.title("AI-Powered Resume Verification & Job Matching")
st.write("Upload your PDF resume to find matching jobs.")

jobs = [
    {
        "title": "Python Developer",
        "company": "Example Tech A",
        "description": """
        Python programming, SQL, Django,
        REST API development and Git.
        """,
    },
    {
        "title": "Data Analyst",
        "company": "Example Tech B",
        "description": """
        SQL, Excel, Power BI, data analysis
        and dashboard development.
        """,
    },
    {
        "title": "Machine Learning Intern",
        "company": "Example Tech C",
        "description": """
        Python, SQL, machine learning,
        data analysis and model evaluation.
        """,
    },
]

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
)

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    raw_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            raw_text += page_text + "\n"

    if not raw_text.strip():
        st.warning("Readable text nahi mila. PDF check karo.")
    else:
        resume_text = clean_resume_text(raw_text)
        resume_skills = extract_skills(resume_text)

        st.subheader("Extracted Skills")
        st.write(", ".join(resume_skills) or "No supported skills found.")

        recommendations = recommend_jobs(
            resume_text,
            resume_skills,
            jobs,
        )

        st.subheader("Ranked Job Recommendations")
        st.caption(
            "Similarity score text overlap dikhata hai, "
            "hiring probability nahi."
        )

        for rank, job in enumerate(recommendations, start=1):
            with st.expander(
                f"#{rank} {job['title']} — {job['score']}% similarity"
            ):
                st.write("**Company:**", job["company"])
                st.write(
                    "**Matched skills:**",
                    ", ".join(job["matched_skills"]) or "None detected",
                )
                st.write(
                    "**Missing skills:**",
                    ", ".join(job["missing_skills"]) or "None detected",
                )

        st.info(
            "Abhi ye demo ke liye sample jobs hain, "
            "real vacancies nahi."
        )

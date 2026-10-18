import streamlit as st

from pypdf import PdfReader

from src.resume_parser import clean_resume_text, extract_skills
from src.job_matcher import recommend_jobs, load_jobs


st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide",
)

st.title("AI-Powered Resume Verification & Job Matching")
st.write("Upload your PDF resume to find matching jobs.")

# Load jobs from the JSON dataset
try:
    jobs = load_jobs()
except (OSError, ValueError) as error:
    st.error(f"Could not load the job dataset: {error}")
    st.stop()
except Exception as error:
    st.error(f"Unexpected error loading jobs: {error}")
    st.stop()

st.caption(f"Jobs available in dataset: {len(jobs)}")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"],
)

if uploaded_file is not None:
    try:
        reader = PdfReader(uploaded_file)
        raw_text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                raw_text += page_text + "\n"

        if not raw_text.strip():
            st.warning(
                "Readable text nahi mila. "
                "PDF check karo; scanned PDFs ke liye OCR ki zarurat ho sakti hai."
            )
        else:
            resume_text = clean_resume_text(raw_text)
            resume_skills = extract_skills(resume_text)

            st.subheader("Extracted Skills")
            st.write(
                ", ".join(resume_skills)
                or "No supported skills found."
            )

            recommendations = recommend_jobs(
                resume_text,
                resume_skills,
                jobs,
            )

            st.subheader("Ranked Job Recommendations")
            st.caption(
                "Similarity score text similarity dikhata hai, "
                "hiring probability nahi."
            )

            if not recommendations:
                st.info("Dataset mein abhi koi job available nahi hai.")

            for rank, job in enumerate(recommendations, start=1):
                with st.expander(
                    f"#{rank} {job['title']} — "
                    f"{job['score']}% similarity"
                ):
                    st.write("**Company:**", job["company"])

                    st.write(
                        "**Matched skills:**",
                        ", ".join(job["matched_skills"])
                        or "None detected",
                    )

                    st.write(
                        "**Missing skills:**",
                        ", ".join(job["missing_skills"])
                        or "None detected",
                    )

                    application_url = job.get("application_url", "")

                    if application_url:
                        st.link_button(
                            "Open application page",
                            application_url,
                        )
                    else:
                        st.caption(
                            "Application link abhi add nahi kiya gaya hai."
                        )

            st.info(
                "Ye sample dataset hai, real vacancies nahi. "
                "Application links ko use karne se pehle verify karna zaroori hai."
            )

    except Exception as error:
        st.error(f"Resume process karte waqt error aaya: {error}")

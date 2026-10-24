import streamlit as st
from pypdf import PdfReader

from src.resume_verifier import verify_resume_text
from src.resume_parser import clean_resume_text, extract_skills
from src.job_matcher import recommend_jobs, load_jobs


st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide",
)

st.title("AI-Powered Resume Verification & Job Matching")
st.write(
    "Upload your PDF resume to review its content and discover "
    "matching job profiles."
)

# Load the job dataset.
try:
    jobs = load_jobs()
except (OSError, ValueError) as error:
    st.error(f"Could not load the job dataset: {error}")
    st.stop()
except Exception as error:
    st.error(f"Unexpected error loading jobs: {error}")
    st.stop()

st.caption(f"Sample job profiles in dataset: {len(jobs)}")

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
                "Readable text nahi mila. PDF check karo. "
                "Scanned PDFs ke liye OCR ki zarurat ho sakti hai."
            )
        else:
            resume_text = clean_resume_text(raw_text)
            resume_skills = extract_skills(resume_text)

            # Resume verification.
            verification = verify_resume_text(raw_text)

            st.subheader("Resume Verification Review")

            if verification["status"] == "No Issues Detected":
                st.success("No Issues Detected")
            else:
                st.warning("Needs Review")

            if verification["issues"]:
                st.markdown("**Issues to check**")
                for issue in verification["issues"]:
                    st.write(f"- {issue}")

            if verification["review_signals"]:
                st.markdown("**Review signals**")
                for signal in verification["review_signals"]:
                    st.write(f"- {signal}")

            if (
                not verification["issues"]
                and not verification["review_signals"]
            ):
                st.write("No review signals were detected by these checks.")

            st.caption(
                "Automated checks can miss inconsistencies or flag normal "
                "content. These results do not establish whether a resume "
                "is genuine or fraudulent."
            )

            # Extracted skills.
            st.subheader("Extracted Skills")

            if resume_skills:
                st.write(", ".join(resume_skills))
                st.caption(f"Supported skills detected: {len(resume_skills)}")
            else:
                st.info("No supported skills found in this resume.")

            # Job recommendations.
            recommendations = recommend_jobs(
                resume_text,
                resume_skills,
                jobs,
            )

            st.subheader("Ranked Job Recommendations")
            st.caption(
                "Match scores estimate similarity to the sample job profiles. "
                "They do not represent hiring or selection probability."
            )

            if not recommendations:
                st.info("No job profiles are available in the dataset.")
            else:
                for rank, job in enumerate(recommendations, start=1):
                    with st.expander(
                        f"#{rank} {job['title']} — "
                        f"{job['score']:.2f}% match"
                    ):
                        st.write("**Company:**", job["company"])

                        col1, col2, col3 = st.columns(3)

                        col1.metric(
                            "Final Match Score",
                            f"{job['score']:.2f}%",
                        )
                        col2.metric(
                            "Text Similarity",
                            f"{job['text_similarity']:.2f}%",
                        )
                        col3.metric(
                            "Skill Coverage",
                            f"{job['skill_coverage']:.2f}%",
                        )

                        st.markdown("**Matched skills**")
                        if job["matched_skills"]:
                            st.write(", ".join(job["matched_skills"]))
                        else:
                            st.write("No required skills matched.")

                        st.markdown("**Skills to develop**")
                        if job["missing_skills"]:
                            st.write(", ".join(job["missing_skills"]))
                        else:
                            st.write(
                                "All skills listed for this sample profile "
                                "were detected."
                            )

                        st.write(
                            "**Experience level:**",
                            job.get("experience_level", "Not specified"),
                        )
                        st.write(
                            "**Location:**",
                            job.get("location", "Not specified"),
                        )
                        st.write(
                            "**Work mode:**",
                            job.get("work_mode", "Not specified"),
                        )
                        st.write(
                            "**Employment type:**",
                            job.get("employment_type", "Not specified"),
                        )

                        application_url = job.get("application_url", "")

                        if application_url:
                            st.link_button(
                                "Open application page",
                                application_url,
                            )
                        else:
                            st.caption(
                                "No application link is available "
                                "for this sample profile."
                            )

            st.info(
                "This dataset contains sample job profiles, not verified "
                "live vacancies. Check an employer and its official listing "
                "before applying."
            )

    except Exception as error:
        st.error(f"Resume process karte waqt error aaya: {error}")

import json
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.resume_parser import (
    extract_resume_text,
    clean_resume_text,
    extract_skills,
)


TEXT_WEIGHT = 0.60
SKILL_WEIGHT = 0.40


def normalize_skill(skill):
    """Normalize common skill names and aliases."""
    skill = re.sub(r"\s+", " ", str(skill).strip().lower())

    aliases = {
        "powerbi": "power bi",
        "scikit learn": "scikit-learn",
        "sklearn": "scikit-learn",
        "rest api development": "rest api",
        "structured query language": "sql",
        "microsoft excel": "excel",
        "ml": "machine learning",
    }

    return aliases.get(skill, skill)


def match_resume_to_job(resume_text, job_description):
    """Calculate TF-IDF text similarity as a percentage."""
    resume_text = clean_resume_text(resume_text or "")
    job_description = clean_resume_text(job_description or "")

    if not resume_text or not job_description:
        return 0.0

    documents = [resume_text, job_description]

    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2],
        )

        return round(float(similarity[0][0]) * 100, 2)

    except ValueError:
        # For example, both documents contain no usable tokens.
        return 0.0


def analyze_skill_gap(resume_skills, required_skills):
    """Return matched and missing required skills."""
    resume_set = {
        normalize_skill(skill)
        for skill in (resume_skills or [])
        if str(skill).strip()
    }

    required_set = {
        normalize_skill(skill)
        for skill in (required_skills or [])
        if str(skill).strip()
    }

    return {
        "matched_skills": sorted(resume_set & required_set),
        "missing_skills": sorted(required_set - resume_set),
    }


def calculate_skill_coverage(resume_skills, required_skills):
    """Calculate the percentage of required skills matched."""
    required_set = {
        normalize_skill(skill)
        for skill in (required_skills or [])
        if str(skill).strip()
    }

    if not required_set:
        return 0.0

    gap = analyze_skill_gap(resume_skills, required_skills)

    return round(
        len(gap["matched_skills"]) / len(required_set) * 100,
        2,
    )


def recommend_jobs(resume_text, resume_skills, jobs):
    """Rank jobs using text similarity and skill coverage."""
    recommendations = []

    for job in jobs:
        if not isinstance(job, dict):
            raise ValueError("Each job must be a dictionary.")

        for field in ("title", "company", "description"):
            if not isinstance(job.get(field), str):
                raise ValueError(
                    f"Each job must have a valid '{field}' field."
                )

        required_skills = job.get("required_skills")

        if required_skills is None:
            required_skills = extract_skills(job["description"])

        if not isinstance(required_skills, list):
            raise ValueError("'required_skills' must be a list.")

        text_score = match_resume_to_job(
            resume_text,
            job["description"],
        )

        gap = analyze_skill_gap(
            resume_skills,
            required_skills,
        )

        skill_score = calculate_skill_coverage(
            resume_skills,
            required_skills,
        )

        final_score = round(
            TEXT_WEIGHT * text_score
            + SKILL_WEIGHT * skill_score,
            2,
        )

        recommendations.append({
            "title": job["title"],
            "company": job["company"],
            "score": final_score,
            "text_similarity": text_score,
            "skill_coverage": skill_score,
            "matched_skills": gap["matched_skills"],
            "missing_skills": gap["missing_skills"],
            "application_url": job.get("application_url", ""),
            "experience_level": job.get("experience_level", ""),
            "location": job.get("location", ""),
            "work_mode": job.get("work_mode", ""),
            "employment_type": job.get("employment_type", ""),
        })

    recommendations.sort(
        key=lambda job: (
            job["score"],
            job["skill_coverage"],
            job["text_similarity"],
        ),
        reverse=True,
    )

    return recommendations


def load_jobs(json_path="data/jobs.json"):
    """Load and validate the job dataset."""
    with open(json_path, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    if not isinstance(jobs, list):
        raise ValueError("jobs.json must contain a list of jobs.")

    for job in jobs:
        if not isinstance(job, dict):
            raise ValueError("Each job must be a dictionary.")

        for field in ("title", "company", "description"):
            if not isinstance(job.get(field), str):
                raise ValueError(
                    f"Each job must have a valid '{field}' field."
                )

        required_skills = job.get("required_skills", [])

        if not isinstance(required_skills, list):
            raise ValueError("'required_skills' must be a list.")

        if not all(
            isinstance(skill, str) for skill in required_skills
        ):
            raise ValueError("Each required skill must be a string.")

        application_url = job.get("application_url", "")

        if not isinstance(application_url, str):
            raise ValueError("'application_url' must be a string.")

    return jobs


if __name__ == "__main__":
    pdf_path = "data/resume.pdf"

    raw_text = extract_resume_text(pdf_path)
    resume_text = clean_resume_text(raw_text)
    resume_skills = extract_skills(resume_text)

    jobs = load_jobs()

    recommendations = recommend_jobs(
        resume_text,
        resume_skills,
        jobs,
    )

    print("\n--- JOB RECOMMENDATIONS ---")
    print("Resume Skills:", resume_skills)

    for rank, job in enumerate(recommendations, start=1):
        print(f"\nRank {rank}: {job['title']}")
        print("Company:", job["company"])
        print(f"Final Match Score: {job['score']}%")
        print(f"Text Similarity: {job['text_similarity']}%")
        print(f"Skill Coverage: {job['skill_coverage']}%")
        print("Matched Skills:", job["matched_skills"])
        print("Missing Skills:", job["missing_skills"])

        if job["application_url"]:
            print("Application URL:", job["application_url"])

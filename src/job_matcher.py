import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.resume_parser import (
    extract_resume_text,
    clean_resume_text,
    extract_skills,
)


def match_resume_to_job(resume_text, job_description):
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )

    return round(float(similarity[0][0]) * 100, 2)


def analyze_skill_gap(resume_skills, required_skills):
    resume_set = {skill.lower() for skill in resume_skills}
    required_set = {skill.lower() for skill in required_skills}

    return {
        "matched_skills": sorted(resume_set & required_set),
        "missing_skills": sorted(required_set - resume_set),
    }


def recommend_jobs(resume_text, resume_skills, jobs):
    recommendations = []

    for job in jobs:
        score = match_resume_to_job(
            resume_text,
            job["description"]
        )

        required_skills = job.get("required_skills")

        if required_skills is None:
            required_skills = extract_skills(job["description"])

        gap = analyze_skill_gap(resume_skills, required_skills)

        recommendations.append({
            "title": job["title"],
            "company": job["company"],
            "score": score,
            "matched_skills": gap["matched_skills"],
            "missing_skills": gap["missing_skills"],
            "application_url": job.get("application_url", ""),
        })

    recommendations.sort(
        key=lambda job: job["score"],
        reverse=True
    )

    return recommendations


def load_jobs(json_path="data/jobs.json"):
    with open(json_path, "r", encoding="utf-8") as file:
        jobs = json.load(file)

    if not isinstance(jobs, list):
        raise ValueError("jobs.json must contain a list of jobs.")

    for job in jobs:
        for field in ("title", "company", "description"):
            if not isinstance(job.get(field), str):
                raise ValueError(
                    f"Each job must have a valid '{field}' field."
                )

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
        jobs
    )

    print("\n--- JOB RECOMMENDATIONS ---")
    print("Resume Skills:", resume_skills)

    for rank, job in enumerate(recommendations, start=1):
        print(f"\nRank {rank}: {job['title']}")
        print("Company:", job["company"])
        print(f"Text Similarity: {job['score']}%")
        print("Matched Skills:", job["matched_skills"])
        print("Missing Skills:", job["missing_skills"])

        if job["application_url"]:
            print("Application URL:", job["application_url"])

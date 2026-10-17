
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

        required_skills = extract_skills(job["description"])
        gap = analyze_skill_gap(resume_skills, required_skills)

        recommendations.append({
            "title": job["title"],
            "company": job["company"],
            "score": score,
            "matched_skills": gap["matched_skills"],
            "missing_skills": gap["missing_skills"],
        })

    recommendations.sort(
        key=lambda job: job["score"],
        reverse=True
    )

    return recommendations


if __name__ == "__main__":
    pdf_path = "data/resume.pdf"

    raw_text = extract_resume_text(pdf_path)
    resume_text = clean_resume_text(raw_text)
    resume_skills = extract_skills(resume_text)

    jobs = [
        {
            "title": "Python Developer",
            "company": "Example Tech A",
            "description": """
            Python programming, SQL, Django,
            REST API development and Git.
            """
        },
        {
            "title": "Data Analyst",
            "company": "Example Tech B",
            "description": """
            SQL, Excel, Power BI, data analysis
            and dashboard development.
            """
        },
        {
            "title": "Machine Learning Intern",
            "company": "Example Tech C",
            "description": """
            Python, SQL, machine learning,
            data analysis and model evaluation.
            """
        },
    ]

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

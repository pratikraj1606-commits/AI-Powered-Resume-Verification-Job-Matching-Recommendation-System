
import unittest

from src.job_matcher import (
    analyze_skill_gap,
    calculate_skill_coverage,
    recommend_jobs,
)


class TestJobMatcher(unittest.TestCase):

    def test_empty_jobs(self):
        results = recommend_jobs(
            "Python SQL",
            ["python", "sql"],
            [],
        )

        self.assertEqual(results, [])

    def test_recommendations_are_ranked(self):
        resume_text = "Python developer with SQL data analysis skills"
        resume_skills = ["python", "sql"]

        jobs = [
            {
                "title": "Python Developer",
                "company": "Company A",
                "description": "Python SQL software development",
                "required_skills": ["python", "sql"],
            },
            {
                "title": "Graphic Designer",
                "company": "Company B",
                "description": "Graphic design illustration and colors",
                "required_skills": ["graphic design", "illustration"],
            },
        ]

        results = recommend_jobs(
            resume_text,
            resume_skills,
            jobs,
        )

        self.assertEqual(len(results), 2)
        self.assertGreaterEqual(
            results[0]["score"],
            results[1]["score"],
        )
        self.assertEqual(results[0]["title"], "Python Developer")

    def test_skill_gap(self):
        gap = analyze_skill_gap(
            ["python", "sql"],
            ["python", "power bi"],
        )

        self.assertEqual(gap["matched_skills"], ["python"])
        self.assertEqual(gap["missing_skills"], ["power bi"])


def test_skill_coverage_normalizes_aliases():
    resume_skills = ["Python", "PowerBI", "ML", "SQL"]

    required_skills = [
        "python",
        "power bi",
        "machine learning",
        "sql",
    ]

    assert calculate_skill_coverage(
        resume_skills,
        required_skills,
    ) == 100.0

    
def test_recommend_jobs_rejects_non_dictionary_job():
    import pytest

    with pytest.raises(ValueError, match="Each job must be a dictionary"):
        recommend_jobs(
            "Python developer",
            ["python"],
            ["invalid job record"],
        )


def test_recommend_jobs_rejects_invalid_required_skills():
    import pytest

    jobs = [
        {
            "title": "Python Developer",
            "company": "Company A",
            "description": "Python development",
            "required_skills": "python",
        }
    ]

    with pytest.raises(
        ValueError,
        match="'required_skills' must be a list",
    ):
        recommend_jobs("Python developer", ["python"], jobs)


def test_recommend_jobs_returns_application_details():
    jobs = [
        {
            "title": "Python Developer",
            "company": "Company A",
            "description": "Python development",
            "required_skills": ["python"],
            "application_url": "https://example.com/jobs/python",
            "experience_level": "Intern",
            "location": "India",
            "work_mode": "Remote",
            "employment_type": "Internship",
        }
    ]

    results = recommend_jobs(
        "Python developer",
        ["python"],
        jobs,
    )

    assert len(results) == 1
    assert results[0]["application_url"] == (
        "https://example.com/jobs/python"
    )
    assert results[0]["experience_level"] == "Intern"
    assert results[0]["work_mode"] == "Remote"


def test_duplicate_skills_do_not_inflate_coverage():
    resume_skills = ["Python", "Python", "SQL"]
    required_skills = ["python", "python", "sql"]

    assert calculate_skill_coverage(
        resume_skills,
        required_skills,
    ) == 100.0


def test_empty_required_skills_return_zero_coverage():
    assert calculate_skill_coverage(
        ["python", "sql"],
        [],
    ) == 0.0


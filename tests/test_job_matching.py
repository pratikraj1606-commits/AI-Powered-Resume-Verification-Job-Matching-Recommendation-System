
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

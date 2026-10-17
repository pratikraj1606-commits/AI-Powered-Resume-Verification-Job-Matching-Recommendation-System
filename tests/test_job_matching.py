
import unittest

from src.job_matcher import (
    analyze_skill_gap,
    recommend_jobs,
)


class TestJobMatcher(unittest.TestCase):

    def test_skill_gap(self):
        result = analyze_skill_gap(
            ["Python", "SQL"],
            ["Python", "SQL", "Power BI"]
        )

        self.assertEqual(
            result["matched_skills"],
            ["python", "sql"]
        )
        self.assertEqual(
            result["missing_skills"],
            ["power bi"]
        )

    def test_recommendations_are_ranked(self):
        resume = "Python SQL programming database"
        skills = ["python", "sql"]

        jobs = [
            {
                "title": "SQL Developer",
                "company": "Example B",
                "description": "Excel dashboard reporting"
            },
            {
                "title": "Python Developer",
                "company": "Example A",
                "description": "Python SQL programming database"
            },
        ]

        results = recommend_jobs(resume, skills, jobs)

        self.assertEqual(len(results), 2)
        self.assertGreaterEqual(
            results[0]["score"],
            results[1]["score"]
        )
        self.assertEqual(
            results[0]["title"],
            "Python Developer"
        )

    def test_empty_jobs(self):
        results = recommend_jobs(
            "Python SQL",
            ["python", "sql"],
            []
        )
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()

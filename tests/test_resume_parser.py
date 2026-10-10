
import unittest

from src.resume_parser import clean_resume_text, extract_skills, categorize_skills


class TestResumeParser(unittest.TestCase):

    def test_clean_resume_text(self):
        result = clean_resume_text("Python  SQL\n\nMachine Learning")
        self.assertEqual(result, "python sql machine learning")

    def test_python_skill(self):
        result = extract_skills("I know Python")
        self.assertIn("python", result)

    def test_sql_skill(self):
        result = extract_skills("I know SQL")
        self.assertIn("sql", result)

    def test_ml_alias(self):
        result = extract_skills("I know ML")
        self.assertIn("machine learning", result)

    def test_powerbi_alias(self):
        result = extract_skills("I know PowerBI")
        self.assertIn("power bi", result)

    def test_sql_not_detected_inside_nosql(self):
        result = extract_skills("I know NoSQL")
        self.assertNotIn("sql", result)

    def test_skill_categories(self):
        skills = ["python", "sql", "machine learning"]
        result = categorize_skills(skills)

        self.assertIn("Python", result["Programming"])
        self.assertIn("Sql", result["Database"])
        self.assertIn("Machine Learning", result["Machine Learning"])


if __name__ == "__main__":
    unittest.main()

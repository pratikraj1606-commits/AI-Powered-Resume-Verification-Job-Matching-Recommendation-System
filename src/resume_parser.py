
import re
from pypdf import PdfReader


def extract_resume_text(pdf_path):
    reader = PdfReader(pdf_path)
    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    return resume_text


def clean_resume_text(text):
    # Remove unwanted replacement characters
    text = text.replace("ï¿½", " ")
    text = text.replace("\ufffd", " ")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


# Canonical skill names and their aliases
SKILL_ALIASES = {
    "python": ["python"],
    "sql": ["sql", "structured query language"],
    "excel": ["excel", "microsoft excel"],
    "machine learning": ["machine learning", "ml"],
    "power bi": ["power bi", "powerbi"],
    "data analysis": ["data analysis", "data analytics"],
}
SKILL_CATEGORIES = {
    "Programming": ["python"],
    "Database": ["sql"],
    "Analytics": ["excel", "power bi", "data analysis"],
    "Machine Learning": ["machine learning"],
}


def categorize_skills(found_skills):
    categorized = {}

    for category, category_skills in SKILL_CATEGORIES.items():
        matched = [
            skill.title()
            for skill in found_skills
            if skill in category_skills
        ]

        if matched:
            categorized[category] = matched

    return categorized

def extract_skills(resume_text):
    text = clean_resume_text(resume_text)
    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(alias)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills


if __name__ == "__main__":
    pdf_path = "data/resume.pdf"

    raw_text = extract_resume_text(pdf_path)
    cleaned_text = clean_resume_text(raw_text)

    print("Resume extracted and cleaned successfully.")
    print("Cleaned text length:", len(cleaned_text))

    print("\n--- CLEANING TEST ---")
    print(clean_resume_text("Python  SQL\n\nMachine Learning"))

    print("\n--- SKILL EXTRACTION ---")
    found_skills = extract_skills(cleaned_text)

    print("Total skills found:", len(found_skills))

    for skill in found_skills:
        print("-", skill.title())
    
    print("\n--- ALIAS TEST ---")

test_resume = "I know Python, ML, SQL and PowerBI."
print("Input:", test_resume)
print("Found:", extract_skills(test_resume))

print("\n--- SKILL CATEGORIES ---")

sample_skills = extract_skills(
    "Python, SQL, Machine Learning, Excel and Power BI"
)

categories = categorize_skills(sample_skills)

for category, skills_list in categories.items():
    print(f"{category}: {', '.join(skills_list)}")

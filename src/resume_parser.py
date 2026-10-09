
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
    text = text.replace("", " ")
    text = text.replace("�", " ")

    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    text = text.lower()

    return text


pdf_path = "data/resume.pdf"

raw_text = extract_resume_text(pdf_path)
cleaned_text = clean_resume_text(raw_text)

print("Resume text extracted and cleaned successfully.")
print("cleaned text length:", len(cleaned_text),"characters")


print("\n--- CLEANING TEST ---")

test_text = "Python  SQL\n\nMachine Learning"
print(clean_resume_text(test_text))
print("\n--- DAY 2 TESTS ---")

test_cases = [
    "Python SQL",
    "MACHINE Learning",
    "Data Science"
]

for test in test_cases:
    print(clean_resume_text(test))

print("\n--- SKILL EXTRACTION ---")

skills = [
    "python",
    "sql",
    "excel",
    "machine learning",
    "power bi",
    "data analysis"
]
print(skills)

found_skills = []

for skill in skills:
    if skill in cleaned_text:
        found_skills.append(skill)
       

print("\nTotal skills found:", len(found_skills))

for skill in found_skills:
    print("-", skill.title())
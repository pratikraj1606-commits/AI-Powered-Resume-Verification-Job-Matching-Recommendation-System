import re
from pypdf import PdfReader

pdf_path = "data/resume.pdf"

reader = PdfReader(pdf_path)

resume_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        resume_text += text + "\n"

# Clean unwanted characters
resume_text = resume_text.replace("", " ")
resume_text = resume_text.replace("�", " ")

# Remove extra spaces and line breaks
resume_text = re.sub(r"\s+", " ", resume_text).strip()

print("CLEANED RESUME TEXT:")
print(resume_text)
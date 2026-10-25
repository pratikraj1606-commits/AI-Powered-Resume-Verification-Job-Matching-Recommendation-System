# AI-Powered Resume Verification, Job Matching & Recommendation System

An AI-powered resume analysis prototype that extracts text and skills from PDF resumes, compares resumes with job descriptions, recommends relevant roles, identifies potential skill gaps, and highlights resume details that may need further review.

The project combines Natural Language Processing (NLP), TF-IDF vectorization, cosine similarity, rule-based skill extraction, and an interactive Streamlit interface.

## Features

- **PDF Resume Parsing:** Extracts text from uploaded PDF resumes.
- **Text Cleaning:** Normalizes extracted text for further analysis.
- **Skill Extraction:** Detects supported technical skills using predefined aliases and pattern matching.
- **Resume Review Signals:** Flags selected patterns and inconsistencies for manual review.
- **Job Matching:** Compares resume content with job descriptions using TF-IDF and cosine similarity.
- **Job Recommendations:** Ranks sample job roles by text similarity.
- **Skill-Gap Analysis:** Identifies detected matching skills and skills missing for a recommended role.
- **Interactive Web Interface:** Upload a resume and explore analysis results using Streamlit.
- **Automated Testing:** Includes tests for resume parsing, job matching, and resume review checks.

## Tech Stack

- Python
- Streamlit
- scikit-learn
- pypdf
- pytest
- NLP and TF-IDF
- Cosine similarity
- Git and GitHub

## Project Structure

```text
AI-Resume-Screening-System/
├── app.py
├── data/
│   ├── jobs.json
│   └── resume.pdf
├── src/
│   ├── resume_parser.py
│   ├── job_matcher.py
│   └── resume_verifier.py
├── tests/
│   ├── test_resume_parser.py
│   ├── test_job_matching.py
│   └── test_resume_verifier.py
├── README.md
└── .gitignore
```

Additional project folders may be used for future API, frontend, model, and notebook development.

## Installation

Clone the repository and navigate to the project directory.

Install the required libraries:

```bash
python -m pip install streamlit scikit-learn pypdf pytest
```

## Run the Application

From the project root directory, run:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal to use the application.

## Run Tests

Run the automated test suite:

```bash
python -m pytest -v
```

## How It Works

1. The user uploads a PDF resume through the Streamlit interface.
2. The application extracts and cleans the resume text.
3. The parser identifies supported skills.
4. The resume review module checks for selected patterns that may require manual verification.
5. The job-matching engine compares resume content with job descriptions.
6. The application ranks matching sample roles and identifies potential skill gaps.
7. Results are displayed through the web interface.

## Important Limitations

- **Demo job data:** The current `data/jobs.json` file contains sample job records, not verified live vacancies. Application links are not currently provided.
- **Similarity scores:** These represent textual similarity, not the probability of getting hired or a guarantee of job suitability.
- **Skill extraction:** Results are limited to the skills and aliases supported by the current implementation.
- **Resume review:** Flags are preliminary review signals, not proof that a resume is fake or fraudulent.
- **PDF quality:** Extraction results may vary depending on document formatting and whether the PDF contains selectable text.

## Future Improvements

- Integrate verified job listings and official application links.
- Expand skill extraction and experience analysis.
- Improve explanations for resume review signals.
- Enhance recommendation ranking and skill-gap analysis.
- Develop a dedicated API and expand automated testing.
- Improve handling of scanned PDFs and unusual document layouts.

## Project Status

The project currently implements PDF resume parsing, text cleaning, skill extraction, resume review checks, TF-IDF-based job matching, skill-gap analysis, and a Streamlit interface.

The prototype has an automated test suite. Real-time job integration, official application links, and further validation remain future improvements.

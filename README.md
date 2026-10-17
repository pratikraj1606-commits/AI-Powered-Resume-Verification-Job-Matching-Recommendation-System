# AI-Powered Resume Verification, Job Matching & Recommendation System

An AI-powered resume analysis project that extracts skills from PDF resumes, compares resume content with job descriptions, recommends relevant roles, and highlights potential skill gaps using Natural Language Processing (NLP) and machine learning techniques.

## Features

- **PDF Resume Parsing:** Extracts text from uploaded PDF resumes.
- **Text Cleaning:** Normalizes extracted text for further processing.
- **Skill Extraction:** Identifies supported skills using predefined aliases and pattern matching.
- **Job Matching:** Uses TF-IDF vectorization and cosine similarity to compare resumes with job descriptions.
- **Job Recommendations:** Ranks sample jobs by text similarity.
- **Skill-Gap Analysis:** Identifies detected matching and missing skills.
- **Interactive Web Interface:** Upload a resume and view results using Streamlit.
- **Automated Tests:** Tests key resume parsing and job-matching functions.

## Tech Stack

- Python
- Streamlit
- scikit-learn
- pypdf
- Python unittest
- NLP and TF-IDF

## Project Structure

```text
AI-Resume-Screening-System/
├── app.py
├── src/
│   ├── resume_parser.py
│   └── job_matcher.py
├── tests/
│   ├── test_resume_parser.py
│   └── test_job_matching.py
├── data/
│   └── resume.pdf
└── README.md
```

## Installation

Install the required libraries:

```bash
python -m pip install streamlit scikit-learn pypdf
```

## Run the Application

From the project root directory, run:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal.

## Testing

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

## Important Notes

- Current job listings are sample data for demonstration; they are not live vacancies.
- Similarity scores represent text similarity, not the probability of being hired.
- Skill extraction is limited to the skills and aliases currently supported by the system.
- Potential resume inconsistencies should be treated as review signals, not definitive proof of fraud.

## Future Improvements

- Connect to real job listings and official application links.
- Expand skill extraction and experience analysis.
- Add explainable resume anomaly checks.
- Improve job recommendations and skill-gap analysis.
- Develop a dedicated API and expand automated testing.

## Project Status

The resume parsing, skill extraction, TF-IDF matching, skill-gap analysis, and Streamlit interface are implemented as an initial working prototype. Further development and validation are ongoing.
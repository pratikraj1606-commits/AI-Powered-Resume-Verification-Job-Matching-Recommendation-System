import re
from pypdf import PdfReader


def extract_resume_text(pdf_path):
    """Extract readable text from a PDF resume."""
    reader = PdfReader(pdf_path)
    resume_text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            resume_text += page_text + "\n"

    return resume_text


def clean_resume_text(text):
    """Normalize extracted resume text."""
    if not isinstance(text, str):
        return ""

    text = text.replace("Ã¯Â¿Â½", " ")
    text = text.replace("\ufffd", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


SKILL_ALIASES = {
    # Programming languages
    "python": ["python", "python programming"],
    "c": ["c programming", "c language"],
    "c++": ["c++", "cpp"],
    "java": ["java programming", "java"],
    "javascript": ["javascript", "js"],

    # Databases
    "sql": ["structured query language", "sql"],
    "mysql": ["mysql", "my sql"],
    "mongodb": ["mongodb", "mongo db"],
    "mongodb atlas": ["mongodb atlas", "mongo db atlas"],
    "mongoose": ["mongoose"],
    "database design": ["database design", "database schema design"],
    "query optimization": ["query optimization", "sql query optimization"],
    "dbms": ["dbms", "database management system"],

    # Frontend development
    "html": ["html5", "html"],
    "css": ["css3", "css", "cascading style sheets"],
    "react": ["react.js", "reactjs", "react"],
    "tailwind css": ["tailwind css", "tailwindcss"],
    "bootstrap": ["bootstrap"],

    # Backend development
    "node.js": ["node.js", "nodejs", "node"],
    "express.js": ["express.js", "expressjs", "express"],
    "rest api": [
        "restful apis",
        "restful api",
        "rest apis",
        "rest api",
    ],
    "jwt authentication": [
        "jwt authentication",
        "json web tokens",
        "json web token",
        "jwt",
    ],
    "api integration": ["api integration"],
    "crud operations": ["crud operations", "crud"],

    # Tools and platforms
    "git": ["git version control", "git"],
    "github": ["github"],
    "vs code": ["visual studio code", "vs code"],
    "postman": ["postman"],
    "powerpoint": [
        "microsoft powerpoint",
        "ms powerpoint",
        "powerpoint",
    ],

    # Analytics and office tools
    "excel": ["microsoft excel", "ms excel", "excel"],
    "power bi": ["microsoft power bi", "powerbi", "power bi"],
    "reporting": ["data reporting", "reporting"],
    "data analysis": [
        "exploratory data analysis",
        "data analytics",
        "data analysis",
    ],
    "data visualization": [
        "data visualisation",
        "data visualization",
    ],
    "statistics": ["statistical analysis", "statistics"],

    # Machine learning
    "machine learning": ["machine learning", "ml"],
    "pandas": ["pandas"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],

    # Software development and testing
    "debugging": ["debugging", "debug"],
    "software testing": [
        "quality assurance",
        "software testing",
        "testing",
    ],
    "test cases": ["test case design", "test cases"],

    # Computer science fundamentals
    "dsa": [
        "data structures and algorithms",
        "data structure and algorithms",
        "dsa",
    ],
    "oop": [
        "object-oriented programming",
        "object oriented programming",
        "oop",
    ],
}


SKILL_CATEGORIES = {
    "Programming": [
        "python",
        "c",
        "c++",
        "java",
        "javascript",
    ],
    "Frontend Development": [
        "html",
        "css",
        "react",
        "tailwind css",
        "bootstrap",
    ],
    "Backend Development": [
        "node.js",
        "express.js",
        "rest api",
        "jwt authentication",
        "api integration",
        "crud operations",
    ],
    # Keep "Database" for compatibility with existing tests.
    "Database": [
        "sql",
        "mysql",
        "mongodb",
        "mongodb atlas",
        "mongoose",
        "database design",
        "query optimization",
        "dbms",
    ],
    "Analytics": [
        "excel",
        "power bi",
        "data analysis",
        "reporting",
        "data visualization",
        "statistics",
    ],
    "Machine Learning": [
        "machine learning",
        "pandas",
        "scikit-learn",
    ],
    "Development Tools": [
        "git",
        "github",
        "vs code",
        "postman",
    ],
    "Software Testing": [
        "debugging",
        "software testing",
        "test cases",
    ],
    "Computer Science Fundamentals": [
        "dsa",
        "oop",
    ],
    "Office Tools": [
        "powerpoint",
    ],
}


def _contains_skill(text, alias):
    """Match a skill without matching it inside a larger word."""
    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(alias.lower())
        + r"(?![a-z0-9])"
    )

    return re.search(pattern, text) is not None


def extract_skills(resume_text):
    """Extract supported skills as canonical skill names."""
    text = clean_resume_text(resume_text)

    if not text:
        return []

    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        if any(_contains_skill(text, alias) for alias in aliases):
            found_skills.append(skill)

    return found_skills


def categorize_skills(found_skills):
    """Group extracted skills into categories."""
    normalized_skills = {
        str(skill).strip().lower()
        for skill in found_skills
        if str(skill).strip()
    }

    categorized = {}

    for category, category_skills in SKILL_CATEGORIES.items():
        matched = [
            skill.title()
            for skill in category_skills
            if skill in normalized_skills
        ]

        if matched:
            categorized[category] = matched

    return categorized

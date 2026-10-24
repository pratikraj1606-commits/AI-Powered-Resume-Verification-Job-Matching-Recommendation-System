import re


def verify_resume_text(text):
    """
    Identify resume content that may need manual review.
    This function does not determine whether a resume is fake.
    """
    issues = []
    review_signals = []

    if not text or not text.strip():
        return {
            "status": "Needs Review",
            "issues": ["Resume text is empty."],
            "review_signals": [],
        }

    cleaned_text = re.sub(r"\s+", " ", text).strip()
    lower_text = cleaned_text.lower()

    # Check whether PDF extraction produced very little text.
    if len(cleaned_text) < 200:
        issues.append(
            "Resume text is unusually short. "
            "Check PDF extraction or resume completeness."
        )

    # Check for an email address.
    email_pattern = (
        r"\b[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    if not re.search(email_pattern, cleaned_text):
        review_signals.append("No email address detected.")

    # Check for a recognizable phone number.
    phone_pattern = (
        r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?"
        r"(?:\(?\d{3,5}\)?[-.\s]?)?"
        r"\d{5,10}(?!\w)"
    )

    if not re.search(phone_pattern, cleaned_text):
        review_signals.append(
            "No recognizable phone number detected."
        )

    # Check common resume sections.
    sections = {
        "Education": ["education", "academic background"],
        "Experience": [
            "experience",
            "work history",
            "employment history",
        ],
        "Skills": ["skills", "technical skills"],
    }

    missing_sections = []

    for section, keywords in sections.items():
        if not any(keyword in lower_text for keyword in keywords):
            missing_sections.append(section)

    if missing_sections:
        review_signals.append(
            "Common sections not detected: "
            + ", ".join(missing_sections)
            + "."
        )

    # Flag identical repeated long lines for manual review.
    lines = [
        line.strip().lower()
        for line in text.splitlines()
        if len(line.strip()) >= 25
    ]

    line_counts = {}

    for line in lines:
        line_counts[line] = line_counts.get(line, 0) + 1

    repeated_count = sum(
        1 for count in line_counts.values() if count > 1
    )

    if repeated_count:
        review_signals.append(
            f"{repeated_count} repeated long line(s) detected."
        )

    # Check explicit year ranges such as 2022-2024 or 2024 to 2022.
    # This is a basic consistency check, not proof of misconduct.
    year_range_pattern = (
        r"\b((?:19|20)\d{2})\s*"
        r"(?:-|–|—|\bto\b)\s*"
        r"((?:19|20)\d{2}|present|current)\b"
    )

    reversed_ranges = []

    for match in re.finditer(year_range_pattern, lower_text):
        start_year = int(match.group(1))
        end_value = match.group(2)

        if end_value.isdigit():
            end_year = int(end_value)

            if start_year > end_year:
                reversed_ranges.append(
                    f"{start_year}-{end_year}"
                )

    if reversed_ranges:
        unique_ranges = sorted(set(reversed_ranges))

        review_signals.append(
            "Date range(s) appear to be in reverse order: "
            + ", ".join(unique_ranges)
            + ". Please verify these dates manually."
        )

    status = (
        "Needs Review"
        if issues or review_signals
        else "No Issues Detected"
    )

    return {
        "status": status,
        "issues": issues,
        "review_signals": review_signals,
    }

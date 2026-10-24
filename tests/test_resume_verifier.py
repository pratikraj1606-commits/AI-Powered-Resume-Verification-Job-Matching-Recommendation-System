from src.resume_verifier import verify_resume_text


def test_empty_resume_text():
    result = verify_resume_text("")

    assert result["status"] == "Needs Review"
    assert result["issues"] == ["Resume text is empty."]
    assert result["review_signals"] == []


def test_short_resume_is_flagged():
    result = verify_resume_text("Python developer")

    assert result["status"] == "Needs Review"
    assert any(
        "unusually short" in issue
        for issue in result["issues"]
    )


def test_missing_contact_is_flagged():
    text = (
        "Education: BTech Electronics Engineering. "
        "Experience: Python developer working on projects. "
        "Skills: Python, SQL, Excel. "
        + "Additional project details. " * 10
    )

    result = verify_resume_text(text)

    assert any(
        "email address" in signal
        for signal in result["review_signals"]
    )
    assert any(
        "phone number" in signal
        for signal in result["review_signals"]
    )


def test_complete_sample_has_no_review_signals():
    text = (
        "Email: john@example.com Phone: +91 9876543210\n"
        "Education\nBTech Electronics and Communication Engineering\n"
        "Experience\nPython developer building software projects\n"
        "Skills\nPython SQL Excel\n"
        + "Developed and tested software applications. " * 6
    )

    result = verify_resume_text(text)

    assert result["status"] == "No Issues Detected"
    assert result["issues"] == []
    assert result["review_signals"] == []


    
def test_reversed_year_range_is_flagged():
    text = (
        "Email: john@example.com Phone: +91 9876543210\n"
        "Education\nBTech Electronics Engineering\n"
        "Experience\nDeveloper role from 2024-2022\n"
        "Skills\nPython SQL Excel\n"
        + "Developed and tested software applications. " * 6
    )

    result = verify_resume_text(text)

    assert result["status"] == "Needs Review"
    assert any(
        "reverse order" in signal
        for signal in result["review_signals"]
    )


def test_valid_year_range_is_not_flagged():
    text = (
        "Email: john@example.com Phone: +91 9876543210\n"
        "Education\nBTech Electronics Engineering 2021-2025\n"
        "Experience\nPython developer from 2023-2024\n"
        "Skills\nPython SQL Excel\n"
        + "Developed and tested software applications. " * 6
    )

    result = verify_resume_text(text)

    assert not any(
        "reverse order" in signal
        for signal in result["review_signals"]
    )


def test_present_end_date_is_not_flagged():
    text = (
        "Email: john@example.com Phone: +91 9876543210\n"
        "Education\nBTech Electronics Engineering 2021-2025\n"
        "Experience\nPython developer 2024-present\n"
        "Skills\nPython SQL Excel\n"
        + "Developed and tested software applications. " * 6
    )

    result = verify_resume_text(text)

    assert not any(
        "reverse order" in signal
        for signal in result["review_signals"]
    )


import re
from pathlib import Path

from document_processor import load_document


def extract_text(file_path: str):
    """
    Extract text from a transcript PDF, TXT, or MD file.
    """

    documents = load_document(file_path)

    text = "\n".join(
        document.page_content
        for document in documents
    )

    return text


def parse_transcript(text: str):
    """
    Extract subject code, subject name, credits,
    and grade from a transcript.

    Expected format:

    Sub code | Subject name | Credits | Grade secured
    CS101    | DBMS         | 4       | C
    """

    subjects = []

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Skip headings
        lower_line = line.lower()

        if (
            "sub code" in lower_line
            or "subject name" in lower_line
            or "marks details" in lower_line
            or "personal details" in lower_line
        ):
            continue

        # Support | separated transcript rows
        if "|" in line:

            parts = [
                part.strip()
                for part in line.split("|")
            ]

            if len(parts) >= 4:

                subject_code = parts[0]
                subject_name = parts[1]
                credits = parts[2]
                grade = parts[3].upper()

                # Check that the last field looks like a grade
                if grade in ["A+", "A", "B", "C", "D", "F"]:

                    subjects.append({
                        "subject_code": subject_code,
                        "subject": subject_name,
                        "credits": credits,
                        "grade": grade
                    })

    return subjects


def parse_transcript_file(file_path: str):
    """
    Complete transcript parsing pipeline.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    text = extract_text(file_path)

    subjects = parse_transcript(text)

    if not subjects:
        raise ValueError(
            "No subject records were detected in the transcript."
        )

    return subjects
import re
import string
from typing import Dict, List, Tuple


SUBJECT_ALIASES = {
    "database management systems": [
        "database management systems",
        "database management",
        "dbms",
        "database systems",
    ],
    "python programming": [
        "python programming",
        "python",
    ],
    "java programming": [
        "java programming",
        "java",
    ],
    "web technologies": [
        "web technologies",
        "web technology",
        "web development",
        "web programming",
    ],
    "computer networks": [
        "computer networks",
        "computer network",
        "networking",
        "networks",
    ],
    "javascript": [
        "javascript",
        "java script",
    ],
    "data science": [
        "data science",
    ],
    "machine learning": [
        "machine learning",
    ],
    "software engineering": [
        "software engineering",
    ],
    "operating systems": [
        "operating systems",
        "operating system",
        "os",
    ],
}


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = text.replace("’", "'")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_topic(text: str) -> str:
    text = normalize_text(text)

    text = text.strip(" -:;,.|")

    text = re.sub(
        r"^(unit|module|chapter|topic)\s*[\divxlc]+\s*[-:.)]?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    return text.strip()


def is_metadata_line(line: str) -> bool:
    normalized = normalize_text(line)

    if not normalized:
        return True

    metadata_patterns = [
        r"^syllabus$",
        r"^course syllabus$",
        r"^course outline$",
        r"^course notes$",
        r"^notes$",
        r"^subject$",
        r"^subject name$",
        r"^unit$",
        r"^module$",
        r"^semester$",
        r"^academic year$",
        r"^department$",
        r"^college$",
        r"^university$",
        r"^course code$",
        r"^sub code$",
        r"^credits$",
    ]

    for pattern in metadata_patterns:
        if re.fullmatch(pattern, normalized):
            return True

    return False


def clean_topic(line: str) -> str:
    topic = normalize_topic(line)

    topic = re.sub(
        r"^(unit|module|chapter)\s+[a-z0-9ivxlc]+\s*[:.)-]\s*",
        "",
        topic,
        flags=re.IGNORECASE,
    )

    topic = re.sub(
        r"^\d+\s*[\.)-]\s*",
        "",
        topic,
    )

    topic = topic.strip(" -:;,.|")

    return topic


def extract_topic_lines(text: str) -> List[str]:
    """
    Supports common syllabus formats:
      Topic
      1. Topic
      - Topic
      Topic | Topic
      Topic; Topic
      Topic: subtopic
    """

    if not text:
        return []

    results = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if is_metadata_line(line):
            continue

        # Pipe-separated content
        if "|" in line:
            parts = line.split("|")
        # Semicolon-separated content
        elif ";" in line:
            parts = line.split(";")
        else:
            parts = [line]

        for part in parts:
            topic = clean_topic(part)

            if not topic:
                continue

            if len(topic) < 3:
                continue

            # Avoid obvious table headings.
            if topic.lower() in {
                "topics",
                "topic",
                "contents",
                "units",
                "unit topics",
            }:
                continue

            results.append(topic)

    return list(dict.fromkeys(results))


def looks_like_subject_heading(line: str) -> bool:
    normalized = normalize_text(line)

    if not normalized:
        return False

    for aliases in SUBJECT_ALIASES.values():
        for alias in aliases:
            if normalized == normalize_text(alias):
                return True

    return False


def find_subject_for_line(line: str) -> str:
    normalized = normalize_text(line)

    for subject, aliases in SUBJECT_ALIASES.items():
        for alias in aliases:
            alias_normalized = normalize_text(alias)

            if normalized == alias_normalized:
                return subject

            if alias_normalized in normalized:
                return subject

    return ""


def extract_subject_topic_groups(
    syllabus_text: str
) -> Dict[str, List[str]]:
    """
    Try to associate topics with subject headings.
    """

    groups: Dict[str, List[str]] = {}

    current_subject = ""

    for raw_line in syllabus_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        subject = find_subject_for_line(line)

        if subject:
            current_subject = subject
            groups.setdefault(current_subject, [])
            continue

        if is_metadata_line(line):
            continue

        topics = extract_topic_lines(line)

        if not topics:
            continue

        if current_subject:
            groups.setdefault(current_subject, [])

            for topic in topics:
                if topic not in groups[current_subject]:
                    groups[current_subject].append(topic)

    return groups


def fallback_group_topics(
    syllabus_text: str
) -> Dict[str, List[str]]:
    topics = extract_topic_lines(syllabus_text)

    if not topics:
        return {}

    return {
        "Other Syllabus Topics": topics
    }


def analyze_syllabus_topics(
    syllabus_text: str
) -> Dict[str, List[str]]:
    """
    Extract syllabus topics grouped by subject.
    """

    if not syllabus_text:
        return {}

    groups = extract_subject_topic_groups(syllabus_text)

    # If headings were not detected, keep all topics instead
    # of returning an empty result.
    if not groups:
        groups = fallback_group_topics(syllabus_text)

    return groups


def analyze_notes_topics(
    notes_text: str,
    syllabus_groups: Dict[str, List[str]]
) -> Dict[str, List[str]]:
    """
    Extract topics from notes.

    If syllabus groups are available, attempt to place note topics
    under those subjects.
    """

    if not notes_text:
        return {}

    if not syllabus_groups:
        topics = extract_topic_lines(notes_text)

        return {
            "Course Notes": topics
        } if topics else {}

    result = {
        subject: []
        for subject in syllabus_groups
    }

    unmatched = []

    for raw_line in notes_text.splitlines():
        line = raw_line.strip()

        if not line or is_metadata_line(line):
            continue

        detected_subject = find_subject_for_line(line)

        if detected_subject and detected_subject in result:
            continue

        topics = extract_topic_lines(line)

        for topic in topics:
            normalized_topic = normalize_text(topic)

            matched_subject = None

            for subject in syllabus_groups:
                if subject == "Other Syllabus Topics":
                    continue

                if normalize_text(subject) in normalized_topic:
                    matched_subject = subject
                    break

                for syllabus_topic in syllabus_groups[subject]:
                    syllabus_normalized = normalize_text(
                        syllabus_topic
                    )

                    if (
                        syllabus_normalized in normalized_topic
                        or normalized_topic in syllabus_normalized
                    ):
                        matched_subject = subject
                        break

                if matched_subject:
                    break

            if matched_subject:
                if topic not in result[matched_subject]:
                    result[matched_subject].append(topic)
            else:
                unmatched.append(topic)

    if unmatched:
        result.setdefault("Other Notes Topics", [])

        for topic in unmatched:
            if topic not in result["Other Notes Topics"]:
                result["Other Notes Topics"].append(topic)

    return {
        subject: topics
        for subject, topics in result.items()
        if topics
    }


def topic_matches(
    syllabus_topic: str,
    notes_topics: List[str]
) -> bool:
    syllabus_normalized = normalize_text(syllabus_topic)

    if not syllabus_normalized:
        return False

    for note_topic in notes_topics:
        note_normalized = normalize_text(note_topic)

        if not note_normalized:
            continue

        if syllabus_normalized == note_normalized:
            return True

        if (
            syllabus_normalized in note_normalized
            or note_normalized in syllabus_normalized
        ):
            return True

        syllabus_words = set(
            syllabus_normalized.split()
        )

        note_words = set(
            note_normalized.split()
        )

        if len(syllabus_words) >= 2:
            overlap = syllabus_words.intersection(note_words)

            if len(overlap) >= max(
                2,
                int(len(syllabus_words) * 0.6)
            ):
                return True

    return False


def find_uncovered_topics(
    syllabus_groups: Dict[str, List[str]],
    notes_groups: Dict[str, List[str]]
) -> Dict[str, List[str]]:
    """
    Return syllabus topics that do not appear to be covered
    by the uploaded notes.
    """

    missing = {}

    for subject, syllabus_topics in syllabus_groups.items():

        if subject == "Other Syllabus Topics":
            notes_topics = notes_groups.get(
                "Course Notes",
                []
            )
        else:
            notes_topics = notes_groups.get(
                subject,
                []
            )

        missing_topics = []

        for topic in syllabus_topics:
            if not topic_matches(
                topic,
                notes_topics
            ):
                missing_topics.append(topic)

        if missing_topics:
            missing[subject] = missing_topics

    return missing


def build_coverage(
    syllabus_groups: Dict[str, List[str]],
    notes_groups: Dict[str, List[str]]
) -> Dict[str, Dict]:
    """
    Produce subject-wise syllabus coverage.
    """

    coverage = {}

    for subject, syllabus_topics in syllabus_groups.items():

        if subject == "Other Syllabus Topics":
            notes_topics = notes_groups.get(
                "Course Notes",
                []
            )
        else:
            notes_topics = notes_groups.get(
                subject,
                []
            )

        topic_results = []

        covered_count = 0

        for topic in syllabus_topics:
            covered = topic_matches(
                topic,
                notes_topics
            )

            if covered:
                covered_count += 1

            topic_results.append({
                "topic": topic,
                "covered": covered
            })

        total = len(syllabus_topics)

        percentage = (
            round((covered_count / total) * 100)
            if total
            else 0
        )

        coverage[subject] = {
            "topics": topic_results,
            "covered": covered_count,
            "total": total,
            "percentage": percentage,
        }

    return coverage
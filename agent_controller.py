from pathlib import Path
from collections import defaultdict
import re

from document_processor import load_document
from transcript_parser import parse_transcript

try:
    from job_search import search_jobs_from_transcript
except Exception:
    search_jobs_from_transcript = None


# ============================================================
# BASIC FILE HELPERS
# ============================================================

def read_material(file_path):
    """
    Reads PDF/TXT/MD material.
    Returns plain text.
    """
    if not file_path:
        return ""

    path = Path(file_path)

    if not path.exists():
        return ""

    try:
        documents = load_document(str(path))
        return "\n".join(
            document.page_content
            for document in documents
        ).strip()
    except Exception:
        return ""


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text_line(line):
    line = str(line).strip()

    line = re.sub(
        r"^[\-\*\•\●\▪\►\→\d\.\)\(:]+\s*",
        "",
        line
    )

    line = re.sub(r"\s+", " ", line)

    return line.strip()


def normalize_text(text):
    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SUBJECT / TOPIC DETECTION
# ============================================================

SUBJECT_KEYWORDS = {
    "database": "Database Management Systems",
    "dbms": "Database Management Systems",
    "sql": "Database Management Systems",

    "python": "Python Programming",
    "programming in python": "Python Programming",

    "java": "Java Programming",
    "java programming": "Java Programming",

    "javascript": "JavaScript",
    "javascript programming": "JavaScript",

    "web technology": "Web Technologies",
    "web technologies": "Web Technologies",
    "web development": "Web Technologies",

    "computer network": "Computer Networks",
    "computer networks": "Computer Networks",
    "networking": "Computer Networks",

    "operating system": "Operating Systems",
    "operating systems": "Operating Systems",

    "software engineering": "Software Engineering",

    "data structure": "Data Structures",
    "data structures": "Data Structures",

    "computer organization": "Computer Organization",

    "artificial intelligence": "Artificial Intelligence",
    "machine learning": "Machine Learning",

    "statistics": "Statistics",
    "mathematics": "Mathematics",

    "cloud computing": "Cloud Computing",

    "cyber security": "Cyber Security",
    "cybersecurity": "Cyber Security",
}


def detect_subject_from_text(text):
    """
    Finds likely subject names from material.
    """
    found = []

    lower = text.lower()

    for keyword, subject in SUBJECT_KEYWORDS.items():
        if keyword in lower and subject not in found:
            found.append(subject)

    return found


def split_topic_text(text):
    """
    Extracts useful topic-like lines from syllabus/notes.
    """
    if not text:
        return []

    topics = []

    for raw_line in text.splitlines():

        line = clean_text_line(raw_line)

        if not line:
            continue

        lower = line.lower()

        ignored = [
            "syllabus",
            "course syllabus",
            "course outline",
            "course notes",
            "notes",
            "unit",
            "semester",
            "subject code",
            "credits",
            "marks",
            "department",
            "university",
            "academic year",
            "internal assessment",
            "external assessment",
        ]

        if any(
            item == lower
            for item in ignored
        ):
            continue

        if len(line) < 3:
            continue

        if len(line) > 150:
            continue

        if lower.startswith("page "):
            continue

        # Subject: Topic 1, Topic 2
        if ":" in line:

            left, right = line.split(":", 1)

            if (
                len(left.strip()) < 70
                and len(right.strip()) > 2
            ):

                right_parts = re.split(
                    r",|;|\|",
                    right
                )

                for part in right_parts:

                    part = clean_text_line(part)

                    if (
                        len(part) >= 3
                        and len(part) <= 120
                    ):
                        topics.append(part)

                continue

        # Pipes
        if "|" in line:

            parts = [
                clean_text_line(x)
                for x in line.split("|")
            ]

            for part in parts:

                if 3 <= len(part) <= 120:
                    topics.append(part)

            continue

        # Semicolons
        if ";" in line:

            parts = [
                clean_text_line(x)
                for x in line.split(";")
            ]

            for part in parts:

                if 3 <= len(part) <= 120:
                    topics.append(part)

            continue

        # Ignore unit/module/chapter headings
        if re.match(
            r"^(unit|module|chapter)\s*[\-:]?\s*\d+",
            lower
        ):
            continue

        topics.append(line)

    # Remove duplicates
    result = []
    seen = set()

    for topic in topics:

        key = normalize_text(topic)

        if not key:
            continue

        if key in seen:
            continue

        seen.add(key)
        result.append(topic)

    return result


def group_topics_by_subject(text):
    """
    Attempts to create:

    {
        subject: [topics]
    }

    It also works when the material does not explicitly
    contain subject headings.
    """

    if not text:
        return {}

    lines = [
        clean_text_line(x)
        for x in text.splitlines()
        if clean_text_line(x)
    ]

    groups = defaultdict(list)
    current_subject = None

    for line in lines:

        lower = line.lower()

        detected_subject = None

        for keyword, subject in SUBJECT_KEYWORDS.items():

            if keyword in lower:

                detected_subject = subject
                break

        if detected_subject:

            normalized_line = normalize_text(line)

            normalized_subject = normalize_text(
                detected_subject
            )

            if (
                normalized_line == normalized_subject
                or len(line) < 80
            ):

                current_subject = detected_subject
                groups[current_subject]

                continue

        # Example:
        # Database Management Systems - SQL, ER Model
        if " - " in line:

            left, right = line.split(
                " - ",
                1
            )

            possible_subject = left.strip()

            if 3 <= len(possible_subject) <= 70:

                subject_match = None

                for keyword, subject in SUBJECT_KEYWORDS.items():

                    if keyword in possible_subject.lower():

                        subject_match = subject
                        break

                if subject_match:

                    current_subject = subject_match

                    for part in re.split(
                        r",|;|\|",
                        right
                    ):

                        part = clean_text_line(part)

                        if len(part) >= 3:
                            groups[current_subject].append(
                                part
                            )

                    continue

        # Topic line
        if current_subject:

            if not re.match(
                r"^(unit|module|chapter)\s*[\-:]?\s*\d+",
                lower
            ):

                if len(line) <= 140:
                    groups[current_subject].append(
                        line
                    )

    # Remove duplicates
    cleaned = {}

    for subject, topics in groups.items():

        unique_topics = []
        seen = set()

        for topic in topics:

            key = normalize_text(topic)

            if not key:
                continue

            if key in seen:
                continue

            seen.add(key)
            unique_topics.append(topic)

        if unique_topics:
            cleaned[subject] = unique_topics

    return cleaned


# ============================================================
# TRANSCRIPT
# ============================================================

def get_transcript_subjects(transcript_file):

    if not transcript_file:
        return []

    text = read_material(
        transcript_file
    )

    if not text:
        return []

    try:

        subjects = parse_transcript(
            text
        )

        if subjects:
            return subjects

    except Exception:
        pass

    return []


# ============================================================
# PERFORMANCE
# ============================================================

GRADE_PRIORITY = {
    "F": 5,
    "D": 4,
    "C": 3,
    "B": 2,
    "A": 1,
    "A+": 0,
}


def performance_data(subjects):

    result = []

    for item in subjects:

        grade = str(
            item.get(
                "grade",
                ""
            )
        ).upper()

        subject = item.get(
            "subject",
            "Unknown Subject"
        )

        credits = item.get(
            "credits",
            ""
        )

        if grade == "A+":

            status = "Excellent"
            priority = "Normal Revision"

        elif grade == "A":

            status = "Very Good"
            priority = "Normal Revision"

        elif grade == "B":

            status = "Good"
            priority = "Regular Revision"

        elif grade == "C":

            status = "Needs Improvement"
            priority = "Medium Priority"

        elif grade == "D":

            status = "Weak"
            priority = "High Priority"

        elif grade == "F":

            status = "Very Weak"
            priority = "Very High Priority"

        else:

            status = "Needs Review"
            priority = "Review"

        result.append({
            "subject": subject,
            "grade": grade,
            "credits": credits,
            "status": status,
            "priority": priority,
            "priority_score": GRADE_PRIORITY.get(
                grade,
                2
            )
        })

    result.sort(
        key=lambda x: x["priority_score"],
        reverse=True
    )

    return result


# ============================================================
# SYLLABUS COVERAGE
# ============================================================

def topic_matches(topic, notes_topics):

    target = normalize_text(topic)

    if not target:
        return False

    target_words = set(
        target.split()
    )

    for note in notes_topics:

        note_normalized = normalize_text(
            note
        )

        if not note_normalized:
            continue

        if (
            target in note_normalized
            or note_normalized in target
        ):
            return True

        note_words = set(
            note_normalized.split()
        )

        if len(target_words) >= 2:

            common = (
                target_words
                & note_words
            )

            if len(common) >= max(
                2,
                int(len(target_words) * 0.6)
            ):
                return True

    return False


def build_coverage(
    syllabus_text,
    notes_text
):

    if not syllabus_text:

        return {
            "mode": "no_syllabus",
            "subjects": [],
            "message": (
                "No syllabus was uploaded. "
                "Upload a syllabus to compare topic coverage."
            )
        }

    syllabus_groups = group_topics_by_subject(
        syllabus_text
    )

    if not syllabus_groups:

        topics = split_topic_text(
            syllabus_text
        )

        if topics:

            syllabus_groups = {
                "Syllabus Topics": topics
            }

    notes_topics = split_topic_text(
        notes_text
    )

    note_groups = group_topics_by_subject(
        notes_text
    )

    for group_topics_list in note_groups.values():

        notes_topics.extend(
            group_topics_list
        )

    # Deduplicate
    unique_notes = []
    seen = set()

    for topic in notes_topics:

        key = normalize_text(topic)

        if key and key not in seen:

            seen.add(key)
            unique_notes.append(topic)

    notes_topics = unique_notes

    result_subjects = []

    for subject, topics in syllabus_groups.items():

        subject_result = {
            "subject": subject,
            "topics": []
        }

        for topic in topics:

            covered = (
                topic_matches(
                    topic,
                    notes_topics
                )
                if notes_text
                else False
            )

            subject_result["topics"].append({
                "topic": topic,
                "covered": covered
            })

        result_subjects.append(
            subject_result
        )

    if not notes_text:

        message = (
            "Syllabus detected. Course notes were not uploaded, "
            "so topics are shown as pending coverage."
        )

    else:

        total = sum(
            len(x["topics"])
            for x in result_subjects
        )

        covered = sum(
            1
            for subject in result_subjects
            for topic in subject["topics"]
            if topic["covered"]
        )

        message = (
            f"{covered} of {total} syllabus topics "
            "are covered by the uploaded notes."
        )

    return {
        "mode": "comparison",
        "subjects": result_subjects,
        "message": message
    }


# ============================================================
# STUDY TOPICS
# ============================================================

def collect_material_topics(
    syllabus_text,
    notes_text
):

    syllabus_groups = group_topics_by_subject(
        syllabus_text
    )

    notes_groups = group_topics_by_subject(
        notes_text
    )

    all_groups = defaultdict(list)

    for subject, topics in syllabus_groups.items():

        all_groups[subject].extend(
            topics
        )

    for subject, topics in notes_groups.items():

        all_groups[subject].extend(
            topics
        )

    if not all_groups:

        topics = []

        topics.extend(
            split_topic_text(
                syllabus_text
            )
        )

        topics.extend(
            split_topic_text(
                notes_text
            )
        )

        if topics:

            all_groups[
                "Course Material"
            ].extend(
                topics
            )

    final_groups = {}

    for subject, topics in all_groups.items():

        seen = set()
        unique = []

        for topic in topics:

            key = normalize_text(
                topic
            )

            if not key:
                continue

            if key in seen:
                continue

            seen.add(key)
            unique.append(topic)

        if unique:
            final_groups[subject] = unique

    return final_groups


# ============================================================
# STUDY PLAN
# ============================================================

def get_subject_priority(
    subject,
    performance
):

    normalized = normalize_text(
        subject
    )

    for item in performance:

        current = normalize_text(
            item["subject"]
        )

        if (
            normalized in current
            or current in normalized
        ):
            return item[
                "priority_score"
            ]

    return 2


def create_study_plan(
    subjects,
    syllabus_text,
    notes_text,
    days,
    hours_per_day
):

    days = int(
        days or 1
    )

    hours_per_day = int(
        hours_per_day or 2
    )

    days = max(
        1,
        min(days, 30)
    )

    hours_per_day = max(
        1,
        min(hours_per_day, 12)
    )

    performance = performance_data(
        subjects
    )

    material_groups = collect_material_topics(
        syllabus_text,
        notes_text
    )

    # If only transcript exists
    if not material_groups and subjects:

        material_groups = {}

        for item in subjects:

            material_groups[
                item["subject"]
            ] = [
                "Core concepts and important topics",
                "Previous concepts and revision",
                "Exam-focused revision",
            ]

    if not material_groups:

        return {
            "days": days,
            "hours_per_day": hours_per_day,
            "total_hours":
                days * hours_per_day,
            "entries": [],
            "message": (
                "Upload at least one academic material "
                "file to generate a study plan."
            )
        }

    subject_scores = {}

    for subject in material_groups:

        subject_scores[subject] = (
            get_subject_priority(
                subject,
                performance
            )
        )

    ordered_subjects = sorted(
        material_groups.keys(),
        key=lambda x: subject_scores[x],
        reverse=True
    )

    entries = []

    for day_number in range(
        1,
        days + 1
    ):

        rotation = (
            day_number - 1
        ) % len(ordered_subjects)

        rotated = (
            ordered_subjects[
                rotation:
            ]
            +
            ordered_subjects[
                :rotation
            ]
        )

        if not rotated:
            rotated = ordered_subjects

        remaining_hours = hours_per_day
        day_entries = []

        subject_index = 0

        while remaining_hours > 0:

            subject = rotated[
                subject_index
                % len(rotated)
            ]

            topics = material_groups[
                subject
            ]

            topic_index = (
                day_number
                + subject_index
            ) % len(topics)

            topic = topics[
                topic_index
            ]

            allocated = 1

            if (
                remaining_hours >= 2
                and subject_scores[subject] >= 4
            ):
                allocated = 2

            allocated = min(
                allocated,
                remaining_hours
            )

            day_entries.append({
                "subject": subject,
                "topic": topic,
                "hours": allocated,
                "priority_score":
                    subject_scores[subject]
            })

            remaining_hours -= allocated
            subject_index += 1

        entries.append({
            "day": day_number,
            "hours": hours_per_day,
            "items": day_entries
        })

    return {
        "days": days,
        "hours_per_day": hours_per_day,
        "total_hours":
            days * hours_per_day,
        "entries": entries,
        "message": (
            f"{days}-day study timetable created "
            f"with {hours_per_day} hours per day "
            f"({days * hours_per_day} total hours)."
        )
    }


# ============================================================
# JOB SUBJECT EXTRACTION
# ============================================================

def build_job_subjects(
    transcript_subjects,
    syllabus_text,
    notes_text
):

    subjects = list(
        transcript_subjects or []
    )

    existing = {
        normalize_text(
            x.get("subject", "")
        )
        for x in subjects
    }

    combined = (
        syllabus_text
        + "\n"
        + notes_text
    )

    inferred = detect_subject_from_text(
        combined
    )

    for subject in inferred:

        key = normalize_text(
            subject
        )

        if key not in existing:

            subjects.append({
                "subject": subject,
                "grade": "B",
                "credits": ""
            })

            existing.add(key)

    return subjects


# ============================================================
# BASIC Q&A HELPERS
# ============================================================

def find_subject_from_question(
    question,
    performance
):
    """
    Finds a subject mentioned in the question.
    Supports:
    DBMS
    Python
    Java
    Networks
    etc.
    """

    q = normalize_text(
        question
    )

    # First check actual transcript subjects
    for item in performance:

        subject = str(
            item.get(
                "subject",
                ""
            )
        )

        if not subject:
            continue

        subject_normalized = normalize_text(
            subject
        )

        if subject_normalized in q:
            return subject

        # Check individual words for common subject names
        words = subject_normalized.split()

        if len(words) >= 2:

            important_words = [
                word
                for word in words
                if len(word) > 2
            ]

            if important_words:

                matches = sum(
                    1
                    for word in important_words
                    if word in q
                )

                if matches >= max(
                    1,
                    len(important_words) // 2
                ):
                    return subject

    # Common aliases
    aliases = {
        "dbms":
            "Database Management Systems",

        "database":
            "Database Management Systems",

        "python":
            "Python Programming",

        "java":
            "Java Programming",

        "javascript":
            "JavaScript",

        "web":
            "Web Technologies",

        "networks":
            "Computer Networks",

        "network":
            "Computer Networks",

        "os":
            "Operating Systems",

        "operating system":
            "Operating Systems",

        "ds":
            "Data Structures",

        "data structures":
            "Data Structures",

        "ai":
            "Artificial Intelligence",

        "ml":
            "Machine Learning",
    }

    for alias, subject in aliases.items():

        if alias in q:

            for item in performance:

                actual = str(
                    item.get(
                        "subject",
                        ""
                    )
                )

                if normalize_text(
                    actual
                ) == normalize_text(
                    subject
                ):
                    return actual

            return subject

    return None


def get_missing_topics(
    coverage
):
    """
    Returns all topics that are not covered.
    """

    missing = []

    if not isinstance(
        coverage,
        dict
    ):
        return missing

    for subject_data in coverage.get(
        "subjects",
        []
    ):

        subject = subject_data.get(
            "subject",
            "Unknown Subject"
        )

        for topic_data in subject_data.get(
            "topics",
            []
        ):

            if not topic_data.get(
                "covered",
                False
            ):

                missing.append({
                    "subject": subject,
                    "topic": topic_data.get(
                        "topic",
                        ""
                    )
                })

    return missing


def find_topic_coverage(
    question,
    coverage
):
    """
    Checks whether a specific topic is
    covered in the uploaded notes.
    """

    if not isinstance(
        coverage,
        dict
    ):
        return None

    q = normalize_text(
        question
    )

    for subject_data in coverage.get(
        "subjects",
        []
    ):

        for topic_data in subject_data.get(
            "topics",
            []
        ):

            topic = topic_data.get(
                "topic",
                ""
            )

            topic_normalized = normalize_text(
                topic
            )

            if not topic_normalized:
                continue

            # Direct match
            if topic_normalized in q:

                return (
                    topic,
                    bool(
                        topic_data.get(
                            "covered",
                            False
                        )
                    ),
                    subject_data.get(
                        "subject",
                        ""
                    )
                )

            # Check meaningful words
            topic_words = [
                word
                for word in topic_normalized.split()
                if len(word) > 3
            ]

            if topic_words:

                matches = sum(
                    1
                    for word in topic_words
                    if word in q
                )

                if matches >= max(
                    1,
                    len(topic_words) // 2
                ):

                    return (
                        topic,
                        bool(
                            topic_data.get(
                                "covered",
                                False
                            )
                        ),
                        subject_data.get(
                            "subject",
                            ""
                        )
                    )

    return None


# ============================================================
# BASIC AGENT INFORMATION
# ============================================================

def answer_agent_information(question):
    """
    Answers basic questions about the agent itself.
    These are intentionally short because this is a
    project-demo Q&A, not a general chatbot.
    """

    q = normalize_text(
        question
    )

    if (
        "what can you do" in q
        or "what does this agent do" in q
        or "what can this agent do" in q
    ):

        return (
            "This agent analyzes your transcript, syllabus and "
            "course notes, identifies weak areas and uncovered "
            "topics, creates a study plan, answers basic "
            "academic questions, and finds relevant jobs or "
            "internships."
        )

    if (
        "how are you made" in q
        or "how were you made" in q
        or "how is this agent made" in q
        or "how does this agent work" in q
    ):

        return (
            "The agent is built in Python with separate modules "
            "for document processing, transcript analysis, "
            "study planning, syllabus coverage, Q&A and job "
            "search."
        )

    if (
        "what files" in q
        or "what can i upload" in q
        or "what can i upload" in q
    ):

        return (
            "You can upload a transcript, syllabus and course "
            "notes. The agent can work with one or more of "
            "these files."
        )

    if (
        "how does the study plan" in q
        or "how is the study plan" in q
        or "how do you create the study plan" in q
    ):

        return (
            "The study plan uses your grades and uploaded "
            "academic material. Lower grades receive higher "
            "priority, while syllabus and notes help select "
            "topics to study."
        )

    if (
        "how do you identify weak" in q
        or "how identify weak" in q
        or "weak subjects" in q
    ):

        return (
            "The agent checks the grades in your transcript. "
            "Lower grades such as F, D and C receive higher "
            "study priority."
        )

    if (
        "how does syllabus coverage" in q
        or "how do you check coverage" in q
        or "how are topics checked" in q
    ):

        return (
            "The agent extracts topics from the syllabus and "
            "checks whether matching topics appear in the "
            "uploaded course notes."
        )

    if (
        "what is rag" in q
        or "why rag" in q
        or "rag used" in q
    ):

        return (
            "RAG means Retrieval-Augmented Generation. It allows "
            "an AI system to retrieve relevant information from "
            "uploaded material before answering a question."
        )

    if (
        "how does job search" in q
        or "how do jobs work" in q
        or "how are jobs found" in q
    ):

        return (
            "The job-search feature uses subjects and academic "
            "information from the student's material to find "
            "relevant job or internship opportunities."
        )

    if (
        "does it use transcript" in q
        or "transcript for jobs" in q
    ):

        return (
            "Yes. The transcript is used to identify the "
            "student's studied subjects and help match relevant "
            "job or internship opportunities."
        )

    if (
        "can i use only notes" in q
        or "only notes" in q
    ):

        return (
            "Yes. The agent can work with only course notes. "
            "Some features, such as transcript-based grades, "
            "will simply have no transcript data to use."
        )

    if (
        "can i use only syllabus" in q
    ):

        return (
            "Yes. A syllabus alone can be used to identify "
            "topics and create a study plan."
        )

    return None


# ============================================================
# MAIN Q&A
# ============================================================

def answer_student_question(
    question,
    state
):
    """
    Simple academic Q&A.

    Uses already processed information from
    process_student_material().

    This intentionally gives short, direct answers.
    """

    if not question or not str(question).strip():

        return (
            "Please enter a question about your "
            "transcript, syllabus, notes or the agent."
        )

    question = str(
        question
    ).strip()

    if not isinstance(
        state,
        dict
    ):

        return (
            "Please upload your academic material and "
            "process it before asking a question."
        )

    if not state.get(
        "success",
        False
    ):

        return (
            "Please process your academic material first."
        )

    q = normalize_text(
        question
    )

    # --------------------------------------------------------
    # Agent / system questions
    # --------------------------------------------------------

    agent_answer = answer_agent_information(
        question
    )

    if agent_answer:
        return agent_answer

    # --------------------------------------------------------
    # Data from processed state
    # --------------------------------------------------------

    performance = state.get(
        "performance",
        []
    )

    coverage = state.get(
        "coverage",
        {}
    )

    plan = state.get(
        "study_plan",
        {}
    )

    # --------------------------------------------------------
    # Grade question
    # --------------------------------------------------------

    asks_grade = any(
        phrase in q
        for phrase in [
            "what grade",
            "which grade",
            "my grade",
            "grade did i get",
            "grade i got",
            "score did i get",
            "what score",
        ]
    )

    if asks_grade:

        subject = find_subject_from_question(
            question,
            performance
        )

        if subject:

            for item in performance:

                if normalize_text(
                    item.get(
                        "subject",
                        ""
                    )
                ) == normalize_text(
                    subject
                ):

                    grade = item.get(
                        "grade",
                        "Not available"
                    )

                    return (
                        f"You got {grade} in "
                        f"{item.get('subject', subject)}."
                    )

            # Flexible match
            for item in performance:

                current = normalize_text(
                    item.get(
                        "subject",
                        ""
                    )
                )

                target = normalize_text(
                    subject
                )

                if (
                    target in current
                    or current in target
                ):

                    return (
                        f"You got "
                        f"{item.get('grade', 'Not available')} "
                        f"in {item.get('subject', subject)}."
                    )

        return (
            "I couldn't identify the subject in your "
            "question. Try asking something like: "
            "'What grade did I get in DBMS?'"
        )

    # --------------------------------------------------------
    # Weakest / needs more time
    # --------------------------------------------------------

    asks_more_time = any(
        phrase in q
        for phrase in [
            "needs more time",
            "need more time",
            "needs the most time",
            "needs most time",
            "which subject should i study more",
            "which subject should i study",
            "which subject to study more",
            "which subject needs improvement",
            "weakest subject",
            "weak subject",
            "weakest",
        ]
    )

    if asks_more_time:

        if not performance:

            return (
                "I need your transcript to determine "
                "which subject needs more study time."
            )

        weakest = max(
            performance,
            key=lambda x: x.get(
                "priority_score",
                0
            )
        )

        return (
            f"{weakest.get('subject', 'Unknown Subject')} "
            f"needs the most study time because you received "
            f"{weakest.get('grade', 'N/A')} in that subject. "
            f"It has {weakest.get('priority', 'higher')}."
        )

    # --------------------------------------------------------
    # Best subject
    # --------------------------------------------------------

    asks_best = any(
        phrase in q
        for phrase in [
            "best subject",
            "highest grade",
            "highest score",
            "which subject did i score best",
            "which subject is best",
            "where did i score best",
        ]
    )

    if asks_best:

        if not performance:

            return (
                "I need your transcript to identify "
                "your highest-performing subject."
            )

        best = min(
            performance,
            key=lambda x: x.get(
                "priority_score",
                99
            )
        )

        return (
            f"Your highest-performing subject is "
            f"{best.get('subject', 'Unknown Subject')} "
            f"with a grade of "
            f"{best.get('grade', 'N/A')}."
        )

    # --------------------------------------------------------
    # Number of subjects
    # --------------------------------------------------------

    if (
        "how many subjects" in q
        or "number of subjects" in q
    ):

        if performance:

            return (
                f"Your transcript contains "
                f"{len(performance)} subjects."
            )

        return (
            "No transcript subjects are currently available."
        )

    # --------------------------------------------------------
    # Weak subjects
    # --------------------------------------------------------

    if (
        "weak subjects" in q
        or "subjects are weak" in q
        or "subjects need improvement" in q
    ):

        weak = [
            item
            for item in performance
            if item.get(
                "grade",
                ""
            ).upper()
            in [
                "C",
                "D",
                "F"
            ]
        ]

        if not weak:

            return (
                "No C, D or F grades were found in "
                "the processed transcript."
            )

        names = [
            f"{item.get('subject')} "
            f"({item.get('grade')})"
            for item in weak
        ]

        return (
            "Subjects needing improvement: "
            + ", ".join(names)
            + "."
        )

    # --------------------------------------------------------
    # Missing topics
    # --------------------------------------------------------

    if (
        "missing topics" in q
        or "uncovered topics" in q
        or "topics are missing" in q
        or "topics not covered" in q
        or "not covered topics" in q
    ):

        missing = get_missing_topics(
            coverage
        )

        if not missing:

            if coverage.get(
                "subjects"
            ):

                return (
                    "No uncovered syllabus topics were found."
                )

            return (
                "I need a syllabus and course notes "
                "to determine missing topics."
            )

        display = [
            f"{item['topic']} "
            f"({item['subject']})"
            for item in missing[:10]
        ]

        answer = (
            "Uncovered topics: "
            + ", ".join(display)
        )

        if len(missing) > 10:

            answer += (
                f" and {len(missing) - 10} more."
            )

        return answer + "."

    # --------------------------------------------------------
    # Specific topic coverage
    # --------------------------------------------------------

    topic_result = find_topic_coverage(
        question,
        coverage
    )

    if topic_result:

        topic, covered, subject = (
            topic_result
        )

        if covered:

            return (
                f"Yes. {topic} is covered "
                f"in the uploaded notes"
                + (
                    f" for {subject}."
                    if subject
                    else "."
                )
            )

        return (
            f"No. {topic} is not covered "
            f"in the uploaded notes"
            + (
                f" for {subject}."
                if subject
                else "."
            )
        )

    # --------------------------------------------------------
    # Coverage summary
    # --------------------------------------------------------

    if (
        "how many topics" in q
        or "how much syllabus" in q
        or "syllabus covered" in q
        or "coverage percentage" in q
        or "coverage" in q
    ):

        message = coverage.get(
            "message"
        )

        if message:

            return message

        return (
            "Upload a syllabus and course notes "
            "to calculate topic coverage."
        )

    # --------------------------------------------------------
    # Study plan questions
    # --------------------------------------------------------

    if (
        "how many days" in q
        and "study plan" in q
    ):

        days = plan.get(
            "days"
        )

        if days:
            return (
                f"Your study plan is {days} day(s) long."
            )

    if (
        "how many hours" in q
        and (
            "study plan" in q
            or "per day" in q
        )
    ):

        hours = plan.get(
            "hours_per_day"
        )

        if hours:

            return (
                f"Your study plan allocates "
                f"{hours} hour(s) per day."
            )

    # --------------------------------------------------------
    # Uploaded material
    # --------------------------------------------------------

    if (
        "what did i upload" in q
        or "which files did i upload" in q
        or "uploaded files" in q
        or "what files are uploaded" in q
    ):

        uploaded = []

        if state.get(
            "transcript_uploaded",
            False
        ):
            uploaded.append(
                "Transcript"
            )

        if state.get(
            "syllabus_uploaded",
            False
        ):
            uploaded.append(
                "Syllabus"
            )

        if state.get(
            "notes_uploaded",
            False
        ):
            uploaded.append(
                "Course Notes"
            )

        if uploaded:

            return (
                "Uploaded material: "
                + ", ".join(uploaded)
                + "."
            )

        return (
            "No academic files were uploaded."
        )

    # --------------------------------------------------------
    # Notes questions
    # --------------------------------------------------------

    if (
        "notes uploaded" in q
        or "course notes" in q
    ):

        if state.get(
            "notes_uploaded",
            False
        ):

            return (
                "Yes. Course notes were uploaded "
                "and used for topic coverage analysis."
            )

        return (
            "Course notes were not uploaded."
        )

    # --------------------------------------------------------
    # Syllabus questions
    # --------------------------------------------------------

    if (
        "syllabus uploaded" in q
        or "did i upload syllabus" in q
    ):

        if state.get(
            "syllabus_uploaded",
            False
        ):

            return (
                "Yes. A syllabus was uploaded and "
                "used for topic analysis."
            )

        return (
            "A syllabus was not uploaded."
        )

    # --------------------------------------------------------
    # Transcript questions
    # --------------------------------------------------------

    if (
        "transcript uploaded" in q
        or "did i upload transcript" in q
    ):

        if state.get(
            "transcript_uploaded",
            False
        ):

            return (
                "Yes. A transcript was uploaded and "
                "used for academic performance analysis."
            )

        return (
            "A transcript was not uploaded."
        )

    # --------------------------------------------------------
    # Total study hours
    # --------------------------------------------------------

    if (
        "total study hours" in q
        or "total hours" in q
    ):

        total = plan.get(
            "total_hours"
        )

        if total:

            return (
                f"Your study plan contains "
                f"{total} total study hours."
            )

    # --------------------------------------------------------
    # Default safe response
    # --------------------------------------------------------

    return (
        "I can answer basic questions about your "
        "grades, weak subjects, study priority, "
        "syllabus coverage, missing topics, uploaded "
        "materials and how the agent works. "
        "Try: 'What grade did I get in DBMS?' or "
        "'Which subject needs more time?'"
    )


# ============================================================
# MAIN PROCESSOR
# ============================================================

def process_student_material(
    transcript_file=None,
    syllabus_file=None,
    notes_file=None,
    days=1,
    hours_per_day=2
):
    """
    Flexible processor.

    Works with:
    - transcript only
    - syllabus only
    - notes only
    - transcript + syllabus
    - transcript + notes
    - syllabus + notes
    - all three
    """

    try:

        # ----------------------------------------------------
        # Read available files
        # ----------------------------------------------------

        transcript_text = read_material(
            transcript_file
        )

        syllabus_text = read_material(
            syllabus_file
        )

        notes_text = read_material(
            notes_file
        )

        # ----------------------------------------------------
        # Transcript
        # ----------------------------------------------------

        subjects = []

        if transcript_text:

            try:

                subjects = parse_transcript(
                    transcript_text
                )

            except Exception:

                subjects = []

        # ----------------------------------------------------
        # Performance
        # ----------------------------------------------------

        performance = performance_data(
            subjects
        )

        # ----------------------------------------------------
        # Study plan
        # ----------------------------------------------------

        plan = create_study_plan(
            subjects=subjects,
            syllabus_text=syllabus_text,
            notes_text=notes_text,
            days=days,
            hours_per_day=hours_per_day
        )

        # ----------------------------------------------------
        # Coverage
        # ----------------------------------------------------

        coverage = build_coverage(
            syllabus_text=syllabus_text,
            notes_text=notes_text
        )

        # ----------------------------------------------------
        # Jobs
        # ----------------------------------------------------

        job_subjects = build_job_subjects(
            transcript_subjects=subjects,
            syllabus_text=syllabus_text,
            notes_text=notes_text
        )

        jobs = {
            "search_keywords": [],
            "jobs": [],
            "role_averages": {},
            "location": "Hyderabad",
            "experience": "Fresher",
            "message": (
                "Upload academic material to "
                "find relevant opportunities."
            )
        }

        if search_jobs_from_transcript:

            try:

                jobs = search_jobs_from_transcript(
                    subjects=job_subjects,
                    location="Hyderabad",
                    experience="Fresher"
                )

                if not isinstance(
                    jobs,
                    dict
                ):

                    jobs = {
                        "jobs": [],
                        "message": (
                            "Job search returned no usable results."
                        )
                    }

            except Exception as error:

                jobs = {
                    "jobs": [],
                    "message": (
                        "Job search could not be completed: "
                        f"{error}"
                    )
                }

        # ----------------------------------------------------
        # Availability summary
        # ----------------------------------------------------

        available = []

        if transcript_file:
            available.append(
                "Transcript"
            )

        if syllabus_file:
            available.append(
                "Syllabus"
            )

        if notes_file:
            available.append(
                "Course Notes"
            )

        if available:

            availability_message = (
                "Using uploaded material: "
                + ", ".join(available)
                + "."
            )

        else:

            availability_message = (
                "No academic material uploaded."
            )

        return {
            "success": True,

            "message":
                availability_message,

            "transcript_uploaded":
                bool(transcript_file),

            "syllabus_uploaded":
                bool(syllabus_file),

            "notes_uploaded":
                bool(notes_file),

            "subjects":
                subjects,

            "performance":
                performance,

            "study_plan":
                plan,

            "coverage":
                coverage,

            "jobs":
                jobs,

            # Available for Q&A.
            "material_text": {
                "transcript":
                    transcript_text,
                "syllabus":
                    syllabus_text,
                "notes":
                    notes_text
            }
        }

    except Exception as error:

        return {
            "success": False,

            "message":
                str(error),

            "subjects":
                [],

            "performance":
                [],

            "study_plan": {
                "entries": []
            },

            "coverage": {
                "subjects": []
            },

            "jobs": {
                "jobs": []
            }
        }


# ============================================================
# JOB SEARCH BUTTON SUPPORT
# ============================================================

def search_student_jobs(
    subjects,
    location="Hyderabad",
    experience="Fresher"
):

    if not search_jobs_from_transcript:

        return {
            "jobs": [],
            "message": (
                "job_search.py could not be imported."
            )
        }

    try:

        return search_jobs_from_transcript(
            subjects=subjects or [],
            location=location,
            experience=experience
        )

    except Exception as error:

        return {
            "jobs": [],
            "message": str(error)
        }
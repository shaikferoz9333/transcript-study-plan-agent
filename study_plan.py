from typing import Dict, List, Tuple


GRADE_WEIGHT = {
    "F": 5,
    "D": 4,
    "C": 3,
    "B": 2,
    "A": 1,
    "A+": 1,
}


def _unique_subjects(subjects: List[dict]) -> List[dict]:
    result = []
    seen = set()

    for subject in subjects or []:
        name = str(
            subject.get("subject", "")
        ).strip()

        if not name:
            continue

        key = name.lower()

        if key in seen:
            continue

        seen.add(key)
        result.append(subject)

    return result


def _grade_priority(grade: str) -> int:
    return GRADE_WEIGHT.get(
        str(grade).upper(),
        3
    )


def _topic_priority(
    missing_topics: List[str]
) -> int:
    if not missing_topics:
        return 0

    return min(
        len(missing_topics),
        5
    )


def _get_missing_topics(
    subject_name: str,
    missing_topics: Dict[str, List[str]]
) -> List[str]:

    if not missing_topics:
        return []

    subject_lower = subject_name.lower()

    for key, topics in missing_topics.items():
        if key.lower() == subject_lower:
            return topics

    return []


def _build_priority_list(
    subjects: List[dict],
    missing_topics: Dict[str, List[str]],
    has_transcript: bool
) -> List[dict]:

    priority = []

    for subject in subjects:

        name = subject.get(
            "subject",
            "Unknown Subject"
        )

        grade = subject.get(
            "grade",
            ""
        )

        missing = _get_missing_topics(
            name,
            missing_topics
        )

        if has_transcript:
            grade_score = _grade_priority(grade)
        else:
            grade_score = 1

        topic_score = _topic_priority(
            missing
        )

        total_score = (
            grade_score * 10
            + topic_score
        )

        priority.append({
            "subject": name,
            "grade": grade,
            "missing_topics": missing,
            "score": total_score,
        })

    priority.sort(
        key=lambda item: (
            -item["score"],
            item["subject"].lower()
        )
    )

    return priority


def _allocate_exact_daily_hours(
    priority_list: List[dict],
    daily_hours: int
) -> List[dict]:

    if not priority_list:
        return []

    daily_hours = max(
        1,
        int(daily_hours)
    )

    count = len(priority_list)

    # When there are more available subjects than hours,
    # allocate one full hour to the highest-priority subjects.
    if daily_hours <= count:
        return [
            {
                "subject": item["subject"],
                "hours": 1,
                "grade": item.get("grade", ""),
                "missing_topics": item.get(
                    "missing_topics",
                    []
                ),
            }
            for item in priority_list[:daily_hours]
        ]

    # Give every subject one hour first.
    allocations = []

    for item in priority_list:
        allocations.append({
            "subject": item["subject"],
            "hours": 1,
            "grade": item.get("grade", ""),
            "missing_topics": item.get(
                "missing_topics",
                []
            ),
        })

    remaining = daily_hours - count

    index = 0

    # Add remaining hours without repeating a subject.
    # The same subject's hour total increases instead.
    while remaining > 0:
        allocations[index]["hours"] += 1

        remaining -= 1
        index += 1

        if index >= len(allocations):
            index = 0

    return allocations


def _add_topic_details(
    allocations: List[dict]
) -> List[dict]:

    for allocation in allocations:
        topics = allocation.get(
            "missing_topics",
            []
        )

        if topics:
            allocation["focus"] = topics[:3]
        else:
            allocation["focus"] = []

    return allocations


def create_timetable(
    subjects: List[dict],
    days: int,
    hours_per_day: int,
    missing_topics: Dict[str, List[str]] = None,
    has_transcript: bool = False,
) -> List[dict]:

    subjects = _unique_subjects(subjects)

    days = min(
        30,
        max(1, int(days))
    )

    hours_per_day = min(
        12,
        max(1, int(hours_per_day))
    )

    missing_topics = missing_topics or {}

    priority_list = _build_priority_list(
        subjects=subjects,
        missing_topics=missing_topics,
        has_transcript=has_transcript,
    )

    if not priority_list:
        return []

    timetable = []

    # Rotate priorities slightly across days so students
    # don't always study the exact same subjects first.
    for day_number in range(1, days + 1):

        if len(priority_list) > 1:
            rotation = (day_number - 1) % len(priority_list)

            rotated = (
                priority_list[rotation:]
                + priority_list[:rotation]
            )
        else:
            rotated = priority_list

        allocations = _allocate_exact_daily_hours(
            rotated,
            hours_per_day
        )

        allocations = _add_topic_details(
            allocations
        )

        timetable.append({
            "day": day_number,
            "total_hours": sum(
                item["hours"]
                for item in allocations
            ),
            "subjects": allocations,
        })

    return timetable


def _format_priority_reason(
    item: dict,
    has_transcript: bool
) -> str:

    grade = item.get(
        "grade",
        ""
    )

    missing = item.get(
        "missing_topics",
        []
    )

    reasons = []

    if has_transcript and grade:
        if grade in ["F", "D"]:
            reasons.append(
                f"Grade {grade}: high priority"
            )
        elif grade == "C":
            reasons.append(
                "Grade C: needs improvement"
            )
        elif grade == "B":
            reasons.append(
                "Grade B: regular revision"
            )
        else:
            reasons.append(
                f"Grade {grade}: maintain performance"
            )

    if missing:
        reasons.append(
            f"{len(missing)} syllabus topic(s) "
            "not found in notes"
        )

    if not reasons:
        reasons.append(
            "Equal-priority study allocation"
        )

    return " • ".join(reasons)


def generate_study_plan(
    subjects: List[dict],
    days: int = 1,
    hours_per_day: int = 2,
    missing_topics: Dict[str, List[str]] = None,
    has_transcript: bool = False,
) -> dict:

    subjects = _unique_subjects(subjects)

    days = min(
        30,
        max(1, int(days))
    )

    hours_per_day = min(
        12,
        max(1, int(hours_per_day))
    )

    missing_topics = missing_topics or {}

    timetable = create_timetable(
        subjects=subjects,
        days=days,
        hours_per_day=hours_per_day,
        missing_topics=missing_topics,
        has_transcript=has_transcript,
    )

    priority_list = _build_priority_list(
        subjects=subjects,
        missing_topics=missing_topics,
        has_transcript=has_transcript,
    )

    performance = []

    for item in priority_list:
        performance.append({
            "subject": item["subject"],
            "grade": item.get("grade", ""),
            "priority": item["score"],
            "reason": _format_priority_reason(
                item,
                has_transcript
            ),
            "missing_topics": item.get(
                "missing_topics",
                []
            ),
        })

    total_hours = (
        days * hours_per_day
    )

    if has_transcript:
        message = (
            "Study time is prioritized using transcript grades "
            "and syllabus topics missing from the uploaded notes."
        )
    elif missing_topics:
        message = (
            "Study time is distributed across the uploaded "
            "subjects, with additional focus on syllabus topics "
            "not found in the notes."
        )
    else:
        message = (
            "No transcript grades were provided, so subjects "
            "receive an equal study allocation."
        )

    return {
        "timetable": timetable,
        "performance": performance,
        "total_days": days,
        "hours_per_day": hours_per_day,
        "total_hours": total_hours,
        "planning_mode": (
            "Transcript-based"
            if has_transcript
            else "Equal-priority"
        ),
        "message": message,
    }


def study_plan_generator(
    subjects: List[dict],
    days: int = 1,
    hours_per_day: int = 2,
    missing_topics: Dict[str, List[str]] = None,
    has_transcript: bool = False,
) -> dict:

    return generate_study_plan(
        subjects=subjects,
        days=days,
        hours_per_day=hours_per_day,
        missing_topics=missing_topics,
        has_transcript=has_transcript,
    )
"""
AchieveHire — Last-Minute Preparation Storage & Attempt History
Guarantees:
1. Unlimited attempts per candidate.
2. Every completed attempt is stored permanently as a separate record.
3. Earlier attempts are NEVER overwritten.
4. Isolated by user_id.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

DATA_DIR = Path("data/last_minute_interviews")


def _get_user_file(user_id: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    clean_id = "".join(c for c in user_id if c.isalnum() or c in "-_")
    return DATA_DIR / f"{clean_id}.json"


def load_user_attempts(user_id: str) -> List[Dict[str, Any]]:
    """Loads all historical Last-Minute Preparation attempts for a candidate."""
    if not user_id:
        return []
    file_path = _get_user_file(user_id)
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "attempts" in data:
            return data["attempts"]
        return []
    except Exception:
        return []


def save_new_attempt(user_id: str, attempt_data: Dict[str, Any]) -> str:
    """
    Appends a new completed attempt to the candidate's permanent record.
    Never overwrites earlier attempts.
    """
    if not user_id:
        user_id = "GUEST"

    attempts = load_user_attempts(user_id)

    # Build concise short detail (topic · score% · duration · date)
    topic = attempt_data.get("topic_title", "Preparation")
    score = attempt_data.get("overall_score", 0)
    dur_min = max(1, attempt_data.get("actual_time_taken_sec", 1800) // 60)
    date_str = datetime.now().strftime("%d %b, %Y")
    attempt_data["short_detail"] = f"{topic} · {score}% · {dur_min}m · {date_str}"

    attempt_id = f"LM-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{len(attempts) + 1}"
    attempt_data["attempt_id"] = attempt_id
    attempt_data["saved_at"] = datetime.now().isoformat()
    if "completion_date" not in attempt_data or not attempt_data["completion_date"]:
        attempt_data["completion_date"] = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    attempts.append(attempt_data)

    file_path = _get_user_file(user_id)
    file_path.write_text(json.dumps(attempts, indent=2, ensure_ascii=False), encoding="utf-8")

    return attempt_id


def get_attempt_by_id(user_id: str, attempt_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a specific past attempt record by ID."""
    attempts = load_user_attempts(user_id)
    for a in attempts:
        if a.get("attempt_id") == attempt_id:
            return a
    return None


def get_attempt_comparison_data(user_id: str, mode: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Returns actual attempt-over-attempt score progression for chart comparisons.
    Only compares genuine stored performance data without fabricating progression.
    """
    attempts = load_user_attempts(user_id)
    if mode:
        attempts = [a for a in attempts if a.get("mode") == mode]

    return [
        {
            "short_detail": a.get("short_detail") or f"{a.get('topic_title', 'Preparation')} · {a.get('overall_score', 0)}%",
            "date": a.get("completion_date", ""),
            "topic": a.get("topic_title", "Preparation"),
            "score": a.get("overall_score", 0),
            "attempt_id": a.get("attempt_id", ""),
        }
        for a in attempts
    ]


def get_attempt_short_detail(attempt: Dict[str, Any]) -> str:
    """Returns concise summary (Topic · Score% · Duration · Date). Never generic 'Attempt X'."""
    if attempt.get("short_detail"):
        return attempt["short_detail"]
    topic = attempt.get("topic_title", "Preparation")
    score = attempt.get("overall_score", 0)
    dur_min = max(1, attempt.get("actual_time_taken_sec", 1800) // 60)
    date_str = attempt.get("completion_date", "").split(" at ")[0] or datetime.now().strftime("%d %b, %Y")
    return f"{topic} · {score}% · {dur_min}m · {date_str}"


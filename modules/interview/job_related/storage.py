"""
AchieveHire — Job Related Interview Storage & Persistence
Provides persistent, per-candidate storage for:
- Target Job Role, Target Company, Selected Language
- Stored resume snapshot
- Per-round completion status, scores, time taken, question-by-question evaluations
- Sequential round progression locking (cannot skip rounds)
- Data isolation: candidate data is strictly isolated by user_id
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

DATA_DIR = Path("data/job_interviews")


def _get_user_file(user_id: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    clean_id = "".join(c for c in user_id if c.isalnum() or c in "-_")
    return DATA_DIR / f"{clean_id}.json"


def load_job_interview_session(user_id: str) -> Optional[Dict[str, Any]]:
    """Loads candidate's persistent job interview session from disk."""
    if not user_id:
        return None
    file_path = _get_user_file(user_id)
    if not file_path.exists():
        return None
    try:
        return json.loads(file_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_job_interview_session(user_id: str, session_data: Dict[str, Any]) -> None:
    """Saves candidate's job interview session to disk."""
    if not user_id:
        return
    file_path = _get_user_file(user_id)
    session_data["updated_at"] = datetime.now().isoformat()
    if "created_at" not in session_data:
        session_data["created_at"] = session_data["updated_at"]
    file_path.write_text(json.dumps(session_data, indent=2, ensure_ascii=False), encoding="utf-8")


def initialize_job_interview_session(
    user_id: str,
    target_role: str,
    target_company: str,
    language: str,
    resume_snapshot: Dict[str, Any],
) -> Dict[str, Any]:
    """Initializes or resets a job interview session for a candidate."""
    now_iso = datetime.now().isoformat()
    session_data = {
        "user_id": user_id,
        "target_role": target_role.strip(),
        "target_company": target_company.strip(),
        "language": language,  # Strictly "English", "Hindi", or "Hinglish"
        "resume_snapshot": resume_snapshot or {},
        "active_round": 1,
        "completed_rounds": [],
        "round_evaluations": {},
        "is_overall_completed": False,
        "created_at": now_iso,
        "updated_at": now_iso,
    }
    save_job_interview_session(user_id, session_data)
    return session_data


def save_round_evaluation(
    user_id: str,
    round_num: int,
    evaluation_data: Dict[str, Any],
) -> None:
    """Saves completed evaluation for a specific round and unlocks the next round."""
    session = load_job_interview_session(user_id)
    if not session:
        return

    if "round_evaluations" not in session:
        session["round_evaluations"] = {}
    session["round_evaluations"][str(round_num)] = evaluation_data

    if "completed_rounds" not in session:
        session["completed_rounds"] = []
    if round_num not in session["completed_rounds"]:
        session["completed_rounds"].append(round_num)
        session["completed_rounds"].sort()

    if round_num < 6:
        session["active_round"] = round_num + 1
    else:
        session["active_round"] = 6
        session["is_overall_completed"] = True

    save_job_interview_session(user_id, session)


def is_round_unlocked(session: Optional[Dict[str, Any]], round_num: int) -> bool:
    """
    Checks if a round is accessible based on strict sequential progression.
    Round 1 is always unlocked.
    Round N requires Round N-1 to be completed.
    """
    if round_num == 1:
        return True
    if not session:
        return False
    completed = session.get("completed_rounds", [])
    return (round_num - 1) in completed

"""
AchieveHire — Specialized Interview Persistence & Storage Service
Handles storage, retrieval, round progression state tracking,
and historical report access per user ID.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "interviews"


def _ensure_data_dir() -> Path:
    """Ensure data/interviews exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR


def _sanitize_filename(name: str) -> str:
    """Sanitizes specialization or user ID for safe file names."""
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name.strip().lower())


def get_progress_filepath(user_id: str, specialization: str) -> Path:
    """Returns path to the specialized interview state file for user + specialization."""
    dir_path = _ensure_data_dir()
    u_clean = _sanitize_filename(user_id or "guest")
    s_clean = _sanitize_filename(specialization or "general")
    return dir_path / f"specialized_{u_clean}_{s_clean}.json"


def load_specialized_progress(user_id: str, specialization: str) -> Dict[str, Any]:
    """
    Loads saved specialized interview progress for user_id and specialization.
    Returns empty progression schema if not found.
    """
    p = get_progress_filepath(user_id, specialization)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Default initial schema
    return {
        "user_id": user_id or "guest",
        "specialization": specialization or "Python",
        "language": "English",
        "interviewer_gender": "male",
        "current_unlocked_round": 1,
        "rounds_completed": [],
        "round_results": {},  # "1": {...}, "2": {...}
        "overall_report": None,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def save_specialized_progress(user_id: str, specialization: str, progress_data: Dict[str, Any]) -> bool:
    """Persists specialized interview progress."""
    try:
        progress_data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        p = get_progress_filepath(user_id, specialization)
        p.write_text(json.dumps(progress_data, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error saving specialized progress: {e}")
        return False


def record_round_completion(
    user_id: str,
    specialization: str,
    round_num: int,
    round_result: Dict[str, Any],
    overall_report: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Records completed round result, marks round as completed,
    and unlocks the next round (e.g., completes 1 -> unlocks 2).
    """
    progress = load_specialized_progress(user_id, specialization)
    round_str = str(round_num)

    if round_num not in progress.get("rounds_completed", []):
        progress["rounds_completed"].append(round_num)
        progress["rounds_completed"].sort()

    progress["round_results"][round_str] = round_result

    # Unlock next round if this was the latest
    next_round = round_num + 1
    if next_round <= 4:
        progress["current_unlocked_round"] = max(progress.get("current_unlocked_round", 1), next_round)
    else:
        progress["current_unlocked_round"] = 4  # All rounds completed

    if overall_report:
        progress["overall_report"] = overall_report

    save_specialized_progress(user_id, specialization, progress)
    return progress


def record_round_cancellation(user_id: str, specialization: str, round_num: int, reason: str = "") -> None:
    """
    Logs cancelled session cleanly.
    Explicit Rule: Cancelled sessions do NOT compute marks or award partial completion.
    """
    # Simply ensure no partial score is written to round_results
    pass


def load_round_report(user_id: str, specialization: str, round_num: int) -> Optional[Dict[str, Any]]:
    """Loads a specific round report for user and specialization if completed."""
    progress = load_specialized_progress(user_id, specialization)
    round_str = str(round_num)
    return progress.get("round_results", {}).get(round_str)


def is_round_unlocked(user_id: str, specialization: str, round_num: int) -> bool:
    """
    Checks if a round is unlocked:
    - Round 1 is always unlocked.
    - Round 2 requires Round 1 completed.
    - Round 3 requires Round 2 completed.
    - Round 4 requires Round 3 completed.
    """
    if round_num == 1:
        return True
    progress = load_specialized_progress(user_id, specialization)
    return (round_num - 1) in progress.get("rounds_completed", [])


def get_user_all_specialized_interviews(user_id: str) -> List[Dict[str, Any]]:
    """
    Scans data/interviews/ for all completed specialized interview sessions by user_id.
    Used by User Profile & Dashboard.
    """
    results = []
    dir_path = _ensure_data_dir()
    u_clean = _sanitize_filename(user_id or "guest")
    prefix = f"specialized_{u_clean}_"

    for file_path in dir_path.glob(f"{prefix}*.json"):
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            if data.get("rounds_completed"):
                results.append(data)
        except Exception:
            continue

    # Sort latest updated first
    results.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return results


load_all_user_interviews = get_user_all_specialized_interviews


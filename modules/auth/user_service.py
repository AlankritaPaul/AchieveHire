"""
AscendCareer — Unique User Identity & Multi-User Isolation Service
Ensures unique User ID generation based on candidate name + unique number,
and strictly separates user resume information, interview attempts, progress, and reports.
"""

import json
import os
import random
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import streamlit as st


DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"

PURPOSE_OPTIONS = [
    "Resume Preparation",
    "Interview Preparation",
    "Both"
]


def _ensure_data_store() -> Dict[str, dict]:
    """Ensures data directory and users.json exist, returning all registered users."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        initial_data = {}
        USERS_FILE.write_text(json.dumps(initial_data, indent=2), encoding="utf-8")
        return initial_data
    try:
        content = USERS_FILE.read_text(encoding="utf-8").strip()
        if not content:
            return {}
        return json.loads(content)
    except Exception:
        return {}


def _save_all_users(users: Dict[str, dict]) -> None:
    """Thread-safe write of all users to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = USERS_FILE.with_suffix(".tmp")
    temp_file.write_text(json.dumps(users, indent=2, ensure_ascii=False), encoding="utf-8")
    temp_file.replace(USERS_FILE)


def generate_unique_user_id(name: str) -> str:
    """
    Generates a guaranteed unique User ID consisting of:
    1st 4 letters of user's name in uppercase + 4 random digits (e.g. 'XRYH3258').
    Ensures complete uniqueness even when multiple candidates share the exact same name.
    """
    users = _ensure_data_store()
    existing_ids = set(users.keys())

    # Extract clean alphabetical characters from the candidate's name
    clean_letters = re.sub(r"[^A-Za-z]", "", name).upper()
    if not clean_letters:
        clean_letters = "USER"
    
    # 1st 4 letters of user's name in capital (padded with 'X' if under 4 letters)
    prefix = (clean_letters + "XXXX")[:4]

    # Generate 4 random digits until guaranteed unique
    while True:
        num = random.randint(1000, 9999)
        candidate_id = f"{prefix}{num}"
        if candidate_id not in existing_ids:
            return candidate_id


def register_user(name: str, purpose: str) -> dict:
    """
    Registers a new candidate with their unique User ID, intended preparation goal,
    and initializes their isolated workspace.
    """
    users = _ensure_data_store()
    user_id = generate_unique_user_id(name)
    now_iso = datetime.now().isoformat()

    sanitized_name = name.strip() if name.strip() else "Candidate"
    clean_name_lower = re.sub(r"[^a-zA-Z0-9]", "", sanitized_name).lower() or "candidate"

    user_record = {
        "user_id": user_id,
        "name": sanitized_name,
        "purpose": purpose if purpose in PURPOSE_OPTIONS else "Both",
        "created_at": now_iso,
        "headline": "Candidate · " + (purpose if purpose in PURPOSE_OPTIONS else "Career Readiness"),
        "email": f"{clean_name_lower}@ascendcareer.ai",
        "location": "India",
        "bio": f"Registered for {purpose} on AscendCareer.",
        "profile_pic": None,
        "stats": {
            "resumes_created": 0,
            "resumes_analyzed": 0,
            "interviews_practiced": 0,
        },
        "resumes": [],
        "interview_attempts": [],
        "reports": [],
    }

    users[user_id] = user_record
    _save_all_users(users)

    # Attach to active session state
    set_active_user(user_record)
    return user_record


def ensure_founder_user_record(purpose: str = "Both") -> dict:
    """
    Ensures the Founder account (ALANKRITA-FOUNDER) exists in the persistent JSON registry 
    with a full candidate profile & workspace, allowing the founder to use and test 
    all candidate account features without restrictions.
    """
    users = _ensure_data_store()
    founder_id = "ALANKRITA-FOUNDER"

    if founder_id not in users:
        now_iso = datetime.now().isoformat()
        users[founder_id] = {
            "user_id": founder_id,
            "name": "Alankrita Pal",
            "purpose": purpose if purpose in PURPOSE_OPTIONS else "Both",
            "created_at": now_iso,
            "headline": "Platform Founder & Leader · Career Readiness",
            "email": "alankrita.pal@ascendcareer.ai",
            "location": "India",
            "bio": "Founder of AscendCareer. Dedicated to helping candidates achieve career excellence.",
            "profile_pic": None,
            "stats": {
                "resumes_created": 0,
                "resumes_analyzed": 0,
                "interviews_practiced": 0,
            },
            "resumes": [],
            "interview_attempts": [],
            "reports": [],
        }
        _save_all_users(users)
    else:
        if purpose in PURPOSE_OPTIONS:
            users[founder_id]["purpose"] = purpose
            _save_all_users(users)

    set_active_user(users[founder_id])
    return users[founder_id]


def get_user_by_id(user_id: str) -> Optional[dict]:
    """Retrieves a user record by their unique User ID."""
    users = _ensure_data_store()
    return users.get(user_id)


def update_user_record(user_id: str, updates: dict) -> Optional[dict]:
    """Updates specific fields of an existing user record in the persistent registry."""
    users = _ensure_data_store()
    if user_id not in users:
        return None
    users[user_id].update(updates)
    _save_all_users(users)
    if st.session_state.get("user_id") == user_id:
        st.session_state["user_data"] = users[user_id]
        if "name" in updates:
            st.session_state["username"] = updates["name"]
        if "profile_pic" in updates:
            st.session_state["user_profile_pic"] = updates["profile_pic"]
    return users[user_id]


def set_active_user(user_record: dict) -> None:
    """Sets the active user across the entire session state."""
    st.session_state["user_id"] = user_record["user_id"]
    st.session_state["username"] = user_record["name"]
    st.session_state["user_purpose"] = user_record.get("purpose", "Both")
    st.session_state["user_data"] = user_record
    st.session_state["is_signed_in"] = True
    st.session_state["user_email"] = user_record.get("email", "candidate@ascendcareer.ai")
    st.session_state["user_headline"] = user_record.get("headline", "Candidate")
    st.session_state["user_location"] = user_record.get("location", "India")
    st.session_state["user_bio"] = user_record.get("bio", "")
    st.session_state["user_profile_pic"] = user_record.get("profile_pic")


def get_current_user() -> Optional[dict]:
    """Returns the current active user record from session state or registry."""
    user_id = st.session_state.get("user_id")
    if not user_id:
        return None
    return get_user_by_id(user_id) or st.session_state.get("user_data")


def sign_out() -> None:
    """Clears the active user session."""
    st.session_state["user_id"] = None
    st.session_state["username"] = "Candidate"
    st.session_state["user_purpose"] = None
    st.session_state["user_data"] = None
    st.session_state["is_signed_in"] = False
    st.session_state["user_profile_pic"] = None
    st.session_state["ac_screen"] = "landing"


def delete_user_account(user_id: str) -> bool:
    """Permanently deletes the user record from the persistent registry and resets session."""
    users = _ensure_data_store()
    if user_id in users:
        del users[user_id]
        _save_all_users(users)
    sign_out()
    return True

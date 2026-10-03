"""
AchieveHire — Specialized Interview Data Models & Constants
Defines round configurations, language mappings, interviewer profiles,
scoring schemas, evaluation categories, and progression data structures.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import datetime


# ─────────────────────────────────────────────────────────────────────────────
# Core Round Configurations
# ─────────────────────────────────────────────────────────────────────────────

ROUNDS_CONFIG: Dict[int, Dict[str, Any]] = {
    1: {
        "round_num": 1,
        "name": "Round 1 — Easy",
        "difficulty": "Easy",
        "duration_minutes": 20,
        "duration_seconds": 20 * 60,
        "badge_icon": "🟢",
        "color": "#10B981",
        "description": "Evaluates fundamental understanding, basic concepts, core terminology, and candidate self-introduction.",
        "target_questions_count": 5,
    },
    2: {
        "round_num": 2,
        "name": "Round 2 — Moderate",
        "difficulty": "Moderate",
        "duration_minutes": 30,
        "duration_seconds": 30 * 60,
        "badge_icon": "🟡",
        "color": "#F59E0B",
        "description": "Evaluates deeper technical understanding, practical implementation, language mechanics, and application scenarios.",
        "target_questions_count": 6,
    },
    3: {
        "round_num": 3,
        "name": "Round 3 — Hard",
        "difficulty": "Hard",
        "duration_minutes": 35,
        "duration_seconds": 35 * 60,
        "badge_icon": "🟠",
        "color": "#EA580C",
        "description": "Evaluates advanced concepts, architectural trade-offs, edge-case handling, system optimization, and debugging reasoning.",
        "target_questions_count": 7,
    },
    4: {
        "round_num": 4,
        "name": "Round 4 — Final Round",
        "difficulty": "Final",
        "duration_minutes": 40,
        "duration_seconds": 40 * 60,
        "badge_icon": "🏆",
        "color": "#8B5CF6",
        "description": "Comprehensive evaluation, introduction evolution assessment, complex scenarios, and candidate-led closing questions.",
        "target_questions_count": 8,
    },
}

LANGUAGE_OPTIONS: List[str] = ["English", "Hindi", "Hinglish"]

INTERVIEWER_OPTIONS: Dict[str, Dict[str, str]] = {
    "male": {
        "id": "male",
        "label": "Male Interviewer (Rohan / David)",
        "voice_gender": "male",
        "name": "David",
        "role": "Lead Technical Evaluator",
        "avatar_icon": "👨‍💼",
    },
    "female": {
        "id": "female",
        "label": "Female Interviewer (Priya / Sarah)",
        "voice_gender": "female",
        "name": "Sarah",
        "role": "Lead Technical Evaluator",
        "avatar_icon": "👩‍💼",
    },
}

PRESET_SPECIALIZATIONS: List[str] = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "TypeScript",
    "Go (Golang)",
    "Rust",
    "React & Frontend Architecture",
    "Node.js & Backend Systems",
    "SQL & Database Engineering",
    "Data Science & Machine Learning",
    "DevOps, Docker & Kubernetes",
    "Cloud Architecture (AWS/GCP/Azure)",
    "System Design & Distributed Systems",
    "Cybersecurity & Application Defense",
    "Android Development (Kotlin)",
    "iOS Development (Swift)",
]

# Classification labels for detailed report diagnostics
ANSWER_CLASSIFICATIONS: List[str] = [
    "Correct",
    "Partially Correct",
    "Correct but Incomplete",
    "Incorrect",
    "Irrelevant",
    "Excessively Long",
    "Unclear",
    "Unanswered / Passed",
]

CLASSIFICATION_BADGES: Dict[str, Dict[str, str]] = {
    "Correct": {"color": "#10B981", "bg": "#ECFDF5", "icon": "✅", "label": "Correct"},
    "Partially Correct": {"color": "#F59E0B", "bg": "#FFFBEB", "icon": "⚠️", "label": "Partially Correct"},
    "Correct but Incomplete": {"color": "#3B82F6", "bg": "#EFF6FF", "icon": "ℹ️", "label": "Correct but Incomplete"},
    "Incorrect": {"color": "#EF4444", "bg": "#FEF2F2", "icon": "❌", "label": "Incorrect Technical Answer"},
    "Irrelevant": {"color": "#8B5CF6", "bg": "#F5F3FF", "icon": "🔄", "label": "Irrelevant / Off-Topic"},
    "Excessively Long": {"color": "#F97316", "bg": "#FFF7ED", "icon": "⏳", "label": "Excessively Long / Unfocused"},
    "Unclear": {"color": "#6B7280", "bg": "#F3F4F6", "icon": "❓", "label": "Unclear Phrasing"},
    "Unanswered / Passed": {"color": "#9CA3AF", "bg": "#F9FAFB", "icon": "🚫", "label": "Unanswered / Passed"},
}


# ─────────────────────────────────────────────────────────────────────────────
# Dataclasses & Data Types
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class QuestionItem:
    id: str
    text_en: str
    text_hi: str
    text_hinglish: str
    difficulty: str  # "Easy", "Moderate", "Hard", "Final"
    specialization: str
    category: str
    expected_points: List[str]
    correct_answer: str
    better_possible_answer: str
    is_intro: bool = False
    is_closing: bool = False
    is_followup: bool = False
    parent_question_id: Optional[str] = None

    def get_text(self, language: str) -> str:
        lang_lower = language.lower()
        if "hinglish" in lang_lower:
            return self.text_hinglish or self.text_en
        elif "hindi" in lang_lower:
            return self.text_hi or self.text_hinglish or self.text_en
        return self.text_en


@dataclass
class QuestionEvaluation:
    question_id: str
    question_text: str
    user_answer: str
    classification: str
    score: float  # 0.0 to 10.0
    what_was_good: str
    what_was_missing: str
    correct_explanation: str
    better_possible_answer: str
    criteria_scores: Dict[str, float] = field(default_factory=dict)
    # criteria_scores: {
    #   "technical_correctness": 8.0,
    #   "relevance": 9.0,
    #   "clarity": 8.5,
    #   "completeness": 7.0,
    #   "conciseness": 8.0,
    #   "depth": 7.5
    # }
    is_intro: bool = False
    is_closing: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_id": self.question_id,
            "question_text": self.question_text,
            "user_answer": self.user_answer,
            "classification": self.classification,
            "score": round(self.score, 1),
            "what_was_good": self.what_was_good,
            "what_was_missing": self.what_was_missing,
            "correct_explanation": self.correct_explanation,
            "better_possible_answer": self.better_possible_answer,
            "criteria_scores": self.criteria_scores,
            "is_intro": self.is_intro,
            "is_closing": self.is_closing,
        }


@dataclass
class RoundResult:
    round_num: int
    round_name: str
    difficulty: str
    specialization: str
    language: str
    interviewer_gender: str
    time_allowed_sec: int
    time_taken_sec: int
    completed_at: str
    status: str  # "completed" or "cancelled"
    overall_score: float  # 0 to 100%
    criteria_breakdown: Dict[str, float]
    evaluations: List[Dict[str, Any]]
    summary_strengths: List[str]
    summary_improvements: List[str]
    what_you_did_well: List[str]
    what_needs_improvement: List[str]
    how_to_improve: List[str]
    what_to_practise_before_next: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "round_num": self.round_num,
            "round_name": self.round_name,
            "difficulty": self.difficulty,
            "specialization": self.specialization,
            "language": self.language,
            "interviewer_gender": self.interviewer_gender,
            "time_allowed_sec": self.time_allowed_sec,
            "time_taken_sec": self.time_taken_sec,
            "completed_at": self.completed_at,
            "status": self.status,
            "overall_score": round(self.overall_score, 1),
            "criteria_breakdown": self.criteria_breakdown,
            "evaluations": self.evaluations,
            "summary_strengths": self.summary_strengths,
            "summary_improvements": self.summary_improvements,
            "what_you_did_well": self.what_you_did_well,
            "what_needs_improvement": self.what_needs_improvement,
            "how_to_improve": self.how_to_improve,
            "what_to_practise_before_next": self.what_to_practise_before_next,
        }

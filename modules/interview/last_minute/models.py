"""
AchieveHire — Last-Minute Preparation Models & Configurations
Specification:
- Duration: Fixed 30 minutes (1800 seconds)
- Unlimited attempts
- Two modes: Last-Minute Specialized Preparation & Last-Minute Job Related Preparation
- Progression within 30 min: Introduction ('Please introduce yourself.') → Easy → Moderate → Hard
- Panel: Multi-interviewer professional panel asking alternately
- Criteria: 9 comprehensive evaluation criteria
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

MODE_SPECIALIZED = "Last-Minute Prep for Specialized"
MODE_JOB_RELATED = "Last-Minute Prep for Job Related"

# Exactly 3 languages permitted for both modes
INTERVIEW_LANGUAGES = ["English", "Hindi", "Hinglish"]

LAST_MINUTE_DURATION_MINUTES = 30
LAST_MINUTE_DURATION_SECONDS = 30 * 60

POPULAR_SPECIALIZATIONS = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "TypeScript",
    "Go (Golang)",
    "Rust",
    "C# / .NET",
    "SQL & Database Engineering",
    "React & Frontend Engineering",
    "Node.js & Backend Architecture",
    "Machine Learning & PyTorch",
    "Cloud Architecture & AWS",
    "Kubernetes & DevOps",
]

EVALUATION_CRITERIA = [
    "Technical/Professional Knowledge",
    "Relevance",
    "Communication",
    "Clarity",
    "Completeness",
    "Depth",
    "Conciseness",
    "Follow-up Handling",
    "Interview Behaviour",
]

ANSWER_CLASSIFICATIONS = [
    "Correct",
    "Partially Correct",
    "Correct but Incomplete",
    "Incorrect",
    "Unanswered",
    "Unclear",
    "Excessively Long",
]


@dataclass
class LastMinutePanelMember:
    id: str
    name: str
    title: str
    department: str
    avatar_emoji: str
    focus_area: str
    voice_gender: str = "Female"


@dataclass
class LastMinuteQuestionRecord:
    question_id: str
    interviewer_id: str
    interviewer_name: str
    interviewer_title: str
    question_text: str
    difficulty: str  # Intro, Easy, Moderate, Hard
    user_answer: str = ""
    classification: str = "Unanswered"
    scores: Dict[str, int] = field(default_factory=dict)
    feedback: str = ""
    better_possible_answer: str = ""
    correct_explanation: str = ""
    reaction: str = ""


@dataclass
class LastMinuteAttemptRecord:
    attempt_id: str
    user_id: str
    mode: str  # MODE_SPECIALIZED or MODE_JOB_RELATED
    topic_title: str  # e.g. "Python" or "Software Engineer at Google"
    configuration: Dict[str, Any]
    duration_allowed_sec: int
    actual_time_taken_sec: int
    completion_date: str
    overall_score: int
    criteria_scores: Dict[str, int]
    questions: List[Dict[str, Any]]
    what_went_well: List[str]
    what_needs_improvement: List[str]
    how_to_improve: List[str]
    what_to_practise_next: List[str]
    executive_summary: str
    short_detail: str = ""

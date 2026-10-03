"""
AchieveHire — Job Related Interview Models & Configuration
Specification:
- Exactly 6 rounds:
  Round 1: Easy, 20 min, 1 interviewer (Question 1 strictly: 'Please introduce yourself.')
  Round 2: Moderate, 25 min, 2 interviewers
  Round 3: Moderate, 30 min, 2 interviewers
  Round 4: Hard, 35 min, 3 interviewers
  Round 5: Hard, 40 min, 3 interviewers
  Round 6: Final, 45 min, 4-5 interviewers (includes closing 'Do you have any questions for us?')
- Languages: STRICTLY English, Hindi, Hinglish (NO manual language entry).
- Job Role: Suggested list + 'Write Your Job Role' (manual entry).
- Company: Suggested list + 'Write Your Company' (manual entry).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

SUGGESTED_JOB_ROLES = [
    "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI / Prompt Engineer",
    "DevOps Engineer",
    "Cloud Solutions Architect",
    "Cybersecurity Analyst",
    "Data Analyst",
    "Database Administrator",
    "Product Manager",
    "Associate Product Manager",
    "UI / UX Designer",
    "QA / Automation Test Engineer",
    "Systems Engineer",
    "Network Engineer",
    "Business Analyst",
    "Engineering Manager",
    "Site Reliability Engineer (SRE)",
    "Mobile Application Developer (iOS/Android)",
    "Embedded Systems Engineer",
]

SUGGESTED_COMPANIES = [
    "Google",
    "Microsoft",
    "Amazon",
    "Apple",
    "Meta",
    "Netflix",
    "Adobe",
    "Salesforce",
    "Uber",
    "Swiggy",
    "Zomato",
    "Flipkart",
    "Paytm",
    "Razorpay",
    "TCS",
    "Infosys",
    "Wipro",
    "Accenture",
    "Cognizant",
    "IBM",
    "Oracle",
    "Cisco",
    "Goldman Sachs",
    "Morgan Stanley",
    "JPMorgan Chase",
    "Stripe",
    "Palantir",
    "Databricks",
    "Atlassian",
    "Spotify",
]

# Strict 3 language choices - user is NOT allowed to manually write any other language
INTERVIEW_LANGUAGES = ["English", "Hindi", "Hinglish"]

JOB_ROUNDS_CONFIG: Dict[int, Dict[str, Any]] = {
    1: {
        "round_num": 1,
        "name": "Round 1 — Easy",
        "difficulty": "Easy",
        "duration_minutes": 20,
        "duration_seconds": 20 * 60,
        "interviewer_count": 1,
        "interviewer_seniority": "Initial / Early Interviewer",
        "first_question": "Please introduce yourself.",
        "description": "Foundational interview covering personal background, introductory role knowledge, and initial resume review.",
        "questions_count": 5,
    },
    2: {
        "round_num": 2,
        "name": "Round 2 — Moderate",
        "difficulty": "Moderate",
        "duration_minutes": 25,
        "duration_seconds": 25 * 60,
        "interviewer_count": 2,
        "interviewer_seniority": "Mid-Level Professional Interviewers",
        "first_question": None,
        "description": "Role-specific competencies, technical workflows, execution rigor, and core tooling expertise.",
        "questions_count": 6,
    },
    3: {
        "round_num": 3,
        "name": "Round 3 — Moderate",
        "difficulty": "Moderate",
        "duration_minutes": 30,
        "duration_seconds": 30 * 60,
        "interviewer_count": 2,
        "interviewer_seniority": "Experienced Domain Specialists",
        "first_question": None,
        "description": "Deep resume dissection, project contributions, technical decisions, and past problem-solving scenarios.",
        "questions_count": 6,
    },
    4: {
        "round_num": 4,
        "name": "Round 4 — Hard",
        "difficulty": "Hard",
        "duration_minutes": 35,
        "duration_seconds": 35 * 60,
        "interviewer_count": 3,
        "interviewer_seniority": "Senior Staff Leads & Architects",
        "first_question": None,
        "description": "High-stakes problem solving, architecture design, trade-offs under constraints, and practical reasoning.",
        "questions_count": 7,
    },
    5: {
        "round_num": 5,
        "name": "Round 5 — Hard",
        "difficulty": "Hard",
        "duration_minutes": 40,
        "duration_seconds": 40 * 60,
        "interviewer_count": 3,
        "interviewer_seniority": "Senior Managers & Functional Leaders",
        "first_question": None,
        "description": "Rigorous cross-functional challenges, edge-case troubleshooting, company alignment, and operational leadership.",
        "questions_count": 7,
    },
    6: {
        "round_num": 6,
        "name": "Round 6 — Final",
        "difficulty": "Final",
        "duration_minutes": 45,
        "duration_seconds": 45 * 60,
        "interviewer_count": 4,
        "interviewer_seniority": "Full Executive Interview Panel (VP / Director / Tech Fellows)",
        "first_question": None,
        "description": "Comprehensive multi-dimensional evaluation across technical vision, business impact, culture fit, and closing Q&A.",
        "questions_count": 8,
    },
}

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
    "Irrelevant",
    "Excessively Long",
    "Unclear",
    "Unanswered",
]


@dataclass
class PanelMember:
    id: str
    name: str
    title: str
    department: str
    avatar_emoji: str
    focus_area: str
    voice_name: str = "en-US-Standard-C"
    voice_gender: str = "Female"


@dataclass
class JobQuestionRecord:
    question_id: str
    interviewer_id: str
    interviewer_name: str
    interviewer_title: str
    question_text: str
    user_answer: str = ""
    classification: str = "Unanswered"
    scores: Dict[str, int] = field(default_factory=dict)
    feedback: str = ""
    better_possible_answer: str = ""
    correct_explanation: str = ""
    reaction: str = ""
    is_clarification: bool = False
    is_follow_up: bool = False
    time_taken_sec: int = 0


@dataclass
class JobRoundEvaluation:
    round_num: int
    difficulty: str
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


@dataclass
class JobInterviewSession:
    user_id: str
    target_role: str
    target_company: str
    language: str  # Strictly "English", "Hindi", or "Hinglish"
    resume_snapshot: Dict[str, Any]
    active_round: int = 1
    completed_rounds: List[int] = field(default_factory=list)
    round_evaluations: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    is_overall_completed: bool = False
    created_at: str = ""
    updated_at: str = ""


@dataclass
class JobInterviewRoundState:
    round_num: int
    is_active: bool = False
    is_completed: bool = False
    start_timestamp: float = 0.0
    elapsed_seconds: int = 0
    active_question_index: int = 0
    questions_list: List[JobQuestionRecord] = field(default_factory=list)
    panel_members: List[PanelMember] = field(default_factory=list)
    active_interviewer_index: int = 0
    candidate_asked_closing_question: bool = False
    closing_candidate_question: str = ""
    closing_panel_response: str = ""

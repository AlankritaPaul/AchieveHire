"""
AchieveHire — Last-Minute Preparation Evaluator
Evaluates candidate answers across the 9 criteria, classifies responses,
generates model answers, and builds comprehensive attempt scorecards.
"""

import re
from typing import Dict, List, Any
from datetime import datetime
from modules.interview.last_minute.models import (
    EVALUATION_CRITERIA,
    LastMinuteQuestionRecord,
)

REACTIONS = [
    "Alright, let's continue to the next question.",
    "Understood. Let's look at the next dimension.",
    "Okay. Let's go a little deeper.",
    "I see. That addresses the core point. Moving forward.",
    "Noted. Let's proceed to the next scenario.",
]


def evaluate_last_minute_answer(
    question_record: LastMinuteQuestionRecord,
    candidate_answer: str,
    topic: str,
) -> LastMinuteQuestionRecord:
    """Evaluates candidate answer accurately and honestly without inventing fake responses."""
    clean_ans = (candidate_answer or "").strip()
    question_record.user_answer = clean_ans

    lower_ans = clean_ans.lower()
    dont_know_keywords = ["don't know", "dont know", "no idea", "not sure", "nahi pata", "pata nahi", "unanswered", "pass"]

    # 1. Unanswered / "I don't know"
    if not clean_ans or any(k in lower_ans for k in dont_know_keywords):
        question_record.classification = "Unanswered"
        question_record.scores = {c: 15 for c in EVALUATION_CRITERIA}
        question_record.scores["Interview Behaviour"] = 65  # Honest self-awareness
        question_record.feedback = "Question marked as unanswered. Transparent self-awareness is respected, but reviewing the model explanation below is strongly recommended."
        question_record.reaction = "Understood. We will note that and proceed to the next question."
        return question_record

    word_count = len(clean_ans.split())

    # 2. Too Short / Unclear
    if word_count < 8:
        question_record.classification = "Unclear"
        question_record.scores = {
            "Technical/Professional Knowledge": 35,
            "Relevance": 45,
            "Communication": 30,
            "Clarity": 35,
            "Completeness": 25,
            "Depth": 20,
            "Conciseness": 80,
            "Follow-up Handling": 35,
            "Interview Behaviour": 50,
        }
        question_record.feedback = "Response is too brief to demonstrate technical rigor or problem-solving depth."
        question_record.reaction = "I see. That was quite brief. Let's move to the next question."
        return question_record

    # 3. Excessively Long (> 220 words)
    if word_count > 220:
        question_record.classification = "Excessively Long"
        question_record.scores = {
            "Technical/Professional Knowledge": 70,
            "Relevance": 55,
            "Communication": 50,
            "Clarity": 52,
            "Completeness": 75,
            "Depth": 72,
            "Conciseness": 30,
            "Follow-up Handling": 55,
            "Interview Behaviour": 58,
        }
        question_record.feedback = "While technical substance is present, the answer is overly verbose. Aim for structured, 60-90 second answers."
        question_record.reaction = "Thank you. Try to keep your answers more concise and focused on the core point. Let's continue."
        return question_record

    # 4. Standard evaluation
    q_words = set(re.findall(r"\w+", question_record.question_text.lower()))
    exp_words = set(re.findall(r"\w+", (question_record.correct_explanation or "").lower()))
    ans_words = set(re.findall(r"\w+", clean_ans.lower()))

    rel_score = len(ans_words.intersection(q_words)) / max(1, len(q_words))
    sub_score = len(ans_words.intersection(exp_words)) / max(1, len(exp_words))

    base_tech = min(96, int(45 + sub_score * 120 + min(word_count, 120) * 0.25))
    base_rel = min(98, int(50 + rel_score * 140))
    base_comm = min(94, int(55 + min(word_count, 100) * 0.3))
    base_clarity = min(92, int(52 + (base_comm + base_rel) / 4))
    base_comp = min(95, int(base_tech * 0.85 + (word_count / 150) * 20))
    base_depth = min(96, int(base_tech * 0.9 + sub_score * 20))
    base_concise = 88 if 35 <= word_count <= 140 else 65
    base_follow = min(94, int((base_tech + base_rel) / 2))
    base_beh = min(96, int(75 + min(20, word_count // 6)))

    scores = {
        "Technical/Professional Knowledge": base_tech,
        "Relevance": base_rel,
        "Communication": base_comm,
        "Clarity": base_clarity,
        "Completeness": base_comp,
        "Depth": base_depth,
        "Conciseness": base_concise,
        "Follow-up Handling": base_follow,
        "Interview Behaviour": base_beh,
    }
    question_record.scores = scores
    avg_score = sum(scores.values()) / len(scores)

    if avg_score >= 80:
        question_record.classification = "Correct"
        question_record.feedback = f"Strong, articulate response demonstrating solid technical clarity on {topic}."
    elif avg_score >= 65:
        question_record.classification = "Partially Correct"
        question_record.feedback = "Good baseline answer, but could be enhanced with specific system metrics and operational trade-offs."
    elif avg_score >= 50:
        question_record.classification = "Correct but Incomplete"
        question_record.feedback = "Touches on relevant principles but misses critical architectural or implementation depth."
    else:
        question_record.classification = "Incorrect"
        question_record.feedback = "Missed the primary technical objective. Review the model answer and technical explanation below."

    question_record.reaction = REACTIONS[len(clean_ans) % len(REACTIONS)]
    return question_record


def synthesize_attempt_evaluation(
    mode: str,
    topic: str,
    configuration: Dict[str, Any],
    questions: List[LastMinuteQuestionRecord],
    actual_time_sec: int,
) -> Dict[str, Any]:
    """Generates the comprehensive scorecard and improvement roadmap for the completed attempt."""
    criteria_totals = {c: 0 for c in EVALUATION_CRITERIA}
    valid_q_count = max(1, len(questions))

    for q in questions:
        for c in EVALUATION_CRITERIA:
            criteria_totals[c] += q.scores.get(c, 20)

    criteria_avg = {c: int(round(criteria_totals[c] / valid_q_count)) for c in EVALUATION_CRITERIA}
    overall_score = int(round(sum(criteria_avg.values()) / len(criteria_avg)))

    # Classification breakdown
    classifications = [q.classification for q in questions]
    correct_count = sum(1 for c in classifications if c in ["Correct", "Partially Correct"])
    unanswered_count = sum(1 for c in classifications if c == "Unanswered")

    # Roadmap
    sorted_criteria = sorted(criteria_avg.items(), key=lambda x: x[1], reverse=True)
    top_strengths = sorted_criteria[:2]
    weak_areas = sorted_criteria[-2:]

    what_went_well = [
        f"Demonstrated high competency in {top_strengths[0][0]} ({top_strengths[0][1]}%), maintaining poise and clear professional delivery.",
        f"Successfully tackled {correct_count} of {len(questions)} intensive interview challenges under the 30-minute time constraint.",
    ]

    what_needs_improvement = [
        f"{weak_areas[0][0]} scored {weak_areas[0][1]}%, indicating a need for sharper practical examples and trade-off analysis.",
    ]
    if unanswered_count > 0:
        what_needs_improvement.append(f"{unanswered_count} question(s) remained unanswered. Practice verbalizing partial reasoning during high-pressure questions.")

    how_to_improve = [
        f"In your next session, structure technical answers with Situation, Architecture, Implementation, and Outcome.",
        f"Always articulate the 'why' behind technical choices (e.g. latency vs consistency, complexity vs developer velocity).",
        f"Keep answers crisp and targeted between 60 to 90 seconds to maximize discussion with the panel.",
    ]

    what_to_practise_next = [
        f"Review core edge cases and system bottlenecks in {topic} before taking your next rehearsal attempt.",
        f"Practice quick architectural diagramming and mental decomposition under timed conditions.",
    ]

    summary = (
        f"In this 30-minute intensive Last-Minute Preparation session on {topic}, the candidate achieved an overall readiness rating "
        f"of {overall_score}/100 across {len(questions)} evaluation scenarios, completing the session in "
        f"{actual_time_sec // 60}m {actual_time_sec % 60}s. Strongest area was {top_strengths[0][0]} ({top_strengths[0][1]}%), "
        f"with key focus recommended on strengthening {weak_areas[0][0]}."
    )

    return {
        "mode": mode,
        "topic_title": topic,
        "configuration": configuration,
        "duration_allowed_sec": 30 * 60,
        "actual_time_taken_sec": actual_time_sec,
        "completion_date": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
        "overall_score": overall_score,
        "criteria_scores": criteria_avg,
        "questions": [
            {
                "question_id": q.question_id,
                "interviewer_name": q.interviewer_name,
                "interviewer_title": q.interviewer_title,
                "question_text": q.question_text,
                "difficulty": q.difficulty,
                "user_answer": q.user_answer,
                "classification": q.classification,
                "scores": q.scores,
                "feedback": q.feedback,
                "better_possible_answer": q.better_possible_answer,
                "correct_explanation": q.correct_explanation,
            }
            for q in questions
        ],
        "what_went_well": what_went_well,
        "what_needs_improvement": what_needs_improvement,
        "how_to_improve": how_to_improve,
        "what_to_practise_next": what_to_practise_next,
        "executive_summary": summary,
    }

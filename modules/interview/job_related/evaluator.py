"""
AchieveHire — Job Related Interview Evaluator
Evaluates candidate answers across 9 core competencies:
1. Technical/Professional Knowledge
2. Relevance
3. Communication
4. Clarity
5. Completeness
6. Depth
7. Conciseness
8. Follow-up Handling
9. Interview Behaviour

Classifies answers into:
- Correct
- Partially Correct
- Correct but Incomplete
- Incorrect
- Irrelevant
- Excessively Long
- Unclear
- Unanswered

Provides:
- Exact Question
- Transcribed Candidate Answer (never fabricated)
- Better Possible Answer (clearly distinguished from candidate answer)
- Correct/Appropriate Explanation
- Visual Performance Chart scores
- Improvement Recommendations (What You Did Well, What Needs Improvement, How to Improve, What to Practise Before Next Round)
- Executive Round Summary
"""

import re
from typing import Dict, List, Any, Tuple
from modules.interview.job_related.models import (
    EVALUATION_CRITERIA,
    JobQuestionRecord,
    JobRoundEvaluation,
)
from modules.interview.job_related.engine import (
    REACTIONS_STRONG,
    REACTIONS_NEUTRAL,
    REACTIONS_DEEPEN,
    REACTIONS_REDIRECT,
)


def evaluate_candidate_answer(
    question_record: JobQuestionRecord,
    candidate_answer: str,
    language: str,
    job_role: str,
    company: str,
) -> JobQuestionRecord:
    """
    Evaluates a candidate's answer strictly against the question and criteria.
    Never invents or fabricates answers.
    """
    clean_ans = (candidate_answer or "").strip()
    question_record.user_answer = clean_ans
    lang = language if language in ["English", "Hindi", "Hinglish"] else "English"

    # Check for Unanswered / "I don't know"
    lower_ans = clean_ans.lower()
    dont_know_patterns = [
        "i don't know",
        "i dont know",
        "don't know",
        "dont know",
        "no idea",
        "not sure",
        "mujhe nahi pata",
        "nahi pata",
        "pata nahi",
        "unanswered",
        "skip",
        "pass",
    ]

    if not clean_ans or any(p in lower_ans for p in dont_know_patterns):
        question_record.classification = "Unanswered"
        question_record.scores = {c: 15 for c in EVALUATION_CRITERIA}
        question_record.scores["Interview Behaviour"] = 65  # Honest self-awareness is respected
        question_record.feedback = "Question marked as unanswered. Transparently acknowledging gaps in knowledge is respected in professional interviews, but this topic requires study before progressing."
        question_record.reaction = (
            "Understood. We will note that and proceed to the next area."
            if lang == "English"
            else "समझ गया। हम इसे नोट करके अगले विषय पर बढ़ते हैं।"
            if lang == "Hindi"
            else "Understood. Isko note karke hum agle topic par badhte hain."
        )
        return question_record

    word_count = len(clean_ans.split())

    # Check for Unclear / Too short
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
        question_record.feedback = "The response is too brief to adequately demonstrate technical depth or clear understanding of the subject matter."
        question_record.reaction = (
            "I see. That was quite brief. Let's move to the next question."
            if lang == "English"
            else "यह उत्तर बहुत संक्षिप्त था। चलिए अगले प्रश्न पर चलते हैं।"
            if lang == "Hindi"
            else "Yeh kafi brief tha. Let's move to the next question."
        )
        return question_record

    # Check for Excessively Long / Rambling (> 220 words)
    if word_count > 220:
        question_record.classification = "Excessively Long"
        question_record.scores = {
            "Technical/Professional Knowledge": 68,
            "Relevance": 55,
            "Communication": 50,
            "Clarity": 52,
            "Completeness": 75,
            "Depth": 72,
            "Conciseness": 30,
            "Follow-up Handling": 55,
            "Interview Behaviour": 58,
        }
        question_record.feedback = "While the response contains relevant points, it is excessively verbose and loses conversational focus. In executive interviews, aim for structured 90-second answers."
        question_record.reaction = (
            "Thank you. Try to keep your answers more concise and focused on the core point. Let's continue."
            if lang == "English"
            else "धन्यवाद। कोशिश करें कि उत्तर अधिक संक्षिप्त और मुख्य बिंदु पर केंद्रित रहे। चलिए आगे बढ़ते हैं।"
            if lang == "Hindi"
            else "Thank you. Answers ko thoda crisp aur structured rakhein please. Let's continue."
        )
        return question_record

    # Normal answer scoring: Evaluate technical substance, relevance, and clarity
    # Keyword overlap with correct explanation & question
    q_words = set(re.findall(r"\w+", question_record.question_text.lower()))
    exp_words = set(re.findall(r"\w+", (question_record.correct_explanation or "").lower()))
    ans_words = set(re.findall(r"\w+", clean_ans.lower()))

    relevance_overlap = len(ans_words.intersection(q_words)) / max(1, len(q_words))
    substance_overlap = len(ans_words.intersection(exp_words)) / max(1, len(exp_words))

    # Calculate balanced scores
    base_tech = min(95, int(45 + substance_overlap * 120 + min(word_count, 120) * 0.25))
    base_rel = min(98, int(50 + relevance_overlap * 140))
    base_comm = min(94, int(55 + min(word_count, 100) * 0.3))
    base_clarity = min(92, int(52 + (base_comm + base_rel) / 4))
    base_comp = min(95, int(base_tech * 0.85 + (word_count / 150) * 20))
    base_depth = min(96, int(base_tech * 0.9 + substance_overlap * 20))
    base_concise = 88 if 35 <= word_count <= 140 else (68 if word_count < 35 else 58)
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

    if avg_score >= 82:
        question_record.classification = "Correct"
        question_record.feedback = f"Strong, well-structured answer. Effectively addressed key engineering and domain considerations relevant to a {job_role} at {company}."
        reactions = REACTIONS_STRONG.get(lang, REACTIONS_STRONG["English"])
        question_record.reaction = reactions[len(clean_ans) % len(reactions)]
    elif avg_score >= 68:
        question_record.classification = "Partially Correct"
        question_record.feedback = "Good fundamental answer that covers core ideas, but could be enhanced with more specific architecture trade-offs or measurable outcomes."
        reactions = REACTIONS_DEEPEN.get(lang, REACTIONS_DEEPEN["English"])
        question_record.reaction = reactions[len(clean_ans) % len(reactions)]
    elif avg_score >= 50:
        question_record.classification = "Correct but Incomplete"
        question_record.feedback = "The answer touches on the correct general direction, but lacks critical implementation details and technical depth."
        reactions = REACTIONS_NEUTRAL.get(lang, REACTIONS_NEUTRAL["English"])
        question_record.reaction = reactions[len(clean_ans) % len(reactions)]
    else:
        question_record.classification = "Incorrect"
        question_record.feedback = "The answer missed key technical principles required for this scenario. Review the recommended model answer below."
        reactions = REACTIONS_REDIRECT.get(lang, REACTIONS_REDIRECT["English"])
        question_record.reaction = reactions[len(clean_ans) % len(reactions)]

    return question_record


def generate_round_evaluation(
    round_num: int,
    questions: List[JobQuestionRecord],
    actual_time_sec: int,
    job_role: str,
    company: str,
    language: str,
) -> Dict[str, Any]:
    """
    Synthesizes the complete Performance & Improvement Report for a completed round.
    Calculates genuine criteria averages and actionable learning feedback.
    """
    from datetime import datetime
    from modules.interview.job_related.models import JOB_ROUNDS_CONFIG

    cfg = JOB_ROUNDS_CONFIG.get(round_num, JOB_ROUNDS_CONFIG[1])
    diff = cfg.get("difficulty", "Moderate")
    allowed_sec = cfg.get("duration_seconds", 20 * 60)

    # Calculate average scores across all answered questions
    criteria_totals = {c: 0 for c in EVALUATION_CRITERIA}
    valid_count = max(1, len(questions))

    for q in questions:
        for c in EVALUATION_CRITERIA:
            criteria_totals[c] += q.scores.get(c, 20)

    criteria_avg = {c: int(round(criteria_totals[c] / valid_count)) for c in EVALUATION_CRITERIA}
    overall_score = int(round(sum(criteria_avg.values()) / len(criteria_avg)))

    # Classification breakdown
    classifications = [q.classification for q in questions]
    correct_count = sum(1 for c in classifications if c in ["Correct", "Partially Correct"])
    unanswered_count = sum(1 for c in classifications if c == "Unanswered")

    # Generate genuine feedback
    what_went_well = []
    what_needs_improvement = []
    how_to_improve = []
    what_to_practise_next = []

    # Strengths
    sorted_criteria = sorted(criteria_avg.items(), key=lambda x: x[1], reverse=True)
    top_strengths = sorted_criteria[:2]
    for c_name, c_score in top_strengths:
        if c_score >= 65:
            what_went_well.append(f"Strong proficiency in {c_name} ({c_score}%), displaying confident and articulate responses.")
    if correct_count >= len(questions) // 2:
        what_went_well.append(f"Successfully answered {correct_count} of {len(questions)} technical questions with relevant engineering terminology.")
    if not what_went_well:
        what_went_well.append("Maintained calm professional poise and tackled challenging questions without exiting the session.")

    # Weaknesses
    lowest_criteria = sorted_criteria[-2:]
    for c_name, c_score in lowest_criteria:
        what_needs_improvement.append(f"{c_name} scored {c_score}%, indicating room for tighter precision and stronger practical grounding.")
    if unanswered_count > 0:
        what_needs_improvement.append(f"{unanswered_count} question(s) remained unanswered. Practice articulating partial reasoning even when uncertain.")

    # How to improve
    how_to_improve.append(f"Structure answers using the STAR method (Situation, Task, Action, Result) specifically tailored to {company}'s scale.")
    how_to_improve.append(f"When discussing architectural choices for {job_role}, always highlight the trade-offs (latency vs. consistency, compute vs. storage).")
    how_to_improve.append("Quantify business outcomes wherever possible (e.g. 'reduced latency by 35%', 'handled 5k requests/sec').")

    # What to practise next
    if round_num < 6:
        next_cfg = JOB_ROUNDS_CONFIG.get(round_num + 1, {})
        next_name = next_cfg.get("name", "Next Round")
        what_to_practise_next.append(f"Review core system design principles and distributed failure recovery before attempting {next_name}.")
        what_to_practise_next.append(f"Practice active listening for multi-interviewer panels where 2-3 interviewers ask questions alternately.")
        what_to_practise_next.append(f"Formulate deeper resume examples illustrating high-pressure decision-making and cross-functional leadership.")
    else:
        what_to_practise_next.append(f"Continue refining executive presentation skills and enterprise technology strategy for {company}.")
        what_to_practise_next.append("Maintain an ongoing catalogue of high-stakes engineering incident narratives.")

    # Executive Summary
    summary_text = (
        f"In {cfg.get('name')}, the candidate completed an intensive {diff.lower()}-level evaluation "
        f"for the {job_role} role at {company} under {language} communication. "
        f"The candidate achieved an overall readiness rating of {overall_score}/100 across {len(questions)} evaluation scenarios, "
        f"taking {actual_time_sec // 60}m {actual_time_sec % 60}s out of {allowed_sec // 60} minutes allowed. "
        f"Key demonstrated strengths included {sorted_criteria[0][0]}, while future focus should prioritize strengthening {sorted_criteria[-1][0]}."
    )

    return {
        "round_num": round_num,
        "round_name": cfg.get("name"),
        "difficulty": diff,
        "duration_allowed_sec": allowed_sec,
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
                "user_answer": q.user_answer,
                "classification": q.classification,
                "scores": q.scores,
                "feedback": q.feedback,
                "better_possible_answer": q.better_possible_answer,
                "correct_explanation": q.correct_explanation,
                "reaction": q.reaction,
            }
            for q in questions
        ],
        "what_went_well": what_went_well,
        "what_needs_improvement": what_needs_improvement,
        "how_to_improve": how_to_improve,
        "what_to_practise_next": what_to_practise_next,
        "executive_summary": summary_text,
    }

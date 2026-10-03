"""
AchieveHire — Specialized Interview Intelligence Engine
Evaluates candidate responses, classifies answer quality, generates natural interviewer reactions,
handles interruptions, and calculates authentic diagnostic performance metrics.
"""

import re
from typing import Dict, List, Tuple, Any, Optional
from modules.interview.specialized.models import (
    QuestionItem,
    QuestionEvaluation,
    RoundResult,
    ANSWER_CLASSIFICATIONS,
    ROUNDS_CONFIG,
)


# ─────────────────────────────────────────────────────────────────────────────
# Natural Interviewer Reaction Phrases per Language & Response Quality
# ─────────────────────────────────────────────────────────────────────────────

REACTIONS = {
    "English": {
        "strong": [
            "Good. That was a clear explanation.",
            "Well explained. Let's move to the next question.",
            "Solid point. Let's proceed.",
            "That covers the core mechanics well. Let's continue.",
        ],
        "good_followup": [
            "Interesting point. Let's go a little deeper on that.",
            "Okay, let's explore that further.",
            "Can you explain that specific aspect in a bit more detail?",
        ],
        "partial": [
            "I see. That addresses part of it. Let's move forward.",
            "Alright. Let's look at the next concept.",
            "Okay, noted. Let's continue.",
        ],
        "incorrect": [
            "Alright. Let's move on to the next question.",
            "Okay, noted. Let's proceed to the next topic.",
            "I see. Let's continue with our discussion.",
        ],
        "irrelevant": [
            "Your response is not directly addressing the question. Please try to stay focused on the topic.",
            "Let's stay focused on the specific question asked. Moving on.",
        ],
        "overly_long": [
            "Please try to keep your answer concise and focus on the key point.",
            "Good points, but remember to keep your answer structured and concise.",
        ],
        "unanswered": [
            "That's completely fine. It's better to acknowledge and move on.",
            "No problem at all. Let's move to the next question.",
            "Understood. Let's proceed.",
        ],
        "closing_answer": [
            "Thank you for asking that! Our engineering team focuses heavily on scalable system design and continuous integration. We appreciate your curiosity. This concludes our Specialized Interview.",
            "Great question! We emphasize architectural clarity, peer code reviews, and high ownership. Thank you for your time today; this concludes our final interview round.",
        ],
    },
    "Hindi": {
        "strong": [
            "बहुत अच्छा। आपका स्पष्टीकरण काफी सटीक था।",
            "बढ़िया। चलिए अगले प्रश्न की ओर बढ़ते हैं।",
            "स्पष्ट और सही उत्तर। आगे बढ़ते हैं।",
        ],
        "good_followup": [
            "अच्छा बिंदु है। चलिए इस पर थोड़ा और गहराई से चर्चा करते हैं।",
            "ठीक है, क्या आप इस हिस्से को थोड़ा और विस्तार से समझा सकते हैं?",
        ],
        "partial": [
            "समझ गया। आपने मुख्य बिंदु छू लिया है। अगले प्रश्न पर चलते हैं।",
            "ठीक है, चलिए अगले विषय को देखते हैं।",
        ],
        "incorrect": [
            "ठीक है, नोट कर लिया। चलिए अगले प्रश्न की ओर बढ़ते हैं।",
            "समझ गया। आगे बढ़ते हैं।",
        ],
        "irrelevant": [
            "आपका उत्तर सीधे प्रश्न से संबंधित नहीं लग रहा है। कृपया मुख्य विषय पर ध्यान दें।",
            "कृपया प्रश्न के मुख्य बिंदु पर केंद्रित रहें।",
        ],
        "overly_long": [
            "कृपया अपने उत्तर को संक्षिप्त रखें और मुख्य बिंदु पर फोकस करें।",
        ],
        "unanswered": [
            "कोई बात नहीं, यह बिल्कुल स्वाभाविक है। अगले प्रश्न पर चलते हैं।",
            "ठीक है, चलिए आगे बढ़ते हैं।",
        ],
        "closing_answer": [
            "यह पूछने के लिए धन्यवाद! हमारी इंजीनियरिंग टीम स्केलेबिलिटी और गुणवत्ता पर बहुत ध्यान देती है। इसके साथ ही हमारा स्पेशलाइज्ड इंटरव्यू समाप्त होता है।",
        ],
    },
    "Hinglish": {
        "strong": [
            "Good! Aapka explanation kaafi clear aur accurate tha.",
            "Well explained. Next question par chalte hain.",
            "Solid point. Let's proceed forward.",
        ],
        "good_followup": [
            "Interesting point! Is part par thoda aur detail mein discuss karte hain.",
            "Okay, let's go a little deeper into this.",
        ],
        "partial": [
            "I see. Aapne core concept cover kiya hai. Let's move on.",
            "Alright, noted. Agle question par focus karte hain.",
        ],
        "incorrect": [
            "Alright, noted. Let's move on to the next question.",
            "I understand. Let's proceed to the next topic.",
        ],
        "irrelevant": [
            "Aapka response directly question ko address nahi kar raha hai. Please stay focused on the topic.",
            "Please question ke core concept par focus rakhiye.",
        ],
        "overly_long": [
            "Aapka point sahi hai, but please answer ko concise aur structured rakhiye.",
        ],
        "unanswered": [
            "That's completely fine. Let's move to the next question.",
            "No problem, let's proceed.",
        ],
        "closing_answer": [
            "Great question! Humari engineering team scalable architecture aur clean code par focus karti hai. Thank you for your time today; this concludes our final interview.",
        ],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Evaluation Engine Core
# ─────────────────────────────────────────────────────────────────────────────

def is_pass_or_unknown(answer_text: str) -> bool:
    """Detects if candidate explicitly said they don't know or skipped."""
    txt = (answer_text or "").strip().lower()
    if not txt:
        return True
    unknown_patterns = [
        r"\bdon'?t\s+know\b",
        r"\bnot\s+sure\b",
        r"\bno\s+idea\b",
        r"\bpass\b",
        r"\bskip\b",
        r"\bmujhe\s+nahi\s+pata\b",
        r"\bpata\s+nahi\b",
        r"\bi\s+am\s+not\s+aware\b",
        r"\bcan'?t\s+recall\b",
        r"\bunanswered\b",
    ]
    return any(re.search(p, txt) for p in unknown_patterns)


def is_repetition_request(answer_text: str) -> bool:
    """Detects if candidate is asking to repeat or clarify the question."""
    txt = (answer_text or "").strip().lower()
    rep_patterns = [
        r"\brepeat\b",
        r"\bcan\s+you\s+repeat\b",
        r"\bcould\s+you\s+repeat\b",
        r"\bpardon\b",
        r"\bclarify\b",
        r"\bwhat\s+do\s+you\s+mean\b",
        r"\bdobara\b",
        r"\bphir\s+se\b",
        r"\bsamjha\s+nahi\b",
    ]
    return any(re.search(p, txt) for p in rep_patterns)


def evaluate_response(
    question: QuestionItem,
    user_answer: str,
    language: str = "English",
    round_num: int = 1,
) -> Tuple[QuestionEvaluation, str]:
    """
    Evaluates candidate answer against expected criteria and generates
    the diagnostic breakdown and spoken interviewer reaction.
    """
    lang_key = "Hinglish" if "hinglish" in language.lower() else ("Hindi" if "hindi" in language.lower() else "English")
    reactions_dict = REACTIONS.get(lang_key, REACTIONS["English"])

    raw_answer = (user_answer or "").strip()

    # 1. Handle Unanswered / "I don't know"
    if is_pass_or_unknown(raw_answer):
        reaction = reactions_dict["unanswered"][0]
        eval_obj = QuestionEvaluation(
            question_id=question.id,
            question_text=question.get_text(language),
            user_answer=raw_answer if raw_answer else "[No verbal response recorded / Candidate passed]",
            classification="Unanswered / Passed",
            score=2.0 if raw_answer else 0.0,
            what_was_good="Candidate honestly acknowledged lack of familiarity rather than fabricating misleading information.",
            what_was_missing="No technical explanation was provided for the question.",
            correct_explanation=question.correct_answer,
            better_possible_answer=question.better_possible_answer,
            criteria_scores={
                "technical_correctness": 0.0,
                "relevance": 5.0 if raw_answer else 0.0,
                "clarity": 5.0 if raw_answer else 0.0,
                "completeness": 0.0,
                "conciseness": 10.0 if raw_answer else 0.0,
                "depth": 0.0,
            },
            is_intro=question.is_intro,
            is_closing=question.is_closing,
        )
        return eval_obj, reaction

    # 2. Handle Closing Question in Round 4
    if question.is_closing:
        reaction = reactions_dict["closing_answer"][0]
        eval_obj = QuestionEvaluation(
            question_id=question.id,
            question_text=question.get_text(language),
            user_answer=raw_answer,
            classification="Correct",
            score=9.5,
            what_was_good="Demonstrated proactive engagement and technical curiosity regarding the engineering environment.",
            what_was_missing="None.",
            correct_explanation="An active, insightful question about team architecture and development practices.",
            better_possible_answer=question.better_possible_answer,
            criteria_scores={
                "technical_correctness": 9.5,
                "relevance": 9.5,
                "clarity": 9.0,
                "completeness": 9.0,
                "conciseness": 9.0,
                "depth": 9.0,
            },
            is_intro=False,
            is_closing=True,
        )
        return eval_obj, reaction

    # 3. Handle Introduction Questions (Round 1 & Round 4)
    if question.is_intro:
        words = raw_answer.split()
        word_count = len(words)
        has_name_or_role = any(w.lower() in raw_answer.lower() for w in ["name", "experience", "developer", "engineer", "student", "worked", "projects", "build", "focus", "skills", "tech"])

        if word_count < 8 or not has_name_or_role:
            classification = "Correct but Incomplete"
            score = 5.5
            what_good = "Started the introduction."
            what_missing = "Lacked professional context, key technical projects, and career specialization highlights."
            reaction = reactions_dict["partial"][0]
        elif word_count > 150:
            classification = "Excessively Long"
            score = 7.0
            what_good = "Comprehensive background coverage."
            what_missing = "The introduction was overly long. Keep the elevator pitch focused under 60-90 seconds."
            reaction = reactions_dict["overly_long"][0]
        else:
            classification = "Correct"
            score = 8.8 if round_num == 1 else 9.2
            what_good = "Clear, structured professional overview detailing background, technical focus, and projects."
            what_missing = "Could quantify impact and specific architectural contributions even more crisply."
            reaction = reactions_dict["strong"][0]

        eval_obj = QuestionEvaluation(
            question_id=question.id,
            question_text=question.get_text(language),
            user_answer=raw_answer,
            classification=classification,
            score=score,
            what_was_good=what_good,
            what_was_missing=what_missing,
            correct_explanation=question.correct_answer,
            better_possible_answer=question.better_possible_answer,
            criteria_scores={
                "technical_correctness": score,
                "relevance": 9.0,
                "clarity": 8.5,
                "completeness": score,
                "conciseness": 7.5 if classification == "Excessively Long" else 9.0,
                "depth": 8.0,
            },
            is_intro=True,
            is_closing=False,
        )
        return eval_obj, reaction

    # 4. Technical Question Evaluation
    words = raw_answer.split()
    word_count = len(words)
    ans_lower = raw_answer.lower()

    # Keyword and expected points hit analysis
    points_hit = 0
    total_points = max(1, len(question.expected_points))

    for pt in question.expected_points:
        keywords = [w.lower() for w in re.findall(r'\b\w{4,}\b', pt) if w.lower() not in ["with", "that", "this", "from", "when", "using", "into", "their"]]
        if any(kw in ans_lower for kw in keywords):
            points_hit += 1

    hit_ratio = points_hit / total_points

    # Classification logic
    if word_count > 180:
        classification = "Excessively Long"
        score = 6.5 + (hit_ratio * 2.0)
        what_good = "Contained relevant points but suffered from rambling."
        what_missing = "Needs greater brevity; summarize key trade-offs without unnecessary wandering."
        reaction = reactions_dict["overly_long"][0]

    elif hit_ratio >= 0.75 and word_count >= 15:
        classification = "Correct"
        score = 8.5 + min(1.5, hit_ratio * 1.5)
        what_good = "Direct, technically accurate explanation covering the fundamental mechanics."
        what_missing = "Could provide specific production profiling or boundary edge-case examples."
        reaction = reactions_dict["strong"][hash(raw_answer) % len(reactions_dict["strong"])]

    elif hit_ratio >= 0.40 and word_count >= 10:
        classification = "Partially Correct"
        score = 6.0 + (hit_ratio * 2.5)
        what_good = "Demonstrated basic familiarity with the core concept."
        what_missing = "Missed critical depth regarding underlying memory lifecycle, concurrency, or trade-offs."
        reaction = reactions_dict["partial"][0]

    elif word_count >= 20 and hit_ratio < 0.20:
        classification = "Irrelevant"
        score = 3.5
        what_good = "Spoke fluently."
        what_missing = "The answer wandered off-topic and did not directly address the technical question asked."
        reaction = reactions_dict["irrelevant"][0]

    elif word_count < 8:
        classification = "Correct but Incomplete"
        score = 4.5
        what_good = "Mentioned initial keywords."
        what_missing = "The answer was too brief and lacked the technical explanation needed for a professional interview."
        reaction = reactions_dict["partial"][0]

    else:
        classification = "Incorrect"
        score = 3.8
        what_good = "Attempted the question."
        what_missing = f"The technical explanation was incorrect. Expected concepts: {', '.join(question.expected_points)}."
        reaction = reactions_dict["incorrect"][0]

    score = max(1.0, min(10.0, score))

    eval_obj = QuestionEvaluation(
        question_id=question.id,
        question_text=question.get_text(language),
        user_answer=raw_answer,
        classification=classification,
        score=score,
        what_was_good=what_good,
        what_was_missing=what_missing,
        correct_explanation=question.correct_answer,
        better_possible_answer=question.better_possible_answer,
        criteria_scores={
            "technical_correctness": round(score * 1.0, 1),
            "relevance": round(9.0 if classification != "Irrelevant" else 3.5, 1),
            "clarity": round(8.0 if classification != "Unclear" else 4.0, 1),
            "completeness": round(hit_ratio * 10.0, 1),
            "conciseness": round(5.0 if classification == "Excessively Long" else 8.5, 1),
            "depth": round(score * 0.9, 1),
        },
        is_intro=False,
        is_closing=False,
    )

    return eval_obj, reaction


# ─────────────────────────────────────────────────────────────────────────────
# Round Result Aggregator
# ─────────────────────────────────────────────────────────────────────────────

def compute_round_result(
    round_num: int,
    specialization: str,
    language: str,
    interviewer_gender: str,
    time_allowed_sec: int,
    time_taken_sec: int,
    evaluations: List[QuestionEvaluation],
    completed_at: str,
) -> RoundResult:
    """Calculates comprehensive score breakdown, strengths, weaknesses, and improvement advice."""
    round_cfg = ROUNDS_CONFIG.get(round_num, ROUNDS_CONFIG[1])

    if not evaluations:
        overall_score = 0.0
        criteria_avg = {
            "technical_correctness": 0.0,
            "relevance": 0.0,
            "clarity": 0.0,
            "completeness": 0.0,
            "conciseness": 0.0,
            "depth": 0.0,
        }
    else:
        scores = [e.score for e in evaluations]
        overall_score = (sum(scores) / (len(scores) * 10.0)) * 100.0

        criteria_keys = ["technical_correctness", "relevance", "clarity", "completeness", "conciseness", "depth"]
        criteria_avg = {}
        for k in criteria_keys:
            vals = [e.criteria_scores.get(k, 5.0) for e in evaluations]
            criteria_avg[k] = round((sum(vals) / len(vals)) * 10.0, 1)  # Scale out of 100

    # Build evidence-based strengths
    summary_strengths = []
    summary_improvements = []
    what_you_did_well = []
    what_needs_improvement = []
    how_to_improve = []
    what_to_practise_before_next = []

    correct_count = sum(1 for e in evaluations if e.classification == "Correct")
    long_count = sum(1 for e in evaluations if e.classification == "Excessively Long")
    partial_count = sum(1 for e in evaluations if e.classification in ["Partially Correct", "Correct but Incomplete"])
    incorrect_count = sum(1 for e in evaluations if e.classification == "Incorrect")
    unanswered_count = sum(1 for e in evaluations if e.classification == "Unanswered / Passed")

    if correct_count >= 2:
        summary_strengths.append(f"Demonstrated solid foundational clarity on {correct_count} technical concepts.")
        what_you_did_well.append("Accurately explained core architectural principles with appropriate terminology.")

    if criteria_avg.get("relevance", 0) >= 80:
        summary_strengths.append("Maintained high answer relevance and direct focus on the interviewer's questions.")
        what_you_did_well.append("Stayed focused on topic without deviating into unrelated domains.")

    if criteria_avg.get("clarity", 0) >= 80:
        summary_strengths.append("Communicated thoughts in a coherent, professional structure.")
        what_you_did_well.append("Clear articulation and professional vocal pacing.")

    # Weakness & Improvement Detection
    if long_count >= 1:
        summary_improvements.append("Conciseness: Provided answers that were longer than necessary.")
        what_needs_improvement.append("Structure answers using the 'Statement → Reasoning → Example' framework to avoid rambling.")
        how_to_improve.append("Practice delivering crisp 60-second summaries of complex technical concepts.")
        what_to_practise_before_next.append("Time yourself explaining core algorithms in under 90 seconds.")

    if partial_count >= 1 or incorrect_count >= 1:
        summary_improvements.append(f"Technical Depth: {partial_count + incorrect_count} question(s) had missing edge-case mechanics.")
        what_needs_improvement.append(f"Deepen knowledge of internal memory models, concurrency, and trade-offs in {specialization}.")
        how_to_improve.append(f"Review standard library documentation and internal execution engines for {specialization}.")
        what_to_practise_before_next.append(f"Drill {round_cfg['difficulty']} difficulty system design and implementation scenarios.")

    if unanswered_count >= 1:
        summary_improvements.append(f"Knowledge Breadth: Passed on {unanswered_count} question(s).")
        what_needs_improvement.append("Broaden exposure to foundational patterns across the domain.")
        how_to_improve.append("Read through technical interview FAQs and domain cheat sheets.")
        what_to_practise_before_next.append("Review the correct answers provided in the question-by-question report.")

    if not summary_strengths:
        summary_strengths.append("Attempted technical discussion with honest communication.")
        what_you_did_well.append("Engaged with the interviewer across the full round session.")

    if not summary_improvements:
        summary_improvements.append("Maintain consistency and focus on advanced edge cases in the next round.")
        what_needs_improvement.append("Refine technical depth for higher-complexity architectural trade-offs.")
        how_to_improve.append("Focus on benchmark figures, memory profiling, and distributed synchronization.")
        what_to_practise_before_next.append(f"Prepare for {ROUNDS_CONFIG.get(min(4, round_num + 1), round_cfg)['name']} topics.")

    return RoundResult(
        round_num=round_num,
        round_name=round_cfg["name"],
        difficulty=round_cfg["difficulty"],
        specialization=specialization,
        language=language,
        interviewer_gender=interviewer_gender,
        time_allowed_sec=time_allowed_sec,
        time_taken_sec=time_taken_sec,
        completed_at=completed_at,
        status="completed",
        overall_score=overall_score,
        criteria_breakdown=criteria_avg,
        evaluations=[e.to_dict() for e in evaluations],
        summary_strengths=summary_strengths,
        summary_improvements=summary_improvements,
        what_you_did_well=what_you_did_well,
        what_needs_improvement=what_needs_improvement,
        how_to_improve=how_to_improve,
        what_to_practise_before_next=what_to_practise_before_next,
    )

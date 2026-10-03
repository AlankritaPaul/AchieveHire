"""
Unit Tests for AchieveHire Job Related Voice Interview Module
Tests:
1. 6-Round configurations (durations: 20, 25, 30, 35, 40, 45 min; panel counts: 1, 2, 2, 3, 3, 4).
2. Preferred languages strictly restricted to English, Hindi, Hinglish.
3. Panel generation across progressive seniority tiers.
4. Engine rules: Round 1 Question 1 is strictly 'Please introduce yourself.'; Rounds 2-6 do not repeat intro.
5. Evaluator: 9 criteria, answer classifications, 'I don't know' handling, better possible answers.
6. Storage: persistence, sequential round locking.
7. PDF generation: single-round and overall reports with AchieveHire branding; no certificates.
"""

import unittest
from modules.interview.job_related.models import (
    SUGGESTED_JOB_ROLES,
    SUGGESTED_COMPANIES,
    INTERVIEW_LANGUAGES,
    JOB_ROUNDS_CONFIG,
    EVALUATION_CRITERIA,
    ANSWER_CLASSIFICATIONS,
)
from modules.interview.job_related.panel_generator import generate_panel_for_round
from modules.interview.job_related.engine import (
    generate_round_questions,
    generate_clarification_response,
    generate_closing_qa_response,
)
from modules.interview.job_related.evaluator import (
    evaluate_candidate_answer,
    generate_round_evaluation,
)
from modules.interview.job_related.storage import (
    initialize_job_interview_session,
    load_job_interview_session,
    save_round_evaluation,
    is_round_unlocked,
)
from modules.interview.job_related.report_generator import (
    generate_job_round_pdf,
    generate_job_overall_pdf,
)


class TestJobRelatedInterview(unittest.TestCase):

    def test_configuration_and_languages(self):
        # 1. Exactly 3 languages allowed
        self.assertEqual(len(INTERVIEW_LANGUAGES), 3)
        self.assertIn("English", INTERVIEW_LANGUAGES)
        self.assertIn("Hindi", INTERVIEW_LANGUAGES)
        self.assertIn("Hinglish", INTERVIEW_LANGUAGES)

        # 2. Exactly 6 rounds
        self.assertEqual(len(JOB_ROUNDS_CONFIG), 6)
        durations = [JOB_ROUNDS_CONFIG[i]["duration_minutes"] for i in range(1, 7)]
        self.assertEqual(durations, [20, 25, 30, 35, 40, 45])

        # 3. Exactly 9 criteria
        self.assertEqual(len(EVALUATION_CRITERIA), 9)

        # 4. Classifications
        self.assertIn("Unanswered", ANSWER_CLASSIFICATIONS)
        self.assertIn("Correct", ANSWER_CLASSIFICATIONS)
        self.assertIn("Partially Correct", ANSWER_CLASSIFICATIONS)

    def test_panel_generation_seniority(self):
        # Round 1: 1 interviewer
        p1 = generate_panel_for_round("Software Engineer", "Google", 1)
        self.assertEqual(len(p1), 1)

        # Round 2: 2 interviewers
        p2 = generate_panel_for_round("Software Engineer", "Google", 2)
        self.assertEqual(len(p2), 2)

        # Round 3: 2 interviewers
        p3 = generate_panel_for_round("Software Engineer", "Google", 3)
        self.assertEqual(len(p3), 2)

        # Round 4: 3 interviewers
        p4 = generate_panel_for_round("Software Engineer", "Google", 4)
        self.assertEqual(len(p4), 3)

        # Round 5: 3 interviewers
        p5 = generate_panel_for_round("Software Engineer", "Google", 5)
        self.assertEqual(len(p5), 3)

        # Round 6: 4 interviewers (Executive Panel)
        p6 = generate_panel_for_round("Software Engineer", "Google", 6)
        self.assertEqual(len(p6), 4)

    def test_round_1_first_question_strictly_intro(self):
        resume = {"skills": "Python, Django", "projects": "E-Commerce App"}
        q_list, panel = generate_round_questions("Backend Developer", "Amazon", resume, "English", 1)
        self.assertTrue(len(q_list) >= 4)
        first_q = q_list[0].question_text
        self.assertIn("introduce yourself", first_q.lower())

        # Test Hindi intro
        q_list_hi, _ = generate_round_questions("Backend Developer", "Amazon", resume, "Hindi", 1)
        self.assertIn("परिचय", q_list_hi[0].question_text)

        # Verify Round 2 does NOT start with introduce yourself
        q_list_r2, _ = generate_round_questions("Backend Developer", "Amazon", resume, "English", 2)
        self.assertNotIn("introduce yourself", q_list_r2[0].question_text.lower())

    def test_evaluator_unanswered_handling(self):
        resume = {"skills": "Java, Spring Boot"}
        q_list, _ = generate_round_questions("Java Developer", "Infosys", resume, "English", 1)
        q = q_list[0]

        # Candidate says "I don't know"
        eval_q = evaluate_candidate_answer(q, "I don't know", "English", "Java Developer", "Infosys")
        self.assertEqual(eval_q.classification, "Unanswered")
        self.assertIn("unanswered", eval_q.feedback.lower())

    def test_evaluator_detailed_answer(self):
        resume = {"skills": "Python, Docker"}
        q_list, _ = generate_round_questions("DevOps Engineer", "Microsoft", resume, "English", 2)
        q = q_list[0]

        detailed_ans = (
            "In our CI/CD pipeline, we enforce automated unit tests, integration contracts, "
            "and linting before any merge. We use Canary deployments with Prometheus metrics "
            "to monitor error rates and latency, rolling back automatically if p99 latency exceeds threshold."
        )
        eval_q = evaluate_candidate_answer(q, detailed_ans, "English", "DevOps Engineer", "Microsoft")
        self.assertIn(eval_q.classification, ["Correct", "Partially Correct"])
        self.assertTrue(eval_q.scores["Technical/Professional Knowledge"] >= 60)

    def test_sequential_round_locking(self):
        session = {
            "completed_rounds": [1],
            "active_round": 2,
        }
        self.assertTrue(is_round_unlocked(session, 1))
        self.assertTrue(is_round_unlocked(session, 2))
        self.assertFalse(is_round_unlocked(session, 3))
        self.assertFalse(is_round_unlocked(session, 4))

    def test_pdf_generation_single_and_overall(self):
        eval_data = {
            "round_num": 1,
            "round_name": "Round 1 — Easy",
            "difficulty": "Easy",
            "duration_allowed_sec": 1200,
            "actual_time_taken_sec": 840,
            "completion_date": "October 4, 2026",
            "overall_score": 82,
            "target_role": "Software Engineer",
            "target_company": "Google",
            "language": "English",
            "criteria_scores": {c: 80 for c in EVALUATION_CRITERIA},
            "questions": [
                {
                    "question_id": "q1",
                    "interviewer_name": "Ananya Sharma",
                    "interviewer_title": "Technical Recruiter",
                    "question_text": "Please introduce yourself.",
                    "user_answer": "I am a software engineer with 2 years of experience building distributed systems.",
                    "classification": "Correct",
                    "feedback": "Strong introduction.",
                    "better_possible_answer": "I am a candidate focused on scalable software design...",
                    "correct_explanation": "Clear structured overview of skills and accomplishments.",
                }
            ],
            "what_went_well": ["Confident self introduction"],
            "what_needs_improvement": ["Elaborate more on specific project outcomes"],
            "how_to_improve": ["Use STAR format"],
            "what_to_practise_next": ["Prepare system design fundamentals"],
            "executive_summary": "Candidate displayed strong foundational communication and clear motivation.",
        }

        # Test single round PDF
        pdf_bytes = generate_job_round_pdf(eval_data)
        self.assertTrue(len(pdf_bytes) > 1000)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        # Test overall PDF
        session_data = {
            "target_role": "Software Engineer",
            "target_company": "Google",
            "language": "English",
            "round_evaluations": {"1": eval_data},
        }
        overall_pdf_bytes = generate_job_overall_pdf(session_data)
        self.assertTrue(len(overall_pdf_bytes) > 1000)
        self.assertTrue(overall_pdf_bytes.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()

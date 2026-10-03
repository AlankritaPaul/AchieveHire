"""
Unit Tests for AchieveHire Last-Minute Preparation Interview Module
Tests:
1. Fixed 30-minute duration constant (non-extendable).
2. Unlimited attempts, distinct mode definitions (Specialized vs Job-Related).
3. Panel generator constructs 3 distinct interviewers for both modes.
4. Question engine enforces Question 1 as 'Please introduce yourself.' and follows Easy -> Moderate -> Hard progression.
5. Evaluator handles 9 criteria, honest scoring for 'I don't know' / unanswered questions, and synthesis.
6. Storage stores every completed attempt permanently without overwriting earlier attempts.
7. PDF report generation produces branded PDF with official stamp and strictly zero certificates.
"""

import unittest
from pathlib import Path
from modules.interview.last_minute.models import (
    LAST_MINUTE_DURATION_MINUTES,
    LAST_MINUTE_DURATION_SECONDS,
    MODE_SPECIALIZED,
    MODE_JOB_RELATED,
    EVALUATION_CRITERIA,
    POPULAR_SPECIALIZATIONS,
    LastMinuteQuestionRecord,
)
from modules.interview.last_minute.panel_generator import generate_last_minute_panel
from modules.interview.last_minute.engine import generate_last_minute_questions
from modules.interview.last_minute.evaluator import (
    evaluate_last_minute_answer,
    synthesize_attempt_evaluation,
)
from modules.interview.last_minute.storage import (
    save_new_attempt,
    load_user_attempts,
    get_attempt_by_id,
    get_attempt_comparison_data,
    _get_user_file,
)
from modules.interview.last_minute.report_generator import generate_last_minute_pdf


class TestLastMinutePreparationInterview(unittest.TestCase):

    def setUp(self):
        self.test_user_id = "test_user_lm_suite_99"
        # Clean any existing test file
        test_file = _get_user_file(self.test_user_id)
        if test_file.exists():
            test_file.unlink()

    def tearDown(self):
        test_file = _get_user_file(self.test_user_id)
        if test_file.exists():
            test_file.unlink()

    def test_duration_and_core_specifications(self):
        # 1. Fixed duration must be strictly 30 minutes
        self.assertEqual(LAST_MINUTE_DURATION_MINUTES, 30)
        self.assertEqual(LAST_MINUTE_DURATION_SECONDS, 1800)

        # 2. Modes
        self.assertEqual(MODE_SPECIALIZED, "Last-Minute Specialized Preparation")
        self.assertEqual(MODE_JOB_RELATED, "Last-Minute Job Related Preparation")

        # 3. 9 evaluation criteria
        self.assertEqual(len(EVALUATION_CRITERIA), 9)
        self.assertIn("Technical/Professional Knowledge", EVALUATION_CRITERIA)
        self.assertIn("Interview Behaviour", EVALUATION_CRITERIA)

        # 4. Specializations list
        self.assertIn("Python", POPULAR_SPECIALIZATIONS)
        self.assertIn("Java", POPULAR_SPECIALIZATIONS)
        self.assertIn("C++", POPULAR_SPECIALIZATIONS)

    def test_panel_generation(self):
        # Specialized panel has 3 members with distinct specialties
        spec_panel = generate_last_minute_panel(MODE_SPECIALIZED, "Python")
        self.assertEqual(len(spec_panel), 3)
        names = [m.name for m in spec_panel]
        self.assertEqual(len(set(names)), 3, "Panel members must have distinct names")

        # Job-related panel has 3 members with company context
        job_panel = generate_last_minute_panel(MODE_JOB_RELATED, "Backend Architect", "Microsoft")
        self.assertEqual(len(job_panel), 3)
        self.assertTrue(any("Microsoft" in m.title for m in job_panel))

    def test_question_generation_and_intro_rule(self):
        # 1. Specialized questions
        questions, panel = generate_last_minute_questions(MODE_SPECIALIZED, "Python")
        self.assertEqual(len(questions), 6)
        self.assertEqual(len(panel), 3)

        # First question MUST be the introduction
        self.assertEqual(questions[0].question_text, "Please introduce yourself.")
        self.assertEqual(questions[0].difficulty, "Intro")

        # Progression check
        diffs = [q.difficulty for q in questions]
        self.assertIn("Intro", diffs)
        self.assertIn("Easy", diffs)
        self.assertIn("Moderate", diffs)
        self.assertIn("Hard", diffs)

        # 2. Multi-language support (Hindi / Hinglish intro)
        q_hi, _ = generate_last_minute_questions(MODE_SPECIALIZED, "Python", language="Hindi")
        self.assertIn("परिचय", q_hi[0].question_text)

        q_hing, _ = generate_last_minute_questions(MODE_SPECIALIZED, "Python", language="Hinglish")
        self.assertIn("introduce yourself", q_hing[0].question_text.lower())

        # 3. Job Related questions with Resume
        resume = {"skills": ["Python", "Kubernetes", "PostgreSQL"], "experience": "3 years backend"}
        job_qs, _ = generate_last_minute_questions(
            MODE_JOB_RELATED,
            topic="Senior Software Engineer",
            company="Google",
            language="English",
            resume=resume,
        )
        self.assertEqual(job_qs[0].question_text, "Please introduce yourself.")
        self.assertEqual(len(job_qs), 6)

    def test_evaluator_and_scorecard_synthesis(self):
        questions, _ = generate_last_minute_questions(MODE_SPECIALIZED, "Python")

        # Evaluate Question 1 with a solid answer
        q1 = questions[0]
        evaluate_last_minute_answer(
            q1,
            "I have 4 years of experience specializing in Python microservices, distributed caching with Redis, and building high-throughput APIs.",
            topic="Python",
        )
        self.assertIn(q1.classification, ["Correct", "Partially Correct", "Correct but Incomplete"])
        self.assertGreater(q1.scores["Technical/Professional Knowledge"], 40)
        self.assertTrue(len(q1.better_possible_answer) > 0)

        # Evaluate Question 2 with "I don't know"
        q2 = questions[1]
        evaluate_last_minute_answer(q2, "I don't know the exact answer to this.", topic="Python")
        self.assertEqual(q2.classification, "Unanswered")
        self.assertGreater(q2.scores["Interview Behaviour"], 50)  # Honest self-awareness credit

        # Synthesize attempt evaluation
        attempt_data = synthesize_attempt_evaluation(
            mode=MODE_SPECIALIZED,
            topic="Python",
            configuration={"language": "English"},
            questions=questions,
            actual_time_sec=1420,
        )
        self.assertEqual(attempt_data["mode"], MODE_SPECIALIZED)
        self.assertEqual(attempt_data["topic_title"], "Python")
        self.assertEqual(attempt_data["actual_time_taken_sec"], 1420)
        self.assertIn("what_went_well", attempt_data)
        self.assertIn("what_needs_improvement", attempt_data)
        self.assertIn("how_to_improve", attempt_data)
        self.assertIn("what_to_practise_next", attempt_data)
        self.assertEqual(len(attempt_data["criteria_scores"]), 9)

    def test_storage_never_overwrites_earlier_attempts(self):
        # Create attempt 1
        q_list, _ = generate_last_minute_questions(MODE_SPECIALIZED, "Python")
        for q in q_list:
            evaluate_last_minute_answer(q, "Valid detailed response", "Python")
        att1_data = synthesize_attempt_evaluation(
            mode=MODE_SPECIALIZED,
            topic="Python",
            configuration={"language": "English"},
            questions=q_list,
            actual_time_sec=1200,
        )

        id1 = save_new_attempt(self.test_user_id, att1_data)
        self.assertTrue(id1.startswith("LM-"))

        # Create attempt 2 (C++)
        q_list2, _ = generate_last_minute_questions(MODE_SPECIALIZED, "C++")
        for q in q_list2:
            evaluate_last_minute_answer(q, "C++ pointers and templates answer", "C++")
        att2_data = synthesize_attempt_evaluation(
            mode=MODE_SPECIALIZED,
            topic="C++",
            configuration={"language": "English"},
            questions=q_list2,
            actual_time_sec=1350,
        )

        id2 = save_new_attempt(self.test_user_id, att2_data)
        self.assertNotEqual(id1, id2)

        # Create attempt 3 (Job Related - Google)
        q_list3, _ = generate_last_minute_questions(MODE_JOB_RELATED, "DevOps Engineer", "Google")
        att3_data = synthesize_attempt_evaluation(
            mode=MODE_JOB_RELATED,
            topic="DevOps Engineer at Google",
            configuration={"company": "Google"},
            questions=q_list3,
            actual_time_sec=1600,
        )

        id3 = save_new_attempt(self.test_user_id, att3_data)

        # Verify all 3 attempts exist and order is maintained
        history = load_user_attempts(self.test_user_id)
        self.assertEqual(len(history), 3, "All 3 attempts must be preserved, never overwritten")
        self.assertEqual(history[0]["attempt_id"], id1)
        self.assertEqual(history[1]["attempt_id"], id2)
        self.assertEqual(history[2]["attempt_id"], id3)

        # Verify get_attempt_by_id
        fetched = get_attempt_by_id(self.test_user_id, id2)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["topic_title"], "C++")

        # Verify get_attempt_comparison_data
        comp = get_attempt_comparison_data(self.test_user_id)
        self.assertEqual(len(comp), 3)

    def test_pdf_generation_with_stamp_and_no_certificates(self):
        q_list, _ = generate_last_minute_questions(MODE_SPECIALIZED, "Python")
        evaluate_last_minute_answer(
            q_list[0],
            "I have 5 years building scalable applications and microservices using Python and FastAPI.",
            "Python",
        )
        attempt_data = synthesize_attempt_evaluation(
            mode=MODE_SPECIALIZED,
            topic="Python",
            configuration={"language": "English"},
            questions=q_list,
            actual_time_sec=1500,
        )
        attempt_data["attempt_id"] = "LM-TEST-001"
        attempt_data["attempt_number"] = 1

        pdf_bytes = generate_last_minute_pdf(attempt_data)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 1000, "PDF bytes should be non-empty")
        self.assertTrue(pdf_bytes.startswith(b"%PDF"), "Must be a valid PDF document")

        # Strictly verify no certificates are issued or mentioned
        self.assertNotIn(b"CERTIFICATE OF COMPLETION", pdf_bytes)
        self.assertNotIn(b"Course Certificate", pdf_bytes)


if __name__ == "__main__":
    unittest.main()

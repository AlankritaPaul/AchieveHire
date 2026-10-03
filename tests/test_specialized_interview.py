"""
AchieveHire — Specialized Interview Module Test Suite
Validates the complete 4-round architecture, manual specialization handling,
question bank generation, intelligence evaluation engine, natural interviewer responses,
progression locks, storage isolation, and PDF report generation.
"""

import unittest
import os
import shutil
from modules.interview.specialized.models import (
    ROUNDS_CONFIG,
    CLASSIFICATION_BADGES,
    QuestionItem,
    QuestionEvaluation,
    RoundResult,
)
from modules.interview.specialized.questions_bank import (
    get_specialized_questions,
    get_self_intro_question,
    get_closing_candidate_inquiry,
)
from modules.interview.specialized.engine import (
    evaluate_response,
    compute_round_result,
)
from modules.interview.specialized.storage import (
    save_specialized_progress,
    load_specialized_progress,
    record_round_completion,
    record_round_cancellation,
    is_round_unlocked,
    load_all_user_interviews,
)
from modules.interview.specialized.report_generator import (
    build_overall_specialized_report,
    generate_round_report_pdf,
    generate_overall_report_pdf,
)


class TestSpecializedInterviewModule(unittest.TestCase):
    """Test suite for the AchieveHire Specialized Interview subsystem."""

    def setUp(self):
        self.test_user = "test_user_spec_99"
        self.test_spec_preset = "Python"
        self.test_spec_custom = "Rust Async Programming"

    def tearDown(self):
        # Clean test files
        p1 = f"data/interviews/specialized_{self.test_user}_{self.test_spec_preset}.json"
        p2 = f"data/interviews/specialized_{self.test_user}_{self.test_spec_custom}.json"
        for p in [p1, p2]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except Exception:
                    pass

    def test_round_configurations(self):
        """Verify the 4 rounds have correct durations, names, and progressive difficulty."""
        self.assertEqual(len(ROUNDS_CONFIG), 4)
        self.assertEqual(ROUNDS_CONFIG[1]["duration_minutes"], 20)
        self.assertEqual(ROUNDS_CONFIG[2]["duration_minutes"], 30)
        self.assertEqual(ROUNDS_CONFIG[3]["duration_minutes"], 35)
        self.assertEqual(ROUNDS_CONFIG[4]["duration_minutes"], 40)

        self.assertEqual(ROUNDS_CONFIG[1]["difficulty"], "Easy")
        self.assertEqual(ROUNDS_CONFIG[2]["difficulty"], "Moderate")
        self.assertEqual(ROUNDS_CONFIG[3]["difficulty"], "Hard")
        self.assertEqual(ROUNDS_CONFIG[4]["difficulty"], "Final")

    def test_question_bank_structure(self):
        """Verify question banks for preset & custom specializations across all languages."""
        for lang in ["English", "Hindi", "Hinglish"]:
            # Round 1: Q1 MUST be self-introduction
            r1_qs = get_specialized_questions("Python", 1, language=lang, count=5)
            self.assertTrue(r1_qs[0].is_intro)
            q_text = (r1_qs[0].text_en + " " + r1_qs[0].text_hi + " " + r1_qs[0].text_hinglish).lower()
            self.assertTrue("introduce" in q_text or "parichay" in q_text or "intro" in q_text)

            # Round 2: MUST NOT be self-introduction
            r2_qs = get_specialized_questions("Python", 2, language=lang, count=6)
            self.assertFalse(r2_qs[0].is_intro)

            # Round 3: MUST NOT be self-introduction
            r3_qs = get_specialized_questions("Python", 3, language=lang, count=6)
            self.assertFalse(r3_qs[0].is_intro)

            # Round 4: Q1 MUST be self-introduction & Last Q MUST be candidate inquiry
            r4_qs = get_specialized_questions("Python", 4, language=lang, count=7)
            self.assertTrue(r4_qs[0].is_intro)
            self.assertTrue(r4_qs[-1].is_closing)

    def test_manual_custom_specialization_questions(self):
        """Verify dynamic generation for arbitrary manually written specializations."""
        custom_spec = "Distributed Consensus in Go"
        qs = get_specialized_questions(custom_spec, 2, language="English", count=5)
        self.assertEqual(len(qs), 5)
        for q in qs:
            self.assertIn(custom_spec, q.text_en)
            self.assertEqual(q.specialization, custom_spec)

    def test_evaluation_engine_classifications(self):
        """Verify response evaluation and scoring across all standard classification outcomes."""
        q = QuestionItem(
            id="test_q1",
            text_en="What is a Python generator and how does yield work?",
            text_hi="पायथन जेनरेटर क्या है और यील्ड कैसे काम करता है?",
            text_hinglish="Python generator kya hai aur yield kaise kaam karta hai?",
            difficulty="Easy",
            specialization="Python",
            category="Core Mechanics",
            expected_points=["yield keyword", "state preservation", "memory efficiency", "lazy evaluation"],
            correct_answer="A generator is a function that produces a sequence of values lazily using the yield keyword.",
            better_possible_answer="In Python, a generator yields values one by one without loading all data into memory at once.",
        )

        # 1. Correct / Partial
        eval_obj, reaction = evaluate_response(
            question=q,
            user_answer="A generator in Python produces values lazily using the yield keyword, preserving execution state and saving memory efficiency.",
            round_num=1,
            language="English",
        )
        self.assertIn(eval_obj.classification, ["Correct", "Partially Correct"])
        self.assertGreaterEqual(eval_obj.score, 6.0)
        self.assertTrue(len(reaction) > 0)

        # 2. Unanswered / Empty
        eval_empty, react_empty = evaluate_response(
            question=q,
            user_answer="",
            round_num=1,
            language="English",
        )
        self.assertEqual(eval_empty.classification, "Unanswered / Passed")
        self.assertEqual(eval_empty.score, 0.0)

        # 3. Pass / I don't know
        eval_pass, react_pass = evaluate_response(
            question=q,
            user_answer="I don't know the answer to this question.",
            round_num=1,
            language="English",
        )
        self.assertEqual(eval_pass.classification, "Unanswered / Passed")
        self.assertTrue(len(react_pass) > 0)

        # 4. Excessively Long
        long_text = "Word " * 280
        eval_long, react_long = evaluate_response(
            question=q,
            user_answer=long_text,
            round_num=1,
            language="English",
        )
        self.assertEqual(eval_long.classification, "Excessively Long")

    def test_storage_and_progression_unlocking(self):
        """Verify round progression lock: R1 unlocked by default, R2 locked until R1 complete."""
        # Initial check
        self.assertTrue(is_round_unlocked(self.test_user, self.test_spec_preset, 1))
        self.assertFalse(is_round_unlocked(self.test_user, self.test_spec_preset, 2))

        # Record Round 1 completion
        dummy_r1_report = {
            "round_num": 1,
            "round_name": "Round 1 — Easy",
            "specialization": self.test_spec_preset,
            "overall_score": 85.0,
            "time_allowed_sec": 1200,
            "time_taken_sec": 480,
            "evaluations": [],
            "what_you_did_well": ["Clear articulation"],
            "what_needs_improvement": ["Elaborate on edge cases"],
            "how_to_improve": ["Practise timer pacing"],
            "what_to_practise_before_next": ["OOP inheritance"],
        }
        record_round_completion(self.test_user, self.test_spec_preset, 1, dummy_r1_report)

        # R2 should now be unlocked
        self.assertTrue(is_round_unlocked(self.test_user, self.test_spec_preset, 2))
        self.assertFalse(is_round_unlocked(self.test_user, self.test_spec_preset, 3))

    def test_cancellation_zero_marks_rule(self):
        """Verify that cancelling or leaving midway cancels the round with 0 marks / partial records discarded."""
        record_round_cancellation(self.test_user, self.test_spec_preset, 2, "Candidate left midway")
        progress = load_specialized_progress(self.test_user, self.test_spec_preset)
        self.assertNotIn(2, progress.get("rounds_completed", []))

    def test_pdf_round_and_overall_generation(self):
        """Verify PDF bytes generation for round report and overall 4-round report without crashing."""
        dummy_round_report = {
            "round_num": 1,
            "round_name": "Round 1 — Easy",
            "specialization": "Python",
            "language": "English",
            "difficulty": "Easy",
            "overall_score": 88.5,
            "time_allowed_sec": 1200,
            "time_taken_sec": 420,
            "completed_at": "2026-10-03 20:00:00",
            "evaluations": [
                {
                    "question_id": "q1",
                    "question_text": "Please introduce yourself and your technical background.",
                    "user_answer": "I am a backend engineer with 3 years of experience in Python and FastAPI.",
                    "classification": "Correct",
                    "score": 9.0,
                    "ideal_answer": "A structured introduction highlighting technical depth and recent impact.",
                    "better_model_answer": "I am a software engineer specializing in scalable backend services...",
                    "what_was_good": "Concise and relevant summary.",
                    "what_was_missing": "Mention specific architecture projects.",
                    "how_to_improve": "Highlight metrics and measurable business impact.",
                    "interviewer_reaction": "Thank you for the concise overview.",
                }
            ],
            "what_you_did_well": ["Clear technical communication", "Quick response time"],
            "what_needs_improvement": ["Include quantifiable results in explanations"],
            "how_to_improve": ["Use the STAR method for experiential questions"],
            "what_to_practise_before_next": ["Deep dive into async event loops"],
        }

        # Test single round PDF
        pdf_bytes = generate_round_report_pdf(dummy_round_report)
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertGreater(len(pdf_bytes), 1000)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        # Test overall 4-round PDF
        dummy_overall_report = {
            "specialization": "Python",
            "overall_score": 86.4,
            "total_time_taken_min": 85,
            "completed_at": "2026-10-03 21:00:00",
            "intro_comparison": {
                "round_1_intro": "I am a developer.",
                "round_4_intro": "I am a senior backend engineer leading distributed systems...",
                "round_1_score": 6.0,
                "round_4_score": 9.2,
                "analysis": "Tremendous improvement in structural confidence and value proposition articulation.",
            },
            "rounds_summary": [
                {"round_num": 1, "round_name": "Round 1 — Easy", "score": 88.5, "status": "Completed"},
                {"round_num": 2, "round_name": "Round 2 — Moderate", "score": 84.0, "status": "Completed"},
                {"round_num": 3, "round_name": "Round 3 — Hard", "score": 82.5, "status": "Completed"},
                {"round_num": 4, "round_name": "Round 4 — Final", "score": 90.5, "status": "Completed"},
            ],
            "overall_strengths": ["High algorithmic clarity", "Strong architectural instinct"],
            "overall_weaknesses": ["Occasionally brief on memory tradeoffs"],
            "final_recommendations": ["Ready for Staff / Lead technical hiring rounds"],
        }

        overall_pdf_bytes = generate_overall_report_pdf(dummy_overall_report)
        self.assertIsInstance(overall_pdf_bytes, bytes)
        self.assertGreater(len(overall_pdf_bytes), 1000)
        self.assertTrue(overall_pdf_bytes.startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()

"""
Comprehensive test suite for AscendCareer Resume Guide module.
"""

import os
import unittest
from modules.resume_guide.parser import extract_text_from_file, parse_resume_sections
from modules.resume_guide.analyzer import ResumeAnalyzer
from modules.resume_guide.optimizer import ResumeOptimizer
from modules.resume_guide.exporter import export_resume_to_pdf, export_resume_to_docx

class TestResumeGuide(unittest.TestCase):
    def setUp(self):
        self.needs_imp_path = os.path.join("sample_resumes", "needs_improvement_resume.txt")
        self.well_aligned_path = os.path.join("sample_resumes", "well_aligned_resume.txt")

        with open(self.needs_imp_path, "r", encoding="utf-8") as f:
            self.needs_imp_text = f.read()

        with open(self.well_aligned_path, "r", encoding="utf-8") as f:
            self.well_aligned_text = f.read()

    def test_parser_sections(self):
        """Test parsing resume into logical sections."""
        sections = parse_resume_sections(self.needs_imp_text)
        self.assertIn("experience", sections)
        self.assertIn("projects", sections)
        self.assertIn("skills", sections)
        self.assertIn("education", sections)

    def test_analyzer_needs_improvement(self):
        """Test analyzer flags areas needing improvement for unoptimized resume."""
        sections = parse_resume_sections(self.needs_imp_text)
        analyzer = ResumeAnalyzer(
            job_role="Software Developer",
            company="Google",
            job_description=None
        )
        res = analyzer.analyze(self.needs_imp_text, sections)

        # Should determine it needs improvement
        self.assertFalse(res["is_well_aligned"])
        self.assertIsNone(res["jd_alignment_score"])  # No JD provided -> no JD score
        self.assertFalse(res["has_jd"])

        # Should identify weak verbs
        self.assertTrue(res["experience_relevance"]["weak_verb_count"] > 0)

        # Should identify unnecessary details
        self.assertTrue(len(res["unnecessary_details"]) > 0)
        self.assertIn("Marital Status", res["unnecessary_details"])

        # High level areas should contain relevant topics
        self.assertTrue(len(res["high_level_areas"]) > 0)
        self.assertIn("Improve job-related keywords", res["high_level_areas"])

    def test_analyzer_with_job_description(self):
        """Test analyzer includes JD Alignment only when JD is provided."""
        sections = parse_resume_sections(self.needs_imp_text)
        sample_jd = "Looking for a Software Developer with experience in Python, REST APIs, and Docker."
        analyzer = ResumeAnalyzer(
            job_role="Software Developer",
            company="Microsoft",
            job_description=sample_jd
        )
        res = analyzer.analyze(self.needs_imp_text, sections)

        self.assertTrue(res["has_jd"])
        self.assertIsNotNone(res["jd_alignment_score"])
        self.assertTrue(res["jd_alignment_score"] > 0)

    def test_analyzer_well_aligned(self):
        """Test analyzer recognizes a strong, well-aligned resume."""
        sections = parse_resume_sections(self.well_aligned_text)
        analyzer = ResumeAnalyzer(
            job_role="Software Developer",
            company="Google",
            job_description=None
        )
        res = analyzer.analyze(self.well_aligned_text, sections)

        self.assertTrue(res["is_well_aligned"])
        self.assertGreaterEqual(res["role_alignment_score"], 82)
        self.assertEqual(len(res["unnecessary_details"]), 0)

    def test_optimizer_accuracy_rule_and_before_after(self):
        """Test optimizer strictly preserves factual accuracy and provides Before/After."""
        sections = parse_resume_sections(self.needs_imp_text)
        analyzer = ResumeAnalyzer(
            job_role="Software Developer",
            company="Google",
            job_description=None
        )
        res = analyzer.analyze(self.needs_imp_text, sections)

        optimizer = ResumeOptimizer(job_role="Software Developer", company="Google")
        improvements = optimizer.generate_improvements(sections, res)

        self.assertTrue(len(improvements) > 0)

        for imp in improvements:
            self.assertIn("before", imp)
            self.assertIn("after", imp)
            self.assertIn("section_title", imp)
            self.assertIn("rationale", imp)

            # Strict Accuracy Rule: original facts like 'State University' must not be replaced with a fake university
            if "State University" in imp["before"]:
                self.assertIn("State University", imp["after"])

        # Test compiling final resume with mixed decisions
        user_decisions = {
            "summary": {
                "decision": "accept",
                "improved": improvements[0]["after"]
            },
            "experience": {
                "decision": "edit",
                "edited": "Software Engineer | TechCo Solutions\n• Architected REST APIs and microservices."
            },
            "skills": {
                "decision": "keep_original",
                "original": sections["skills"]
            }
        }

        final_text = ResumeOptimizer.compile_final_resume(sections, user_decisions)
        self.assertIn("Architected REST APIs", final_text)
        self.assertIn("State University", final_text)

    def test_exporter_pdf_and_docx(self):
        """Test export utilities output valid PDF and DOCX binary payloads."""
        pdf_bytes = export_resume_to_pdf(self.well_aligned_text, "Elena Rostova Resume")
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        docx_bytes = export_resume_to_docx(self.well_aligned_text)
        self.assertTrue(docx_bytes.startswith(b"PK"))  # DOCX is a zip archive

if __name__ == "__main__":
    unittest.main()

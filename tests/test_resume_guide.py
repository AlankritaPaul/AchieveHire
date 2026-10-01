"""
Comprehensive test suite for AscendCareer Resume Guide module.
Validates the updated Resume Analysis & Resume Improvement principles:
- Accurate independent evaluation
- Clear distinction between "Already Correct", "Needs Improvement", and "Missing Information"
- Fair scoring for freshers/students without work experience penalty
- Accuracy Rule: Never fabricate skills, projects, summary, or experience
- User control: provide, edit, or decline/skip missing sections
- Preserving authentic sections untouched
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
        self.assertIn("Upgrade passive verbs in experience to strong action verbs", res["high_level_areas"])

        # Section audits should distinguish already_correct vs needs_improvement
        correct_keys = [s["key"] for s in res["already_correct"]]
        self.assertIn("education", correct_keys)

        needs_imp_keys = [s["key"] for s in res["needs_improvement_sections"]]
        self.assertIn("experience", needs_imp_keys)
        self.assertIn("projects", needs_imp_keys)
        self.assertIn("skills", needs_imp_keys)

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
        """Test analyzer recognizes a strong, well-aligned resume without false improvement warnings."""
        sections = parse_resume_sections(self.well_aligned_text)
        analyzer = ResumeAnalyzer(
            job_role="Software Developer",
            company="Google",
            job_description=None
        )
        res = analyzer.analyze(self.well_aligned_text, sections)

        self.assertTrue(res["is_well_aligned"])
        self.assertGreaterEqual(res["role_alignment_score"], 80)
        self.assertEqual(len(res["unnecessary_details"]), 0)
        self.assertEqual(len(res["needs_improvement_sections"]), 0)
        self.assertTrue(len(res["already_correct"]) >= 4)

    def test_fresher_resume_without_work_experience(self):
        """Test that freshers/students with projects are not penalized for lacking work experience."""
        fresher_text = (
            "Rohan Sharma\n"
            "Software Developer | Bangalore, India | rohan.sharma@email.com | github.com/rohans\n\n"
            "EDUCATION\n"
            "Bachelor of Technology in Computer Science\n"
            "Indian Institute of Information Technology | 2024\n\n"
            "TECHNICAL PROJECTS\n"
            "Distributed Key-Value Store | Python, Docker, REST API\n"
            "• Engineered distributed replication system handling 10,000+ operations/sec.\n"
            "• Optimized latency and deployed live benchmark at github.com/rohans/kv-store.\n\n"
            "Cloud File Manager | Python, FastAPI, PostgreSQL, Redis\n"
            "• Developed secure multi-tenant storage system with JWT authentication.\n"
            "• Integrated unit testing achieving 92% code coverage.\n\n"
            "TECHNICAL SKILLS\n"
            "• Programming Languages: Python, C++, Java, SQL\n"
            "• Frameworks: FastAPI, Django\n"
            "• Databases & Tools: PostgreSQL, Redis, Docker, Git, REST API, Unit Testing\n"
        )
        sections = parse_resume_sections(fresher_text)
        analyzer = ResumeAnalyzer(
            job_role="Software Developer",
            company="Google",
            job_description=None
        )
        res = analyzer.analyze(fresher_text, sections)

        # Work experience should be marked as optional missing info
        missing_exp = [s for s in res["missing_info_sections"] if s["key"] == "experience"]
        self.assertEqual(len(missing_exp), 1)
        self.assertTrue(missing_exp[0]["is_optional"])

        # Projects and skills carry practical weight; alignment score should be solid (>= 80)
        self.assertGreaterEqual(res["role_alignment_score"], 80)

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

    def test_optimizer_never_fabricates_missing_sections(self):
        """Test that optimizer does NOT invent summary, projects, or experience when absent."""
        bare_resume = (
            "Alex Smith\n"
            "alex@email.com\n\n"
            "EDUCATION\n"
            "B.S. in Computer Science | MIT | 2024\n\n"
            "SKILLS\n"
            "Python, Java, Git, SQL\n"
        )
        sections = parse_resume_sections(bare_resume)
        analyzer = ResumeAnalyzer(job_role="Software Developer", company="Google")
        res = analyzer.analyze(bare_resume, sections)

        optimizer = ResumeOptimizer(job_role="Software Developer", company="Google")
        # When user provides no additional info and declines missing sections
        user_info = {"declined_sections": ["summary", "projects", "experience"]}
        improvements = optimizer.generate_improvements(sections, res, user_info)

        improved_keys = [imp["section_key"] for imp in improvements]
        # Should NOT fabricate summary, projects, or experience
        self.assertNotIn("summary", improved_keys)
        self.assertNotIn("projects", improved_keys)
        self.assertNotIn("experience", improved_keys)

    def test_optimizer_incorporates_user_provided_info(self):
        """Test that user-provided authentic details are incorporated without fabrication."""
        bare_resume = (
            "Alex Smith\n"
            "alex@email.com\n\n"
            "EDUCATION\n"
            "B.S. in Computer Science | MIT | 2024\n\n"
            "SKILLS\n"
            "Python, Java, Git, SQL\n"
        )
        sections = parse_resume_sections(bare_resume)
        analyzer = ResumeAnalyzer(job_role="Software Developer", company="Google")
        res = analyzer.analyze(bare_resume, sections)

        user_info = {
            "projects": {
                "name": "Distributed Cache",
                "description": "Implemented LRU memory cache with thread-safe locking.",
                "tools": "Python, Redis, Docker",
                "outcome": "Achieved sub-millisecond lookups."
            }
        }

        optimizer = ResumeOptimizer(job_role="Software Developer", company="Google")
        improvements = optimizer.generate_improvements(sections, res, user_info)

        proj_imp = next((imp for imp in improvements if imp["section_key"] == "projects"), None)
        self.assertIsNotNone(proj_imp)
        self.assertIn("Distributed Cache", proj_imp["after"])
        self.assertIn("Python, Redis, Docker", proj_imp["after"])
        self.assertIn("Achieved sub-millisecond lookups", proj_imp["after"])

    def test_preserve_correct_sections_untouched(self):
        """Test that already_correct sections are never modified by optimizer or final compilation."""
        sections = parse_resume_sections(self.well_aligned_text)
        analyzer = ResumeAnalyzer(job_role="Software Developer", company="Google")
        res = analyzer.analyze(self.well_aligned_text, sections)

        # In well_aligned_resume, everything is already correct
        self.assertEqual(len(res["needs_improvement_sections"]), 0)
        optimizer = ResumeOptimizer(job_role="Software Developer", company="Google")
        improvements = optimizer.generate_improvements(sections, res)

        # No improvements should be generated for already-correct sections
        self.assertEqual(len(improvements), 0)

        # Compiling final resume without changes preserves 100% of original sections
        final_text = ResumeOptimizer.compile_final_resume(sections, {})
        self.assertIn("Elena Rostova", final_text)
        self.assertIn("San Francisco, CA", final_text)
        self.assertIn("ScaleCloud Systems", final_text)
        self.assertIn("University of California, Berkeley", final_text)

    def test_user_declining_optional_section(self):
        """Test that candidate declining optional work experience results in clean resume without placeholders."""
        fresher_text = (
            "Aarav Patel\n"
            "Software Developer | aarav@email.com\n\n"
            "EDUCATION\n"
            "B.Tech in Computer Science | IIT Delhi | 2024\n\n"
            "TECHNICAL PROJECTS\n"
            "• Search Engine\n"
            "  Built inverted index in Python.\n\n"
            "TECHNICAL SKILLS\n"
            "• Languages: Python, C++\n"
        )
        sections = parse_resume_sections(fresher_text)
        analyzer = ResumeAnalyzer(job_role="Software Developer", company="Google")
        res = analyzer.analyze(fresher_text, sections)

        optimizer = ResumeOptimizer(job_role="Software Developer", company="Google")
        # Candidate explicitly declines work experience and summary
        user_info = {"declined_sections": ["experience", "summary"]}
        improvements = optimizer.generate_improvements(sections, res, user_info)

        imp_keys = [imp["section_key"] for imp in improvements]
        self.assertNotIn("experience", imp_keys)
        self.assertNotIn("summary", imp_keys)

        final_text = ResumeOptimizer.compile_final_resume(sections, {})
        self.assertNotIn("WORK EXPERIENCE", final_text)
        self.assertNotIn("PROFESSIONAL SUMMARY", final_text)
        self.assertIn("IIT Delhi", final_text)

    def test_exporter_pdf_and_docx(self):
        """Test export utilities output valid PDF and DOCX binary payloads."""
        pdf_bytes = export_resume_to_pdf(self.well_aligned_text, "Elena Rostova Resume")
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        docx_bytes = export_resume_to_docx(self.well_aligned_text)
        self.assertTrue(docx_bytes.startswith(b"PK"))  # DOCX is a zip archive

if __name__ == "__main__":
    unittest.main()

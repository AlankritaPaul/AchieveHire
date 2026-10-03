"""
End-to-end simulation of the complete user journey in AchieveHire Resume Guide.
"""

import os
import unittest
from modules.resume_guide.parser import extract_text_from_file, parse_resume_sections
from modules.resume_guide.analyzer import ResumeAnalyzer
from modules.resume_guide.optimizer import ResumeOptimizer
from modules.resume_guide.exporter import export_resume_to_pdf, export_resume_to_docx

class TestCompleteUserJourney(unittest.TestCase):
    def test_full_needs_improvement_journey(self):
        # 1. User selects/provides inputs
        job_role = "Backend Developer"
        company = "Startup (Growth / Series B+)"
        jd = "Looking for a Backend Developer proficient in Python, REST APIs, and Docker to scale cloud infrastructure."
        
        # 2. User uploads resume file
        sample_path = os.path.join("sample_resumes", "needs_improvement_resume.txt")
        with open(sample_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        sections = parse_resume_sections(raw_text)

        # 3. Resume Match Analysis
        analyzer = ResumeAnalyzer(job_role=job_role, company=company, job_description=jd)
        analysis = analyzer.analyze(raw_text, sections)

        self.assertFalse(analysis["is_well_aligned"])
        self.assertIsNotNone(analysis["jd_alignment_score"])
        self.assertTrue(len(analysis["high_level_areas"]) > 0)

        # 4. View Suggestions
        suggestions = analysis["suggestions"]
        self.assertTrue(len(suggestions) > 0)
        for s in suggestions:
            self.assertTrue(bool(s["observation"]))
            self.assertTrue(bool(s["recommendation"]))

        # 5. Improve Resume
        optimizer = ResumeOptimizer(job_role=job_role, company=company, job_description=jd)
        improvements = optimizer.generate_improvements(sections, analysis)
        self.assertTrue(len(improvements) > 0)

        # 6. User decision simulation (Accept, Edit, Keep Original)
        user_decisions = {}
        for imp in improvements:
            sec_key = imp["section_key"]
            if sec_key == "summary":
                user_decisions[sec_key] = {"decision": "accept", "improved": imp["after"]}
            elif sec_key == "experience":
                user_decisions[sec_key] = {
                    "decision": "edit",
                    "edited": imp["after"] + "\n• Spearheaded cross-team collaboration."
                }
            else:
                user_decisions[sec_key] = {"decision": "keep_original", "original": imp["before"]}

        # 7. Final Updated Resume Compilation
        final_resume = ResumeOptimizer.compile_final_resume(sections, user_decisions)
        self.assertTrue(len(final_resume) > 100)
        self.assertIn("PROFESSIONAL SUMMARY", final_resume)
        self.assertIn("Spearheaded cross-team collaboration", final_resume)

        # 8. Download Exports
        pdf = export_resume_to_pdf(final_resume, "Updated Backend Developer Resume")
        docx = export_resume_to_docx(final_resume)
        self.assertGreater(len(pdf), 500)
        self.assertGreater(len(docx), 500)

    def test_full_well_aligned_journey(self):
        job_role = "Software Developer"
        company = "Google"
        jd = None  # No JD provided

        sample_path = os.path.join("sample_resumes", "well_aligned_resume.txt")
        with open(sample_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        sections = parse_resume_sections(raw_text)

        analyzer = ResumeAnalyzer(job_role=job_role, company=company, job_description=jd)
        analysis = analyzer.analyze(raw_text, sections)

        # Verify no JD claims
        self.assertIsNone(analysis["jd_alignment_score"])
        self.assertFalse(analysis["has_jd"])

        # Verify well-aligned determination
        self.assertTrue(analysis["is_well_aligned"])
        self.assertEqual(len(analysis["unnecessary_details"]), 0)

if __name__ == "__main__":
    unittest.main()

"""
Unit tests for Resume Builder and template rendering.
"""

import unittest
from modules.resume_guide.builder import ResumeBuilderModel, DEFAULT_DECLARATION
from modules.resume_guide.builder_templates import (
    TEMPLATES_INFO,
    render_resume_html,
    export_builder_resume_to_pdf
)
from modules.resume_guide.exporter import export_resume_to_docx

class TestResumeBuilder(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "job_role": "Data Analyst",
            "company": "Google",
            "job_description": "Proficiency in SQL, Python, Tableau, and data modeling required.",
            "full_name": "Maya Lin",
            "email": "maya.lin@email.com",
            "phone": "+1-555-0123",
            "location": "Seattle, WA",
            "education": "B.S. in Statistics | University of Washington | 2023",
            "skills": "SQL, Python, Tableau, Excel, Data Visualization",
            "experience": "Junior Analyst | DataInsights Co. | Jun 2023 - Present\n• Worked on customer churn dashboards in Tableau.\n• Handled SQL query optimization for sales reporting.",
            "projects": "Healthcare Analytics Model\n• Built predictive analytics pipeline using Python and Pandas.",
            "certifications": "Google Data Analytics Professional Certificate",
            "custom_sections": [
                {"title": "Leadership & Volunteering", "content": "Led analytics workshop for 40+ university students."}
            ],
            "declaration": DEFAULT_DECLARATION,
            "date_val": "2026-10-15",
            "sig_val": "Maya Lin",
            "template_name": "Modern"
        }

    def test_builder_accuracy_rule_and_tailoring(self):
        """Test builder polishes passive verbs without inventing facts."""
        tailored = ResumeBuilderModel.tailor_content(self.sample_data)

        # Factual check
        self.assertIn("Maya Lin", tailored["full_name"])
        self.assertIn("University of Washington", tailored["education"])
        self.assertIn("DataInsights Co.", tailored["experience"])

        # Verb enhancement
        self.assertNotIn("Worked on", tailored["experience"])
        self.assertIn("Architected", tailored["experience"])

        # Summary generation without fake info
        self.assertIn("Data Analyst", tailored["summary"])
        self.assertIn("Google", tailored["summary"])

    def test_templates_exist_and_render_html(self):
        """Test all 6 required templates render HTML properly."""
        expected_templates = ["Classic", "Modern", "Minimal", "Professional", "Creative", "Technical"]
        for tpl in expected_templates:
            self.assertIn(tpl, TEMPLATES_INFO)
            html = render_resume_html(self.sample_data, template_name=tpl)
            self.assertIn("MAYA LIN" if tpl == "Classic" else "Maya Lin", html)
            self.assertIn("DECLARATION", html)
            self.assertIn("Date:", html)
            self.assertIn("Signature:", html)
            self.assertIn("Leadership &amp; Volunteering" if "&amp;" in html else "LEADERSHIP & VOLUNTEERING", html)

    def test_export_builder_pdf_and_docx(self):
        """Test PDF and DOCX export from builder data."""
        pdf_bytes = export_builder_resume_to_pdf(self.sample_data, "Professional")
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        plain_text = ResumeBuilderModel.to_plain_text(self.sample_data)
        docx_bytes = export_resume_to_docx(plain_text)
        self.assertTrue(docx_bytes.startswith(b"PK"))

if __name__ == "__main__":
    unittest.main()

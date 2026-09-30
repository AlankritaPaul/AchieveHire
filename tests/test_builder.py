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
            self.assertIn("Signature", html)
            self.assertIn("Leadership &amp; Volunteering" if "&amp;" in html else "LEADERSHIP & VOLUNTEERING", html)

    def test_export_builder_pdf_and_docx(self):
        """Test PDF and DOCX export from builder data."""
        pdf_bytes = export_builder_resume_to_pdf(self.sample_data, "Professional")
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        plain_text = ResumeBuilderModel.to_plain_text(self.sample_data)
        docx_bytes = export_resume_to_docx(plain_text)
        self.assertTrue(docx_bytes.startswith(b"PK"))

    def test_enhance_qualifications(self):
        """Test professional keyword enhancement preserves facts while standardizing terms."""
        raw_edu = "btech in cse from IIT Delhi 2020-2024 with 8.9 cgpa\n12th CBSE from DPS RK Puram 2020 with 94 percentage"
        enhanced = ResumeBuilderModel.enhance_qualifications(raw_edu)

        # Preserves user's actual facts
        self.assertIn("IIT Delhi", enhanced)
        self.assertIn("2020-2024", enhanced)
        self.assertIn("DPS RK Puram", enhanced)

        # Standardizes professional keywords
        self.assertIn("B.Tech (Bachelor of Technology)", enhanced)
        self.assertIn("Computer Science & Engineering", enhanced)
        self.assertIn("Higher Secondary Certificate (Class XII)", enhanced)
        self.assertIn("CGPA: 8.9", enhanced)
        self.assertIn("Score: 94%", enhanced)

    def test_passport_photo_space_and_upload(self):
        """Test passport photo space and digital upload in HTML and PDF."""
        # Box mode
        box_data = dict(self.sample_data)
        box_data["photo_mode"] = "box"
        html_box = render_resume_html(box_data, template_name="Modern")
        self.assertIn("Affix Passport Size Photo", html_box)
        pdf_box = export_builder_resume_to_pdf(box_data, "Modern")
        self.assertTrue(pdf_box.startswith(b"%PDF"))

        # Upload mode
        dummy_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        upload_data = dict(self.sample_data)
        upload_data["photo_mode"] = "upload"
        upload_data["photo_b64"] = dummy_b64
        html_upload = render_resume_html(upload_data, template_name="Modern", photo_b64=dummy_b64)
        self.assertIn("data:image/jpeg;base64,", html_upload)
        pdf_upload = export_builder_resume_to_pdf(upload_data, "Modern")
        self.assertTrue(pdf_upload.startswith(b"%PDF"))

    def test_signature_options(self):
        """Test write signature, upload signature, and blank line in HTML and PDF."""
        # Write mode
        write_data = dict(self.sample_data)
        write_data["signature_mode"] = "write"
        write_data["sig_val"] = "Maya Lin Signature"
        html_write = render_resume_html(write_data, template_name="Modern")
        self.assertIn("Maya Lin Signature", html_write)

        # Upload mode
        dummy_sig_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        sig_upload_data = dict(self.sample_data)
        sig_upload_data["signature_mode"] = "upload"
        sig_upload_data["signature_img_b64"] = dummy_sig_b64
        html_sig_upload = render_resume_html(sig_upload_data, template_name="Modern")
        self.assertIn("data:image/png;base64,", html_sig_upload)
        pdf_sig = export_builder_resume_to_pdf(sig_upload_data, "Modern")
        self.assertTrue(pdf_sig.startswith(b"%PDF"))

        # Blank mode
        blank_data = dict(self.sample_data)
        blank_data["signature_mode"] = "blank"
        html_blank = render_resume_html(blank_data, template_name="Modern")
        self.assertIn("Signature: ____________________", html_blank)
        pdf_blank = export_builder_resume_to_pdf(blank_data, "Modern")
        self.assertTrue(pdf_blank.startswith(b"%PDF"))

if __name__ == "__main__":
    unittest.main()

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

    def test_structured_education_and_compilation(self):
        """Test realistic multi-qualification structured education entries and compilation."""
        entries = [
            {
                "level": "college",
                "degree": "btech",
                "stream": "cse",
                "institution": "Delhi Technological University",
                "board_univ": "DTU",
                "year": "2020 - 2024",
                "grade": "8.6 cgpa"
            },
            {
                "level": "12th",
                "degree": "12th pass",
                "stream": "pcm",
                "institution": "Delhi Public School",
                "board_univ": "cbse",
                "year": "2020",
                "grade": "92.4 percentage"
            },
            {
                "level": "10th",
                "degree": "10th",
                "stream": "",
                "institution": "Delhi Public School",
                "board_univ": "cbse",
                "year": "2018",
                "grade": "94.6%"
            }
        ]

        enhanced = ResumeBuilderModel.enhance_education_entries(entries)
        # Degree and stream enhancements
        self.assertIn("B.Tech (Bachelor of Technology)", enhanced[0]["degree"])
        self.assertIn("Computer Science & Engineering", enhanced[0]["stream"])
        self.assertIn("CGPA: 8.6", enhanced[0]["grade"])

        self.assertIn("Higher Secondary Certificate (Class XII)", enhanced[1]["degree"])
        self.assertIn("Science (Physics, Chemistry, Maths)", enhanced[1]["stream"])
        self.assertIn("CBSE Board", enhanced[1]["board_univ"])
        self.assertIn("Score: 92.4%", enhanced[1]["grade"])

        compiled = ResumeBuilderModel.compile_education_entries(enhanced)
        self.assertIn("• B.Tech (Bachelor of Technology) in Computer Science & Engineering", compiled)
        self.assertIn("Delhi Technological University | DTU | 2020 - 2024 | CGPA: 8.6", compiled)
        self.assertIn("• Higher Secondary Certificate (Class XII) in Science (Physics, Chemistry, Maths)", compiled)
        self.assertIn("Delhi Public School | CBSE Board | 2020 | Score: 92.4%", compiled)
        self.assertIn("• Secondary School Certificate (Class X)", compiled)

    def test_enhance_skills_grouping(self):
        """Test skill enhancement groups into industry categories and normalizes keywords."""
        raw_skills = "python, reactjs, nodejs, postgresql, git, aws, dsa, problem solving"
        enhanced = ResumeBuilderModel.enhance_skills(raw_skills)

        self.assertIn("Programming Languages: Python", enhanced)
        self.assertIn("Frameworks & Libraries: React.js, Node.js", enhanced)
        self.assertIn("Databases: PostgreSQL", enhanced)
        self.assertIn("Tools & Cloud Technologies: Git, AWS (Amazon Web Services)", enhanced)
        self.assertIn("Core Competencies & Methodologies: Data Structures & Algorithms, Problem Solving", enhanced)

    def test_enhance_experience_and_projects(self):
        """Test experience and project text enhancement upgrades action verbs and technical phrasing."""
        raw_exp = "worked on user management module\nhelped in query optimization"
        enh_exp = ResumeBuilderModel.enhance_experience(raw_exp)
        self.assertNotIn("worked on", enh_exp.lower())
        self.assertIn("Architected", enh_exp)
        self.assertIn("Engineered", enh_exp)

        raw_proj = "Inventory System\nmade a website for warehouse tracking\nused python for backend"
        enh_proj = ResumeBuilderModel.enhance_projects(raw_proj)
        self.assertNotIn("made a website", enh_proj)
        self.assertIn("Architected and developed a responsive web application", enh_proj)
        self.assertIn("Leveraged Python to implement backend logic", enh_proj)

    def test_education_and_qualifications_section_redesign(self):
        """Test Education and Qualifications subsection rules, dynamic dates, and optional fields."""
        edu_entries = [
            {
                "degree": "btech",
                "field_of_study": "cse",
                "institution": "Stanford University",
                "board_univ": "",  # Optional, omitted
                "location": "Stanford, CA",
                "status": "Currently Pursuing",
                "start_year": "2023",
                "end_year": "",
                "expected_grad_year": "2027",
                "cgpa": "3.92",
                "percentage": "",
                "grade": ""
            },
            {
                "degree": "12th pass",
                "field_of_study": "pcm",
                "institution": "Lincoln High School",
                "board_univ": "State Board",
                "location": "San Jose, CA",
                "status": "Completed",
                "start_year": "2021",
                "end_year": "2023",
                "expected_grad_year": "",
                "cgpa": "",
                "percentage": "95%",
                "grade": "A+"
            }
        ]

        qual_entries = [
            {
                "title": "AWS Certified Solutions Architect",
                "organization": "Amazon Web Services",
                "year": "2024",
                "details": "Validation ID: AWS-12345"
            }
        ]

        # 1. Test enhance
        enhanced_edu = ResumeBuilderModel.enhance_education_entries(edu_entries)
        enhanced_qual = ResumeBuilderModel.enhance_qualification_entries(qual_entries)

        self.assertIn("B.Tech (Bachelor of Technology)", enhanced_edu[0]["degree"])
        self.assertIn("Computer Science & Engineering", enhanced_edu[0]["field_of_study"])
        self.assertEqual(enhanced_edu[0]["cgpa"], "3.92")

        self.assertIn("Higher Secondary Certificate (Class XII)", enhanced_edu[1]["degree"])
        self.assertIn("Science (Physics, Chemistry, Maths)", enhanced_edu[1]["field_of_study"])
        self.assertEqual(enhanced_edu[1]["percentage"], "95%")

        # 2. Test compilation with both subsections
        compiled = ResumeBuilderModel.compile_education_and_qualifications(enhanced_edu, enhanced_qual)

        # Main headings / Subsections check
        self.assertIn("Education\n", compiled)
        self.assertIn("Qualifications\n", compiled)

        # No internal labels
        self.assertNotIn("Education 1", compiled)
        self.assertNotIn("Education 2", compiled)
        self.assertNotIn("Qualification 1", compiled)

        # Independent status date check
        # Entry 0 (Currently Pursuing): start year + expected grad year
        self.assertIn("2023 - Present (Expected: 2027)", compiled)
        # Entry 1 (Completed): start year + end year
        self.assertIn("2021 - 2023", compiled)

        # Optional board: Stanford has no board_univ, so board shouldn't appear
        self.assertIn("Stanford University | Stanford, CA | 2023 - Present (Expected: 2027) | CGPA: 3.92", compiled)

        # Entry 1 academic results: Percentage and Grade
        self.assertIn("Percentage: 95%", compiled)
        self.assertIn("Grade: A+", compiled)

        # Qualifications subsection content
        self.assertIn("• AWS Certified Solutions Architect", compiled)
        self.assertIn("Amazon Web Services | 2024 | Validation ID: AWS-12345", compiled)

        # 3. Test compilation without Qualifications (optional subsection omitted cleanly)
        compiled_no_qual = ResumeBuilderModel.compile_education_and_qualifications(enhanced_edu, [])
        self.assertIn("Education\n", compiled_no_qual)
        self.assertNotIn("Qualifications", compiled_no_qual)

        # 4. Test Plain text, HTML and PDF templates title check
        test_data = dict(self.sample_data)
        test_data["education"] = compiled
        plain = ResumeBuilderModel.to_plain_text(test_data)
        self.assertIn("EDUCATION AND QUALIFICATIONS", plain)

        html = render_resume_html(test_data, "Modern")
        self.assertIn("EDUCATION AND QUALIFICATIONS", html)

        pdf = export_builder_resume_to_pdf(test_data, "Modern")
        self.assertTrue(pdf.startswith(b"%PDF"))

    def test_work_experience_section_redesign(self):
        """Test Work Experience structured entries, suggested & custom types, dynamic dates, and optionality."""
        exp_entries = [
            {
                "experience_type": "Internship",
                "custom_experience_type": "",
                "company": "Google",
                "position": "software engineering intern",
                "location": "Mountain View, CA",
                "status": "Currently Ongoing",
                "start_date": "Jun 2024",
                "end_date": "",
                "description": "contributed to cloud infrastructure logging pipeline",
                "responsibilities": "worked on microservices handling 10M requests\nhelped in reducing query latency by 20%"
            },
            {
                "experience_type": "Write Your Own",
                "custom_experience_type": "Graduate Research Fellow",
                "company": "MIT CSAIL",
                "position": "Research Assistant",
                "location": "Cambridge, MA",
                "status": "Completed",
                "start_date": "Sep 2022",
                "end_date": "May 2024",
                "description": "Conducted research on distributed systems fault tolerance.",
                "responsibilities": "Architected simulation framework.\nPublished findings at academic symposium."
            }
        ]

        # 1. Test enhance
        enhanced_exp = ResumeBuilderModel.enhance_experience_entries(exp_entries)
        # Check custom type preserved exactly as entered by user
        self.assertEqual(enhanced_exp[1]["custom_experience_type"], "Graduate Research Fellow")
        # Check position capitalized
        self.assertEqual(enhanced_exp[0]["position"], "Software engineering intern")
        # Check weak verbs enhanced
        self.assertIn("Spearheaded", enhanced_exp[0]["description"])
        self.assertIn("Architected", enhanced_exp[0]["responsibilities"])
        self.assertIn("Engineered", enhanced_exp[0]["responsibilities"])

        # 2. Test compilation
        compiled = ResumeBuilderModel.compile_experience_entries(enhanced_exp)

        # Title line checks (including custom type)
        self.assertIn("• Software engineering intern (Internship)", compiled)
        self.assertIn("• Research Assistant (Graduate Research Fellow)", compiled)

        # Metadata line checks
        self.assertIn("Google | Mountain View, CA | Jun 2024 - Present", compiled)
        self.assertIn("MIT CSAIL | Cambridge, MA | Sep 2022 - May 2024", compiled)

        # No internal labels
        self.assertNotIn("Experience 1", compiled)
        self.assertNotIn("Experience 2", compiled)

        # Description and bullet points
        self.assertIn("Spearheaded cloud infrastructure logging pipeline", compiled)
        self.assertIn("- Architected microservices handling 10M requests", compiled)

        # 3. Test optionality: empty entries list produces empty string
        compiled_empty = ResumeBuilderModel.compile_experience_entries([])
        self.assertEqual(compiled_empty, "")

        # 4. Verify templates render "WORK EXPERIENCE" title
        test_data = dict(self.sample_data)
        test_data["experience"] = compiled
        html = render_resume_html(test_data, "Modern")
        self.assertIn("WORK EXPERIENCE", html)

        pdf = export_builder_resume_to_pdf(test_data, "Modern")
        self.assertTrue(pdf.startswith(b"%PDF"))

if __name__ == "__main__":
    unittest.main()

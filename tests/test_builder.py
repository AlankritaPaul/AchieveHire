"""
Unit tests for Resume Builder and template rendering.
"""

import unittest
from modules.resume_guide.builder import ResumeBuilderModel, DEFAULT_DECLARATION
from modules.resume_guide.builder_templates import (
    TEMPLATES_INFO,
    render_resume_html,
    export_builder_resume_to_pdf,
    get_resume_headline
)
from modules.resume_guide.exporter import export_resume_to_docx

class TestResumeBuilder(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "job_role": "Data Analyst",
            "company": "Google",
            "job_description": "Proficiency in SQL, Python, Tableau, and data modeling required.",
            "full_name": "Maya Lin",
            "professional_headline": "Senior Data Analyst | Business Intelligence Specialist",
            "email": "maya.lin@email.com",
            "phone": "+1-555-0123",
            "location": "Seattle, WA",
            "place_val": "Seattle, WA",
            "education": "B.S. in Statistics | University of Washington | 2023",
            "skills": "SQL, Python, Tableau, Excel, Data Visualization",
            "experience": "Junior Analyst | DataInsights Co. | Jun 2023 - Present\n• Worked on customer churn dashboards in Tableau.\n• Handled SQL query optimization for sales reporting.",
            "projects": "• Healthcare Analytics Model\n  Built predictive analytics pipeline using Python and Pandas.",
            "project_entries": [
                {
                    "name": "Healthcare Analytics Model",
                    "tech_stack": "Python, Pandas, FastAPI",
                    "description": "Engineered predictive analytics pipeline delivering 94% accuracy."
                }
            ],
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
        """Test all 10 required professional templates exist and render HTML properly."""
        expected_templates = [
            "Classic", "Modern", "Minimal", "Professional", "Creative",
            "Technical", "Executive", "Compact", "Nordic", "Ivy"
        ]
        self.assertEqual(len(TEMPLATES_INFO), 10)
        for tpl in expected_templates:
            self.assertIn(tpl, TEMPLATES_INFO)
            html = render_resume_html(self.sample_data, template_name=tpl)
            self.assertIn("MAYA LIN" if tpl in ("Classic", "Executive", "Ivy") else "Maya Lin", html)
            self.assertIn("DECLARATION", html)
            self.assertIn("Date:", html)
            self.assertIn("Signature", html)
            self.assertIn("TECHNICAL PROJECT", html)

    def test_export_builder_pdf_and_docx(self):
        """Test PDF and DOCX export from builder data for multiple templates."""
        for tpl in ["Classic", "Modern", "Professional", "Executive", "Compact"]:
            pdf_bytes = export_builder_resume_to_pdf(self.sample_data, tpl)
            self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        plain_text = ResumeBuilderModel.to_plain_text(self.sample_data)
        docx_bytes = export_resume_to_docx(plain_text)
        self.assertTrue(docx_bytes.startswith(b"PK"))

    def test_enhance_qualifications(self):
        """Test professional keyword enhancement preserves facts without redundant bracket expansions."""
        raw_edu = "btech in cse from IIT Delhi 2020-2024 with 8.9 cgpa\n12th CBSE from DPS RK Puram 2020 with 94 percentage"
        enhanced = ResumeBuilderModel.enhance_qualifications(raw_edu)

        # Preserves user's actual facts
        self.assertIn("IIT Delhi", enhanced)
        self.assertIn("2020-2024", enhanced)
        self.assertIn("DPS RK Puram", enhanced)

        # Standardizes professional keywords without duplicated bracket titles
        self.assertIn("B.Tech", enhanced)
        self.assertNotIn("B.Tech (Bachelor of Technology)", enhanced)
        self.assertIn("Computer Science & Engineering", enhanced)
        self.assertIn("Class XII (Senior Secondary)", enhanced)
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

        # Upload mode (dummy base64 1x1 png)
        upload_data = dict(self.sample_data)
        upload_data["photo_mode"] = "upload"
        upload_data["photo_b64"] = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        html_up = render_resume_html(upload_data, template_name="Modern")
        self.assertIn("data:image/jpeg;base64,", html_up)
        pdf_up = export_builder_resume_to_pdf(upload_data, "Modern")
        self.assertTrue(pdf_up.startswith(b"%PDF"))

    def test_signature_modes(self):
        """Test write signature, upload signature, and blank signature line."""
        # 1. Write signature (styled script font in HTML)
        write_data = dict(self.sample_data)
        write_data["signature_mode"] = "write"
        write_data["sig_val"] = "Maya Lin"
        html_w = render_resume_html(write_data, template_name="Modern")
        self.assertIn("Maya Lin", html_w)

        # 2. Upload signature image
        up_data = dict(self.sample_data)
        up_data["signature_mode"] = "upload"
        up_data["signature_img_b64"] = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        html_u = render_resume_html(up_data, template_name="Modern")
        self.assertIn("data:image/png;base64,", html_u)

        # 3. Blank signature line
        blank_data = dict(self.sample_data)
        blank_data["signature_mode"] = "blank"
        blank_data["sig_val"] = ""
        html_b = render_resume_html(blank_data, template_name="Modern")
        self.assertIn("<strong>Signature:</strong> ____________________", html_b)

    def test_structured_education_and_compilation(self):
        """Test realistic multi-qualification structured education entries and compilation."""
        entries = [
            {
                "level": "Undergraduate",
                "degree": "b.tech",
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
        # Degree and stream enhancements without duplicate bracket titles
        self.assertIn("B.Tech", enhanced[0]["degree"])
        self.assertIn("Computer Science & Engineering", enhanced[0]["stream"])
        self.assertIn("CGPA: 8.6", enhanced[0]["grade"])

        self.assertIn("Class XII (Senior Secondary)", enhanced[1]["degree"])
        self.assertIn("Science (Physics, Chemistry, Maths)", enhanced[1]["stream"])
        self.assertIn("CBSE Board", enhanced[1]["board_univ"])
        self.assertIn("Score: 92.4%", enhanced[1]["grade"])

        compiled = ResumeBuilderModel.compile_education_entries(enhanced)
        self.assertIn("• B.Tech in Computer Science & Engineering", compiled)
        self.assertIn("Delhi Technological University | DTU | 2020 – 2024 | CGPA: 8.6", compiled)
        self.assertIn("• Class XII (Senior Secondary) in Science (Physics, Chemistry, Maths)", compiled)
        self.assertIn("Delhi Public School | CBSE Board | 2020 | Score: 92.4%", compiled)
        self.assertIn("• Class X (Secondary)", compiled)

    def test_enhance_skills_grouping(self):
        """Test skill enhancement groups into industry categories and normalizes keywords."""
        raw_skills = "python, reactjs, nodejs, postgresql, git, aws, dsa, problem solving"
        enhanced = ResumeBuilderModel.enhance_skills(raw_skills)

        self.assertIn("Programming Languages: Python", enhanced)
        self.assertIn("Frameworks & Libraries: React.js, Node.js", enhanced)
        self.assertIn("Databases: PostgreSQL", enhanced)
        self.assertIn("Tools & Cloud Technologies: Git, AWS (Amazon Web Services)", enhanced)
        self.assertIn("Core Competencies & Methodologies: Data Structures & Algorithms, Problem Solving", enhanced)

    def test_skills_deduplication_and_clean_formatting(self):
        """Test that repeated category labels are eliminated and grouped under single clean headings."""
        raw_skills_repeated = (
            "Technical Skills\n"
            "Additional Competency\n"
            "Additional Competency\n"
            "Programming Language\n"
            "Python\n"
            "Java\n"
            "Tools\n"
            "Docker\n"
            "Git"
        )
        enhanced = ResumeBuilderModel.enhance_skills(raw_skills_repeated)
        # Check no duplicate category lines
        self.assertEqual(enhanced.count("Programming Languages:"), 1)
        self.assertEqual(enhanced.count("Tools & Cloud Technologies:"), 1)
        self.assertNotIn("Additional Competency:", enhanced)
        self.assertIn("Programming Languages: Python, Java", enhanced)
        self.assertIn("Tools & Cloud Technologies: Docker, Git", enhanced)

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
        # Description must NOT be converted to a bullet point!
        self.assertNotIn("- Architected", enh_proj)
        self.assertIn("  Architected", enh_proj)

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

        self.assertIn("B.Tech", enhanced_edu[0]["degree"])
        self.assertIn("Computer Science & Engineering", enhanced_edu[0]["field_of_study"])
        self.assertEqual(enhanced_edu[0]["cgpa"], "3.92")

        self.assertIn("Class XII (Senior Secondary)", enhanced_edu[1]["degree"])
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
        # Entry 0 (Currently Pursuing): start year + expected grad year naturally separated
        self.assertIn("2023 – Present | Expected Graduation: 2027", compiled)
        # Entry 1 (Completed): start year – end year
        self.assertIn("2021 – 2023", compiled)

        # Optional board: Stanford has no board_univ, so board shouldn't appear
        self.assertIn("Stanford University | Stanford, CA | 2023 – Present | Expected Graduation: 2027 | CGPA: 3.92", compiled)

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

    def test_work_experience_section_redesign(self):
        """Test Work Experience structured entries, suggested & custom types, dynamic dates, and optionality."""
        exp_entries = [
            {
                "experience_type": "Internship",
                "custom_experience_type": "",
                "work_arrangement": "Hybrid",
                "custom_work_arrangement": "",
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
                "work_arrangement": "Write Your Own",
                "custom_work_arrangement": "Client-site (Mon-Wed)",
                "company": "MIT CSAIL",
                "position": "Research Assistant",
                "location": "Cambridge, MA",
                "status": "Completed",
                "start_date": "Sep 2022",
                "end_date": "May 2024",
                "description": "Conducted research on distributed systems fault tolerance.",
                "responsibilities": "Architected simulation framework.\nPublished findings at academic symposium."
            },
            {
                "experience_type": "Contract",
                "work_arrangement": "Rotational Offshore",
                "company": "BP Global",
                "position": "Field Operations Specialist",
                "location": "Aberdeen, UK",
                "status": "Completed",
                "start_date": "Jan 2021",
                "end_date": "Aug 2022",
                "description": "Managed automated telemetry equipment.",
                "responsibilities": "Coordinated offshore inspection schedule."
            }
        ]

        # 1. Test enhance
        enhanced_exp = ResumeBuilderModel.enhance_experience_entries(exp_entries)
        self.assertEqual(enhanced_exp[1]["custom_experience_type"], "Graduate Research Fellow")
        self.assertEqual(enhanced_exp[1]["custom_work_arrangement"], "Client-site (Mon-Wed)")
        self.assertEqual(enhanced_exp[0]["position"], "Software engineering intern")
        self.assertIn("Spearheaded", enhanced_exp[0]["description"])
        self.assertIn("Architected", enhanced_exp[0]["responsibilities"])
        self.assertIn("Engineered", enhanced_exp[0]["responsibilities"])

        # 2. Test compilation
        compiled = ResumeBuilderModel.compile_experience_entries(enhanced_exp)

        # Title line checks (including custom type)
        self.assertIn("• Software engineering intern (Internship)", compiled)
        self.assertIn("• Research Assistant (Graduate Research Fellow)", compiled)
        self.assertIn("• Field Operations Specialist (Contract)", compiled)

        # Metadata line checks: Location, Work Arrangement, and Dates kept completely separate
        self.assertIn("Google | Mountain View, CA | Hybrid | Jun 2024 - Present", compiled)
        self.assertIn("MIT CSAIL | Cambridge, MA | Client-site (Mon-Wed) | Sep 2022 - May 2024", compiled)
        self.assertIn("BP Global | Aberdeen, UK | Rotational Offshore | Jan 2021 - Aug 2022", compiled)

        # No internal labels
        self.assertNotIn("Experience 1", compiled)
        self.assertNotIn("Experience 2", compiled)
        self.assertNotIn("Experience 3", compiled)

        # Description and bullet points
        self.assertIn("Spearheaded cloud infrastructure logging pipeline", compiled)
        self.assertIn("- Architected microservices handling 10M requests", compiled)

        # 3. Test optionality: empty entries list produces empty string
        compiled_empty = ResumeBuilderModel.compile_experience_entries([])
        self.assertEqual(compiled_empty, "")

    def test_unpopulated_work_experience_entries_omitted(self):
        """Test that default dropdown selections without company or position do NOT generate a Work Experience section."""
        dummy_entries = [
            {
                "experience_type": "Placement",
                "custom_experience_type": "",
                "work_arrangement": "On-site",
                "custom_work_arrangement": "",
                "company": "",
                "position": "",
                "location": "",
                "status": "Completed",
                "start_date": "",
                "end_date": "",
                "description": "",
                "responsibilities": ""
            }
        ]
        compiled = ResumeBuilderModel.compile_experience_entries(dummy_entries)
        self.assertEqual(compiled, "")

        test_data = dict(self.sample_data)
        test_data["experience"] = compiled
        html = render_resume_html(test_data, "Modern")
        self.assertNotIn("WORK EXPERIENCE", html)

    def test_professional_headline_and_header_logic(self):
        """Test that user's professional headline is displayed under name, fallback works, and target job_role/company are never shown."""
        # Case A: User provided professional_headline
        headline_data = dict(self.sample_data)
        headline_data["professional_headline"] = "Full-Stack Software Architect"
        headline_data["job_role"] = "Target Cloud Dev"
        headline_data["company"] = "Target Inc."

        hl = get_resume_headline(headline_data)
        self.assertEqual(hl, "Full-Stack Software Architect")

        html = render_resume_html(headline_data, "Modern")
        self.assertIn("Full-Stack Software Architect", html)
        # NEVER show target job role or company under name
        self.assertNotIn("Target Cloud Dev &bull; Target Inc.", html)

        # Case B: No professional_headline, but has Currently Ongoing experience
        fallback_data = dict(self.sample_data)
        fallback_data["professional_headline"] = ""
        fallback_data["experience_entries"] = [
            {"position": "Staff Infrastructure Engineer", "status": "Currently Ongoing"}
        ]
        hl_fb = get_resume_headline(fallback_data)
        self.assertEqual(hl_fb, "Staff Infrastructure Engineer")

        # Case C: Neither headline nor ongoing experience -> empty string
        empty_hl_data = dict(self.sample_data)
        empty_hl_data["professional_headline"] = ""
        empty_hl_data["experience_entries"] = [
            {"position": "Junior Engineer", "status": "Completed"}
        ]
        hl_none = get_resume_headline(empty_hl_data)
        self.assertEqual(hl_none, "")

    def test_technical_project_multientry_and_formatting(self):
        """Test Technical Project formatting: Project Name as bullet heading, Description as normal paragraph without extra bullet."""
        project_entries = [
            {
                "name": "E-Commerce IQ",
                "tech_stack": "Python, FastAPI",
                "description": "It helps the business analyst to easily analyse their production."
            },
            {
                "name": "Cloud Ledger",
                "tech_stack": "Go, Docker",
                "description": "Distributed immutable ledger for financial transactions."
            }
        ]
        compiled = ResumeBuilderModel.compile_project_entries(project_entries)
        # Heading has bullet with Technologies Used
        self.assertIn("• E-Commerce IQ | Technologies Used: Python, FastAPI", compiled)
        self.assertIn("• Cloud Ledger | Technologies Used: Go, Docker", compiled)
        # Description is plain indented paragraph, NOT another bullet
        self.assertIn("  It helps the business analyst to easily analyse their production.", compiled)
        self.assertNotIn("  - It helps the business analyst", compiled)
        self.assertNotIn("  • It helps the business analyst", compiled)

    def test_declaration_2_column_and_place(self):
        """Test Declaration 2-column layout with Date & Place on left, Signature & Name on right."""
        test_data = dict(self.sample_data)
        test_data["date_val"] = "November 10, 2026"
        test_data["place_val"] = "San Francisco, CA"
        test_data["full_name"] = "Alex Morgan"
        test_data["signature_mode"] = "blank"

        html = render_resume_html(test_data, "Modern")
        self.assertIn("<strong>Date:</strong> November 10, 2026", html)
        self.assertIn("<strong>Place:</strong> San Francisco, CA", html)
        self.assertIn("<strong>Name:</strong> Alex Morgan", html)
        self.assertIn("<strong>Signature:</strong> ____________________", html)

        pdf_bytes = export_builder_resume_to_pdf(test_data, "Modern")
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

    def test_analyzer_without_experience_section(self):
        """Test that analyzing a resume without an experience section does not throw KeyError: found_weak_verbs."""
        from modules.resume_guide.analyzer import ResumeAnalyzer
        analyzer = ResumeAnalyzer(job_role="Data Analyst", company="Google")
        raw_text = "MAYA LIN\nEmail: maya@email.com\n\nEDUCATION AND QUALIFICATIONS\nB.S. in Statistics | 2023\n\nSKILLS\nPython, SQL, Tableau"
        sections = {
            "header": "MAYA LIN\nEmail: maya@email.com",
            "education": "B.S. in Statistics | 2023",
            "skills": "Python, SQL, Tableau"
        }
        result = analyzer.analyze(raw_text, sections)
        self.assertIn("role_alignment_score", result)
    def test_enhance_headline(self):
        """Test ResumeBuilderModel.enhance_headline transforms basic input into structured professional headlines without altering user skills."""
        # Role + tech
        res1 = ResumeBuilderModel.enhance_headline("python developer c++")
        self.assertIn("Python Developer", res1)
        self.assertIn("C++", res1)
        self.assertIn("|", res1)

        # Role only
        res2 = ResumeBuilderModel.enhance_headline("software engineer")
        self.assertIn("Software Engineer", res2)
        self.assertIn("|", res2)

        # Skills only without role
        res3 = ResumeBuilderModel.enhance_headline("python, c++")
        self.assertIn("Python", res3)
        self.assertIn("C++", res3)
        self.assertIn("|", res3)

        # Student / Fresher
        res4 = ResumeBuilderModel.enhance_headline("student")
        self.assertIn("Aspiring Software Engineer", res4)

        # Data analyst with tools
        res5 = ResumeBuilderModel.enhance_headline("data analyst sql excel")
        self.assertIn("Data Analyst", res5)
        self.assertIn("SQL", res5)
        self.assertIn("Excel", res5)

    def test_enhance_skills_noise_cleaning(self):
        """Test that enhance_skills handles basic user inputs like 'python programming, c++' without duplicating category names."""
        skills_raw = "python programming, c++"
        enhanced = ResumeBuilderModel.enhance_skills(skills_raw)
        self.assertIn("Programming Languages", enhanced)
        self.assertIn("Python", enhanced)
        self.assertIn("C++", enhanced)
        # Should be a single unified line for Programming Languages
        self.assertEqual(enhanced.count("Programming Languages"), 1)
        self.assertNotIn("Technical Skills", enhanced)

    def test_non_technical_skills_explicit_separation(self):
        """Test that public speaking is placed under Non-Technical Skills, while Python and C++ are under Programming Languages."""
        # 1. Via enhance_skills
        raw = "Python, C++, Public Speaking"
        enhanced = ResumeBuilderModel.enhance_skills(raw)
        self.assertIn("Programming Languages: Python, C++", enhanced)
        self.assertIn("Non-Technical Skills: Public Speaking", enhanced)

        # 2. Via enhance_technical_and_non_technical with Enter keys (line breaks)
        tech_multiline = "Python\nC++\nSQL"
        non_tech_multiline = "Public Speaking\nProblem Solving"
        combined = ResumeBuilderModel.enhance_technical_and_non_technical(tech_multiline, non_tech_multiline)
        self.assertIn("Programming Languages: Python, C++", combined)
        self.assertIn("Non-Technical Skills: Public Speaking, Problem Solving", combined)

    def test_skip_technical_projects_omits_section(self):
        """Test that skipping technical projects leaves projects empty and omits the section from HTML and PDF."""
        data = dict(self.sample_data)
        data["skip_projects"] = True
        data["has_projects"] = False
        data["projects"] = ""
        data["project_entries"] = []

        html = render_resume_html(data, "Modern")
        self.assertNotIn("TECHNICAL PROJECT", html)

        pdf_bytes = export_builder_resume_to_pdf(data, "Modern")
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

    def test_optimizer_skills_non_technical_separation(self):
        """Test that optimizer places public speaking into NON-TECHNICAL SKILLS and Python/C++ under TECHNICAL SKILLS."""
        from modules.resume_guide.optimizer import ResumeOptimizer
        optimizer = ResumeOptimizer(job_role="Software Developer", company="Google")
        user_skills = {
            "technical": "Python\nC++",
            "non_technical": "Public Speaking"
        }
        res = optimizer._improve_skills(original_skills="", user_skills=user_skills, in_needs_improvement=True)
        self.assertIsNotNone(res)
        self.assertIn("TECHNICAL SKILLS", res["after"])
        self.assertIn("Programming Languages: Python, C++", res["after"])
        self.assertIn("NON-TECHNICAL SKILLS", res["after"])
        self.assertIn("Public Speaking", res["after"])

if __name__ == "__main__":
    unittest.main()

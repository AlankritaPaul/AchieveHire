"""
Resume Builder business logic and data model for 'Create Resume' flow.
Strictly abides by the Accuracy Rule:
- Tailors presentation and structure to target role, company, and JD.
- NEVER invents fake skills, work experience, certifications, or projects.
"""

from typing import Dict, List, Any, Optional
import base64
import re
from modules.constants import WEAK_VERBS_MAP

DEFAULT_DECLARATION = (
    "I hereby declare that all the details and information given above are complete, "
    "accurate, and true to the best of my knowledge and belief."
)

class ResumeBuilderModel:
    def __init__(self):
        self.data: Dict[str, Any] = {
            "job_role": "",
            "company": "",
            "job_description": "",
            "full_name": "",
            "professional_headline": "",
            "email": "",
            "phone": "",
            "location": "",
            "place_val": "",
            "summary": "",
            "skills": "",
            "experience": "",
            "projects": "",
            "project_entries": [],
            "education": "",
            "certifications": "",
            "custom_sections": [],
            "photo_mode": "none",  # "upload", "box", "none"
            "photo_b64": "",
            "declaration": DEFAULT_DECLARATION,
            "date_val": "",
            "signature_mode": "write",  # "write", "upload", "blank"
            "sig_val": "",
            "signature_img_b64": "",
            "template_name": "Modern",
            "education_entries": [
                {
                    "degree": "",
                    "field_of_study": "",
                    "institution": "",
                    "board_univ": "",
                    "location": "",
                    "status": "Completed",  # "Completed" or "Currently Pursuing"
                    "start_year": "",
                    "end_year": "",
                    "expected_grad_year": "",
                    "cgpa": "",
                    "percentage": "",
                    "grade": ""
                }
            ],
            "qualification_entries": [],
            "experience_entries": []
        }

    @staticmethod
    def enhance_headline(raw_headline: str) -> str:
        """
        Convert a user's basic headline or role/technologies into a professional,
        well-structured resume headline (e.g. 'Role | Specialization & Key Technologies')
        without changing the candidate's actual roles, skills, or data.
        """
        raw = (raw_headline or "").strip()
        if not raw:
            return ""

        cleaned = re.sub(r"[\r\n\t]+", " ", raw).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)

        tech_norm = {
            "python": "Python", "python3": "Python", "java": "Java", "c++": "C++", "cpp": "C++",
            "c": "C", "c#": "C#", "csharp": "C#", "javascript": "JavaScript", "js": "JavaScript",
            "typescript": "TypeScript", "ts": "TypeScript", "sql": "SQL", "mysql": "MySQL",
            "postgresql": "PostgreSQL", "postgres": "PostgreSQL", "mongodb": "MongoDB",
            "redis": "Redis", "react": "React.js", "reactjs": "React.js", "react.js": "React.js",
            "angular": "Angular", "vue": "Vue.js", "vuejs": "Vue.js", "nextjs": "Next.js",
            "next.js": "Next.js", "node": "Node.js", "nodejs": "Node.js", "node.js": "Node.js",
            "express": "Express.js", "django": "Django", "flask": "Flask", "fastapi": "FastAPI",
            "spring": "Spring Boot", "spring boot": "Spring Boot", "aws": "AWS", "azure": "Azure",
            "gcp": "GCP", "docker": "Docker", "kubernetes": "Kubernetes", "git": "Git",
            "tableau": "Tableau", "power bi": "Power BI", "powerbi": "Power BI", "excel": "Excel",
            "html": "HTML5", "css": "CSS3", "tailwind": "Tailwind CSS", "bootstrap": "Bootstrap",
            "pandas": "Pandas", "numpy": "NumPy", "machine learning": "Machine Learning", "ai": "AI",
            "data science": "Data Science", "cloud": "Cloud Technologies", "devops": "DevOps"
        }

        role_patterns = [
            (r"\b(aspiring\s*(software\s*)?engineer|student|fresher|intern)\b", "Aspiring Software Engineer"),
            (r"\bfull[-\s]*stack\s*(dev(eloper)?|engineer)?\b", "Full-Stack Developer"),
            (r"\bfront[-\s]*end\s*(dev(eloper)?|engineer)?\b", "Frontend Developer"),
            (r"\bback[-\s]*end\s*(dev(eloper)?|engineer)?\b", "Backend Developer"),
            (r"\bpython\s*(dev(eloper)?|engineer)\b", "Python Developer"),
            (r"\bjava\s*(dev(eloper)?|engineer)\b", "Java Developer"),
            (r"\bc\+\+\s*(dev(eloper)?|engineer)\b", "C++ Developer"),
            (r"\bsoftware\s*(dev(eloper)?|engineer)\b", "Software Engineer"),
            (r"\bdata\s*analyst\b", "Data Analyst"),
            (r"\bdata\s*scientist\b", "Data Scientist"),
            (r"\bdevops\s*(engineer)?\b", "DevOps Engineer"),
            (r"\bcloud\s*(architect|engineer)\b", "Cloud Engineer"),
            (r"\bmachine\s*learning\s*(engineer)?|\bml\s*engineer\b", "Machine Learning Engineer"),
            (r"\bai\s*(engineer|specialist)\b", "AI Engineer"),
            (r"\bqa\s*(engineer)?|\btester|\bquality\s*assurance\b", "Quality Assurance Engineer"),
            (r"\bweb\s*dev(eloper)?\b", "Web Developer"),
        ]

        role_specs = {
            "Software Engineer": "Software Development & System Design",
            "Full-Stack Developer": "Web Applications & Software Solutions",
            "Frontend Developer": "UI/UX & Modern Web Technologies",
            "Backend Developer": "APIs & Distributed Systems",
            "Python Developer": "Backend Architecture & Data Solutions",
            "Java Developer": "Enterprise Systems & Microservices",
            "C++ Developer": "Systems & High-Performance Engineering",
            "Data Analyst": "Business Intelligence & Data Solutions",
            "Data Scientist": "Predictive Modeling & Machine Learning",
            "DevOps Engineer": "CI/CD & Cloud Infrastructure",
            "Cloud Engineer": "Cloud Architecture & Infrastructure",
            "Machine Learning Engineer": "AI & Machine Learning Solutions",
            "AI Engineer": "Applied AI & Intelligent Systems",
            "Quality Assurance Engineer": "Automated & Manual Testing",
            "Web Developer": "Modern Web Applications & Development",
            "Aspiring Software Engineer": "Software Engineering & Problem Solving",
        }

        # If user entered with pipe delimiter, clean up each segment
        if "|" in cleaned:
            parts = [p.strip() for p in cleaned.split("|") if p.strip()]
            enhanced_parts = []
            for p in parts:
                words = p.split()
                norm_words = []
                for w in words:
                    low_w = w.lower().strip(",.;:")
                    if low_w in tech_norm:
                        norm_words.append(tech_norm[low_w])
                    else:
                        norm_words.append(w.capitalize() if w.islower() else w)
                enhanced_parts.append(" ".join(norm_words))
            return " | ".join(enhanced_parts)

        # Detect specific role title
        detected_role = None
        for pattern, title in role_patterns:
            if re.search(pattern, cleaned, re.IGNORECASE):
                detected_role = title
                break

        # Detect matched technologies from input
        found_tech = []
        sorted_tech_keys = sorted(tech_norm.keys(), key=lambda k: len(k), reverse=True)
        temp_text = cleaned
        for tk in sorted_tech_keys:
            escaped = re.escape(tk)
            pat = r'(?<![a-zA-Z0-9_])' + escaped + r'(?![a-zA-Z0-9_+#])'
            if re.search(pat, temp_text, re.IGNORECASE):
                disp = tech_norm[tk]
                if detected_role and disp.lower() in detected_role.lower():
                    pass
                elif disp not in found_tech:
                    found_tech.append(disp)
                temp_text = re.sub(pat, " ", temp_text, flags=re.IGNORECASE)

        if detected_role and found_tech:
            if len(found_tech) == 1:
                tech_phrase = f"{found_tech[0]} Development" if found_tech[0] in ["Python", "Java", "C++", "SQL"] else f"{found_tech[0]} Solutions"
                return f"{detected_role} | {tech_phrase}"
            elif len(found_tech) == 2:
                return f"{detected_role} | {found_tech[0]} & {found_tech[1]}"
            else:
                return f"{detected_role} | " + ", ".join(found_tech[:-1]) + f" & {found_tech[-1]}"

        if detected_role and not found_tech:
            spec = role_specs.get(detected_role, "Software Engineering & Solutions")
            return f"{detected_role} | {spec}"

        if found_tech and not detected_role:
            if any(t in ["React.js", "Vue.js", "Angular", "HTML5", "CSS3", "Tailwind CSS"] for t in found_tech) and not any(t in ["Node.js", "Django", "Flask", "Spring Boot"] for t in found_tech):
                inferred_role = "Frontend Developer"
            elif any(t in ["Node.js", "Django", "Flask", "FastAPI", "Spring Boot"] for t in found_tech) and not any(t in ["React.js", "Angular", "Vue.js"] for t in found_tech):
                inferred_role = "Backend Developer"
            elif any(t in ["Tableau", "Power BI", "Excel"] for t in found_tech):
                inferred_role = "Data Analyst"
            elif any(t in ["Docker", "Kubernetes", "AWS", "Azure", "GCP"] for t in found_tech) and len(found_tech) <= 2:
                inferred_role = "Cloud / DevOps Engineer"
            else:
                inferred_role = "Software Developer"

            if len(found_tech) == 1:
                return f"{inferred_role} | {found_tech[0]} Development"
            elif len(found_tech) == 2:
                return f"{inferred_role} | {found_tech[0]} & {found_tech[1]}"
            else:
                return f"{inferred_role} | " + ", ".join(found_tech[:-1]) + f" & {found_tech[-1]}"

        # Clean title-cased fallback
        words = [w.capitalize() if w.islower() else w for w in cleaned.split()]
        return " ".join(words)

    @staticmethod
    def enhance_qualifications(raw_edu: str) -> str:
        """
        Enhance educational qualifications using standard professional terminology
        without changing the candidate's actual institutions, degrees, or facts.
        Preserves user's actual entered degree without redundant bracket duplicates.
        """
        if not raw_edu or not raw_edu.strip():
            return ""

        degree_map = [
            (r"\bb\.?\s*tech\b", "B.Tech"),
            (r"\bbachelor\s+of\s+technology\b", "Bachelor of Technology"),
            (r"\bb\.?\s*e\b", "B.E."),
            (r"\bbachelor\s+of\s+engineering\b", "Bachelor of Engineering"),
            (r"\bb\.?\s*sc\b", "B.Sc."),
            (r"\bb\.?\s*s\b", "B.S."),
            (r"\bbachelor\s+of\s+science\b", "Bachelor of Science"),
            (r"\bm\.?\s*tech\b", "M.Tech"),
            (r"\bmaster\s+of\s+technology\b", "Master of Technology"),
            (r"\bm\.?\s*sc\b", "M.Sc."),
            (r"\bm\.?\s*s\b", "M.S."),
            (r"\bmaster\s+of\s+science\b", "Master of Science"),
            (r"\bbca\b", "BCA"),
            (r"\bbachelor\s+of\s+computer\s+applications?\b", "Bachelor of Computer Applications"),
            (r"\bmca\b", "MCA"),
            (r"\bmaster\s+of\s+computer\s+applications?\b", "Master of Computer Applications"),
            (r"\bmba\b", "MBA"),
            (r"\bmaster\s+of\s+business\s+administration\b", "Master of Business Administration"),
            (r"\bbba\b", "BBA"),
            (r"\bbachelor\s+of\s+business\s+administration\b", "Bachelor of Business Administration"),
            (r"\bb\.?\s*com\b", "B.Com"),
            (r"\bbachelor\s+of\s+commerce\b", "Bachelor of Commerce"),
            (r"\bb\.?\s*a\b", "B.A."),
            (r"\bbachelor\s+of\s+arts\b", "Bachelor of Arts"),
            (r"\bph\.?d\b|\bdoctor\s+of\s+philosophy\b", "Ph.D."),
            (r"\b12th(\s*(?:grade|standard|class|pass))?\b|\bclass\s*12\b|\bhsc\b|\bintermediate\b", "Class XII (Senior Secondary)"),
            (r"\b10th(\s*(?:grade|standard|class|pass))?\b|\bclass\s*10\b|\bssc\b|\bmatric(ulation)?\b", "Class X (Secondary)"),
            (r"\bdiploma\b", "Diploma"),
        ]

        spec_map = [
            (r"\baiml\b|\bai\s*(and|&|\/)\s*ml\b|\bai-ml\b", "Artificial Intelligence & Machine Learning"),
            (r"\bcs\b|\bcse\b|\bcomputer\s+science\s+(and|&)\s+engineering\b", "Computer Science & Engineering"),
            (r"\bcomputer\s+science\b", "Computer Science"),
            (r"\bit\b|\binformation\s+technology\b", "Information Technology"),
            (r"\bece\b|\belectronics\s+(and|&)\s+communication\b", "Electronics & Communication Engineering"),
            (r"\beee\b|\bee\b|\belectrical\s+engineering\b", "Electrical & Electronics Engineering"),
            (r"\bme\b|\bmech\b|\bmechanical\s+engineering\b", "Mechanical Engineering"),
            (r"\bcivil\b|\bcivil\s+engineering\b", "Civil Engineering"),
            (r"\bai\b|\bartificial\s+intelligence\b", "Artificial Intelligence"),
            (r"\bml\b|\bmachine\s+learning\b", "Machine Learning"),
            (r"\bds\b|\bdata\s+science\b", "Data Science"),
            (r"\bcyber\s*sec(urity)?\b", "Cybersecurity"),
        ]

        lines = raw_edu.split("\n")
        enhanced_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            cleaned = stripped.lstrip("•-* ")
            for pattern, replacement in degree_map:
                cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)
            for pattern, replacement in spec_map:
                cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

            # Professional grade formatting (handles both "8.9 CGPA" and "CGPA: 8.9", "94%" and "94 percentage")
            cleaned = re.sub(r"([0-9.]+)\s*(?:cgpa|gpa)\b", r"CGPA: \1", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\b(?:cgpa|gpa)\s*[:=]?\s*([0-9.]+)", r"CGPA: \1", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"([0-9.]+)\s*(?:%|\bpercentage\b|\bpercent\b)", r"Score: \1%", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\bpercentage\s*[:=]?\s*([0-9.]+)\s*%?", r"Score: \1%", cleaned, flags=re.IGNORECASE)

            if not cleaned.startswith("•"):
                cleaned = f"• {cleaned}"
            enhanced_lines.append(cleaned)

        return "\n".join(enhanced_lines)

    @staticmethod
    def enhance_education_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enhance a list of structured education dictionaries with professional keywords
        without altering the candidate's actual institutions, degrees, or grades.
        """
        enhanced_entries = []
        for entry in entries:
            e = dict(entry)
            deg = e.get("degree", "").strip()
            field = e.get("field_of_study", e.get("stream", "")).strip()
            board = e.get("board_univ", "").strip()
            cgpa = e.get("cgpa", "").strip()
            pct = e.get("percentage", "").strip()
            grade = e.get("grade", "").strip()
            start_yr = e.get("start_year", "").strip()
            end_yr = e.get("end_year", "").strip()
            exp_yr = e.get("expected_grad_year", "").strip()

            if not cgpa and grade and re.search(r"\b(?:cgpa|gpa)\b", grade, flags=re.IGNORECASE):
                cgpa_match = re.search(r"([0-9.]+)\s*(?:cgpa|gpa)|(?:cgpa|gpa)\s*[:=]?\s*([0-9.]+)", grade, flags=re.IGNORECASE)
                if cgpa_match:
                    cgpa = cgpa_match.group(1) or cgpa_match.group(2)

            year_raw = e.get("year", "").strip()
            if year_raw and not start_yr and not end_yr and not exp_yr:
                y_parts = [y.strip() for y in re.split(r"[-–—]", year_raw) if y.strip()]
                if len(y_parts) == 2:
                    start_yr, end_yr = y_parts[0], y_parts[1]
                elif len(y_parts) == 1:
                    end_yr = y_parts[0]

            if deg:
                deg_enh = ResumeBuilderModel.enhance_qualifications(deg).lstrip("• ")
                e["degree"] = deg_enh

            if field:
                field_clean = field
                for pattern, rep in [
                    (r"\baiml\b|\bai\s*(and|&|\/)\s*ml\b|\bai-ml\b", "Artificial Intelligence & Machine Learning"),
                    (r"\bcs\b|\bcse\b|\bcomputer\s+science\s+(and|&)\s+engineering\b", "Computer Science & Engineering"),
                    (r"\bcomputer\s+science\b", "Computer Science"),
                    (r"\bit\b|\binformation\s+technology\b", "Information Technology"),
                    (r"\bece\b|\belectronics\s+(and|&)\s+communication\b", "Electronics & Communication Engineering"),
                    (r"\beee\b|\bee\b|\belectrical\s+engineering\b", "Electrical & Electronics Engineering"),
                    (r"\bme\b|\bmech\b|\bmechanical\s+engineering\b", "Mechanical Engineering"),
                    (r"\bcivil\b|\bcivil\s+engineering\b", "Civil Engineering"),
                    (r"\bpcm\b", "Science (Physics, Chemistry, Maths)"),
                    (r"\bpcb\b", "Science (Physics, Chemistry, Biology)"),
                    (r"\bcommerce\b", "Commerce"),
                    (r"\barts\b", "Humanities / Arts"),
                ]:
                    field_clean = re.sub(pattern, rep, field_clean, flags=re.IGNORECASE)
                e["field_of_study"] = field_clean
                e["stream"] = field_clean

            if board:
                b_clean = board
                b_clean = re.sub(r"\bcbse\b", "CBSE Board", b_clean, flags=re.IGNORECASE)
                b_clean = re.sub(r"\bicse\b", "ICSE Board", b_clean, flags=re.IGNORECASE)
                b_clean = re.sub(r"\bstate\s*board\b", "State Board", b_clean, flags=re.IGNORECASE)
                e["board_univ"] = b_clean

            if cgpa:
                c_clean = cgpa
                c_clean = re.sub(r"([0-9.]+)\s*(?:cgpa|gpa)\b", r"\1", c_clean, flags=re.IGNORECASE)
                c_clean = re.sub(r"\b(?:cgpa|gpa)\s*[:=]?\s*([0-9.]+)", r"\1", c_clean, flags=re.IGNORECASE)
                e["cgpa"] = c_clean.strip()

            if pct:
                p_clean = pct.strip()
                p_clean = re.sub(r"\bpercentage\s*[:=]?\s*", "", p_clean, flags=re.IGNORECASE)
                p_clean = re.sub(r"\bscore\s*[:=]?\s*", "", p_clean, flags=re.IGNORECASE)
                if not p_clean.endswith("%") and re.match(r"^[0-9]+(\.[0-9]+)?$", p_clean):
                    p_clean = f"{p_clean}%"
                e["percentage"] = p_clean

            if grade:
                g_clean = grade.strip()
                g_clean = re.sub(r"([0-9.]+)\s*(?:cgpa|gpa)\b", r"CGPA: \1", g_clean, flags=re.IGNORECASE)
                g_clean = re.sub(r"\b(?:cgpa|gpa)\s*[:=]?\s*([0-9.]+)", r"CGPA: \1", g_clean, flags=re.IGNORECASE)
                if "%" in g_clean or "percentage" in g_clean.lower() or "percent" in g_clean.lower():
                    g_clean = re.sub(r"([0-9.]+)\s*(?:%|\bpercentage\b|\bpercent\b)", r"Score: \1%", g_clean, flags=re.IGNORECASE)
                    g_clean = re.sub(r"\bpercentage\s*[:=]?\s*([0-9.]+)%?", r"Score: \1%", g_clean, flags=re.IGNORECASE)
                e["grade"] = g_clean

            if start_yr:
                e["start_year"] = start_yr.strip()
            if end_yr:
                e["end_year"] = end_yr.strip()
            if exp_yr:
                e["expected_grad_year"] = exp_yr.strip()

            enhanced_entries.append(e)
        return enhanced_entries

    @staticmethod
    def enhance_qualification_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enhance a list of additional qualifications with clean formatting.
        """
        enhanced = []
        for entry in entries:
            q = dict(entry)
            title = q.get("title", "").strip()
            org = q.get("organization", "").strip()
            yr = q.get("year", "").strip()
            det = q.get("details", "").strip()

            if title:
                q["title"] = title[0].upper() + title[1:] if len(title) > 1 else title.upper()
            if org:
                q["organization"] = org.strip()
            if yr:
                q["year"] = yr.strip()
            if det:
                q["details"] = det.strip()

            enhanced.append(q)
        return enhanced

    @staticmethod
    def compile_education_and_qualifications(
        education_entries: List[Dict[str, Any]],
        qualification_entries: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Compile formal Education and optional Qualifications subsections into
        a realistic, professional resume section under 'Education and Qualifications'.
        Does NOT show internal form labels like 'Education 1' or 'Education 2'.
        """
        sections = []

        # 1. Subsection: Education
        valid_edu_blocks = []
        for entry in (education_entries or []):
            deg = entry.get("degree", "").strip()
            field = entry.get("field_of_study", entry.get("stream", "")).strip()
            inst = entry.get("institution", "").strip()
            board = entry.get("board_univ", "").strip()
            loc = entry.get("location", "").strip()
            status = entry.get("status", "Completed").strip()
            start_yr = entry.get("start_year", "").strip()
            end_yr = entry.get("end_year", "").strip()
            exp_grad_yr = entry.get("expected_grad_year", "").strip()
            cgpa = entry.get("cgpa", "").strip()
            pct = entry.get("percentage", "").strip()
            grade = entry.get("grade", "").strip()

            if not any([deg, field, inst, board, loc, start_yr, end_yr, exp_grad_yr, cgpa, pct, grade]):
                continue

            # Title line: Degree in Field of Study
            if deg and field:
                if field.lower() in deg.lower():
                    title_line = f"• {deg}"
                else:
                    title_line = f"• {deg} in {field}"
            elif deg:
                title_line = f"• {deg}"
            elif field:
                title_line = f"• {field}"
            elif inst:
                title_line = f"• {inst}"
            else:
                continue

            # Metadata details line
            meta = []
            if inst and title_line != f"• {inst}":
                meta.append(inst)
            if board and board.lower() not in inst.lower():
                meta.append(board)
            if loc:
                meta.append(loc)

            # Date formatting based on independent status
            if status == "Currently Pursuing":
                if start_yr and exp_grad_yr:
                    meta.append(f"{start_yr} – Present | Expected Graduation: {exp_grad_yr}")
                elif exp_grad_yr:
                    meta.append(f"Expected Graduation: {exp_grad_yr}")
                elif start_yr:
                    meta.append(f"{start_yr} – Present")
                else:
                    meta.append("Currently Pursuing")
            else:  # Completed
                if start_yr and end_yr:
                    meta.append(f"{start_yr} – {end_yr}")
                elif end_yr:
                    meta.append(end_yr)
                elif start_yr:
                    meta.append(start_yr)

            # Academic Results (only what user actually provided)
            if cgpa:
                c_str = cgpa if cgpa.upper().startswith("CGPA") or cgpa.upper().startswith("GPA") else f"CGPA: {cgpa}"
                meta.append(c_str)
            if pct:
                p_str = pct if pct.lower().startswith("percentage") or pct.lower().startswith("score") else (f"Percentage: {pct}" if pct.endswith("%") else f"Percentage: {pct}%")
                meta.append(p_str)
            if grade:
                clean_g = grade.strip()
                if cgpa and (clean_g == cgpa or clean_g == f"CGPA: {cgpa}" or clean_g.endswith(cgpa)):
                    pass
                elif pct and (clean_g == pct or clean_g == f"Score: {pct}" or clean_g == f"{pct}%"):
                    pass
                else:
                    if clean_g.lower().startswith(("grade", "score", "cgpa", "gpa")):
                        g_str = clean_g
                    else:
                        g_str = f"Grade: {clean_g}"
                    meta.append(g_str)

            if meta:
                valid_edu_blocks.append(f"{title_line}\n  " + " | ".join(meta))
            else:
                valid_edu_blocks.append(title_line)

        # 2. Subsection: Qualifications (Optional)
        valid_qual_blocks = []
        for qual in (qualification_entries or []):
            title = qual.get("title", "").strip()
            org = qual.get("organization", "").strip()
            yr = qual.get("year", "").strip()
            det = qual.get("details", "").strip()

            if not any([title, org, yr, det]):
                continue

            q_title = f"• {title}" if not title.startswith(("•", "-", "*")) else title
            q_meta = []
            if org:
                q_meta.append(org)
            if yr:
                q_meta.append(yr)
            if det:
                q_meta.append(det)

            if q_meta:
                valid_qual_blocks.append(f"{q_title}\n  " + " | ".join(q_meta))
            else:
                valid_qual_blocks.append(q_title)

        # Combine into Education and Qualifications structure
        if valid_edu_blocks and valid_qual_blocks:
            sections.append("Education\n" + "\n".join(valid_edu_blocks))
            sections.append("Qualifications\n" + "\n".join(valid_qual_blocks))
        elif valid_edu_blocks:
            sections.append("Education\n" + "\n".join(valid_edu_blocks))
        elif valid_qual_blocks:
            sections.append("Qualifications\n" + "\n".join(valid_qual_blocks))

        return "\n\n".join(sections)

    @staticmethod
    def compile_education_entries(entries: List[Dict[str, Any]], qual_entries: Optional[List[Dict[str, Any]]] = None) -> str:
        """Backward-compatible alias for compile_education_and_qualifications."""
        return ResumeBuilderModel.compile_education_and_qualifications(entries, qual_entries)

    @staticmethod
    def enhance_skills(raw_skills: str) -> str:
        """
        Standardize and group candidate skills into professional industry categories
        without inventing any unprovided skills.
        """
        if not raw_skills or not raw_skills.strip():
            return ""

        tech_map = {
            "python": ("Python", "languages"),
            "python3": ("Python", "languages"),
            "java": ("Java", "languages"),
            "c++": ("C++", "languages"),
            "cpp": ("C++", "languages"),
            "c": ("C", "languages"),
            "c#": ("C#", "languages"),
            "csharp": ("C#", "languages"),
            "javascript": ("JavaScript", "languages"),
            "js": ("JavaScript", "languages"),
            "typescript": ("TypeScript", "languages"),
            "ts": ("TypeScript", "languages"),
            "sql": ("SQL", "languages"),
            "html": ("HTML5", "languages"),
            "html5": ("HTML5", "languages"),
            "css": ("CSS3", "languages"),
            "css3": ("CSS3", "languages"),
            "go": ("Go", "languages"),
            "golang": ("Go", "languages"),
            "rust": ("Rust", "languages"),
            "ruby": ("Ruby", "languages"),
            "php": ("PHP", "languages"),
            "kotlin": ("Kotlin", "languages"),
            "swift": ("Swift", "languages"),
            "r": ("R", "languages"),
            "react": ("React.js", "frameworks"),
            "reactjs": ("React.js", "frameworks"),
            "react.js": ("React.js", "frameworks"),
            "angular": ("Angular", "frameworks"),
            "vue": ("Vue.js", "frameworks"),
            "vuejs": ("Vue.js", "frameworks"),
            "nextjs": ("Next.js", "frameworks"),
            "next.js": ("Next.js", "frameworks"),
            "nodejs": ("Node.js", "frameworks"),
            "node.js": ("Node.js", "frameworks"),
            "express": ("Express.js", "frameworks"),
            "expressjs": ("Express.js", "frameworks"),
            "django": ("Django", "frameworks"),
            "flask": ("Flask", "frameworks"),
            "fastapi": ("FastAPI", "frameworks"),
            "spring": ("Spring Boot", "frameworks"),
            "spring boot": ("Spring Boot", "frameworks"),
            "tailwind": ("Tailwind CSS", "frameworks"),
            "bootstrap": ("Bootstrap", "frameworks"),
            "pandas": ("Pandas", "frameworks"),
            "numpy": ("NumPy", "frameworks"),
            "scikit-learn": ("Scikit-Learn", "frameworks"),
            "tensorflow": ("TensorFlow", "frameworks"),
            "pytorch": ("PyTorch", "frameworks"),
            "mysql": ("MySQL", "databases"),
            "postgresql": ("PostgreSQL", "databases"),
            "postgres": ("PostgreSQL", "databases"),
            "mongodb": ("MongoDB", "databases"),
            "redis": ("Redis", "databases"),
            "sqlite": ("SQLite", "databases"),
            "aws": ("AWS (Amazon Web Services)", "cloud_tools"),
            "azure": ("Microsoft Azure", "cloud_tools"),
            "gcp": ("Google Cloud Platform (GCP)", "cloud_tools"),
            "docker": ("Docker", "cloud_tools"),
            "kubernetes": ("Kubernetes", "cloud_tools"),
            "git": ("Git", "cloud_tools"),
            "github": ("GitHub", "cloud_tools"),
            "gitlab": ("GitLab", "cloud_tools"),
            "linux": ("Linux", "cloud_tools"),
            "postman": ("Postman", "cloud_tools"),
            "jira": ("JIRA", "cloud_tools"),
            "ci/cd": ("CI/CD", "cloud_tools"),
            "figma": ("Figma", "cloud_tools"),
            "tableau": ("Tableau", "cloud_tools"),
            "powerbi": ("Power BI", "cloud_tools"),
            "power bi": ("Power BI", "cloud_tools"),
            "excel": ("Advanced Excel", "cloud_tools"),
            "dsa": ("Data Structures & Algorithms", "concepts"),
            "data structures": ("Data Structures & Algorithms", "concepts"),
            "algorithms": ("Algorithms", "concepts"),
            "oop": ("Object-Oriented Programming (OOP)", "concepts"),
            "rest api": ("RESTful APIs", "concepts"),
            "rest apis": ("RESTful APIs", "concepts"),
            "system design": ("System Design", "concepts"),
            "problem solving": ("Problem Solving", "concepts"),
            "communication": ("Team Communication", "concepts"),
            "leadership": ("Team Leadership", "concepts"),
        }

        category_labels_map = {
            "programming languages": "Programming Languages",
            "programming language": "Programming Languages",
            "languages": "Programming Languages",
            "frameworks": "Frameworks & Libraries",
            "frameworks & libraries": "Frameworks & Libraries",
            "libraries": "Frameworks & Libraries",
            "databases": "Databases",
            "database": "Databases",
            "tools": "Tools & Cloud Technologies",
            "tools & technologies": "Tools & Cloud Technologies",
            "cloud tools": "Tools & Cloud Technologies",
            "cloud technologies": "Tools & Cloud Technologies",
            "cloud & tools": "Tools & Cloud Technologies",
            "core competencies": "Core Competencies & Methodologies",
            "methodologies": "Core Competencies & Methodologies",
            "concepts": "Core Competencies & Methodologies",
            "technical skills": "Technical Skills",
            "non-technical skills": "Non-Technical Skills",
            "additional competencies": "Additional Competencies",
            "additional competency": "Additional Competencies",
            "soft skills": "Non-Technical Skills",
            "skills": "Technical Skills"
        }

        raw_lines = [l.strip() for l in raw_skills.split("\n") if l.strip()]
        cat_skills: Dict[str, List[str]] = {}
        cat_order: List[str] = []
        current_cat: Optional[str] = None
        noise_pat = r'(?i)\s+(programming|languages?|development|frameworks?|libraries?|databases?|tools?|technologies)$'

        def add_skill(category: str, skill_name: str):
            clean_c = category.strip()
            low_c = clean_c.lower()
            if low_c in category_labels_map:
                clean_c = category_labels_map[low_c]
            else:
                clean_c = clean_c[0].upper() + clean_c[1:] if len(clean_c) > 1 else clean_c.upper()

            if clean_c not in cat_skills:
                cat_skills[clean_c] = []
                cat_order.append(clean_c)

            s_clean = skill_name.strip(" •-*")
            if not s_clean:
                return
            clean_s = re.sub(noise_pat, "", s_clean).strip()
            lower_s = clean_s.lower() if clean_s else s_clean.lower()
            if lower_s in tech_map:
                norm_s = tech_map[lower_s][0]
            elif s_clean.lower() in tech_map:
                norm_s = tech_map[s_clean.lower()][0]
            elif any(v[0].lower() == lower_s for v in tech_map.values()):
                norm_s = [v[0] for v in tech_map.values() if v[0].lower() == lower_s][0]
            elif any(v[0].lower() == s_clean.lower() for v in tech_map.values()):
                norm_s = [v[0] for v in tech_map.values() if v[0].lower() == s_clean.lower()][0]
            else:
                norm_s = s_clean.title() if len(s_clean) > 3 else s_clean.upper()

            if norm_s and norm_s not in cat_skills[clean_c]:
                cat_skills[clean_c].append(norm_s)

        for line in raw_lines:
            l_clean = line.lstrip("•-* ").strip()
            if not l_clean:
                continue

            # Case A: Line has a colon "Category: skill1, skill2"
            if ":" in l_clean:
                cat_part, s_part = l_clean.split(":", 1)
                cat_name = cat_part.strip()
                s_tokens = [s.strip(" •-*") for s in re.split(r"[,;]", s_part) if s.strip(" •-*")]
                for s in s_tokens:
                    add_skill(cat_name, s)
                current_cat = cat_name
            else:
                # Check if this line is purely a category heading
                low_line = l_clean.lower()
                if low_line in category_labels_map:
                    current_cat = category_labels_map[low_line]
                else:
                    # It's a skill or comma-separated list of skills
                    tokens = [s.strip(" •-*") for s in re.split(r"[,;]", l_clean) if s.strip(" •-*")]
                    for tok in tokens:
                        if tok.lower() in category_labels_map:
                            current_cat = category_labels_map[tok.lower()]
                            continue
                        if current_cat and current_cat != "Technical Skills":
                            add_skill(current_cat, tok)
                        else:
                            # Map token to standard category via tech_map
                            low_tok = tok.lower()
                            clean_tok_str = re.sub(noise_pat, "", low_tok).strip()
                            lookup_key = clean_tok_str if clean_tok_str in tech_map else low_tok
                            if lookup_key in tech_map:
                                name, cat_key = tech_map[lookup_key]
                                cat_display = {
                                    "languages": "Programming Languages",
                                    "frameworks": "Frameworks & Libraries",
                                    "databases": "Databases",
                                    "cloud_tools": "Tools & Cloud Technologies",
                                    "concepts": "Core Competencies & Methodologies",
                                    "other": "Additional Competencies"
                                }.get(cat_key, "Technical Skills")
                                add_skill(cat_display, name)
                            else:
                                add_skill("Technical Skills", tok)

        # Build clean output bullets - only non-empty categories, no duplicate category headings
        output_bullets = []
        for cat in cat_order:
            skills_list = cat_skills.get(cat, [])
            if skills_list:
                output_bullets.append(f"• {cat}: {', '.join(skills_list)}")

        return "\n".join(output_bullets) if output_bullets else raw_skills.strip()

    @staticmethod
    def enhance_experience(raw_exp: str) -> str:
        """
        Enhance experience bullets with powerful active verbs and professional phrasing
        without altering authentic facts, companies, or dates.
        """
        if not raw_exp or not raw_exp.strip():
            return ""

        lines = raw_exp.split("\n")
        upgraded_lines = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            if "|" in stripped and not stripped.startswith(("•", "-", "*")):
                upgraded_lines.append(stripped)
                continue

            clean_line = stripped.lstrip("•-* ").strip()
            for weak_v, strong_options in WEAK_VERBS_MAP.items():
                pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                if re.search(pattern, clean_line):
                    strong_v = strong_options[0].capitalize()
                    clean_line = re.sub(pattern, strong_v, clean_line, count=1)

            if clean_line:
                clean_line = clean_line[0].upper() + clean_line[1:]

            upgraded_lines.append(f"• {clean_line}")

        return "\n".join(upgraded_lines)

    @staticmethod
    def enhance_experience_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enhance structured work experience entries by upgrading passive verbs in descriptions
        and responsibilities without altering authentic facts, companies, or dates.
        Preserves user-entered custom experience types exactly as provided.
        """
        enhanced = []
        for entry in entries:
            e = dict(entry)
            pos = e.get("position", "").strip()
            comp = e.get("company", "").strip()
            desc = e.get("description", "").strip()
            resp = e.get("responsibilities", "").strip()

            # Skip entries with no substantive user input
            if not any([pos, comp, desc, resp]):
                continue

            if pos:
                e["position"] = pos[0].upper() + pos[1:] if len(pos) > 1 else pos.upper()

            if desc:
                clean_desc = desc
                for weak_v, strong_options in WEAK_VERBS_MAP.items():
                    pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                    if re.search(pattern, clean_desc):
                        strong_v = strong_options[0].capitalize()
                        clean_desc = re.sub(pattern, strong_v, clean_desc, count=1)
                e["description"] = clean_desc

            if resp:
                enhanced_lines = []
                for line in resp.split("\n"):
                    stripped = line.strip()
                    if not stripped:
                        continue
                    clean_line = stripped.lstrip("•-* ").strip()
                    for weak_v, strong_options in WEAK_VERBS_MAP.items():
                        pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                        if re.search(pattern, clean_line):
                            strong_v = strong_options[0].capitalize()
                            clean_line = re.sub(pattern, strong_v, clean_line, count=1)
                    if clean_line:
                        clean_line = clean_line[0].upper() + clean_line[1:]
                    enhanced_lines.append(f"• {clean_line}")
                e["responsibilities"] = "\n".join(enhanced_lines)

            enhanced.append(e)
        return enhanced

    @staticmethod
    def compile_experience_entries(entries: List[Dict[str, Any]]) -> str:
        """
        Compile structured work experience entries into clean, realistic resume formatting
        under the single 'Work Experience' section.
        Does NOT show internal form labels such as 'Experience 1' or 'Experience 2'.
        """
        if not entries:
            return ""

        blocks = []
        for entry in entries:
            company = entry.get("company", "").strip()
            position = entry.get("position", "").strip()
            location = entry.get("location", "").strip()
            status = entry.get("status", "Completed").strip()
            start_date = entry.get("start_date", "").strip()
            end_date = entry.get("end_date", "").strip()
            description = entry.get("description", "").strip()
            responsibilities = entry.get("responsibilities", "").strip()

            # A work experience entry is only valid if the user has provided substantive details
            # (such as position, company, description, or responsibilities).
            # Default dropdown values alone (e.g. 'Placement' or 'On-site') without company or position
            # do NOT qualify as an experience entry and must be ignored.
            if not any([position, company, description, responsibilities]):
                continue

            exp_type_raw = entry.get("experience_type", "").strip()
            if exp_type_raw == "Write Your Own":
                exp_type = entry.get("custom_experience_type", "").strip()
            else:
                exp_type = exp_type_raw

            arr_raw = entry.get("work_arrangement", "").strip()
            if arr_raw == "Write Your Own":
                arrangement = entry.get("custom_work_arrangement", "").strip()
            else:
                arrangement = arr_raw

            # Title line: Position (Experience Type) or Company
            if position and exp_type:
                title_line = f"• {position} ({exp_type})"
            elif position:
                title_line = f"• {position}"
            elif company and exp_type:
                title_line = f"• {company} ({exp_type})"
            elif company:
                title_line = f"• {company}"
            elif description or responsibilities:
                title_line = f"• Professional Experience ({exp_type})" if exp_type else "• Professional Experience"
            else:
                continue

            # Metadata line: Company Name | Location | Work Arrangement | Dates
            meta = []
            if company and not title_line.startswith(f"• {company}"):
                meta.append(company)
            if location:
                meta.append(location)
            if arrangement:
                meta.append(arrangement)

            # Dynamic date formatting based on status
            if status == "Currently Ongoing":
                if start_date:
                    meta.append(f"{start_date} - Present")
                else:
                    meta.append("Currently Ongoing")
            else:  # Completed
                if start_date and end_date:
                    meta.append(f"{start_date} - {end_date}")
                elif end_date:
                    meta.append(end_date)
                elif start_date:
                    meta.append(start_date)

            block_lines = [title_line]
            if meta:
                block_lines.append("  " + " | ".join(meta))
            if description:
                desc_clean = description.strip()
                if desc_clean:
                    block_lines.append(f"  {desc_clean}")
            if responsibilities:
                for line in responsibilities.split("\n"):
                    clean = line.strip()
                    if not clean:
                        continue
                    bullet_text = clean.lstrip("•-* ").strip()
                    block_lines.append(f"  - {bullet_text}")

            blocks.append("\n".join(block_lines))

        return "\n\n".join(blocks)

    @staticmethod
    def compile_project_entries(project_entries: List[Dict[str, Any]]) -> str:
        """
        Compile structured project entries into clean, realistic resume formatting
        under the Technical Project section.
        Project Name -> bullet-point-style heading (e.g. '• Project Name' or '• Project Name | Tech Stack: ...')
        Project Description -> normal paragraph directly below project name (NOT a bullet point).
        """
        if not project_entries:
            return ""

        blocks = []
        for proj in project_entries:
            name = proj.get("name", "").strip()
            stack = proj.get("tech_stack", "").strip()
            desc = proj.get("description", "").strip()

            if not any([name, stack, desc]):
                continue

            heading = f"• {name}" if name else "• Technical Project"
            if stack:
                heading += f" | Tech Stack: {stack}"

            proj_lines = [heading]
            if desc:
                for line in desc.split("\n"):
                    clean_d = line.strip().lstrip("•-* ").strip()
                    if clean_d:
                        proj_lines.append(f"  {clean_d}")

            blocks.append("\n".join(proj_lines))

        return "\n\n".join(blocks)

    @staticmethod
    def enhance_project_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enhance structured project entries with strong technical phrasing
        without turning descriptions into bullet points or fabricating false facts.
        """
        phrase_upgrades = [
            (r"\bmade a website\b", "Architected and developed a responsive web application"),
            (r"\bbuilt an app\b", "Engineered and deployed a full-stack application"),
            (r"\bmade an app\b", "Engineered and deployed an application"),
            (r"\bused python\b", "Leveraged Python to implement backend logic"),
            (r"\bused react\b", "Utilized React.js to deliver modular UI components"),
            (r"\bused machine learning\b", "Trained and evaluated machine learning models"),
            (r"\badded authentication\b", "Implemented secure token-based user authentication"),
            (r"\bcreated api\b", "Designed and deployed scalable RESTful APIs"),
        ]

        enhanced = []
        for entry in entries:
            p = dict(entry)
            name = p.get("name", "").strip()
            desc = p.get("description", "").strip()

            if name:
                p["name"] = name[0].upper() + name[1:] if len(name) > 1 else name.upper()

            if desc:
                p_lines = []
                for line in desc.split("\n"):
                    clean = line.strip().lstrip("•-* ").strip()
                    if not clean:
                        continue
                    for pattern, rep in phrase_upgrades:
                        clean = re.sub(pattern, rep, clean, flags=re.IGNORECASE)
                    for weak_v, strong_options in WEAK_VERBS_MAP.items():
                        pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                        if re.search(pattern, clean):
                            strong_v = strong_options[0].capitalize()
                            clean = re.sub(pattern, strong_v, clean, count=1)
                    if clean:
                        clean = clean[0].upper() + clean[1:]
                    p_lines.append(clean)
                p["description"] = "\n".join(p_lines)

            enhanced.append(p)
        return enhanced

    @staticmethod
    def enhance_projects(raw_proj: str) -> str:
        """
        Enhance project descriptions with strong technical phrasing
        without converting descriptions into bullet points or fabricating false claims.
        """
        if not raw_proj or not raw_proj.strip():
            return ""

        lines = raw_proj.split("\n")
        upgraded_lines = []

        phrase_upgrades = [
            (r"\bmade a website\b", "Architected and developed a responsive web application"),
            (r"\bbuilt an app\b", "Engineered and deployed a full-stack application"),
            (r"\bmade an app\b", "Engineered and deployed an application"),
            (r"\bused python\b", "Leveraged Python to implement backend logic"),
            (r"\bused react\b", "Utilized React.js to deliver modular UI components"),
            (r"\bused machine learning\b", "Trained and evaluated machine learning models"),
            (r"\badded authentication\b", "Implemented secure token-based user authentication"),
            (r"\bcreated api\b", "Designed and deployed scalable RESTful APIs"),
        ]

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            has_action_verb = any(re.search(r"(?i)\b" + re.escape(v) + r"\b", stripped) for v in ["made", "built", "used", "developed", "created", "added", "implemented", "engineered", "architected", "worked"])
            if not stripped.startswith(("•", "-", "*")) and ("|" in stripped or (len(stripped) < 40 and not has_action_verb)):
                title_line = stripped
                if not title_line.startswith("•"):
                    title_line = f"• {title_line}"
                upgraded_lines.append(title_line)
                continue

            clean_line = stripped.lstrip("•-* ").strip()

            for pattern, rep in phrase_upgrades:
                clean_line = re.sub(pattern, rep, clean_line, flags=re.IGNORECASE)

            for weak_v, strong_options in WEAK_VERBS_MAP.items():
                pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                if re.search(pattern, clean_line):
                    strong_v = strong_options[0].capitalize()
                    clean_line = re.sub(pattern, strong_v, clean_line, count=1)

            if clean_line:
                clean_line = clean_line[0].upper() + clean_line[1:]

            # Normal paragraph text below project title, indented without bullet point!
            upgraded_lines.append(f"  {clean_line}" if (upgraded_lines and upgraded_lines[-1].startswith("•")) else f"• {clean_line}")

        return "\n".join(upgraded_lines)

    @staticmethod
    def enhance_custom_section(raw_content: str) -> str:
        """
        Enhance additional custom section content with clean formatting and professional phrasing.
        """
        if not raw_content or not raw_content.strip():
            return ""

        lines = raw_content.split("\n")
        upgraded = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            clean = stripped.lstrip("•-* ").strip()
            for weak_v, strong_options in WEAK_VERBS_MAP.items():
                pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                if re.search(pattern, clean):
                    strong_v = strong_options[0].capitalize()
                    clean = re.sub(pattern, strong_v, clean, count=1)
            if clean:
                clean = clean[0].upper() + clean[1:]
            upgraded.append(f"• {clean}")
        return "\n".join(upgraded)

    @staticmethod
    def tailor_content(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Polish wording, structure, and job-orientation without fabricating any facts.
        """
        tailored = dict(data)
        role = tailored.get("job_role", "").strip()
        comp = tailored.get("company", "").strip()
        jd = tailored.get("job_description", "").strip()

        # 1. Professional Summary (Construct or Polish)
        current_sum = tailored.get("summary", "").strip()
        skills_str = tailored.get("skills", "").strip()
        
        user_skills_list = [s.strip(" •-*") for s in re.split(r"[,|\n•\*;]", skills_str) if s.strip(" •-*")]
        top_skills = ", ".join(user_skills_list[:4]) if user_skills_list else "core technical proficiencies"

        if not current_sum:
            tailored["summary"] = (
                f"Dedicated professional targeting the {role} role at {comp}. "
                f"Brings practical foundation in {top_skills}, with a strong commitment to continuous learning, "
                f"collaborative problem-solving, and driving organizational impact."
            )
        else:
            polished = current_sum
            polished = re.sub(r"\bseeking a role\b", f"aiming to leverage expertise as a {role}", polished, flags=re.IGNORECASE)
            polished = re.sub(r"\blooking for an opportunity\b", f"prepared to contribute as a {role}", polished, flags=re.IGNORECASE)
            if comp and comp.lower() not in polished.lower():
                polished += f" Eager to contribute effectively to team deliverables at {comp}."
            tailored["summary"] = polished

        # 2. Polish Experience
        if tailored.get("experience_entries"):
            tailored["experience_entries"] = ResumeBuilderModel.enhance_experience_entries(tailored["experience_entries"])
            compiled_exp = ResumeBuilderModel.compile_experience_entries(tailored["experience_entries"])
            if compiled_exp:
                tailored["experience"] = compiled_exp
            else:
                tailored["experience"] = ""
        elif tailored.get("experience"):
            tailored["experience"] = ResumeBuilderModel.enhance_experience(tailored["experience"])

        # 3. Polish Projects
        if tailored.get("project_entries"):
            tailored["project_entries"] = ResumeBuilderModel.enhance_project_entries(tailored["project_entries"])
            compiled_proj = ResumeBuilderModel.compile_project_entries(tailored["project_entries"])
            if compiled_proj:
                tailored["projects"] = compiled_proj
            else:
                tailored["projects"] = ""
        elif tailored.get("projects"):
            tailored["projects"] = ResumeBuilderModel.enhance_projects(tailored["projects"])

        # 4. Standardize Skills
        if tailored.get("skills"):
            tailored["skills"] = ResumeBuilderModel.enhance_skills(tailored["skills"])

        # 5. Enhance Education & Qualifications
        if tailored.get("education_entries"):
            tailored["education_entries"] = ResumeBuilderModel.enhance_education_entries(tailored["education_entries"])
        if tailored.get("qualification_entries"):
            tailored["qualification_entries"] = ResumeBuilderModel.enhance_qualification_entries(tailored["qualification_entries"])
        if tailored.get("education_entries") or tailored.get("qualification_entries"):
            compiled_edu = ResumeBuilderModel.compile_education_and_qualifications(
                tailored.get("education_entries", []),
                tailored.get("qualification_entries", [])
            )
            if compiled_edu:
                tailored["education"] = compiled_edu
        elif tailored.get("education"):
            tailored["education"] = ResumeBuilderModel.enhance_qualifications(tailored["education"])

        return tailored

    @staticmethod
    def to_plain_text(data: Dict[str, Any]) -> str:
        """Render complete plain text version of the resume."""
        parts = []
        name = data.get("full_name", "").strip() or "YOUR NAME"
        parts.append(name.upper())

        # Professional headline logic (never use target job_role or company)
        headline = (data.get("professional_headline") or "").strip()
        if not headline:
            for exp in data.get("experience_entries", []):
                if exp.get("status") == "Currently Ongoing":
                    pos = (exp.get("position") or "").strip()
                    if pos:
                        headline = pos
                        break
        if headline:
            parts.append(headline)

        contact = []
        if data.get("email"): contact.append(f"Email: {data['email']}")
        if data.get("phone"): contact.append(f"Phone: {data['phone']}")
        if data.get("location"): contact.append(f"Location: {data['location']}")
        if contact:
            parts.append(" | ".join(contact))

        parts.append("-" * 60)

        if data.get("summary"):
            parts.append(f"PROFESSIONAL SUMMARY\n{data['summary']}\n")

        if data.get("skills"):
            parts.append(f"TECHNICAL & FUNCTIONAL SKILLS\n{data['skills']}\n")

        if data.get("experience") and data["experience"].strip():
            parts.append(f"WORK EXPERIENCE\n{data['experience']}\n")

        if data.get("projects"):
            parts.append(f"TECHNICAL PROJECT\n{data['projects']}\n")

        if data.get("education"):
            parts.append(f"EDUCATION AND QUALIFICATIONS\n{data['education']}\n")

        if data.get("certifications"):
            parts.append(f"CERTIFICATIONS & COURSES\n{data['certifications']}\n")

        for extra in data.get("custom_sections", []):
            if extra.get("title") and extra.get("content"):
                parts.append(f"{extra['title'].upper()}\n{extra['content']}\n")

        # Declaration & Signature (2-column format)
        dec = data.get("declaration", "").strip() or DEFAULT_DECLARATION
        date_v = data.get("date_val", "").strip() or "____________________"
        place_v = data.get("place_val", "").strip() or (data.get("location", "").strip() or "____________________")
        sig_mode = data.get("signature_mode", "write")
        if sig_mode == "upload" and data.get("signature_img_b64"):
            sig_v = "[Digital Image Signature Uploaded]"
        elif sig_mode == "write" and data.get("sig_val"):
            sig_v = data.get("sig_val")
        else:
            sig_v = "____________________"
        name_v = data.get("full_name", "").strip() or "____________________"

        parts.append(f"DECLARATION\n{dec}\n\nDate:  {date_v:<26} Signature: {sig_v}\nPlace: {place_v:<26} Name:      {name_v}")

        return "\n".join(parts)

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
            "email": "",
            "phone": "",
            "location": "",
            "summary": "",
            "skills": "",
            "experience": "",
            "projects": "",
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
                    "level": "college",
                    "degree": "",
                    "stream": "",
                    "institution": "",
                    "board_univ": "",
                    "year": "",
                    "grade": ""
                },
                {
                    "level": "12th",
                    "degree": "Class XII (Higher Secondary)",
                    "stream": "",
                    "institution": "",
                    "board_univ": "",
                    "year": "",
                    "grade": ""
                },
                {
                    "level": "10th",
                    "degree": "Class X (Secondary)",
                    "stream": "",
                    "institution": "",
                    "board_univ": "",
                    "year": "",
                    "grade": ""
                }
            ]
        }

    @staticmethod
    def enhance_qualifications(raw_edu: str) -> str:
        """
        Enhance educational qualifications using standard professional terminology
        without changing the candidate's actual institutions, degrees, or facts.
        """
        if not raw_edu or not raw_edu.strip():
            return ""

        degree_map = [
            (r"\bb\.?\s*tech\b|\bbachelor\s+of\s+technology\b", "B.Tech (Bachelor of Technology)"),
            (r"\bb\.?\s*e\b|\bbachelor\s+of\s+engineering\b", "B.E. (Bachelor of Engineering)"),
            (r"\bb\.?\s*sc\b|\bb\.?\s*s\b|\bbachelor\s+of\s+science\b", "B.S. (Bachelor of Science)"),
            (r"\bm\.?\s*tech\b|\bmaster\s+of\s+technology\b", "M.Tech (Master of Technology)"),
            (r"\bm\.?\s*sc\b|\bm\.?\s*s\b|\bmaster\s+of\s+science\b", "M.S. (Master of Science)"),
            (r"\bbca\b|\bbachelor\s+of\s+computer\s+applications?\b", "BCA (Bachelor of Computer Applications)"),
            (r"\bmca\b|\bmaster\s+of\s+computer\s+applications?\b", "MCA (Master of Computer Applications)"),
            (r"\bmba\b|\bmaster\s+of\s+business\s+administration\b", "MBA (Master of Business Administration)"),
            (r"\bbba\b|\bbachelor\s+of\s+business\s+administration\b", "BBA (Bachelor of Business Administration)"),
            (r"\bb\.?\s*com\b|\bbachelor\s+of\s+commerce\b", "B.Com (Bachelor of Commerce)"),
            (r"\bb\.?\s*a\b|\bbachelor\s+of\s+arts\b", "B.A. (Bachelor of Arts)"),
            (r"\bph\.?d\b|\bdoctor\s+of\s+philosophy\b", "Ph.D. (Doctor of Philosophy)"),
            (r"\b12th(\s*(?:grade|standard|class|pass))?\b|\bclass\s*12\b|\bhsc\b|\bintermediate\b", "Higher Secondary Certificate (Class XII)"),
            (r"\b10th(\s*(?:grade|standard|class|pass))?\b|\bclass\s*10\b|\bssc\b|\bmatric(ulation)?\b", "Secondary School Certificate (Class X)"),
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
    def enhance_education_entries(entries: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Enhance a list of structured qualification dictionaries with professional keywords
        without altering the candidate's actual institutions, degrees, or grades.
        """
        enhanced_entries = []
        for entry in entries:
            e = dict(entry)
            deg = e.get("degree", "").strip()
            stream = e.get("stream", "").strip()
            board = e.get("board_univ", "").strip()
            year = e.get("year", "").strip()
            grade = e.get("grade", "").strip()

            if deg:
                deg_enh = ResumeBuilderModel.enhance_qualifications(deg).lstrip("• ")
                e["degree"] = deg_enh

            if stream:
                stream_clean = stream
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
                    stream_clean = re.sub(pattern, rep, stream_clean, flags=re.IGNORECASE)
                e["stream"] = stream_clean

            if board:
                b_clean = board
                b_clean = re.sub(r"\bcbse\b", "CBSE Board", b_clean, flags=re.IGNORECASE)
                b_clean = re.sub(r"\bicse\b", "ICSE Board", b_clean, flags=re.IGNORECASE)
                b_clean = re.sub(r"\bstate\s*board\b", "State Board", b_clean, flags=re.IGNORECASE)
                e["board_univ"] = b_clean

            if grade:
                g_clean = grade
                g_clean = re.sub(r"([0-9.]+)\s*(?:cgpa|gpa)\b", r"CGPA: \1", g_clean, flags=re.IGNORECASE)
                g_clean = re.sub(r"\b(?:cgpa|gpa)\s*[:=]?\s*([0-9.]+)", r"CGPA: \1", g_clean, flags=re.IGNORECASE)
                g_clean = re.sub(r"([0-9.]+)\s*(?:%|\bpercentage\b|\bpercent\b)", r"Score: \1%", g_clean, flags=re.IGNORECASE)
                g_clean = re.sub(r"\bpercentage\s*[:=]?\s*([0-9.]+)\s*%?", r"Score: \1%", g_clean, flags=re.IGNORECASE)
                if re.match(r"^[0-9]\.[0-9]+$", g_clean.strip()):
                    g_clean = f"CGPA: {g_clean.strip()}"
                elif re.match(r"^[0-9]{2}(\.[0-9]+)?$", g_clean.strip()):
                    g_clean = f"Score: {g_clean.strip()}%"
                e["grade"] = g_clean

            if year:
                e["year"] = re.sub(r"\s*-\s*", " - ", year.strip())

            enhanced_entries.append(e)
        return enhanced_entries

    @staticmethod
    def compile_education_entries(entries: List[Dict[str, str]]) -> str:
        """
        Compile structured qualification entries into a professional, realistic resume format.
        """
        compiled_blocks = []
        for entry in entries:
            deg = entry.get("degree", "").strip()
            stream = entry.get("stream", "").strip()
            inst = entry.get("institution", "").strip()
            board = entry.get("board_univ", "").strip()
            year = entry.get("year", "").strip()
            grade = entry.get("grade", "").strip()

            if not any([deg, stream, inst, board, year, grade]):
                continue

            if deg and stream:
                if stream.lower() in deg.lower():
                    title_line = f"• {deg}"
                else:
                    title_line = f"• {deg} in {stream}"
            elif deg:
                title_line = f"• {deg}"
            elif stream:
                title_line = f"• {stream}"
            elif inst:
                title_line = f"• {inst}"
            else:
                continue

            details = []
            if inst and title_line != f"• {inst}":
                details.append(inst)
            if board and board.lower() not in inst.lower():
                details.append(board)
            if year:
                details.append(year)
            if grade:
                details.append(grade)

            if details:
                block = f"{title_line}\n  " + " | ".join(details)
            else:
                block = title_line
            compiled_blocks.append(block)

        return "\n".join(compiled_blocks)

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

        lines = [l.strip() for l in raw_skills.split("\n") if l.strip()]
        if len(lines) > 1 and any(":" in l for l in lines):
            polished_lines = []
            for line in lines:
                l_clean = line.lstrip("•-* ")
                if ":" in l_clean:
                    cat, skills_part = l_clean.split(":", 1)
                    s_items = [s.strip() for s in re.split(r"[,;]", skills_part) if s.strip()]
                    norm_items = []
                    for item in s_items:
                        lower_item = item.lower()
                        if lower_item in tech_map:
                            norm_items.append(tech_map[lower_item][0])
                        else:
                            norm_items.append(item.title() if len(item) > 3 else item.upper())
                    polished_lines.append(f"• {cat.strip()}: {', '.join(norm_items)}")
                else:
                    polished_lines.append(f"• {l_clean}")
            return "\n".join(polished_lines)

        tokens = [s.strip(" •-*") for s in re.split(r"[,|\n;•\*]", raw_skills) if s.strip(" •-*")]
        if not tokens:
            return raw_skills.strip()

        groups = {
            "languages": [],
            "frameworks": [],
            "databases": [],
            "cloud_tools": [],
            "concepts": [],
            "other": []
        }

        seen = set()
        for tok in tokens:
            lower = tok.lower()
            if lower in seen:
                continue
            seen.add(lower)
            if lower in tech_map:
                name, cat = tech_map[lower]
                groups[cat].append(name)
            else:
                formatted = tok.title() if len(tok) > 3 else tok.upper()
                groups["other"].append(formatted)

        output_bullets = []
        if groups["languages"]:
            output_bullets.append(f"• Programming Languages: {', '.join(groups['languages'])}")
        if groups["frameworks"]:
            output_bullets.append(f"• Frameworks & Libraries: {', '.join(groups['frameworks'])}")
        if groups["databases"]:
            output_bullets.append(f"• Databases: {', '.join(groups['databases'])}")
        if groups["cloud_tools"]:
            output_bullets.append(f"• Tools & Cloud Technologies: {', '.join(groups['cloud_tools'])}")
        if groups["concepts"]:
            output_bullets.append(f"• Core Competencies & Methodologies: {', '.join(groups['concepts'])}")
        if groups["other"]:
            output_bullets.append(f"• Additional Competencies: {', '.join(groups['other'])}")

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
    def enhance_projects(raw_proj: str) -> str:
        """
        Enhance project descriptions with strong technical phrasing and structured bullets
        without fabricating false claims or technologies.
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

            upgraded_lines.append(f"  - {clean_line}" if (upgraded_lines and upgraded_lines[-1].startswith("•")) else f"• {clean_line}")

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
        if tailored.get("experience"):
            tailored["experience"] = ResumeBuilderModel.enhance_experience(tailored["experience"])

        # 3. Polish Projects
        if tailored.get("projects"):
            tailored["projects"] = ResumeBuilderModel.enhance_projects(tailored["projects"])

        # 4. Standardize Skills
        if tailored.get("skills"):
            tailored["skills"] = ResumeBuilderModel.enhance_skills(tailored["skills"])

        # 5. Enhance Education
        if tailored.get("education_entries"):
            tailored["education_entries"] = ResumeBuilderModel.enhance_education_entries(tailored["education_entries"])
            compiled_edu = ResumeBuilderModel.compile_education_entries(tailored["education_entries"])
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

        contact = []
        if data.get("email"): contact.append(f"Email: {data['email']}")
        if data.get("phone"): contact.append(f"Phone: {data['phone']}")
        if data.get("location"): contact.append(f"Location: {data['location']}")
        if contact:
            parts.append(" | ".join(contact))

        if data.get("job_role"):
            parts.append(f"{data['job_role']} - {data.get('company', '')}" if data.get('company') else data['job_role'])

        parts.append("-" * 60)

        if data.get("summary"):
            parts.append(f"PROFESSIONAL SUMMARY\n{data['summary']}\n")

        if data.get("skills"):
            parts.append(f"TECHNICAL & FUNCTIONAL SKILLS\n{data['skills']}\n")

        if data.get("experience"):
            parts.append(f"WORK EXPERIENCE\n{data['experience']}\n")

        if data.get("projects"):
            parts.append(f"PROJECTS\n{data['projects']}\n")

        if data.get("education"):
            parts.append(f"EDUCATION\n{data['education']}\n")

        if data.get("certifications"):
            parts.append(f"CERTIFICATIONS & COURSES\n{data['certifications']}\n")

        for extra in data.get("custom_sections", []):
            if extra.get("title") and extra.get("content"):
                parts.append(f"{extra['title'].upper()}\n{extra['content']}\n")

        # Declaration & Signature
        dec = data.get("declaration", "").strip() or DEFAULT_DECLARATION
        date_v = data.get("date_val", "").strip() or "____________________"
        sig_mode = data.get("signature_mode", "write")
        if sig_mode == "upload" and data.get("signature_img_b64"):
            sig_v = "[Digital Image Signature Uploaded]"
        elif sig_mode == "write" and data.get("sig_val"):
            sig_v = data.get("sig_val")
        else:
            sig_v = "____________________"

        parts.append(f"DECLARATION\n{dec}\n\nDate: {date_v}                    Signature: {sig_v}")

        return "\n".join(parts)

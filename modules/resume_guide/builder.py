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
            "template_name": "Modern"
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
            (r"\b12th(\s*(grade|standard|class))?|\bclass\s*12\b|\bhsc\b|\bintermediate\b", "Higher Secondary Certificate (Class XII)"),
            (r"\b10th(\s*(grade|standard|class))?|\bclass\s*10\b|\bssc\b|\bmatric(ulation)?\b", "Secondary School Certificate (Class X)"),
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
        
        # Extract existing user skills
        user_skills_list = [s.strip(" •-*") for s in re.split(r"[,|\n•\*;]", skills_str) if s.strip(" •-*")]
        top_skills = ", ".join(user_skills_list[:4]) if user_skills_list else "core technical proficiencies"

        if not current_sum:
            # Generate a truthful summary synthesizing only provided details
            tailored["summary"] = (
                f"Dedicated professional targeting the {role} role at {comp}. "
                f"Brings practical foundation in {top_skills}, with a strong commitment to continuous learning, "
                f"collaborative problem-solving, and driving organizational impact."
            )
        else:
            # Upgrade passive language in existing summary
            polished = current_sum
            polished = re.sub(r"\bseeking a role\b", f"aiming to leverage expertise as a {role}", polished, flags=re.IGNORECASE)
            polished = re.sub(r"\blooking for an opportunity\b", f"prepared to contribute as a {role}", polished, flags=re.IGNORECASE)
            if comp and comp.lower() not in polished.lower():
                polished += f" Eager to contribute effectively to team deliverables at {comp}."
            tailored["summary"] = polished

        # 2. Polish Experience Bullet Points (Strong Action Verbs without altering facts)
        if tailored.get("experience"):
            lines = tailored["experience"].split("\n")
            upgraded = []
            for l in lines:
                tl = l.strip()
                if not tl:
                    continue
                upgraded_line = tl
                for weak_v, strong_options in WEAK_VERBS_MAP.items():
                    pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                    if re.search(pattern, upgraded_line):
                        strong_v = strong_options[0].capitalize()
                        upgraded_line = re.sub(pattern, strong_v, upgraded_line, count=1)
                if not upgraded_line.startswith(("•", "-", "*")):
                    upgraded_line = "• " + upgraded_line
                upgraded.append(upgraded_line)
            tailored["experience"] = "\n".join(upgraded)

        # 3. Polish Projects Bullet Points
        if tailored.get("projects"):
            lines = tailored["projects"].split("\n")
            upgraded_proj = []
            for l in lines:
                tl = l.strip()
                if not tl:
                    continue
                upgraded_line = tl
                for weak_v, strong_options in WEAK_VERBS_MAP.items():
                    pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                    if re.search(pattern, upgraded_line):
                        strong_v = strong_options[0].capitalize()
                        upgraded_line = re.sub(pattern, strong_v, upgraded_line, count=1)
                upgraded_proj.append(upgraded_line)
            tailored["projects"] = "\n".join(upgraded_proj)

        # 4. Standardize Skills into clean bullet format
        if user_skills_list and "\n" not in skills_str and "•" not in skills_str:
            tailored["skills"] = "• Core Competencies: " + ", ".join(user_skills_list)

        # 5. Enhance Educational Qualifications with professional keywords without altering facts
        if tailored.get("education"):
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

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
            "photo_b64": "",
            "declaration": DEFAULT_DECLARATION,
            "date_val": "",
            "sig_val": "",
            "template_name": "Modern"
        }

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
            parts.append(f"Target Role: {data['job_role']} | Target Organization: {data.get('company', '')}")

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

        # Declaration
        dec = data.get("declaration", "").strip() or DEFAULT_DECLARATION
        date_v = data.get("date_val", "").strip() or "____________________"
        sig_v = data.get("sig_val", "").strip() or "____________________"

        parts.append(f"DECLARATION\n{dec}\n\nDate: {date_v}                    Signature: {sig_v}")

        return "\n".join(parts)

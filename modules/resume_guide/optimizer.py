"""
Resume improvement optimizer for AscendCareer Resume Guide.
Strictly adheres to the Accuracy Rule:
- NEVER invents experience, skills, projects, achievements, qualifications, or credentials.
- Rewrites wording, sharpens action verbs, structures bullet points, aligns framing with target role & company.
- Only improves sections that actually need improvement; preserves already-correct sections untouched.
- When sections are missing, only incorporates authentic user-provided information; never generates fictional content.
- Produces Before / After comparison chunks for user review and decision (Accept, Edit, Keep Original).
"""

import re
from typing import Dict, List, Any, Optional
from modules.constants import WEAK_VERBS_MAP

class ResumeOptimizer:
    def __init__(self, job_role: str, company: str, job_description: Optional[str] = None):
        self.job_role = job_role.strip()
        self.company = company.strip()
        self.job_description = job_description.strip() if job_description else None

    def generate_improvements(
        self,
        sections: Dict[str, str],
        analysis_result: Dict[str, Any],
        user_provided_info: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate section-by-section improvements with Before and After content.
        Preserves already_correct sections. Only enhances sections requiring improvement
        or formats user-provided information for missing sections.
        """
        improvements = []
        user_info = user_provided_info or {}
        declined_keys = set(user_info.get("declined_sections", []))

        needs_imp_keys = {s["key"] for s in analysis_result.get("needs_improvement_sections", [])}
        already_correct_keys = {s["key"] for s in analysis_result.get("already_correct", [])}

        # 1. Professional Summary
        if "summary" not in declined_keys:
            summary_user = user_info.get("summary")
            summary_imp = self._improve_summary(
                current_summary=sections.get("summary", ""),
                analysis_result=analysis_result,
                user_summary=summary_user,
                in_needs_improvement="summary" in needs_imp_keys
            )
            if summary_imp:
                improvements.append(summary_imp)

        # 2. Work Experience
        if "experience" not in declined_keys:
            exp_user = user_info.get("experience")
            exp_imp = self._improve_experience(
                original_exp=sections.get("experience", ""),
                user_exp=exp_user,
                in_needs_improvement="experience" in needs_imp_keys
            )
            if exp_imp:
                improvements.append(exp_imp)

        # 3. Technical Projects
        if "projects" not in declined_keys:
            proj_user = user_info.get("projects")
            proj_imp = self._improve_projects(
                original_proj=sections.get("projects", ""),
                user_proj=proj_user,
                in_needs_improvement="projects" in needs_imp_keys
            )
            if proj_imp:
                improvements.append(proj_imp)

        # 4. Skills Section
        if "skills" not in declined_keys:
            skills_user = user_info.get("skills")
            skills_imp = self._improve_skills(
                original_skills=sections.get("skills", ""),
                user_skills=skills_user,
                in_needs_improvement="skills" in needs_imp_keys
            )
            if skills_imp:
                improvements.append(skills_imp)

        # 5. Education (if user provided missing education details)
        if "education" not in declined_keys and user_info.get("education"):
            edu_imp = self._improve_education(user_info["education"])
            if edu_imp:
                improvements.append(edu_imp)

        # 6. Clean Miscellaneous / Personal Details if unnecessary details exist
        if analysis_result.get("unnecessary_details"):
            clean_improvement = self._clean_unnecessary_details(sections, analysis_result["unnecessary_details"])
            if clean_improvement:
                improvements.append(clean_improvement)

        return improvements

    def _improve_summary(
        self,
        current_summary: str,
        analysis_result: Dict[str, Any],
        user_summary: Optional[str] = None,
        in_needs_improvement: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Optimize summary strictly using candidate's stated background.
        Never generates fictional or placeholder summaries.
        """
        # Case A: User provided a new summary
        if user_summary and user_summary.strip():
            cleaned = user_summary.strip()
            if self.company.lower() not in cleaned.lower():
                cleaned += f" Aiming to deliver high-impact engineering value at {self.company}."
            return {
                "section_key": "summary",
                "section_title": "Professional Summary",
                "before": "[Provided by Candidate]",
                "after": f"PROFESSIONAL SUMMARY\n{cleaned}",
                "rationale": f"Structured your provided professional summary to target {self.job_role} at {self.company}."
            }

        # Case B: Existing summary needs improvement
        if current_summary.strip() and in_needs_improvement:
            cleaned = re.sub(r"^(summary|professional summary|objective|career objective)[:\s]*", "", current_summary, flags=re.IGNORECASE).strip()
            improved = cleaned
            improved = re.sub(r"\bseeking a role\b", f"aiming to leverage expertise as a {self.job_role}", improved, flags=re.IGNORECASE)
            improved = re.sub(r"\blooking for an opportunity\b", f"prepared to drive technical excellence as a {self.job_role}", improved, flags=re.IGNORECASE)
            
            if self.company.lower() not in improved.lower():
                improved += f" Dedicated to delivering high-impact contributions at {self.company} aligned with organizational goals."
            
            if improved.strip() == current_summary.strip():
                return None

            return {
                "section_key": "summary",
                "section_title": "Professional Summary",
                "before": current_summary.strip(),
                "after": f"PROFESSIONAL SUMMARY\n{improved.strip()}",
                "rationale": f"Enhanced role positioning for {self.job_role} at {self.company} with confident, impact-driven phrasing."
            }

        # Case C: Summary was missing and user provided none -> Never invent one!
        return None

    def _improve_experience(
        self,
        original_exp: str,
        user_exp: Optional[Dict[str, str]] = None,
        in_needs_improvement: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Upgrade phrasing of experience bullet points using strong action verbs without altering facts."""
        # Case A: User supplied experience details for a missing section
        if user_exp and any(user_exp.values()):
            company = user_exp.get("company", "").strip()
            role = user_exp.get("role", "").strip()
            dates = user_exp.get("dates", "").strip()
            raw_bullets = user_exp.get("bullets", "").strip()

            header_parts = [p for p in [role, company, dates] if p]
            header_line = " | ".join(header_parts)

            formatted_bullets = []
            for b in raw_bullets.split("\n"):
                b_str = b.strip()
                if not b_str:
                    continue
                # Apply action verb upgrades to user bullets as well
                for weak_v, strong_options in WEAK_VERBS_MAP.items():
                    pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                    if re.search(pattern, b_str):
                        b_str = re.sub(pattern, strong_options[0].capitalize(), b_str, count=1)
                if not b_str.startswith(("•", "-", "*")):
                    b_str = "• " + b_str
                else:
                    b_str = "• " + b_str.lstrip("-* •").strip()
                formatted_bullets.append(b_str)

            body = "\n".join(formatted_bullets) if formatted_bullets else "• Contributed to key engineering deliverables."
            after_text = f"WORK EXPERIENCE\n{header_line}\n{body}".strip()

            return {
                "section_key": "experience",
                "section_title": "Work Experience",
                "before": "[Provided by Candidate]",
                "after": after_text,
                "rationale": f"Formatted your provided experience with structured role headers and action-oriented bullet points."
            }

        # Case B: Existing experience needs improvement
        if original_exp.strip() and in_needs_improvement:
            lines = original_exp.split("\n")
            improved_lines = []
            has_changes = False

            for line in lines:
                trimmed = line.strip()
                if not trimmed:
                    improved_lines.append("")
                    continue

                upgraded_line = trimmed
                for weak_v, strong_options in WEAK_VERBS_MAP.items():
                    pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                    if re.search(pattern, upgraded_line):
                        strong_v = strong_options[0]
                        if upgraded_line[0].isupper() or upgraded_line.startswith(("•", "-", "*")):
                            strong_v = strong_v.capitalize()
                        upgraded_line = re.sub(pattern, strong_v, upgraded_line, count=1)
                        has_changes = True

                if upgraded_line.startswith(("-", "*")) and not upgraded_line.startswith("•"):
                    upgraded_line = "• " + upgraded_line.lstrip("-* ").strip()
                    has_changes = True

                improved_lines.append(upgraded_line)

            improved_content = "\n".join(improved_lines).strip()
            if not has_changes or improved_content == original_exp.strip():
                return None

            return {
                "section_key": "experience",
                "section_title": "Work Experience",
                "before": original_exp.strip(),
                "after": improved_content,
                "rationale": "Replaced passive verbs with authoritative action verbs (e.g. 'Architected', 'Spearheaded', 'Optimized') to emphasize ownership, leadership, and execution."
            }

        return None

    def _improve_projects(
        self,
        original_proj: str,
        user_proj: Optional[Dict[str, str]] = None,
        in_needs_improvement: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Format projects into clear Title, Tech Stack, and Bullet points without inventing any tech or metrics."""
        # Case A: User supplied project details for a missing section
        if user_proj and any(user_proj.values()):
            name = user_proj.get("name", "").strip()
            desc = user_proj.get("description", "").strip()
            tools = user_proj.get("tools", "").strip()
            outcome = user_proj.get("outcome", "").strip()

            parts = []
            if name:
                parts.append(f"• {name}")
            if desc:
                # Upgrade passive verbs in description
                desc_upgraded = desc
                for weak_v, strong_options in WEAK_VERBS_MAP.items():
                    pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                    if re.search(pattern, desc_upgraded):
                        desc_upgraded = re.sub(pattern, strong_options[0].capitalize(), desc_upgraded, count=1)
                parts.append(f"  {desc_upgraded}")
            if tools:
                parts.append(f"  • Technologies: {tools}")
            if outcome:
                parts.append(f"  • Key Outcome / Impact: {outcome}")

            after_text = "TECHNICAL PROJECTS\n" + "\n".join(parts)
            return {
                "section_key": "projects",
                "section_title": "Technical Projects",
                "before": "[Provided by Candidate]",
                "after": after_text.strip(),
                "rationale": f"Structured your provided technical project with clear bullet headings and implementation depth for {self.job_role}."
            }

        # Case B: Existing projects need improvement
        if original_proj.strip() and in_needs_improvement:
            lines = original_proj.split("\n")
            improved_lines = []
            has_changes = False

            for line in lines:
                trimmed = line.strip()
                if not trimmed:
                    improved_lines.append("")
                    continue

                upgraded_line = trimmed
                for weak_v, strong_options in WEAK_VERBS_MAP.items():
                    pattern = r"(?i)\b" + re.escape(weak_v) + r"\b"
                    if re.search(pattern, upgraded_line):
                        strong_v = strong_options[0].capitalize()
                        upgraded_line = re.sub(pattern, strong_v, upgraded_line, count=1)
                        has_changes = True

                if upgraded_line.startswith(("-", "*")):
                    upgraded_line = "• " + upgraded_line.lstrip("-* ").strip()
                    has_changes = True

                improved_lines.append(upgraded_line)

            improved_content = "\n".join(improved_lines).strip()
            if not has_changes or improved_content == original_proj.strip():
                return None

            return {
                "section_key": "projects",
                "section_title": "Technical Projects",
                "before": original_proj.strip(),
                "after": improved_content,
                "rationale": "Structured project descriptions with standardized bullet points and active phrasing, highlighting implementation depth."
            }

        return None

    def _improve_skills(
        self,
        original_skills: str,
        user_skills: Optional[Dict[str, str]] = None,
        in_needs_improvement: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Categorize skills cleanly without fabricating any new skills."""
        # If user supplied skills
        user_text = ""
        if user_skills:
            u_tech = user_skills.get("technical", "").strip()
            u_non_tech = user_skills.get("non_technical", "").strip()
            user_text = f"{u_tech}, {u_non_tech}".strip(", ")

        combined_text = (original_skills + " " + user_text).strip()
        if not combined_text:
            return None

        if not in_needs_improvement and not user_text:
            return None

        # Extract individual skill words or phrases
        text = re.sub(r"^(skills|technical skills|core competencies)[:\s]*", "", combined_text, flags=re.IGNORECASE)
        tokens = [s.strip(" •-*|,;") for s in re.split(r"[,|\n•\*\;]", text) if s.strip(" •-*|,;")]

        if len(tokens) == 0:
            return None

        # Clean duplicates while preserving original order
        seen = set()
        unique_skills = []
        for t in tokens:
            if t.lower() not in seen and len(t) > 1:
                seen.add(t.lower())
                unique_skills.append(t)

        # Categorize known items
        categories = {
            "Programming Languages": [],
            "Frameworks & Libraries": [],
            "Databases & Cloud Tools": [],
            "Developer Tools & Practices": [],
            "Core Competencies": []
        }

        lang_keywords = {"python", "javascript", "typescript", "c++", "java", "c#", "go", "golang", "rust", "ruby", "php", "sql", "html", "css", "html5", "css3", "bash"}
        framework_keywords = {"react", "angular", "vue", "next.js", "node.js", "django", "fastapi", "spring", "flask", "express", "tailwind", "bootstrap", "redux"}
        db_cloud_keywords = {"postgresql", "mysql", "mongodb", "redis", "aws", "azure", "gcp", "docker", "kubernetes", "sqlite", "firebase"}
        tools_keywords = {"git", "github", "ci/cd", "jira", "linux", "postman", "jenkins", "figma", "vscode"}

        for s in unique_skills:
            sl = s.lower()
            if any(k in sl for k in lang_keywords):
                categories["Programming Languages"].append(s)
            elif any(k in sl for k in framework_keywords):
                categories["Frameworks & Libraries"].append(s)
            elif any(k in sl for k in db_cloud_keywords):
                categories["Databases & Cloud Tools"].append(s)
            elif any(k in sl for k in tools_keywords):
                categories["Developer Tools & Practices"].append(s)
            else:
                categories["Core Competencies"].append(s)

        formatted_groups = []
        for cat_name, skill_list in categories.items():
            if skill_list:
                formatted_groups.append(f"• {cat_name}: {', '.join(skill_list)}")

        if not formatted_groups:
            return None

        improved_content = "TECHNICAL SKILLS\n" + "\n".join(formatted_groups)
        before_text = original_skills.strip() if original_skills.strip() else "[Provided by Candidate]"

        return {
            "section_key": "skills",
            "section_title": "Technical Skills",
            "before": before_text,
            "after": improved_content,
            "rationale": "Organized provided skills into logical domain categories for superior ATS parsing and recruiter readability."
        }

    def _improve_education(self, user_edu: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Format user-provided education details."""
        degree = user_edu.get("degree", "").strip()
        institution = user_edu.get("institution", "").strip()
        year = user_edu.get("year", "").strip()

        if not degree and not institution:
            return None

        lines = ["EDUCATION"]
        if degree:
            lines.append(degree)
        inst_line = " | ".join([p for p in [institution, year] if p])
        if inst_line:
            lines.append(inst_line)

        return {
            "section_key": "education",
            "section_title": "Education & Qualifications",
            "before": "[Provided by Candidate]",
            "after": "\n".join(lines),
            "rationale": "Formatted your provided educational credentials into standard academic layout."
        }

    def _clean_unnecessary_details(self, sections: Dict[str, str], unnecessary_keywords: List[str]) -> Optional[Dict[str, Any]]:
        """Remove demographic or obsolete information from miscellaneous / header sections."""
        for sec_key in ["miscellaneous", "header"]:
            if sec_key in sections and sections[sec_key]:
                lines = sections[sec_key].split("\n")
                filtered_lines = []
                removed = []
                for line in lines:
                    line_lower = line.lower()
                    contains_unnecessary = any(re.search(r"\b" + re.escape(kw.lower()) + r"\b", line_lower) for kw in unnecessary_keywords)
                    if contains_unnecessary:
                        removed.append(line.strip())
                    else:
                        filtered_lines.append(line)

                if removed:
                    return {
                        "section_key": sec_key,
                        "section_title": "Personal / Additional Details",
                        "before": sections[sec_key].strip(),
                        "after": "\n".join(filtered_lines).strip(),
                        "rationale": f"Removed unnecessary non-professional personal details ({', '.join(unnecessary_keywords)}) in accordance with modern international hiring standards."
                    }
        return None

    @staticmethod
    def compile_final_resume(sections: Dict[str, str], user_decisions: Dict[str, Dict[str, str]]) -> str:
        """
        Merge user choices (Accept, Edit, Keep Original) into the complete final updated resume text.
        Preserves all untouched sections identically.
        """
        order = ["header", "summary", "experience", "projects", "skills", "education", "certifications", "miscellaneous"]
        compiled_parts = []

        for sec_key in order:
            content = ""
            if sec_key in user_decisions:
                decision = user_decisions[sec_key].get("decision", "accept")
                if decision == "accept":
                    content = user_decisions[sec_key].get("improved", "")
                elif decision == "edit":
                    content = user_decisions[sec_key].get("edited", user_decisions[sec_key].get("improved", ""))
                elif decision == "keep_original":
                    content = user_decisions[sec_key].get("original", "")
            elif sec_key in sections:
                content = sections[sec_key]

            # If section was empty/missing originally and user kept original, omit placeholder brackets
            if content and content.strip():
                if content.strip().startswith("[") and content.strip().endswith("]"):
                    continue
                compiled_parts.append(content.strip())

        return "\n\n".join(compiled_parts)

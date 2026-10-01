"""
Core analysis engine for AscendCareer Resume Guide.
Evaluates resume suitability against target job role, target company, and optional job description.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from modules.constants import (
    ROLE_SKILL_DATABASE,
    WEAK_VERBS_MAP,
    UNNECESSARY_DETAILS_KEYWORDS
)

class ResumeAnalyzer:
    def __init__(self, job_role: str, company: str, job_description: Optional[str] = None):
        self.job_role = job_role.strip()
        self.company = company.strip()
        self.job_description = job_description.strip() if job_description else None

    def analyze(self, resume_text: str, sections: Dict[str, str]) -> Dict[str, Any]:
        """Perform comprehensive resume match analysis."""
        resume_lower = resume_text.lower()
        role_lower = self.job_role.lower()

        # 1. Identify target skills for role and JD
        expected_skills = self._get_expected_skills(role_lower, self.job_description)
        matched_skills, missing_skills = self._match_skills(resume_lower, expected_skills)

        # 2. Evaluate Projects Relevance
        project_eval = self._evaluate_projects(sections.get("projects", ""), matched_skills, role_lower)

        # 3. Evaluate Experience Relevance
        experience_eval = self._evaluate_experience(sections.get("experience", ""), role_lower)

        # 4. Check for Unnecessary Details
        unnecessary_details = self._detect_unnecessary_details(resume_lower)

        # 5. Check Structure & Job-orientation
        job_oriented_check = self._evaluate_job_orientation(resume_lower, sections, role_lower, self.company.lower())

        # 6. Calculate Alignment Scores
        role_alignment_score = self._calculate_role_score(
            matched_skills=matched_skills,
            expected_skills=expected_skills,
            project_eval=project_eval,
            experience_eval=experience_eval,
            job_oriented=job_oriented_check["is_job_oriented"]
        )

        jd_alignment_score = None
        jd_match_details = None
        if self.job_description:
            jd_alignment_score, jd_match_details = self._calculate_jd_alignment(resume_lower, self.job_description)

        # 7. Determine Suitability & Status
        is_well_aligned = (
            role_alignment_score >= 82 and
            len(missing_skills) <= 2 and
            project_eval["score"] >= 75 and
            experience_eval["score"] >= 75 and
            not unnecessary_details
        )

        # 8. Section-wise Feedback
        section_feedback = self._generate_section_feedback(
            sections=sections,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            project_eval=project_eval,
            experience_eval=experience_eval,
            unnecessary_details=unnecessary_details
        )

        # 9. Determine High-Level Areas (Only relevant ones!)
        high_level_areas = []
        if missing_skills:
            high_level_areas.append("Add relevant skills")
        if experience_eval.get("weak_verb_count", 0) > 0 or (experience_eval.get("has_experience", False) and not experience_eval.get("has_metrics", False)) or role_alignment_score < 80:
            high_level_areas.append("Improve job-related keywords")
        if project_eval.get("score", 0) < 80 or not project_eval.get("has_projects", False):
            high_level_areas.append("Highlight relevant projects")
        if unnecessary_details:
            high_level_areas.append("Remove outdated personal details")
        if not sections.get("summary"):
            high_level_areas.append("Add targeted professional summary")

        # 10. Personalized Suggestions (dynamic, non-generic)
        suggestions = self._generate_dynamic_suggestions(
            role_alignment_score=role_alignment_score,
            missing_skills=missing_skills,
            matched_skills=matched_skills,
            project_eval=project_eval,
            experience_eval=experience_eval,
            unnecessary_details=unnecessary_details,
            sections=sections
        )

        return {
            "job_role": self.job_role,
            "company": self.company,
            "has_jd": bool(self.job_description),
            "role_alignment_score": role_alignment_score,
            "jd_alignment_score": jd_alignment_score,
            "jd_match_details": jd_match_details,
            "is_well_aligned": is_well_aligned,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "project_relevance": project_eval,
            "experience_relevance": experience_eval,
            "unnecessary_details": unnecessary_details,
            "job_oriented_check": job_oriented_check,
            "section_feedback": section_feedback,
            "high_level_areas": high_level_areas,
            "suggestions": suggestions,
        }

    def _get_expected_skills(self, role_lower: str, jd_text: Optional[str]) -> List[str]:
        """Collect relevant skills based on role database or dynamic extraction."""
        skills = set()
        
        # Check predefined database
        found_exact = False
        for db_role, role_skills in ROLE_SKILL_DATABASE.items():
            if db_role in role_lower or role_lower in db_role:
                skills.update(role_skills)
                found_exact = True

        # If custom role or not exact match, dynamically extract keywords from role title
        if not found_exact:
            tokens = re.findall(r"\b[a-zA-Z\+\#]{2,}\b", role_lower)
            for token in tokens:
                if token not in ["engineer", "developer", "analyst", "specialist", "lead", "senior", "junior", "manager"]:
                    skills.add(token)
            # Default fundamental tech skills if none found
            if not skills:
                skills.update(["problem solving", "git", "communication", "team collaboration", "project management"])

        # Extract from JD if provided
        if jd_text:
            jd_lower = jd_text.lower()
            # Extract common tech keywords mentioned in JD
            common_tech_lexicon = [
                "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust", "ruby", "php",
                "react", "angular", "vue", "next.js", "node.js", "django", "fastapi", "spring", "flask",
                "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "kafka",
                "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "terraform", "linux",
                "rest api", "graphql", "microservices", "agile", "scrum", "git", "unit testing"
            ]
            for kw in common_tech_lexicon:
                if re.search(r"\b" + re.escape(kw) + r"\b", jd_lower):
                    skills.add(kw)

        return sorted(list(skills))

    def _match_skills(self, resume_lower: str, expected_skills: List[str]) -> Tuple[List[str], List[str]]:
        matched = []
        missing = []
        for skill in expected_skills:
            # Handle special characters like c++, c#
            pattern = r"(?:\b|_)" + re.escape(skill) + r"(?:\b|_)"
            if skill in ["c++", "c#"]:
                pattern = re.escape(skill)
            if re.search(pattern, resume_lower):
                matched.append(skill)
            else:
                missing.append(skill)
        return matched, missing

    def _evaluate_projects(self, projects_text: str, matched_skills: List[str], role_lower: str) -> Dict[str, Any]:
        if not projects_text.strip():
            return {
                "has_projects": False,
                "score": 40,
                "skills_in_projects": [],
                "has_metrics": False,
                "has_links": False,
                "summary": "No dedicated Projects section was identified in the resume.",
                "details": "Adding relevant personal or academic projects demonstrates practical capability for " + self.job_role + "."
            }

        text_lower = projects_text.lower()
        # Check how many matched skills appear in projects
        skills_in_projects = [s for s in matched_skills if s in text_lower]
        has_metrics = bool(re.search(r"\b\d+([%kKmM\+]|\s*(users|requests|ms|seconds|fps|stars|downloads|efficiency))\b", projects_text))
        has_github_or_demo = bool(re.search(r"(github\.com|gitlab\.com|demo|deployed|live|link|http)", text_lower))

        score = 60
        if skills_in_projects:
            score += min(25, len(skills_in_projects) * 5)
        if has_metrics:
            score += 10
        if has_github_or_demo:
            score += 5
        score = min(100, score)

        summary = f"Projects demonstrate application of {len(skills_in_projects)} relevant technologies."
        if has_metrics:
            summary += " Quantitative outcomes were identified."
        else:
            summary += " Could be strengthened with measurable results (e.g. latency, scale, active users)."

        return {
            "has_projects": True,
            "score": score,
            "skills_in_projects": skills_in_projects,
            "has_metrics": has_metrics,
            "has_links": has_github_or_demo,
            "summary": summary
        }

    def _evaluate_experience(self, exp_text: str, role_lower: str) -> Dict[str, Any]:
        if not exp_text.strip():
            return {
                "has_experience": False,
                "score": 50,
                "weak_verb_count": 0,
                "found_weak_verbs": [],
                "has_metrics": False,
                "summary": "No professional experience section found. (If applying as entry-level/fresher, highlight project outcomes and internships)."
            }

        text_lower = exp_text.lower()
        # Find weak verbs
        found_weak_verbs = []
        for weak_v in WEAK_VERBS_MAP.keys():
            if re.search(r"\b" + re.escape(weak_v) + r"\b", text_lower):
                found_weak_verbs.append(weak_v)

        has_metrics = bool(re.search(r"\b\d+([%kKmM\+]|\s*(users|clients|revenue|latency|team|members|tasks))\b", exp_text))

        score = 70
        if has_metrics:
            score += 15
        if not found_weak_verbs:
            score += 15
        else:
            score -= min(20, len(found_weak_verbs) * 5)
        score = max(30, min(100, score))

        summary = "Experience highlights professional contributions."
        if found_weak_verbs:
            summary += f" Contains passive verbs like '{found_weak_verbs[0]}' which can be upgraded to high-impact action verbs."
        if not has_metrics:
            summary += " Lacks quantitative business impact or measurable results."

        return {
            "has_experience": True,
            "score": score,
            "weak_verb_count": len(found_weak_verbs),
            "found_weak_verbs": found_weak_verbs,
            "has_metrics": has_metrics,
            "summary": summary
        }

    def _detect_unnecessary_details(self, resume_lower: str) -> List[str]:
        flagged = []
        for kw in UNNECESSARY_DETAILS_KEYWORDS:
            if re.search(r"\b" + re.escape(kw) + r"\b", resume_lower):
                flagged.append(kw.title())
        return flagged

    def _evaluate_job_orientation(self, resume_lower: str, sections: Dict[str, str], role_lower: str, company_lower: str) -> Dict[str, Any]:
        role_tokens = [t for t in re.findall(r"\b[a-zA-Z]{3,}\b", role_lower) if t not in ["the", "and", "for"]]
        role_mentions = sum(1 for t in role_tokens if t in resume_lower)
        is_job_oriented = role_mentions >= max(1, len(role_tokens) // 2)

        return {
            "is_job_oriented": is_job_oriented,
            "role_mentions_count": role_mentions,
            "mentions_company_domain": bool(company_lower in resume_lower)
        }

    def _calculate_role_score(self, matched_skills, expected_skills, project_eval, experience_eval, job_oriented) -> int:
        if not expected_skills:
            skill_score = 80
        else:
            skill_score = min(100, int((len(matched_skills) / len(expected_skills)) * 100))

        score = (
            (skill_score * 0.40) +
            (project_eval["score"] * 0.25) +
            (experience_eval["score"] * 0.25) +
            (10 if job_oriented else 0)
        )
        return int(max(25, min(98, score)))

    def _calculate_jd_alignment(self, resume_lower: str, jd_text: str) -> Tuple[int, Dict[str, Any]]:
        # Extract meaningful terms from JD (ignore stop words)
        stop_words = {"the", "and", "to", "of", "a", "in", "is", "that", "for", "with", "as", "are", "on", "be", "this", "by", "at", "or", "from"}
        jd_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", jd_text.lower())) - stop_words
        
        if not jd_words:
            return 80, {"matched_keywords": [], "missing_keywords": []}

        matched_kw = [w for w in jd_words if w in resume_lower]
        missing_kw = [w for w in jd_words if w not in resume_lower]

        ratio = len(matched_kw) / len(jd_words)
        score = int(min(98, max(30, ratio * 100 + 15)))

        return score, {
            "total_jd_keywords": len(jd_words),
            "matched_count": len(matched_kw),
            "missing_sample": missing_kw[:8]
        }

    def _generate_section_feedback(self, sections: Dict[str, str], matched_skills, missing_skills, project_eval, experience_eval, unnecessary_details) -> Dict[str, str]:
        feedback = {}

        # Summary
        if "summary" in sections:
            feedback["Professional Summary"] = "Summary is present. Ensure it explicitly targets the " + self.job_role + " role and states your core domain strengths."
        else:
            feedback["Professional Summary"] = "No professional summary detected. A concise 2-3 sentence overview targeting " + self.job_role + " helps establish immediate relevance."

        # Skills
        if "skills" in sections:
            if missing_skills:
                feedback["Skills"] = f"Detected {len(matched_skills)} relevant skills. Missing critical target skills: {', '.join(missing_skills[:5])}."
            else:
                feedback["Skills"] = f"Excellent skill coverage for {self.job_role}. {len(matched_skills)} core competencies identified."
        else:
            feedback["Skills"] = "No explicit Skills section found. Grouping technical and functional competencies into categorized subsections is strongly advised."

        # Experience
        if "experience" in sections:
            feedback["Work Experience"] = experience_eval["summary"]
        else:
            feedback["Work Experience"] = "No work experience section found. If you have internship or freelance work, include it with quantified accomplishments."

        # Projects
        if "projects" in sections:
            feedback["Projects"] = project_eval["summary"]
        else:
            feedback["Projects"] = "No dedicated projects section. Projects are essential for demonstrating hands-on ability for " + self.job_role + "."

        # Education
        if "education" in sections:
            feedback["Education"] = "Education section is structured properly."
        else:
            feedback["Education"] = "Ensure degrees, universities, and graduation dates are clearly listed."

        # Personal / Unnecessary Details
        if unnecessary_details:
            feedback["Personal Details"] = f"Contains unnecessary personal information ({', '.join(unnecessary_details)}) which should be removed to follow modern hiring standards."

        return feedback

    def _generate_dynamic_suggestions(self, role_alignment_score: int, missing_skills: List[str], matched_skills: List[str], project_eval: Dict, experience_eval: Dict, unnecessary_details: List[str], sections: Dict[str, str]) -> List[Dict[str, str]]:
        suggestions = []

        if missing_skills:
            suggestions.append({
                "title": f"Incorporate Missing Core Skills for {self.job_role}",
                "category": "Skills & Keywords",
                "observation": f"The resume does not mention: {', '.join(missing_skills[:6])}.",
                "recommendation": f"If you have hands-on experience or coursework in these areas, explicitly list them in your technical skills or reference them in your project bullet points."
            })

        if experience_eval.get("found_weak_verbs"):
            suggestions.append({
                "title": "Upgrade Passive Phrases to High-Impact Action Verbs",
                "category": "Impact & Presentation",
                "observation": f"Found weak passive phrasing such as: {', '.join(experience_eval['found_weak_verbs'])}.",
                "recommendation": "Begin experience bullet points with strong power verbs like 'Architected', 'Spearheaded', 'Optimized', or 'Engineered' to convey ownership and initiative."
            })

        if experience_eval.get("has_experience", False) and not experience_eval.get("has_metrics", False):
            suggestions.append({
                "title": "Quantify Achievements with Data & Scale",
                "category": "Accomplishments",
                "observation": "Bullet points primarily list duties rather than measurable results.",
                "recommendation": "Use numbers, percentages, or scale metrics where applicable (e.g., 'improved query performance by 35%', 'supported 10,000+ daily active users')."
            })

        if project_eval.get("has_projects", False) and not project_eval.get("has_metrics", False):
            suggestions.append({
                "title": "Add Measurable Scope to Projects",
                "category": "Project Relevance",
                "observation": "Projects lack clear outcome or scale indicators.",
                "recommendation": "Specify the problem solved, tech stack utilized, and the tangible outcome or deployment link (e.g., live URL or GitHub repo)."
            })

        if unnecessary_details:
            suggestions.append({
                "title": "Remove Non-Job-Related Personal Attributes",
                "category": "ATS & Modern Formatting",
                "observation": f"The resume includes demographic fields: {', '.join(unnecessary_details)}.",
                "recommendation": "Remove personal demographic data (DOB, marital status, religion) to comply with international hiring standards and protect candidate privacy."
            })

        if "summary" not in sections:
            suggestions.append({
                "title": f"Introduce a Tailored Professional Summary",
                "category": "Role Positioning",
                "observation": "There is no executive summary at the top of the resume.",
                "recommendation": f"Add a sharp 2-3 line summary framing your profile as a '{self.job_role}' aiming to contribute to {self.company}."
            })

        return suggestions

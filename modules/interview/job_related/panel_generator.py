"""
AchieveHire — Interviewer Panel Generator
Generates realistic professional interview panels based on:
1. Target Job Role (e.g., Software Engineer, Product Manager, Data Scientist)
2. Target Company (e.g., Google, Microsoft, Amazon, or custom company)
3. Round Seniority Progression:
   - Round 1: 1 Initial/Early Interviewer
   - Round 2: 2 Mid-Level Professional Interviewers
   - Round 3: 2 Experienced Domain Specialists
   - Round 4: 3 Senior Staff Leads & Architects
   - Round 5: 3 Senior Managers & Functional Leaders
   - Round 6: 4 Full Executive Panel Members
"""

from typing import List
from modules.interview.job_related.models import PanelMember


def generate_panel_for_round(job_role: str, company: str, round_num: int) -> List[PanelMember]:
    """
    Constructs a contextual panel of interviewers matching the target company and role.
    Each interviewer has a distinct title, persona, and focus area.
    """
    clean_role = job_role.strip() if job_role else "Software Engineer"
    clean_company = company.strip() if company else "Technology Solutions"

    # Pre-defined professional personas with progressive seniority
    if round_num == 1:
        # 1 Initial / Early Interviewer
        return [
            PanelMember(
                id="r1_p1",
                name="Ananya Sharma",
                title=f"Talent Acquisition & Technical Recruiter, {clean_company}",
                department="Global Talent & People Team",
                avatar_emoji="👩‍💼",
                focus_area="Candidate Introduction, Communication, Career Trajectory, and Core Aptitude",
                voice_name="hi-IN-Standard-A",
                voice_gender="Female",
            )
        ]

    elif round_num == 2:
        # 2 Mid-Level Professional Interviewers
        return [
            PanelMember(
                id="r2_p1",
                name="Rohit Verma",
                title=f"Senior {clean_role}, {clean_company}",
                department="Core Product & Engineering",
                avatar_emoji="👨‍💻",
                focus_area="Role Competencies, Implementation Rigor, and Technical Fundamentals",
                voice_name="hi-IN-Standard-B",
                voice_gender="Male",
            ),
            PanelMember(
                id="r2_p2",
                name="Priya Nair",
                title=f"Technical Specialist ({clean_role} Team), {clean_company}",
                department="Operational Engineering",
                avatar_emoji="👩‍💻",
                focus_area="Tooling Mastery, Workflow Optimization, and Execution Quality",
                voice_name="hi-IN-Standard-D",
                voice_gender="Female",
            ),
        ]

    elif round_num == 3:
        # 2 Experienced Domain Specialists
        return [
            PanelMember(
                id="r3_p1",
                name="Dr. Vikram Sen",
                title=f"Staff {clean_role} & Domain Lead, {clean_company}",
                department="Platform & Domain Excellence",
                avatar_emoji="👨‍🔬",
                focus_area="Resume Project Dissection, Technical Decisions, and Root-Cause Reasoning",
                voice_name="hi-IN-Standard-B",
                voice_gender="Male",
            ),
            PanelMember(
                id="r3_p2",
                name="Sneha Kulkarni",
                title=f"Lead Systems Engineer, {clean_company}",
                department="Infrastructure & Reliability",
                avatar_emoji="👩‍🔬",
                focus_area="Failure Modes, Problem-Solving Under Ambiguity, and Real-World Trade-Offs",
                voice_name="hi-IN-Standard-A",
                voice_gender="Female",
            ),
        ]

    elif round_num == 4:
        # 3 Senior Staff Leads & Architects
        return [
            PanelMember(
                id="r4_p1",
                name="Arjun Malhotra",
                title=f"Principal Solutions Architect, {clean_company}",
                department="Enterprise Architecture Group",
                avatar_emoji="👨‍💼",
                focus_area="High-Scale Architecture, System Design, and Scalability Limits",
                voice_name="hi-IN-Standard-B",
                voice_gender="Male",
            ),
            PanelMember(
                id="r4_p2",
                name="Meera Iyer",
                title=f"Engineering Manager ({clean_role} Org), {clean_company}",
                department="Engineering Leadership",
                avatar_emoji="👩‍💼",
                focus_area="Design Trade-offs, Resource Constraints, and Technical Ownership",
                voice_name="hi-IN-Standard-D",
                voice_gender="Female",
            ),
            PanelMember(
                id="r4_p3",
                name="Kavita Reddy",
                title=f"Staff Quality & Reliability Lead, {clean_company}",
                department="Reliability & Performance Engineering",
                avatar_emoji="👩‍💻",
                focus_area="Resilience, Edge-Case Handling, and Verification Under Pressure",
                voice_name="hi-IN-Standard-A",
                voice_gender="Female",
            ),
        ]

    elif round_num == 5:
        # 3 Senior Managers & Functional Leaders
        return [
            PanelMember(
                id="r5_p1",
                name="Rajesh Mehra",
                title=f"Director of Engineering, {clean_company}",
                department="Product Engineering Division",
                avatar_emoji="👨‍💼",
                focus_area="Strategic Execution, Cross-Functional Alignment, and Business Impact",
                voice_name="hi-IN-Standard-B",
                voice_gender="Male",
            ),
            PanelMember(
                id="r5_p2",
                name="Siddharth Rao",
                title=f"Head of Technical Operations, {clean_company}",
                department="Global Operations & Infrastructure",
                avatar_emoji="👨‍💼",
                focus_area="Incident Management, Operational Excellence, and Governance",
                voice_name="hi-IN-Standard-C",
                voice_gender="Male",
            ),
            PanelMember(
                id="r5_p3",
                name="Pooja Deshmukh",
                title=f"Senior Product Operations Lead, {clean_company}",
                department="Cross-Functional Product Strategy",
                avatar_emoji="👩‍💼",
                focus_area="Product Sense, Stakeholder Conflict Resolution, and Value Delivery",
                voice_name="hi-IN-Standard-A",
                voice_gender="Female",
            ),
        ]

    else:
        # Round 6: 4 Full Executive Interview Panel Members
        return [
            PanelMember(
                id="r6_p1",
                name="Devendra Singhania",
                title=f"Vice President of Engineering / CTO Group, {clean_company}",
                department="Executive Leadership",
                avatar_emoji="👔",
                focus_area="Architectural Vision, Technical Innovation, and Long-Term Value",
                voice_name="hi-IN-Standard-B",
                voice_gender="Male",
            ),
            PanelMember(
                id="r6_p2",
                name="Sunita Bannerjee",
                title=f"Chief People Officer & Head of Talent, {clean_company}",
                department="Executive Human Resources",
                avatar_emoji="👩‍💼",
                focus_area="Leadership Principles, Values Synergy, and Professional Ethics",
                voice_name="hi-IN-Standard-A",
                voice_gender="Female",
            ),
            PanelMember(
                id="r6_p3",
                name="Harshavardhan Joshi",
                title=f"Distinguished Technical Fellow, {clean_company}",
                department="Advanced Technology Research",
                avatar_emoji="👨‍🏫",
                focus_area="Deep Analytical Reasoning, Systemic Thinking, and Industry Standards",
                voice_name="hi-IN-Standard-C",
                voice_gender="Male",
            ),
            PanelMember(
                id="r6_p4",
                name="Nandita Kapoor",
                title=f"Senior Director of Global Delivery, {clean_company}",
                department="Global Business Operations",
                avatar_emoji="👩‍💼",
                focus_area="High-Pressure Delivery, Organizational Impact, and Final Candidate Q&A",
                voice_name="hi-IN-Standard-D",
                voice_gender="Female",
            ),
        ]

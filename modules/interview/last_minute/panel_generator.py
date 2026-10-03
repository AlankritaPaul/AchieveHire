"""
AchieveHire — Last-Minute Preparation Panel Generator
Generates multi-interviewer panels for both Specialized and Job Related modes.
Ensures interviews feel like realistic professional panels rather than single-voice chatbots.
"""

from typing import List
from modules.interview.last_minute.models import LastMinutePanelMember, MODE_SPECIALIZED


def generate_last_minute_panel(
    mode: str,
    topic: str,
    company: str = "Technology Solutions",
) -> List[LastMinutePanelMember]:
    """Constructs a 3-member professional panel asking questions from distinct angles."""
    clean_topic = topic.strip() if topic else "Technical Core"
    clean_company = company.strip() if company else "Technology Solutions"

    if mode == MODE_SPECIALIZED:
        return [
            LastMinutePanelMember(
                id="lm_sp_1",
                name="Ananya Sharma",
                title=f"Lead {clean_topic} Specialist",
                department="Language Architecture & Standards",
                avatar_emoji="👩‍💻",
                focus_area=f"Core {clean_topic} Syntax, Memory Model, and Language Idioms",
                voice_gender="Female",
            ),
            LastMinutePanelMember(
                id="lm_sp_2",
                name="Rohan Mehra",
                title=f"Staff Systems Engineer",
                department="Distributed Systems & Performance",
                avatar_emoji="👨‍💻",
                focus_area=f"Concurrency, High-Throughput Scenarios, and Performance Tuning",
                voice_gender="Male",
            ),
            LastMinutePanelMember(
                id="lm_sp_3",
                name="Dr. Kavita Rao",
                title=f"Principal Technical Architect",
                department="Architecture Review Board",
                avatar_emoji="👩‍🏫",
                focus_area=f"System Design, Robustness Under Stress, and Architectural Trade-Offs",
                voice_gender="Female",
            ),
        ]
    else:
        # Job Related Mode Panel (Increasing Seniority)
        return [
            LastMinutePanelMember(
                id="lm_job_1",
                name="Priya Nair",
                title=f"Senior {clean_topic}, {clean_company}",
                department="Product Engineering",
                avatar_emoji="👩‍💼",
                focus_area="Candidate Introduction, Role Competencies, and Implementation Rigor",
                voice_gender="Female",
            ),
            LastMinutePanelMember(
                id="lm_job_2",
                name="Vikram Sen",
                title=f"Lead Technical Specialist, {clean_company}",
                department="Core Platform Org",
                avatar_emoji="👨‍🔬",
                focus_area="Resume Project Dissection, Architecture Decisions, and Deep Follow-ups",
                voice_gender="Male",
            ),
            LastMinutePanelMember(
                id="lm_job_3",
                name="Siddharth Malhotra",
                title=f"Engineering Manager & Hiring Lead, {clean_company}",
                department="Engineering Leadership Group",
                avatar_emoji="👨‍💼",
                focus_area="Incident Management, High-Stakes Problem Solving, and Operational Leadership",
                voice_gender="Male",
            ),
        ]

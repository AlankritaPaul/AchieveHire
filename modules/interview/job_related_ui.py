"""
AchieveHire — Job Related Voice Interview Main UI Router
Manages the complete lifecycle of the Job Related Interview module:
1. Overview Page (Vertical flow, branding, single continuous session rule)
2. Setup Page (Job Role, Company, Language [STRICTLY 3], Resume inspection, Round selection)
3. Live Room (Voice-first, questions NOT displayed as text, multi-interviewer rotation, timer, controls)
4. Post-Round Report & Final Overall Report (Question breakdown, criteria chart with stamp, roadmap, PDF download)
"""

import streamlit as st
from modules.landing.ui import THEMES
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer
from modules.interview.job_related.overview_ui import render_job_interview_overview
from modules.interview.job_related.setup_ui import render_job_interview_setup
from modules.interview.job_related.session_ui import render_job_live_interview_session
from modules.interview.job_related.report_ui import (
    render_job_round_report,
    render_job_overall_report,
)


INTERVIEW_ROUNDS = [
    {
        "id": "round_1",
        "title": "Round 1: Foundational & Behavioral (STAR)",
        "icon": "👥",
        "desc": "Personal background, introductory role knowledge, and initial resume review.",
    },
    {
        "id": "round_2",
        "title": "Round 2: Role Competency & Technical Dissection",
        "icon": "⚙️",
        "desc": "Core job responsibilities, tooling expertise, workflow execution, and domain rigor.",
    },
    {
        "id": "round_3",
        "title": "Round 3: Situational & Project Problem Solving",
        "icon": "💡",
        "desc": "Resume project dissection, technical decisions, root-cause reasoning.",
    },
    {
        "id": "round_4",
        "title": "Round 4: High-Stakes Architecture & System Design",
        "icon": "🏗️",
        "desc": "High-scale architecture, constraints, failure modes, trade-offs.",
    },
    {
        "id": "round_5",
        "title": "Round 5: P0 Incidents & Cross-Functional Operations",
        "icon": "🚨",
        "desc": "Incident leadership, cross-functional alignment, and operational excellence.",
    },
    {
        "id": "round_6",
        "title": "Round 6: Executive Panel & Candidate Closing Q&A",
        "icon": "🏆",
        "desc": "Strategic vision, values integrity, and final candidate Q&A.",
    },
]


def render_job_related_interview():
    """Renders the comprehensive, production-oriented Job Related Interview interface."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Interview › Job Related Interview")

    view_mode = st.session_state.get("job_view_mode", "overview")

    if view_mode == "overview":
        render_job_interview_overview(
            on_proceed_callback=lambda: (
                st.session_state.update({"job_view_mode": "setup"}),
                st.rerun(),
            )
        )
    elif view_mode == "setup":
        render_job_interview_setup()
    elif view_mode == "live":
        round_num = st.session_state.get("job_active_round_num", 1)
        render_job_live_interview_session(round_num)
    elif view_mode == "report":
        report_round = st.session_state.get("job_report_round", 1)
        render_job_round_report(report_round)
    elif view_mode == "overall_report":
        render_job_overall_report()
    else:
        render_job_interview_overview()

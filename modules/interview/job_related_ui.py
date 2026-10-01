"""
AscendCareer — Job Related Interview Flow
Target job role and target company-aligned conversational interview preparation.
Covers behavioral questions, situational judgment (STAR methodology), culture alignment,
and role-specific operational scenarios.
"""

import streamlit as st
from modules.constants import SUGGESTED_JOB_ROLES, SUGGESTED_COMPANIES
from modules.landing.ui import THEMES, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer


INTERVIEW_ROUNDS = [
    {
        "id": "round_behavioral",
        "title": "Round 1: Behavioral & Leadership (STAR)",
        "icon": "👥",
        "desc": "Past experiences, conflict resolution, ownership, and handling ambiguity.",
    },
    {
        "id": "round_competency",
        "title": "Round 2: Role Competency & Technical Dissection",
        "icon": "⚙️",
        "desc": "Core job responsibilities, tooling expertise, workflow execution, and domain rigor.",
    },
    {
        "id": "round_situational",
        "title": "Round 3: Situational & High-Stakes Problem Solving",
        "icon": "💡",
        "desc": "Hypothetical crises, deadline pressures, prioritization, and executive decision-making.",
    },
    {
        "id": "round_culture_fit",
        "title": "Round 4: Culture Alignment & Candidate Questions",
        "icon": "🎯",
        "desc": "Values synergy, long-term trajectory, and thoughtful questions for the interview panel.",
    },
]


def render_job_related_interview():
    """Renders the Job-Related Interview preparation interface."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Interview › Job Related Interview")

    st.markdown(clean_html(f"""
    <div style="max-width:1080px; margin: 24px auto; padding: 0 16px;">
        <div style="margin-bottom: 24px;">
            <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.80rem; font-weight:700; padding:4px 14px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
                Role & Organization Alignment
            </div>
            <h1 style="font-size: 2.1rem; font-weight: 800; color:{t['text_primary']}; margin:0 0 6px;">
                Job Related Interview
            </h1>
            <p style="font-size: 1.02rem; color:{t['text_secondary']}; max-width:820px; line-height:1.65; margin:0;">
                Target-specific interview practice structured around your intended role, company archetype,
                and interview rounds. Practice real-time responses under realistic conversational conditions.
            </p>
        </div>
    </div>
    """), unsafe_allow_html=True)

    col_setup, col_rounds = st.columns([48, 52], gap="large")

    with col_setup:
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-bottom:14px;'>1. Target Context (Session Only)</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            target_role = st.selectbox(
                "Target Job Role",
                options=SUGGESTED_JOB_ROLES,
                index=0,
                help="Select your target position for this specific practice session.",
            )
            custom_role = st.text_input("Or specify custom title:", placeholder="e.g. Lead Staff Security Architect")
            effective_role = custom_role.strip() if custom_role.strip() else target_role

            target_company = st.selectbox(
                "Target Company Archetype / Organization",
                options=SUGGESTED_COMPANIES,
                index=0,
                help="Tailors corporate culture and questioning style.",
            )
            custom_company = st.text_input("Or specify specific company:", placeholder="e.g. Stripe, Palantir, Databricks")
            effective_company = custom_company.strip() if custom_company.strip() else target_company

            st.text_area(
                "Optional: Job Description Excerpt",
                placeholder="Paste key responsibilities or requirements from the job posting to tune questions specifically to the opening...",
                height=110,
            )

    with col_rounds:
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-bottom:14px;'>2. Select Target Round</h3>", unsafe_allow_html=True)
        if "job_interview_round" not in st.session_state:
            st.session_state["job_interview_round"] = INTERVIEW_ROUNDS[0]["id"]

        for rnd in INTERVIEW_ROUNDS:
            is_active = st.session_state["job_interview_round"] == rnd["id"]
            active_border = t["accent"] if is_active else t["border"]
            active_bg = t["accent_soft"] if is_active else t["surface"]

            st.markdown(f"""
            <div style="border: 1.5px solid {active_border}; background: {active_bg}; border-radius: 12px; padding: 14px 16px; margin-bottom: 10px;">
                <div style="display:flex; align-items:flex-start; gap:12px;">
                    <span style="font-size:1.35rem;">{rnd['icon']}</span>
                    <div style="flex:1;">
                        <div style="font-weight:700; font-size:0.98rem; color:{t['text_primary']};">{rnd['title']}</div>
                        <div style="font-size:0.84rem; color:{t['text_secondary']}; margin-top:3px;">{rnd['desc']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select: {rnd['title']}", key=f"btn_rnd_{rnd['id']}", use_container_width=True):
                st.session_state["job_interview_round"] = rnd["id"]
                st.rerun()

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        if st.button(f"🎯  Start {effective_role} Interview", type="primary", use_container_width=True, key="btn_start_job_interview"):
            st.session_state["job_session_active"] = True
            st.success(f"Configured practice session for {effective_role} at {effective_company}! Initializing round simulation...")

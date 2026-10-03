"""
AchieveHire — Specialized Interview Main Router & Hub
Integrates the complete Specialized Interview experience:
Overview -> Setup -> Live Conversational Voice Session -> Performance & Improvement Report -> Overall Report
"""

import streamlit as st
from modules.landing.ui import THEMES, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer

from modules.interview.specialized.overview_ui import render_specialized_overview
from modules.interview.specialized.setup_ui import render_specialized_setup
from modules.interview.specialized.session_ui import (
    render_specialized_session,
    init_specialized_session,
)
from modules.interview.specialized.report_ui import render_specialized_report_screen
from modules.interview.specialized.storage import (
    load_specialized_progress,
    load_round_report,
    load_all_user_interviews,
)

SPECIALIZED_DOMAINS = [
    {
        "id": "swe_sys_design",
        "title": "Software Engineering & Distributed Systems",
        "icon": "⚡",
        "description": "High-concurrency architecture, API contracts, caching tiers, data modeling, and fault tolerance.",
        "topics": ["System Scalability", "Low-Latency Services", "Distributed Consensus", "Database Sharding"],
    },
    {
        "id": "ai_data_science",
        "title": "AI, Machine Learning & Data Engineering",
        "icon": "🧠",
        "description": "Deep learning models, inference pipelines, feature stores, LLM orchestration, and ETL workflows.",
        "topics": ["Model Evaluation", "Vector Indexing & RAG", "Data Pipelines", "Production Inference"],
    },
    {
        "id": "product_management",
        "title": "Product Management & Technical Strategy",
        "icon": "📊",
        "description": "User problem discovery, MVP scoping, product roadmaps, metrics architecture, and stakeholder trade-offs.",
        "topics": ["Product Sense", "Execution & Metrics", "Go-to-Market Strategy", "Technical Feasibility"],
    },
    {
        "id": "cloud_devops",
        "title": "Cloud Architecture & Site Reliability",
        "icon": "☁️",
        "description": "Container orchestration (K8s), infrastructure-as-code, zero-trust security, and observability.",
        "topics": ["Kubernetes & CI/CD", "Cloud Networking", "Incident Management", "Security & IAM"],
    },
]



def render_specialized_interview():
    """Main entry point and state router for Specialized Interview."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Interview › Specialized Interview")

    # State initialization
    if "spec_view_state" not in st.session_state:
        st.session_state["spec_view_state"] = "overview"

    view_state = st.session_state["spec_view_state"]

    # Callbacks
    def on_start_setup():
        st.session_state["spec_view_state"] = "setup"

    def on_launch_session(specialization, language, interviewer_gender, round_num):
        init_specialized_session(
            specialization=specialization,
            language=language,
            interviewer_gender=interviewer_gender,
            round_num=round_num,
        )
        st.session_state["spec_view_state"] = "session"

    def on_complete_round(round_report, overall_report=None):
        st.session_state["spec_current_round_report"] = round_report
        st.session_state["spec_current_overall_report"] = overall_report
        st.session_state["spec_view_state"] = "report"

    def on_cancel_session():
        st.session_state["spec_sess_active"] = False
        st.session_state["spec_view_state"] = "overview"

    def on_next_round(next_round_num):
        # Read saved configuration to launch next round
        spec = st.session_state.get("specialized_selected_domain", "Python")
        lang = (
            st.session_state.get("specialized_selected_language")
            or st.session_state.get("specialized_language")
            or "English"
        )
        gender = (
            st.session_state.get("specialized_interviewer_gender")
            or st.session_state.get("specialized_interviewer")
            or "male"
        )
        init_specialized_session(
            specialization=spec,
            language=lang,
            interviewer_gender=gender,
            round_num=next_round_num,
        )
        st.session_state["spec_view_state"] = "session"

    def on_return_overview():
        st.session_state["spec_view_state"] = "overview"

    def on_view_reports(specialization=None):
        if specialization:
            st.session_state["specialized_selected_domain"] = specialization
        st.session_state["spec_view_state"] = "report"


    # Route according to current view state
    if view_state == "overview":
        render_specialized_overview(t, on_start_setup=on_start_setup)

    elif view_state == "setup":
        render_specialized_setup(
            t,
            on_launch_session=on_launch_session,
            on_view_reports=on_view_reports,
        )

    elif view_state == "session":
        render_specialized_session(
            t,
            on_complete_round=on_complete_round,
            on_cancel_session=on_cancel_session,
        )

    elif view_state == "report":
        report_data = st.session_state.get("spec_current_round_report")
        overall_data = st.session_state.get("spec_current_overall_report")
        
        if not report_data:
            user_id = st.session_state.get("user_id", "guest")
            spec = st.session_state.get("specialized_selected_domain", "Python")
            # Try to load latest completed round report
            progress = load_specialized_progress(user_id, spec)
            completed_rounds = progress.get("rounds_completed", [])
            if completed_rounds:
                last_r = max(completed_rounds)
                report_data = load_round_report(user_id, spec, last_r)
                overall_data = progress.get("overall_report")
        
        if report_data:
            render_specialized_report_screen(
                t,
                report_data=report_data,
                overall_report=overall_data,
                on_next_round=on_next_round,
                on_return_overview=on_return_overview,
            )
        else:
            st.info("No report currently available. Please complete an interview round first.")
            if st.button("⬅️ Return to Overview", use_container_width=True):
                st.session_state["spec_view_state"] = "overview"
                st.rerun()

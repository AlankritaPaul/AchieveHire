"""
AchieveHire — Job Related Interview Overview Page
Displays the clean vertical progression flow, branding,
round breakdown, and session integrity rules.
"""

import streamlit as st
from modules.landing.ui import THEMES, clean_html


def render_job_interview_overview(on_proceed_callback=None):
    """Renders the clean, uncluttered Job Related Interview Overview page."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    # Branding Header
    st.markdown(clean_html(f"""
    <div style="max-width:860px; margin: 20px auto 10px; text-align:center;">
        <div style="font-size:2.2rem; font-weight:900; letter-spacing:-0.03em; color:{t['text_primary']}; margin-bottom:2px;">
            AchieveHire
        </div>
        <div style="font-size:1.05rem; font-weight:600; color:{t['accent']}; letter-spacing:0.04em; margin-bottom:20px;">
            Better Preparation. Stronger Presentation.
        </div>
        <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.82rem; font-weight:700; padding:5px 16px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:12px;">
            💼 Role &amp; Organization Alignment System
        </div>
        <h1 style="font-size:1.85rem; font-weight:800; color:{t['text_primary']}; margin:0 0 10px;">
            Job Related Interview Overview
        </h1>
        <p style="font-size:1.02rem; color:{t['text_secondary']}; max-width:720px; margin:0 auto 24px; line-height:1.65;">
            Experience a realistic conversational job interview tailored to your target position, target company,
            and actual resume. Progress through six structured rounds with increasing panel seniority and depth.
        </p>
    </div>
    """), unsafe_allow_html=True)

    # Simple Vertical Flow with Arrows
    flow_steps = [
        {"title": "Choose Job Role", "desc": "Select or write your target position", "icon": "🎯"},
        {"title": "Choose Company", "desc": "Select or write your target organization", "icon": "🏢"},
        {"title": "Choose Interview Language", "desc": "English, Hindi, or natural Indian Hinglish", "icon": "🌐"},
        {"title": "Show / Analyse Resume", "desc": "Interviewer reviews your real AchieveHire resume", "icon": "📄"},
        {"title": "Round 1 — Easy — 20 Minutes", "desc": "1 Interviewer · Starts strictly with 'Please introduce yourself'", "icon": "🟢"},
        {"title": "Performance & Improvement Report", "desc": "Question-by-question breakdown, criteria chart & recommendations", "icon": "📊"},
        {"title": "Round 2 — Moderate — 25 Minutes", "desc": "2 Interviewers · Role competencies & workflow execution", "icon": "🟡"},
        {"title": "Performance & Improvement Report", "desc": "Question-by-question breakdown, criteria chart & recommendations", "icon": "📊"},
        {"title": "Round 3 — Moderate — 30 Minutes", "desc": "2 Interviewers · Resume project dissection & root-cause reasoning", "icon": "🟡"},
        {"title": "Performance & Improvement Report", "desc": "Question-by-question breakdown, criteria chart & recommendations", "icon": "📊"},
        {"title": "Round 4 — Hard — 35 Minutes", "desc": "3 Interviewers · High-stakes architecture, constraints & trade-offs", "icon": "🔴"},
        {"title": "Performance & Improvement Report", "desc": "Question-by-question breakdown, criteria chart & recommendations", "icon": "📊"},
        {"title": "Round 5 — Hard — 40 Minutes", "desc": "3 Interviewers · P0 incident leadership & operational excellence", "icon": "🔴"},
        {"title": "Performance & Improvement Report", "desc": "Question-by-question breakdown, criteria chart & recommendations", "icon": "📊"},
        {"title": "Round 6 — Final — 45 Minutes", "desc": "4–5 Interviewers · Full Executive Panel + Closing Candidate Q&A", "icon": "🏆"},
        {"title": "Overall Performance & Improvement Report", "desc": "Comprehensive 6-round growth trajectory, strengths & mastery audit", "icon": "📈"},
    ]

    st.markdown(clean_html(f"""
    <div style="max-width:680px; margin: 0 auto 28px; padding: 0 16px;">
        <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:16px; padding:24px 28px; box-shadow:{t['card_shadow']};">
    """), unsafe_allow_html=True)

    for i, step in enumerate(flow_steps):
        is_report = "Report" in step["title"]
        bg_color = t['surface2'] if not is_report else t['accent_soft']
        border_color = t['accent'] if is_report else t['border']
        text_color = t['accent'] if is_report else t['text_primary']

        st.markdown(clean_html(f"""
        <div style="display:flex; align-items:center; gap:16px; padding:12px 16px; background:{bg_color}; border:1px solid {border_color}; border-radius:10px; margin-bottom:4px;">
            <div style="font-size:1.35rem; width:36px; text-align:center; flex-shrink:0;">
                {step['icon']}
            </div>
            <div style="flex:1;">
                <div style="font-weight:700; font-size:0.98rem; color:{text_color};">
                    {step['title']}
                </div>
                <div style="font-size:0.82rem; color:{t['text_secondary']}; margin-top:2px;">
                    {step['desc']}
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        if i < len(flow_steps) - 1:
            st.markdown(f"""
            <div style="text-align:center; color:{t['accent']}; font-weight:800; font-size:1.1rem; line-height:1; margin: 3px 0;">
                ↓
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Important Note & Single-Session Rule
    st.markdown(clean_html(f"""
    <div style="max-width:680px; margin: 0 auto 24px; padding: 0 16px;">
        <div style="background:#FFFBEB; border-left:4px solid #F59E0B; border-radius:8px; padding:16px 20px;">
            <div style="font-weight:800; font-size:0.95rem; color:#92400E; margin-bottom:4px; display:flex; align-items:center; gap:8px;">
                <span>⚠️</span>
                <span>Important Session Requirement</span>
            </div>
            <div style="font-size:0.88rem; color:#78350F; line-height:1.55;">
                <strong>Important:</strong> Once a round starts, it must be completed in the same continuous session.
                If you leave, close the application, or stop midway, that round will be cancelled and no marks
                or performance will be calculated. Partial completion will not be considered.
            </div>
            <div style="font-size:0.84rem; color:#92400E; margin-top:8px;">
                💡 <em>Note: You do not have to complete all six rounds on the same day. You can complete different rounds on different days at your convenience.</em>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # Proceed Button
    st.markdown(f"<div style='max-width:680px; margin: 0 auto; padding: 0 16px;'>", unsafe_allow_html=True)
    if st.button("Begin Setup & Role Selection ›", type="primary", use_container_width=True, key="job_overview_proceed_btn"):
        if on_proceed_callback:
            on_proceed_callback()
        else:
            st.session_state["job_view_mode"] = "setup"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

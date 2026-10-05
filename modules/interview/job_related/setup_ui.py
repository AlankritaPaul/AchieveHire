# -*- coding: utf-8 -*-
"""
AchieveHire — Job Related Interview Setup Screen
Converts setup into a clean 2-column layout (Role/Company/Language on left, Round selection on right)
without tab switching bugs.
"""

import streamlit as st
from modules.landing.ui import THEMES, clean_html
from modules.interview.job_related.models import (
    JOB_ROUNDS_CONFIG,
    SUGGESTED_JOB_ROLES,
    SUGGESTED_COMPANIES,
    INTERVIEW_LANGUAGES,
)
from modules.interview.job_related.storage import (
    load_job_interview_session,
    initialize_job_interview_session,
    is_round_unlocked,
)
from modules.resume_guide.parser import get_candidate_stored_resume


def render_job_interview_setup(on_start_round_callback=None):
    """Renders the clean Job Related Interview setup screen."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id", "guest")

    session = load_job_interview_session(user_id)
    stored_resume = get_candidate_stored_resume(user_id)

    st.markdown(clean_html(f"""
    <div style="max-width:980px; margin: 16px auto 20px; padding: 0 16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
                <div style="font-size:0.80rem; font-weight:700; color:{t['accent']}; text-transform:uppercase; letter-spacing:0.06em;">
                    AchieveHire — Better Preparation. Stronger Presentation.
                </div>
                <h2 style="font-size:1.8rem; font-weight:800; color:{t['text_primary']}; margin:4px 0 0;">
                    Job Related Interview Setup
                </h2>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    col_main, col_rounds = st.columns([52, 48], gap="large")

    with col_main:
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-bottom:8px;'>1. Configure Target Position</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            # 1. Job Role Selection
            st.markdown(f"<div style='font-weight:700; font-size:0.95rem; color:{t['text_primary']}; margin-bottom:4px;'>Target Job Role</div>", unsafe_allow_html=True)
            default_role = session.get("target_role", "Software Engineer") if session else "Software Engineer"
            role_options = ["Write Your Job Role"] + SUGGESTED_JOB_ROLES

            selected_role_mode = st.selectbox(
                "Select Suggested Role or Choose 'Write Your Job Role'",
                options=role_options,
                index=role_options.index(default_role) if default_role in role_options else 0,
                key="job_role_dropdown",
                label_visibility="collapsed",
            )

            if selected_role_mode == "Write Your Job Role":
                effective_role = st.text_input(
                    "Write Your Job Role (verbatim):",
                    value=default_role if default_role not in SUGGESTED_JOB_ROLES else "",
                    placeholder="e.g. Lead Staff Security Architect, Quantitative Trader",
                    key="job_role_manual_input",
                ).strip()
            else:
                effective_role = selected_role_mode

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

            # 2. Company Selection
            st.markdown(f"<div style='font-weight:700; font-size:0.95rem; color:{t['text_primary']}; margin-bottom:4px;'>Target Organization / Company</div>", unsafe_allow_html=True)
            default_company = session.get("target_company", "Google") if session else "Google"
            company_options = ["Write Your Company"] + SUGGESTED_COMPANIES

            selected_company_mode = st.selectbox(
                "Select Suggested Company or Choose 'Write Your Company'",
                options=company_options,
                index=company_options.index(default_company) if default_company in company_options else 0,
                key="job_company_dropdown",
                label_visibility="collapsed",
            )

            if selected_company_mode == "Write Your Company":
                effective_company = st.text_input(
                    "Write Your Company (verbatim):",
                    value=default_company if default_company not in SUGGESTED_COMPANIES else "",
                    placeholder="e.g. OpenAI, Stripe, Zerodha, Palantir",
                    key="job_company_manual_input",
                ).strip()
            else:
                effective_company = selected_company_mode

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

            # 3. Interview Language
            st.markdown(f"<div style='font-weight:700; font-size:0.95rem; color:{t['text_primary']}; margin-bottom:4px;'>Interview Spoken Language</div>", unsafe_allow_html=True)
            default_lang = session.get("language", "English") if session else "English"
            if default_lang not in INTERVIEW_LANGUAGES:
                default_lang = "English"

            selected_language = st.radio(
                "Interview Language",
                options=INTERVIEW_LANGUAGES,
                index=INTERVIEW_LANGUAGES.index(default_lang),
                key="job_language_radio",
                label_visibility="collapsed",
            )

            st.session_state["job_effective_role"] = effective_role
            st.session_state["job_effective_company"] = effective_company
            st.session_state["job_effective_language"] = selected_language

            st.markdown(clean_html(f"""
            <div style="background:{t['surface2']}; border:1px solid {t['border']}; border-radius:8px; padding:10px 14px; margin-top:10px; font-size:0.82rem; color:{t['text_secondary']};">
                Selected Target: <strong>{effective_role}</strong> at <strong>{effective_company}</strong> ({selected_language})
            </div>
            """), unsafe_allow_html=True)

    with col_rounds:
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-bottom:8px;'>2. Select &amp; Start Round</h3>", unsafe_allow_html=True)
        
        effective_role = st.session_state.get("job_effective_role", "Software Engineer")
        effective_company = st.session_state.get("job_effective_company", "Google")
        effective_lang = st.session_state.get("job_effective_language", "English")

        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:10px; padding:12px 16px; margin-bottom:14px;">
            <div style="font-weight:700; font-size:0.92rem; color:{t['text_primary']}; margin-bottom:2px;">
                Active Target: <span style="color:{t['accent']};">{effective_role}</span> at <span style="color:{t['accent']};">{effective_company}</span>
            </div>
            <div style="font-size:0.80rem; color:{t['text_secondary']};">
                Language: {effective_lang} · Sequential unlocking enforced.
            </div>
        </div>
        """), unsafe_allow_html=True)

        for r_num in range(1, 7):
            r_cfg = JOB_ROUNDS_CONFIG[r_num]
            unlocked = is_round_unlocked(session, r_num)
            is_completed = session and r_num in session.get("completed_rounds", [])

            status_badge = ""
            if is_completed:
                score = session["round_evaluations"].get(str(r_num), {}).get("overall_score", 0)
                status_badge = f'<span style="background:#D1FAE5; color:#065F46; font-weight:700; font-size:0.75rem; padding:2px 8px; border-radius:50px;">✓ Completed ({score}/100)</span>'
            elif unlocked:
                status_badge = f'<span style="background:{t["accent_soft"]}; color:{t["accent"]}; font-weight:700; font-size:0.75rem; padding:2px 8px; border-radius:50px;">🟢 Unlocked</span>'
            else:
                status_badge = f'<span style="background:#F3F4F6; color:#6B7280; font-weight:700; font-size:0.75rem; padding:2px 8px; border-radius:50px;">🔒 Locked</span>'

            with st.container(border=True):
                col_info, col_action = st.columns([65, 35])
                with col_info:
                    st.markdown(clean_html(f"""
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:2px;">
                        <h4 style="font-size:0.98rem; font-weight:800; color:{t['text_primary']}; margin:0;">
                            {r_cfg['name']}
                        </h4>
                        {status_badge}
                    </div>
                    <div style="font-size:0.80rem; color:{t['text_secondary']};">
                        ⏱️ {r_cfg['duration_minutes']} Mins · 👥 {r_cfg['interviewer_count']} Panelist(s) ({r_cfg['interviewer_seniority']})
                    </div>
                    """), unsafe_allow_html=True)

                with col_action:
                    if is_completed:
                        if st.button("📊 Report", key=f"btn_view_report_r{r_num}", use_container_width=True):
                            st.session_state["job_view_mode"] = "report"
                            st.session_state["job_report_round"] = r_num
                            st.rerun()
                    elif unlocked:
                        if st.button(f"🚀 Start R{r_num}", key=f"btn_start_round_{r_num}", type="primary", use_container_width=True):
                            if not effective_role or not effective_company:
                                st.error("Please select both a Job Role and Company.")
                            else:
                                session = initialize_job_interview_session(
                                    user_id=user_id,
                                    target_role=effective_role,
                                    target_company=effective_company,
                                    language=effective_lang,
                                    resume_snapshot=stored_resume,
                                )
                                st.session_state["job_active_round_num"] = r_num
                                st.session_state["job_view_mode"] = "live"
                                st.rerun()
                    else:
                        st.button("🔒 Locked", key=f"btn_locked_r{r_num}", disabled=True, use_container_width=True)

        if session and session.get("is_overall_completed"):
            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(f"<h3 style='font-size:1.1rem; font-weight:800; color:{t['accent']}; margin-bottom:6px;'>🏆 All 6 Rounds Completed!</h3>", unsafe_allow_html=True)
                if st.button(" View Final Report", type="primary", use_container_width=True, key="btn_view_overall_final_rep"):
                    st.session_state["job_view_mode"] = "overall_report"
                    st.rerun()

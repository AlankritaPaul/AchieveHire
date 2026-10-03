"""
AchieveHire — Last-Minute Preparation Setup UI
Allows user to:
1. Select Mode: Last-Minute Specialized Preparation vs Last-Minute Job Related Preparation
2. Configure specialization, role, company, language, and resume
3. View permanent Attempt History and attempt-over-attempt score progression
4. Launch the 30-minute intensive session
"""

import streamlit as st
from typing import Dict, Any, List
from modules.landing.ui import THEMES, clean_html
from modules.interview.last_minute.models import (
    MODE_SPECIALIZED,
    MODE_JOB_RELATED,
    POPULAR_SPECIALIZATIONS,
    INTERVIEW_LANGUAGES,
)
from modules.interview.last_minute.storage import (
    load_user_attempts,
    get_attempt_comparison_data,
    get_attempt_short_detail,
)
from modules.interview.last_minute.engine import check_level_completion
from modules.interview.job_related.models import (
    SUGGESTED_JOB_ROLES,
    SUGGESTED_COMPANIES,
)
from modules.interview.job_related.setup_ui import get_candidate_stored_resume


@st.dialog("💡 Preparation Strategy Advisory")
def show_incomplete_level_dialog(mode: str, level_label: str, target_screen: str):
    display_stage = "4 levels" if "Specialized" in mode else "6 rounds"
    st.markdown(f"### Would you like to proceed with Last-Minute Prep before completing the {display_stage}?")
    st.markdown(
        f"""
        <div style="background:#EEF2FF; border-left:4px solid #4F46E5; border-radius:8px; padding:14px 18px; margin: 14px 0;">
            <div style="font-weight:700; color:#312E81; font-size:0.95rem; margin-bottom:4px;">Recommended Strategy:</div>
            <div style="color:#3730A3; font-size:0.90rem; line-height:1.6;">
                Each progressive stage is specifically designed to build your confidence, depth, and composure step-by-step.
                Jumping directly into the rapid 30-minute panel simulation may feel intense without warming up through the foundational rounds first.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Continue to Last-Minute Prep", type="primary", use_container_width=True, key="btn_dlg_continue_lm"):
            st.session_state["lm_level_warning_confirmed"] = True
            st.session_state["lm_view_mode"] = "live"
            st.rerun()
    with col2:
        dest_title = "Stage Practice (4 Levels)" if "Specialized" in mode else "Round Practice (6 Rounds)"
        if st.button(f"🎯 Practice Stages First (Recommended)", use_container_width=True, key="btn_dlg_go_stage"):
            st.session_state["ac_screen"] = target_screen
            st.rerun()


def render_last_minute_setup():
    """Renders the comprehensive setup screen with attempt history."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id") or "GUEST"

    attempts = load_user_attempts(user_id)
    stored_resume = get_candidate_stored_resume(user_id)

    # Header Branding
    st.markdown(clean_html(f"""
    <div style="max-width:960px; margin: 16px auto 16px; padding: 0 16px;">
        <div style="font-size:0.80rem; font-weight:700; color:{t['accent']}; text-transform:uppercase; letter-spacing:0.06em;">
            AchieveHire · Better Preparation. Stronger Presentation.
        </div>
        <h1 style="font-size:1.95rem; font-weight:800; color:{t['text_primary']}; margin:4px 0 6px;">
            ⚡ Last-Minute Preparation Interview
        </h1>
        <p style="font-size:0.98rem; color:{t['text_secondary']}; max-width:760px; line-height:1.6; margin:0;">
            A fast, intensive 30-minute interview rehearsal simulation with a multi-interviewer panel.
            Designed for immediate practice right before your real interview. Unlimited attempts with permanent history.
        </p>
    </div>
    """), unsafe_allow_html=True)

    tab_config, tab_history = st.tabs([
        "⚙️ Configure & Start Rehearsal",
        f"📜 Attempt History & Past Scorecards ({len(attempts)})",
    ])

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 1: Configure & Start Rehearsal
    # ─────────────────────────────────────────────────────────────────────────
    with tab_config:
        # Pre-select if redirected from test sections
        if st.session_state.get("lm_active_mode") and not st.session_state.get("lm_chosen_mode"):
            st.session_state["lm_chosen_mode"] = st.session_state["lm_active_mode"]

        chosen_mode = st.session_state.get("lm_chosen_mode")

        # ── STEP 1: Separate Mode Selection Page ─────────────────────────────
        if not chosen_mode:
            st.markdown(clean_html(f"""
            <div style="margin-bottom:20px;">
                <h2 style="font-size:1.35rem; font-weight:800; color:{t['text_primary']}; margin:0 0 6px;">
                    Select Preparation Category
                </h2>
                <p style="font-size:0.92rem; color:{t['text_secondary']}; margin:0;">
                    Choose which type of intensive 30-minute interview rehearsal you want to practice.
                </p>
            </div>
            """), unsafe_allow_html=True)

            col_card_spec, col_card_job = st.columns(2, gap="large")

            with col_card_spec:
                st.markdown(clean_html(f"""
                <div style="background:{t['surface']}; border:2px solid {t['border']}; border-radius:14px; padding:24px; box-shadow:{t['card_shadow']}; min-height:220px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <div style="font-size:2rem; margin-bottom:8px;">🎯</div>
                        <h3 style="font-size:1.25rem; font-weight:800; color:{t['text_primary']}; margin:0 0 8px;">
                            Last-Minute Prep for Specialized
                        </h3>
                        <p style="font-size:0.90rem; color:{t['text_secondary']}; line-height:1.55; margin:0;">
                            For programming languages, cloud frameworks, and technical domains (Python, Java, C++, React, DevOps, etc.). Select or write your specialization.
                        </p>
                    </div>
                </div>
                """), unsafe_allow_html=True)
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                if st.button("Prepare for Specialized →", type="primary", use_container_width=True, key="btn_choose_spec_mode"):
                    st.session_state["lm_chosen_mode"] = MODE_SPECIALIZED
                    st.rerun()

            with col_card_job:
                st.markdown(clean_html(f"""
                <div style="background:{t['surface']}; border:2px solid {t['border']}; border-radius:14px; padding:24px; box-shadow:{t['card_shadow']}; min-height:220px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <div style="font-size:2rem; margin-bottom:8px;">💼</div>
                        <h3 style="font-size:1.25rem; font-weight:800; color:{t['text_primary']}; margin:0 0 8px;">
                            Last-Minute Prep for Job Related
                        </h3>
                        <p style="font-size:0.90rem; color:{t['text_secondary']}; line-height:1.55; margin:0;">
                            For target company roles. Choose or write your job role and target company with verified resume integration and a 3-interviewer company panel.
                        </p>
                    </div>
                </div>
                """), unsafe_allow_html=True)
                st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
                if st.button("Prepare for Job Related →", type="primary", use_container_width=True, key="btn_choose_job_mode"):
                    st.session_state["lm_chosen_mode"] = MODE_JOB_RELATED
                    st.rerun()

        # ── STEP 2: Dedicated Configuration Page ─────────────────────────────
        else:
            col_back, col_title = st.columns([25, 75])
            with col_back:
                if st.button("← Change Category", key="btn_back_to_mode_select"):
                    st.session_state["lm_chosen_mode"] = None
                    st.session_state["lm_active_mode"] = None
                    st.rerun()
            with col_title:
                st.markdown(f"<div style='font-size:1.15rem; font-weight:800; color:{t['text_primary']}; padding-top:4px;'>{chosen_mode}</div>", unsafe_allow_html=True)

            st.markdown("<hr style='margin:12px 0 16px;'/>", unsafe_allow_html=True)

            col_left, col_right = st.columns([1, 1], gap="large")

            if chosen_mode == MODE_SPECIALIZED:
                with col_left:
                    st.markdown(f"<div style='font-weight:700; font-size:1rem; color:{t['text_primary']}; margin-bottom:6px;'>Select Technical Specialization</div>", unsafe_allow_html=True)
                    spec_opts = ["Write Your Specialization"] + POPULAR_SPECIALIZATIONS
                    chosen_spec_mode = st.selectbox(
                        "Specialization",
                        options=spec_opts,
                        index=1,
                        key="lm_spec_dropdown",
                        label_visibility="collapsed",
                    )

                    if chosen_spec_mode == "Write Your Specialization":
                        effective_topic = st.text_input(
                            "Write Your Specialization (verbatim):",
                            placeholder="e.g. Flutter, Kotlin, GraphQL, Distributed Systems",
                            key="lm_spec_manual",
                        ).strip()
                    else:
                        effective_topic = chosen_spec_mode

                    effective_company = "Technology Solutions"

                with col_right:
                    st.markdown(f"<div style='font-weight:700; font-size:1rem; color:{t['text_primary']}; margin-bottom:6px;'>Interview Spoken Language</div>", unsafe_allow_html=True)
                    chosen_lang = st.radio(
                        "Language",
                        options=INTERVIEW_LANGUAGES,
                        index=0,
                        key="lm_lang_radio",
                        label_visibility="collapsed",
                        help="Only English, Hindi, and Hinglish are supported.",
                    )
                    st.markdown(f"<div style='font-size:0.82rem; color:{t['text_muted']}; margin-top:10px;'>Technical terms remain in English where appropriate.</div>", unsafe_allow_html=True)

            else:
                with col_left:
                    st.markdown(f"<div style='font-weight:700; font-size:1rem; color:{t['text_primary']}; margin-bottom:6px;'>Target Job Role</div>", unsafe_allow_html=True)
                    role_opts = ["Write Your Job Role"] + SUGGESTED_JOB_ROLES
                    chosen_role_mode = st.selectbox(
                        "Job Role",
                        options=role_opts,
                        index=1,
                        key="lm_role_dropdown",
                        label_visibility="collapsed",
                    )
                    if chosen_role_mode == "Write Your Job Role":
                        effective_topic = st.text_input("Write Your Job Role:", placeholder="e.g. Senior Backend Engineer", key="lm_role_manual").strip()
                    else:
                        effective_topic = chosen_role_mode

                    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-weight:700; font-size:1rem; color:{t['text_primary']}; margin-bottom:6px;'>Target Company</div>", unsafe_allow_html=True)
                    comp_opts = ["Write Your Company"] + SUGGESTED_COMPANIES
                    chosen_comp_mode = st.selectbox(
                        "Company",
                        options=comp_opts,
                        index=1,
                        key="lm_comp_dropdown",
                        label_visibility="collapsed",
                    )
                    if chosen_comp_mode == "Write Your Company":
                        effective_company = st.text_input("Write Your Company:", placeholder="e.g. Google, Microsoft, Stripe", key="lm_comp_manual").strip()
                    else:
                        effective_company = chosen_comp_mode

                with col_right:
                    st.markdown(f"<div style='font-weight:700; font-size:1rem; color:{t['text_primary']}; margin-bottom:6px;'>Interview Spoken Language</div>", unsafe_allow_html=True)
                    chosen_lang = st.radio(
                        "Language",
                        options=INTERVIEW_LANGUAGES,
                        index=0,
                        key="lm_job_lang_radio",
                        label_visibility="collapsed",
                    )

                    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
                    with st.container(border=True):
                        st.markdown(f"<div style='font-weight:700; font-size:0.85rem; color:{t['accent']};'>📄 Resume Integration Active</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='font-size:0.82rem; color:{t['text_secondary']};'>Using verified candidate resume for <strong>{user_id}</strong>. Questions will probe genuine skills and past projects.</div>", unsafe_allow_html=True)

            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

            # 30-Minute Session Info Card
            st.markdown(clean_html(f"""
            <div style="background:#FFFBEB; border-left:4px solid #F59E0B; border-radius:10px; padding:16px 20px; margin-bottom:20px;">
                <div style="font-weight:800; font-size:0.95rem; color:#92400E; margin-bottom:4px;">
                    ⏱️ Fixed 30-Minute Rehearsal Rules
                </div>
                <div style="font-size:0.85rem; color:#78350F; line-height:1.55;">
                    • <strong>Duration:</strong> Exactly 30 minutes. Non-extendable.<br>
                    • <strong>Sequence:</strong> Starts strictly with <em>“Please introduce yourself.”</em> and advances rapidly: Easy → Moderate → Hard.<br>
                    • <strong>Voice-Only Live Mode:</strong> Questions are asked verbally to simulate a real interview panel. Questions are not displayed on-screen until the report.<br>
                    • <strong>Unlimited Rehearsals:</strong> Practise as many times as you like. Every completed session is preserved permanently.
                </div>
            </div>
            """), unsafe_allow_html=True)

            if st.button("🚀  Start 30-Minute Intensive Preparation", type="primary", use_container_width=True, key="btn_start_lm_session"):
                if not effective_topic:
                    st.error("Please specify your target topic, specialization, or job role.")
                else:
                    st.session_state["lm_active_mode"] = chosen_mode
                    st.session_state["lm_active_topic"] = effective_topic
                    st.session_state["lm_active_company"] = effective_company
                    st.session_state["lm_active_language"] = chosen_lang
                    st.session_state["lm_resume_snapshot"] = stored_resume

                    # Check level completion before starting
                    is_completed, req_cnt, level_label = check_level_completion(user_id, chosen_mode)
                    if not is_completed and not st.session_state.get("lm_level_warning_confirmed"):
                        target_scr = "interview_specialized" if "Specialized" in chosen_mode else "interview_job"
                        show_incomplete_level_dialog(chosen_mode, level_label, target_scr)
                    else:
                        st.session_state["lm_view_mode"] = "live"
                        st.rerun()

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 2: Attempt History & Past Scorecards
    # ─────────────────────────────────────────────────────────────────────────
    with tab_history:
        if not attempts:
            st.info("No prior rehearsal attempts found under your User ID. Complete your first 30-minute session to begin your permanent scorecard history.")
        else:
            st.markdown(clean_html(f"""
            <div style="margin-bottom:16px;">
                <h3 style="font-size:1.15rem; font-weight:800; color:{t['text_primary']}; margin:0 0 4px;">
                    Permanent Rehearsal Record for User ID: <span style="color:{t['accent']}; font-family:monospace;">{user_id}</span>
                </h3>
                <p style="font-size:0.90rem; color:{t['text_secondary']}; margin:0;">
                    {len(attempts)} completed rehearsal attempt(s) saved. Select any past rehearsal to review its full scorecard and download its official PDF.
                </p>
            </div>
            """), unsafe_allow_html=True)

            for att in reversed(attempts):
                with st.container(border=True):
                    col_inf, col_btn = st.columns([75, 25])
                    with col_inf:
                        short_detail = get_attempt_short_detail(att)
                        st.markdown(f"#### ⚡ {short_detail}")
                        st.markdown(f"**Mode:** {att.get('mode', '')} &nbsp;·&nbsp; **Saved at:** {att.get('completion_date', '')}")
                        st.markdown(f"<span style='font-size:0.75rem; color:{t['text_muted']}; font-family:monospace;'>ID: {att.get('attempt_id', '')}</span>", unsafe_allow_html=True)
                    with col_btn:
                        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
                        if st.button("📄 View Scorecard", key=f"btn_hist_view_{att.get('attempt_id')}", use_container_width=True):
                            st.session_state["lm_view_attempt_id"] = att.get("attempt_id")
                            st.session_state["lm_view_mode"] = "report"
                            st.rerun()

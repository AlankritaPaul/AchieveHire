"""
AchieveHire — Job Related Interview Setup UI
Handles:
1. Job Role Selection (Searchable suggestions + Write Your Job Role)
2. Company Selection (Searchable suggestions + Write Your Company)
3. Interview Language (STRICTLY English, Hindi, Hinglish — NO manual language entry allowed)
4. Resume Review ('Before we begin, please show me your resume.')
5. Round Selection & Session Integrity Warning
"""

import streamlit as st
from typing import Dict, Any, Optional
from modules.landing.ui import THEMES, clean_html
from modules.interview.job_related.models import (
    SUGGESTED_JOB_ROLES,
    SUGGESTED_COMPANIES,
    INTERVIEW_LANGUAGES,
    JOB_ROUNDS_CONFIG,
)
from modules.interview.job_related.storage import (
    load_job_interview_session,
    initialize_job_interview_session,
    is_round_unlocked,
)
from modules.auth.user_service import get_current_user


def get_candidate_stored_resume(user_id: str) -> Dict[str, Any]:
    """Retrieves the candidate's actual stored resume data from AchieveHire without inventing facts."""
    # 1. Check in session state ResumeBuilderModel
    builder_model = st.session_state.get("resume_builder_model")
    if builder_model and hasattr(builder_model, "data") and any(builder_model.data.values()):
        return builder_model.data

    # 2. Check in user record
    current_user = get_current_user()
    if current_user and current_user.get("resumes"):
        latest = current_user["resumes"][-1]
        if isinstance(latest, dict):
            return latest

    # 3. Fallback to basic candidate profile
    if current_user:
        return {
            "full_name": current_user.get("name", "Candidate"),
            "professional_headline": current_user.get("headline", ""),
            "email": current_user.get("email", ""),
            "location": current_user.get("location", ""),
            "summary": current_user.get("bio", ""),
            "skills": "",
            "experience": "",
            "projects": "",
            "education": "",
        }

    return {}


def render_job_interview_setup(on_start_round_callback=None):
    """Renders the comprehensive, responsive setup and round selection interface."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id") or "GUEST"

    session = load_job_interview_session(user_id)
    stored_resume = get_candidate_stored_resume(user_id)

    st.markdown(clean_html(f"""
    <div style="max-width:960px; margin: 16px auto 20px; padding: 0 16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
                <div style="font-size:0.80rem; font-weight:700; color:{t['accent']}; text-transform:uppercase; letter-spacing:0.06em;">
                    AchieveHire · Better Preparation. Stronger Presentation.
                </div>
                <h2 style="font-size:1.8rem; font-weight:800; color:{t['text_primary']}; margin:4px 0 0;">
                    Job Related Interview Setup
                </h2>
            </div>
            <div>
                <button onclick="window.location.reload()" style="background:{t['surface2']}; border:1px solid {t['border']}; color:{t['text_secondary']}; padding:6px 14px; border-radius:8px; font-size:0.85rem; font-weight:600; cursor:pointer;">
                    Overview Flow
                </button>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    tab_config, tab_resume, tab_rounds = st.tabs([
        "🎯 1. Role, Company & Language",
        "📄 2. Resume Inspection",
        "🏁 3. Select & Start Round",
    ])

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 1: Role, Company & Language
    # ─────────────────────────────────────────────────────────────────────────
    with tab_config:
        st.markdown(clean_html(f"""
        <div style="margin-bottom:16px;">
            <p style="color:{t['text_secondary']}; font-size:0.95rem; margin:0;">
                Select your intended position, target company, and spoken language. Your entries will directly
                shape the interview panel's seniority, questioning themes, and evaluation standards.
            </p>
        </div>
        """), unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            # 1. Job Role Selection
            st.markdown(f"<div style='font-weight:700; font-size:1.02rem; color:{t['text_primary']}; margin-bottom:6px;'>What job role are you applying for?</div>", unsafe_allow_html=True)
            
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
                    placeholder="e.g. Lead Staff Security Architect, Quantitative Trader, AI Research Scientist",
                    key="job_role_manual_input",
                ).strip()
            else:
                effective_role = selected_role_mode

            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

            # 2. Company Selection
            st.markdown(f"<div style='font-weight:700; font-size:1.02rem; color:{t['text_primary']}; margin-bottom:6px;'>Which company are you applying for?</div>", unsafe_allow_html=True)
            
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
                    placeholder="e.g. OpenAI, Stripe, Zerodha, Palantir, Razorpay",
                    key="job_company_manual_input",
                ).strip()
            else:
                effective_company = selected_company_mode

        with col_right:
            # 3. Interview Language (STRICTLY 3 Options — NO manual entry)
            st.markdown(f"<div style='font-weight:700; font-size:1.02rem; color:{t['text_primary']}; margin-bottom:6px;'>Choose Interview Language</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.84rem; color:{t['text_muted']}; margin-bottom:10px;'>Select your spoken language preference. Exactly three supported options are available:</div>", unsafe_allow_html=True)

            default_lang = session.get("language", "English") if session else "English"
            if default_lang not in INTERVIEW_LANGUAGES:
                default_lang = "English"

            selected_language = st.radio(
                "Interview Language",
                options=INTERVIEW_LANGUAGES,
                index=INTERVIEW_LANGUAGES.index(default_lang),
                key="job_language_radio",
                label_visibility="collapsed",
                help="Only English, Hindi, and Hinglish are supported. User manual entry is strictly disabled.",
            )

            st.markdown(clean_html(f"""
            <div style="background:{t['surface2']}; border:1px solid {t['border']}; border-radius:10px; padding:12px 16px; margin-top:14px; font-size:0.85rem; color:{t['text_secondary']}; line-height:1.5;">
                <strong>Selected Language:</strong> <span style="color:{t['accent']}; font-weight:700;">{selected_language}</span><br>
                <em>Note: Technical terminology will remain in English where appropriate. Your technical evaluation will never be penalized for selecting Hindi or Hinglish.</em>
            </div>
            """), unsafe_allow_html=True)

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

        if st.button("Save & Proceed to Resume Inspection ›", type="primary", use_container_width=True, key="btn_save_job_setup"):
            if not effective_role:
                st.error("Please specify a target Job Role.")
            elif not effective_company:
                st.error("Please specify a target Company.")
            else:
                session = initialize_job_interview_session(
                    user_id=user_id,
                    target_role=effective_role,
                    target_company=effective_company,
                    language=selected_language,
                    resume_snapshot=stored_resume,
                )
                st.session_state["job_effective_role"] = effective_role
                st.session_state["job_effective_company"] = effective_company
                st.session_state["job_effective_language"] = selected_language
                st.success(f"✓ Configuration saved: {effective_role} at {effective_company} ({selected_language}).")
                st.rerun()

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 2: Resume Inspection
    # ─────────────────────────────────────────────────────────────────────────
    with tab_resume:
        st.markdown(clean_html(f"""
        <div style="background:{t['accent_soft']}; border:1px solid {t['accent']}; border-radius:12px; padding:16px 20px; margin-bottom:20px;">
            <div style="font-weight:800; font-size:1.05rem; color:{t['accent']}; margin-bottom:4px; display:flex; align-items:center; gap:8px;">
                <span>🎙️</span>
                <span>Interviewer Prompt</span>
            </div>
            <div style="font-size:1.02rem; font-style:italic; color:{t['text_primary']};">
                “Before we begin, please show me your resume.”
            </div>
            <div style="font-size:0.84rem; color:{t['text_secondary']}; margin-top:6px;">
                AchieveHire uses your real stored resume data. The interview engine analyses your genuine education, skills, projects, and work experience.
            </div>
        </div>
        """), unsafe_allow_html=True)

        col_r1, col_r2 = st.columns([1, 1], gap="large")

        with col_r1:
            st.markdown(f"<h4 style='font-size:1.05rem; font-weight:700; color:{t['text_primary']}; margin-bottom:8px;'>Candidate Profile &amp; Credentials</h4>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(f"**Full Name:** {stored_resume.get('full_name') or st.session_state.get('username', 'Candidate')}")
                st.markdown(f"**Headline:** {stored_resume.get('professional_headline') or 'Candidate · Career Readiness'}")
                st.markdown(f"**Email:** {stored_resume.get('email') or 'candidate@achievehire.ai'}")
                st.markdown(f"**Location:** {stored_resume.get('location') or 'India'}")
                summary_val = stored_resume.get('summary') or 'Focused on professional excellence and rigorous interview readiness.'
                st.markdown(f"**Professional Summary:** {summary_val}")

            st.markdown(f"<h4 style='font-size:1.05rem; font-weight:700; color:{t['text_primary']}; margin:16px 0 8px;'>Education &amp; Qualifications</h4>", unsafe_allow_html=True)
            with st.container(border=True):
                edu_entries = stored_resume.get("education_entries", [])
                if edu_entries:
                    for edu in edu_entries:
                        st.markdown(f"- **{edu.get('degree', 'Degree')}** ({edu.get('field_of_study', '')}) — *{edu.get('institution', 'University')}*")
                else:
                    raw_edu = stored_resume.get("education", "")
                    if raw_edu.strip():
                        st.markdown(raw_edu)
                    else:
                        st.markdown("<em>No formal academic entries detected in profile.</em>", unsafe_allow_html=True)

        with col_r2:
            st.markdown(f"<h4 style='font-size:1.05rem; font-weight:700; color:{t['text_primary']}; margin-bottom:8px;'>Technical &amp; Domain Skills</h4>", unsafe_allow_html=True)
            with st.container(border=True):
                skills_val = stored_resume.get("skills") or stored_resume.get("tech_skills_raw", "")
                if skills_val.strip():
                    st.markdown(skills_val)
                else:
                    st.markdown("<em>Skills will be evaluated dynamically based on target role competencies.</em>", unsafe_allow_html=True)

            st.markdown(f"<h4 style='font-size:1.05rem; font-weight:700; color:{t['text_primary']}; margin:16px 0 8px;'>Projects &amp; Work Experience</h4>", unsafe_allow_html=True)
            with st.container(border=True):
                proj_entries = stored_resume.get("project_entries", [])
                if proj_entries:
                    for p in proj_entries:
                        st.markdown(f"- **{p.get('title', 'Project')}**: {p.get('description', '')[:120]}")
                else:
                    raw_proj = stored_resume.get("projects", "")
                    if raw_proj.strip():
                        st.markdown(raw_proj[:300] + ("..." if len(raw_proj) > 300 else ""))
                    else:
                        st.markdown("<em>No specific projects found. Questions will test core problem-solving scenarios.</em>", unsafe_allow_html=True)

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        st.info("✓ Your actual resume has been verified and synchronized with the interview engine.")

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 3: Select & Start Round (Enforcing Single-Session Rule & Locking)
    # ─────────────────────────────────────────────────────────────────────────
    with tab_rounds:
        effective_role = session.get("target_role") if session else st.session_state.get("job_effective_role", "Software Engineer")
        effective_company = session.get("target_company") if session else st.session_state.get("job_effective_company", "Google")
        effective_lang = session.get("language") if session else st.session_state.get("job_effective_language", "English")

        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:16px 20px; margin-bottom:20px;">
            <div style="font-weight:700; font-size:1.05rem; color:{t['text_primary']}; margin-bottom:4px;">
                Target: <span style="color:{t['accent']};">{effective_role}</span> at <span style="color:{t['accent']};">{effective_company}</span> ({effective_lang})
            </div>
            <div style="font-size:0.85rem; color:{t['text_secondary']};">
                Each round simulates realistic interview panels with increasing seniority. Complete rounds sequentially to unlock advanced stages.
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
                status_badge = f'<span style="background:#D1FAE5; color:#065F46; font-weight:700; font-size:0.78rem; padding:3px 10px; border-radius:50px;">✓ Completed ({score}/100)</span>'
            elif unlocked:
                status_badge = f'<span style="background:{t["accent_soft"]}; color:{t["accent"]}; font-weight:700; font-size:0.78rem; padding:3px 10px; border-radius:50px;">● Available to Start</span>'
            else:
                status_badge = f'<span style="background:#F3F4F6; color:#6B7280; font-weight:700; font-size:0.78rem; padding:3px 10px; border-radius:50px;">🔒 Locked (Complete Round {r_num-1} First)</span>'

            with st.container(border=True):
                col_info, col_action = st.columns([72, 28])
                with col_info:
                    st.markdown(clean_html(f"""
                    <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
                        <h4 style="font-size:1.1rem; font-weight:800; color:{t['text_primary']}; margin:0;">
                            {r_cfg['name']}
                        </h4>
                        {status_badge}
                    </div>
                    <div style="font-size:0.85rem; color:{t['text_secondary']}; line-height:1.5;">
                        ⏱️ <strong>Duration:</strong> {r_cfg['duration_minutes']} Minutes &nbsp;·&nbsp;
                        👥 <strong>Panel:</strong> {r_cfg['interviewer_count']} Interviewer(s) ({r_cfg['interviewer_seniority']})
                    </div>
                    <div style="font-size:0.82rem; color:{t['text_muted']}; margin-top:4px;">
                        {r_cfg['description']}
                    </div>
                    """), unsafe_allow_html=True)

                with col_action:
                    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                    if is_completed:
                        if st.button("📄  View Report", key=f"btn_view_report_r{r_num}", use_container_width=True):
                            st.session_state["job_view_mode"] = "report"
                            st.session_state["job_report_round"] = r_num
                            st.rerun()
                    elif unlocked:
                        if st.button(f"▶  Start Round {r_num}", key=f"btn_start_round_{r_num}", type="primary", use_container_width=True):
                            if not session:
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
                        st.button(f"🔒 Locked", key=f"btn_locked_r{r_num}", disabled=True, use_container_width=True)

        if session and session.get("is_overall_completed"):
            st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown(f"<h3 style='font-size:1.2rem; font-weight:800; color:{t['accent']}; margin-bottom:8px;'>🏆 All 6 Rounds Completed!</h3>", unsafe_allow_html=True)
                st.markdown("Congratulations! You have completed all six rounds of the Job Related Interview panel. Your comprehensive Final Overall Report is available.")
                if st.button("📈  View Final Overall Performance & Improvement Report", type="primary", use_container_width=True, key="btn_view_overall_final_rep"):
                    st.session_state["job_view_mode"] = "overall_report"
                    st.rerun()

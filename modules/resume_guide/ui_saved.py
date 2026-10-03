"""
AchieveHire — Multiple Saved Resumes Management UI
Allows candidates to:
1. View all saved resumes created under their unique User ID
2. Inspect resume details (skills, target role, education, experience)
3. Send any resume directly to Resume Analysis
4. Create new additional resumes without overwriting earlier resumes
"""

import streamlit as st
from modules.landing.ui import THEMES, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer
from modules.auth.user_service import get_user_resumes, get_current_user, update_user_record


def render_saved_resumes_screen():
    """Renders the candidate's multiple saved resumes management dashboard."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id") or "GUEST"

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Resume › My Saved Resumes")

    resumes = get_user_resumes(user_id)

    st.markdown(clean_html(f"""
    <div style="max-width:960px; margin: 16px auto 20px; padding: 0 16px;">
        <div style="font-size:0.80rem; font-weight:700; color:{t['accent']}; text-transform:uppercase; letter-spacing:0.06em;">
            AchieveHire · Multiple Resumes Workspace
        </div>
        <h1 style="font-size:1.9rem; font-weight:800; color:{t['text_primary']}; margin:4px 0 6px;">
            📂 My Saved Resumes
        </h1>
        <p style="font-size:0.95rem; color:{t['text_secondary']}; max-width:760px; line-height:1.55; margin:0;">
            Manage and analyze your multiple resumes. Every resume you create or upload is preserved permanently under User ID: <code>{user_id}</code>.
        </p>
    </div>
    """), unsafe_allow_html=True)

    col_btn, col_count = st.columns([1, 1], gap="medium")
    with col_btn:
        if st.button("➕ Create Another Resume", type="primary", use_container_width=True, key="btn_create_another_res"):
            st.session_state["ac_screen"] = "resume_create"
            st.rerun()
    with col_count:
        st.markdown(f"<div style='font-size:0.95rem; font-weight:600; color:{t['text_secondary']}; padding-top:8px;'>Total Resumes Available: <strong>{len(resumes)}</strong></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    if not resumes:
        st.info("No resumes currently saved under your account. Click 'Create Another Resume' or upload a resume in Resume Analysis to start building your collection.")
    else:
        for idx, res in enumerate(reversed(resumes)):
            with st.container(border=True):
                r_col_info, r_col_actions = st.columns([70, 30])
                r_title = res.get("target_role") or res.get("title") or f"Resume #{len(resumes) - idx}"
                r_name = res.get("full_name") or res.get("name") or "Candidate"
                r_date = res.get("saved_at") or res.get("created_at") or "Recently saved"
                r_skills = res.get("skills", "")
                if isinstance(r_skills, list):
                    r_skills = ", ".join(r_skills)

                with r_col_info:
                    st.markdown(f"### 📄 {r_title}")
                    st.markdown(f"**Candidate:** {r_name} &nbsp;·&nbsp; **Saved on:** {r_date}")
                    if r_skills:
                        st.markdown(f"<div style='font-size:0.85rem; color:{t['text_secondary']}; margin-top:4px;'><strong>Skills:</strong> {r_skills[:120]}...</div>", unsafe_allow_html=True)
                    if res.get("summary"):
                        st.markdown(f"<div style='font-size:0.82rem; color:{t['text_muted']}; margin-top:4px;'><em>{res.get('summary')[:160]}...</em></div>", unsafe_allow_html=True)

                with r_col_actions:
                    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                    if st.button("🔍 Analyze This Resume", key=f"btn_analyze_saved_{res.get('id', idx)}", use_container_width=True, type="primary"):
                        st.session_state["active_analysis_resume"] = res
                        st.session_state["ac_screen"] = "resume_analysis"
                        st.rerun()

                    if st.button("🗑️ Delete", key=f"btn_delete_saved_{res.get('id', idx)}", use_container_width=True):
                        user = get_current_user()
                        if user and "resumes" in user:
                            user["resumes"] = [r for r in user["resumes"] if r.get("id") != res.get("id")]
                            update_user_record(user_id, {"resumes": user["resumes"]})
                            st.rerun()

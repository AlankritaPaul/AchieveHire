"""
Main Resume Guide router for AscendCareer.
Presents a dedicated landing page where the user chooses between:
1. Resume Analysis
2. Create Resume
No 'I have / not have' text, no 'path', no 'active' badges.
"""

import streamlit as st
from modules.landing.ui import THEMES
from modules.resume_guide.ui_analysis import render_resume_analysis_flow
from modules.resume_guide.ui_builder import render_create_resume_flow

def render_resume_guide():
    """Render the top-level Resume Guide section."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    if "resume_guide_mode" not in st.session_state:
        st.session_state.resume_guide_mode = None

    # Top Header
    st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <h1 style="font-size: 2.2rem; font-weight: 800; color: {t['text_primary']}; margin: 0;">Resume Guide</h1>
            <p style="font-size: 1.05rem; color: {t['text_secondary']}; margin-top: 4px;">Choose an option to begin preparing your resume.</p>
        </div>
    """, unsafe_allow_html=True)

    # LANDING PAGE: Choose between Resume Analysis and Create Resume
    if st.session_state.resume_guide_mode is None:
        st.markdown(f"<h3 style='color:{t['text_primary']};'>Choose an Option</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
                <div style="border: 1.5px solid {t['border']}; border-radius: 10px; padding: 24px; background: {t['surface']}; height: 190px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: {t['card_shadow']};">
                    <div>
                        <h3 style="margin: 0; color: {t['accent']}; font-size: 1.35rem;">Resume Analysis</h3>
                        <p style="color: {t['text_secondary']}; font-size: 0.95rem; margin-top: 8px;">Upload your current resume to evaluate its alignment with your selected job role, company, and optional job description.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("Open Resume Analysis →", type="primary", use_container_width=True, key="btn_choose_analysis"):
                st.session_state.resume_guide_mode = "Resume Analysis"
                st.session_state.analysis_step = 1
                st.rerun()

        with col2:
            st.markdown(f"""
                <div style="border: 1.5px solid {t['border']}; border-radius: 10px; padding: 24px; background: {t['surface']}; height: 190px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: {t['card_shadow']};">
                    <div>
                        <h3 style="margin: 0; color: #10B981; font-size: 1.35rem;">Create Resume</h3>
                        <p style="color: {t['text_secondary']}; font-size: 0.95rem; margin-top: 8px;">Create a well-structured, professional resume tailored to your target job role and company.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("Open Create Resume →", type="primary", use_container_width=True, key="btn_choose_create"):
                st.session_state.resume_guide_mode = "Create Resume"
                st.session_state.builder_step = 1
                st.rerun()

    # SUB-FLOW: Resume Analysis
    elif st.session_state.resume_guide_mode == "Resume Analysis":
        col_nav, col_space = st.columns([1, 4])
        with col_nav:
            if st.button("← Back to Options", key="btn_back_to_home_from_analysis"):
                st.session_state.resume_guide_mode = None
                st.rerun()
        st.markdown("---")
        render_resume_analysis_flow()

    # SUB-FLOW: Create Resume
    elif st.session_state.resume_guide_mode == "Create Resume":
        col_nav, col_space = st.columns([1, 4])
        with col_nav:
            if st.button("← Back to Options", key="btn_back_to_home_from_builder"):
                st.session_state.resume_guide_mode = None
                st.rerun()
        st.markdown("---")
        render_create_resume_flow()

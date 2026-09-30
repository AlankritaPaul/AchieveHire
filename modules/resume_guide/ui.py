"""
Main Resume Guide router for AscendCareer.
Provides the two primary user paths:
1. 'I Have a Resume' -> Continue to Resume Analysis
2. 'I Don't Have a Resume' -> Continue to Create Resume
Users can switch between paths at any time.
"""

import streamlit as st
from modules.resume_guide.ui_analysis import render_resume_analysis_flow
from modules.resume_guide.ui_builder import render_create_resume_flow

def render_resume_guide():
    """Render the top-level Resume Guide section with two paths."""
    st.markdown("""
        <style>
        .guide-main-header {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1A365D;
            margin-bottom: 0.2rem;
        }
        .guide-sub-header {
            font-size: 1.05rem;
            color: #4A5568;
            margin-bottom: 1.5rem;
        }
        .path-selector-card {
            border: 2px solid #E2E8F0;
            border-radius: 10px;
            padding: 18px;
            background: #FFFFFF;
            transition: all 0.2s ease-in-out;
        }
        .path-selector-card:hover {
            border-color: #3182CE;
            box-shadow: 0 4px 12px rgba(49, 130, 206, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="guide-main-header">📄 Resume Guide</div>', unsafe_allow_html=True)
    st.markdown('<div class="guide-sub-header">Select your path to either evaluate your existing resume or craft a targeted, high-impact resume from scratch.</div>', unsafe_allow_html=True)

    if "resume_path_choice" not in st.session_state:
        st.session_state.resume_path_choice = "I Have a Resume"

    # Top Path Switcher / Radio buttons
    col_path, col_status = st.columns([3, 1])
    with col_path:
        path_selected = st.radio(
            "Choose your starting point:",
            options=["I Have a Resume", "I Don't Have a Resume"],
            index=0 if st.session_state.resume_path_choice == "I Have a Resume" else 1,
            horizontal=True,
            key="guide_path_radio"
        )
        st.session_state.resume_path_choice = path_selected

    with col_status:
        if path_selected == "I Have a Resume":
            st.markdown("""
                <div style="background: #EBF8FF; border-left: 3px solid #3182CE; padding: 6px 12px; border-radius: 4px; font-size: 0.85rem; color: #2B6CB0; margin-top: 15px;">
                    <strong>Active:</strong> Resume Analysis
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background: #F0FFF4; border-left: 3px solid #38A169; padding: 6px 12px; border-radius: 4px; font-size: 0.85rem; color: #22543D; margin-top: 15px;">
                    <strong>Active:</strong> Create Resume
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Route based on user selection
    if st.session_state.resume_path_choice == "I Have a Resume":
        render_resume_analysis_flow()
    else:
        render_create_resume_flow()

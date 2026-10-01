"""
AscendCareer - Comprehensive Voice-Based Interview Preparation & Career-Readiness Platform
Main Streamlit Application Entrypoint
"""

import streamlit as st
from modules.landing.ui import render_landing

# Page Configuration
st.set_page_config(
    page_title="AscendCareer | AI Career & Interview Readiness",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main():
    # ── Session state defaults ────────────────────────────────────────────────
    if "ac_screen" not in st.session_state:
        st.session_state["ac_screen"] = "landing"   # Start on landing screen

    screen = st.session_state["ac_screen"]

    # ── Landing Screen ────────────────────────────────────────────────────────
    if screen == "landing":
        result = render_landing()
        if result["proceed"]:
            # Sign In clicked → maintain screen (user specified: what will come after clicking sign in option I will tell you later)
            st.session_state["ac_screen"] = "landing"
            st.rerun()

    # ── Resume Create Flow ────────────────────────────────────────────────────
    elif screen == "resume_create":
        from modules.landing.ui import THEMES
        from modules.navigation.panel import render_navigation_drawer, render_top_nav_bar
        from modules.resume_guide.ui_builder import render_create_resume_flow
        t = THEMES[st.session_state.get("ac_theme", "light")]
        render_navigation_drawer(t)
        render_top_nav_bar(t, title="Resume › Resume Create", show_signin=True)
        render_create_resume_flow()

    # ── Resume Analysis Flow ──────────────────────────────────────────────────
    elif screen == "resume_analysis":
        from modules.landing.ui import THEMES
        from modules.navigation.panel import render_navigation_drawer, render_top_nav_bar
        from modules.resume_guide.ui_analysis import render_resume_analysis_flow
        t = THEMES[st.session_state.get("ac_theme", "light")]
        render_navigation_drawer(t)
        render_top_nav_bar(t, title="Resume › Resume Analysis", show_signin=True)
        render_resume_analysis_flow()

    # ── Specialized Interview Flow ────────────────────────────────────────────
    elif screen == "interview_specialized":
        from modules.interview.specialized_ui import render_specialized_interview
        render_specialized_interview()

    # ── Job Related Interview Flow ────────────────────────────────────────────
    elif screen == "interview_job":
        from modules.interview.job_related_ui import render_job_related_interview
        render_job_related_interview()

    # ── Complete User Profile Page ────────────────────────────────────────────
    elif screen == "profile":
        from modules.profile.ui import render_user_profile
        render_user_profile()

    # ── Privacy Policy Section ────────────────────────────────────────────────
    elif screen == "privacy":
        from modules.legal.privacy_ui import render_privacy_page
        render_privacy_page()

    # ── Terms & Conditions Page ───────────────────────────────────────────────
    elif screen == "terms":
        from modules.legal.terms_ui import render_terms_page
        render_terms_page()

    # ── Main Application (legacy fallback) ───────────────────────────────────
    elif screen == "app":
        _render_main_app()


def _render_main_app():
    """
    Renders the main AscendCareer application after authentication.
    Sign-in / profile setup steps will be inserted before this in the next milestone.
    """
    # Sidebar Branding & Navigation
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h1 style="font-size: 1.8rem; margin: 0; color: #1A365D;">AscendCareer</h1>
                <p style="font-size: 0.85rem; color: #718096; margin-top: 4px;">Realistic AI Interview Preparation & Career Readiness</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Platform Modules")

        # Main section selection
        app_mode = st.radio(
            "Navigation",
            options=[
                "📄 Resume Guide",
                "🎙️ Voice Interview (Stage 1-6)",
                "📈 Preparation Analytics",
                "🏅 Certified Profile"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("""
            <div style="background-color: #EDF2F7; padding: 0.8rem; border-radius: 6px; font-size: 0.8rem; color: #4A5568;">
                <strong>Cycle of Improvement:</strong><br>
                Weakness → Training → Re-practice → Verification → Improvement
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("← Back to Landing", key="back_to_landing"):
            st.session_state["ac_screen"] = "landing"
            st.rerun()

    # Route navigation
    if app_mode == "📄 Resume Guide":
        from modules.resume_guide.ui import render_resume_guide
        render_resume_guide()
    elif app_mode == "🎙️ Voice Interview (Stage 1-6)":
        st.info("🎙️ **Voice Interview Simulator**: Real-time microphone-driven conversational engine across progressive Levels 1-6 will be activated in the upcoming milestone.")
    elif app_mode == "📈 Preparation Analytics":
        st.info("📈 **Preparation Analytics**: Historical progress, weakness tracking, and readiness metrics dashboard.")
    elif app_mode == "🏅 Certified Profile":
        st.info("🏅 **Certified Profile**: Verifiable completion certificates and public career profiles.")


if __name__ == "__main__":
    main()

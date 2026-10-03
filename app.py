"""
AchieveHire - Comprehensive Voice-Based Interview Preparation & Career-Readiness Platform
Main Streamlit Application Entrypoint
"""

import streamlit as st
from modules.landing.ui import render_landing

# Page Configuration
st.set_page_config(
    page_title="AchieveHire | AI Career & Interview Readiness",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main():
    from modules.admin.analytics_ui import track_platform_visit
    track_platform_visit()

    # ── Session state defaults ────────────────────────────────────────────────
    if "ac_screen" not in st.session_state:
        st.session_state["ac_screen"] = "landing"   # Start on landing screen

    if "ac_theme" not in st.session_state:
        if "theme" in st.query_params and st.query_params.get("theme") in ["light", "dark"]:
            st.session_state["ac_theme"] = st.query_params.get("theme")
        else:
            st.session_state["ac_theme"] = "light"

    screen = st.session_state["ac_screen"]
    
    from modules.landing.ui import THEMES, _inject_css
    t = THEMES[st.session_state["ac_theme"]]
    _inject_css(t)

    # ── Authentication Guard for Core Platform Features ───────────────────────
    PROTECTED_SCREENS = {
        "resume_create": "Resume Create & Builder",
        "resume_analysis": "Resume Analysis & Audit",
        "interview_specialized": "Specialized Voice Interview",
        "interview_job": "Job Related Voice Interview",
    }
    if screen in PROTECTED_SCREENS and not st.session_state.get("user_id"):
        st.session_state["auth_popup_open"] = True
        st.session_state["auth_popup_feature"] = PROTECTED_SCREENS[screen]
        st.session_state["ac_screen"] = "landing"
        st.rerun()

    # ── Landing Screen ────────────────────────────────────────────────────────
    if screen == "landing":
        result = render_landing()
        if result["proceed"]:
            # Sign In clicked → route to Candidate Setup & User ID Generation flow
            st.session_state["ac_screen"] = "signin"
            st.rerun()

    # ── Candidate Sign In & User ID Generation Flow ───────────────────────────
    elif screen == "signin":
        from modules.auth.signin_ui import render_signin_flow
        render_signin_flow()

    # ── Resume Create Flow ────────────────────────────────────────────────────
    elif screen == "resume_create":
        from modules.landing.ui import THEMES
        from modules.navigation.panel import render_navigation_drawer, render_top_nav_bar
        from modules.resume_guide.ui_builder import render_create_resume_flow
        t = THEMES[st.session_state.get("ac_theme", "light")]
        render_navigation_drawer(t)
        render_top_nav_bar(t, title="Resume › Resume Create")
        render_create_resume_flow()

    # ── Resume Analysis Flow ──────────────────────────────────────────────────
    elif screen == "resume_analysis":
        from modules.landing.ui import THEMES
        from modules.navigation.panel import render_navigation_drawer, render_top_nav_bar
        from modules.resume_guide.ui_analysis import render_resume_analysis_flow
        t = THEMES[st.session_state.get("ac_theme", "light")]
        render_navigation_drawer(t)
        render_top_nav_bar(t, title="Resume › Resume Analysis")
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

    # ── FAQ Page ─────────────────────────────────────────────────────────────
    elif screen == "faq":
        from modules.legal.faq_ui import render_faq_page
        render_faq_page()

    # ── Privacy Policy Section ────────────────────────────────────────────────
    elif screen == "privacy":
        from modules.legal.privacy_ui import render_privacy_page
        render_privacy_page()

    # ── Terms & Conditions Page ───────────────────────────────────────────────
    elif screen == "terms":
        from modules.legal.terms_ui import render_terms_page
        render_terms_page()

    # ── Application Settings Page ────────────────────────────────────────────
    elif screen == "settings":
        from modules.settings.ui import render_settings_page
        render_settings_page()

    # ── Founder Analytics Dashboard ───────────────────────────────────────────
    elif screen == "founder_analytics":
        from modules.admin.analytics_ui import render_analytics_dashboard
        render_analytics_dashboard()

    # ── Main Application (legacy fallback) ───────────────────────────────────
    elif screen == "app":
        _render_main_app()


def _render_main_app():
    """
    Renders the main AchieveHire application after authentication.
    Sign-in / profile setup steps will be inserted before this in the next milestone.
    """
    # Sidebar Branding & Navigation
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h1 style="font-size: 1.8rem; margin: 0; color: #1A365D;">AchieveHire</h1>
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

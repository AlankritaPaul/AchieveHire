"""
AchieveHire — Frequently Asked Questions (FAQ) Section
Provides clear, authoritative answers regarding platform workflow,
resume creation, analysis accuracy, account controls, pricing, and interview practice.
"""

import streamlit as st
from modules.landing.ui import THEMES, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer


FAQ_ITEMS = [
    {
        "number": "1",
        "q": "How does AchieveHire work?",
        "a": "AchieveHire is a career-preparation platform designed to help candidates prepare for opportunities through resume creation, resume analysis, and interview practice. Users can create and manage their professional profile, prepare a job-oriented resume, review and improve their resume, and practise interviews based on their selected career goals.",
    },
    {
        "number": "2",
        "q": "How do I create a resume?",
        "a": "Go to the Resume section and select Resume Create. Enter your professional information, education, qualifications, skills, projects, experience, and other relevant details. You can choose from the available resume templates and customise your information before generating your resume.",
    },
    {
        "number": "3",
        "q": "Can I edit my resume after creating it?",
        "a": "Yes. Your resume remains under your control. You can update, edit, add, or remove information whenever required. Changes to your personal or professional information should not require creating a completely new account.",
    },
    {
        "number": "4",
        "q": "How does Resume Analysis work?",
        "a": "Resume Analysis reviews the information actually provided in your resume. It identifies areas that are well-presented and areas that may need improvement. AchieveHire does not assume or invent missing projects, skills, education, experience, achievements, or other information. If important information is missing, you may be asked to provide that information before an improvement can be suggested.",
    },
    {
        "number": "5",
        "q": "Can I delete my account?",
        "a": "Yes. You can request or initiate account deletion through the Account or Privacy section, depending on the available account controls. Account deletion should be clearly communicated before the final confirmation so that you understand what will happen to your account and associated data.",
    },
    {
        "number": "6",
        "q": "What happens to my resume and profile after account deletion?",
        "a": "When an account is deleted, your associated profile and resume data will be handled according to AchieveHire's Privacy Policy and applicable data-retention requirements. Information that is no longer required should be deleted according to the platform's stated deletion process. Any information that must be retained for legitimate legal or security purposes will be handled according to the Privacy Policy.",
    },
    {
        "number": "7",
        "q": "Is AchieveHire free?",
        "a": "Yes. AchieveHire is designed as a free career-preparation platform. Any feature that may require payment in the future must be clearly identified before a user is asked to pay.",
    },
    {
        "number": "8",
        "q": "How does Interview Practice work?",
        "a": "Interview Practice allows candidates to practise interviews based on their selected job role and company-related preferences. Depending on the selected interview mode, the experience may include realistic interview questions, multiple interviewer perspectives or voices, and structured practice designed to help candidates prepare more effectively. The system should not present practice results as guaranteed predictions of actual interview outcomes.",
    },
]


def render_faq_page():
    """Renders the comprehensive Frequently Asked Questions page."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Platform Guidance › FAQ")

    st.markdown(clean_html(f"""
    <div style="max-width:960px; margin: 24px auto; padding: 0 16px;">
        <div style="margin-bottom: 24px;">
            <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.80rem; font-weight:700; padding:4px 14px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
                Platform Guidance & Architecture
            </div>
            <h1 style="font-size: 2.2rem; font-weight: 800; color:{t['text_primary']}; margin:0 0 8px;">
                Frequently Asked Questions (FAQ)
            </h1>
            <p style="font-size: 1.05rem; color:{t['text_secondary']}; max-width:800px; line-height:1.75; margin:0;">
                Clear, transparent answers on how AchieveHire works, how your data is protected, and how to maximize your preparation.
            </p>
        </div>
    </div>
    """), unsafe_allow_html=True)

    for item in FAQ_ITEMS:
        st.markdown(clean_html(f"""
        <div style="max-width:960px; margin: 8px auto; padding: 0 16px;">
        </div>
        """), unsafe_allow_html=True)
        with st.expander(f"❓  {item['number']}. {item['q']}", expanded=True):
            st.markdown(
                f"<div style='font-size:0.98rem; color:{t['text_secondary']}; line-height:1.8; padding:4px 2px;'>"
                f"{item['a']}"
                f"</div>",
                unsafe_allow_html=True,
            )

"""
AscendCareer — Dedicated Privacy Section
Provides transparent, detailed explanation of personal information protection,
resume handling, uploaded document storage, zero unauthorized sharing, and account deletion.
"""

import streamlit as st
from modules.landing.content import PRIVACY_STATEMENT, PRIVACY_SECTIONS
from modules.landing.ui import THEMES, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer


def render_privacy_page():
    """Renders the comprehensive Privacy section."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Platform Policies › Privacy Policy")

    st.markdown(clean_html(f"""
    <div style="max-width:960px; margin: 24px auto; padding: 0 16px;">
        <div style="margin-bottom: 24px;">
            <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.80rem; font-weight:700; padding:4px 14px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
                Transparency & Data Protection
            </div>
            <h1 style="font-size: 2.2rem; font-weight: 800; color:{t['text_primary']}; margin:0 0 8px;">
                Privacy Policy & Information Handling
            </h1>
            <p style="font-size: 1.05rem; color:{t['text_secondary']}; max-width:800px; line-height:1.75; margin:0;">
                {PRIVACY_STATEMENT}
            </p>
        </div>

        <div style="background:{t['surface']}; border:1px solid {t['border']}; border-left:4px solid {t['accent']}; border-radius:12px; padding:20px 24px; margin-bottom:32px;">
            <div style="font-weight:700; font-size:1.02rem; color:{t['text_primary']}; margin-bottom:6px;">
                Our Privacy Pledge
            </div>
            <div style="font-size:0.94rem; color:{t['text_secondary']}; line-height:1.7;">
                AscendCareer does not sell, monetize, or disclose candidate resumes, personal profiles, or interview recordings to third parties or recruiters without explicit candidate authorization. Your data belongs exclusively to you.
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # Render Q&A Sections from finalized content
    for section in PRIVACY_SECTIONS:
        # We focus on Privacy Policy, Account Deletion, Secure Authentication, Data Protection
        if "Terms" in section["title"]:
            continue
        st.markdown(clean_html(f"""
        <div style="max-width:960px; margin: 16px auto; padding: 0 16px;">
            <h2 style="font-size: 1.3rem; font-weight: 700; color:{t['text_primary']}; margin: 24px 0 12px; border-bottom:1px solid {t['border']}; padding-bottom:8px;">
                {section['title']}
            </h2>
        </div>
        """), unsafe_allow_html=True)

        for item in section["qa"]:
            with st.expander(f"📌  {item['q']}", expanded=True):
                st.markdown(f"<div style='font-size:0.95rem; color:{t['text_secondary']}; line-height:1.75;'>{item['a']}</div>", unsafe_allow_html=True)

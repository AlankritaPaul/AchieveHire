"""
AscendCareer — Founder Analytics Dashboard
Provides high-level aggregated usage statistics exclusively for the founder.
100% honest metrics derived directly from real database records.
"""

import json
import os
import streamlit as st
import pandas as pd
from modules.landing.ui import THEMES, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "users.json")

def _get_platform_stats():
    """Reads users.json and computes real, truthful aggregated metrics without exposing personal details."""
    stats = {
        "total_signins": 0,
        "resume_users": 0,
        "interview_users": 0,
        "both_users": 0,
        "total_resumes_created": 0,
        "total_interviews_practiced": 0,
    }
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
                stats["total_signins"] = len(users)
                for uid, udata in users.items():
                    purpose = udata.get("purpose", "Both")
                    if purpose == "Resume Preparation":
                        stats["resume_users"] += 1
                    elif purpose == "Interview Preparation":
                        stats["interview_users"] += 1
                    else:
                        stats["both_users"] += 1
                    
                    user_stats = udata.get("stats", {})
                    stats["total_resumes_created"] += user_stats.get("resumes_created", 0)
                    stats["total_interviews_practiced"] += user_stats.get("interviews_practiced", 0)
        except Exception:
            pass
            
    return stats


def render_analytics_dashboard():
    """Renders the analytics dashboard (Restricted to ALANKRITA-FOUNDER)."""
    # Security Check
    if st.session_state.get("user_id") != "ALANKRITA-FOUNDER":
        st.error("🔒 Access Denied: This dashboard is strictly restricted to the Founder.")
        if st.button("Return Home"):
            st.session_state["ac_screen"] = "landing"
            st.rerun()
        return

    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Founder Controls › Platform Analytics", show_signin=False, show_theme=False)

    stats = _get_platform_stats()

    st.markdown(clean_html(f"""
    <div style="max-width:900px; margin: 0 auto; padding: 24px 16px;">
        <h1 style="font-family:'Playfair Display', serif; font-size:2.2rem; color:{t['text_primary']}; margin-bottom:8px;">
            Platform Analytics
        </h1>
        <p style="font-size:1.05rem; color:{t['text_muted']}; margin-bottom:32px;">
            Real, aggregated platform data. No personal candidate details or names are exposed.
        </p>
    </div>
    """), unsafe_allow_html=True)

    # Real Metrics Row (Truthful numbers only)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; padding:24px; border-radius:16px; border:1px solid {t['border']}; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="font-size:1.8rem; margin-bottom:8px;">👥</div>
            <div style="font-size:0.9rem; color:{t['text_muted']}; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Registered Candidates</div>
            <div style="font-size:2.4rem; font-weight:800; color:{t['text_primary']};">{stats['total_signins']}</div>
        </div>
        """), unsafe_allow_html=True)
    with m2:
        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; padding:24px; border-radius:16px; border:1px solid {t['border']}; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="font-size:1.8rem; margin-bottom:8px;">📄</div>
            <div style="font-size:0.9rem; color:{t['text_muted']}; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Resume Focus Users</div>
            <div style="font-size:2.4rem; font-weight:800; color:{t['text_primary']};">{stats['resume_users'] + stats['both_users']}</div>
        </div>
        """), unsafe_allow_html=True)
    with m3:
        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; padding:24px; border-radius:16px; border:1px solid {t['border']}; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="font-size:1.8rem; margin-bottom:8px;">🎙️</div>
            <div style="font-size:0.9rem; color:{t['text_muted']}; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Interview Focus Users</div>
            <div style="font-size:2.4rem; font-weight:800; color:{t['text_primary']};">{stats['interview_users'] + stats['both_users']}</div>
        </div>
        """), unsafe_allow_html=True)

    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

    # Chart Section Header
    st.markdown(clean_html(f"""
    <div style="max-width:900px; margin: 0 auto;">
        <h3 style="font-family:'DM Sans', sans-serif; font-size:1.3rem; color:{t['text_primary']}; margin-bottom:16px;">
            Feature Focus Distribution
        </h3>
    </div>
    """), unsafe_allow_html=True)

    # Prepare data for Streamlit native bar chart safely outside f-strings
    chart_df = pd.DataFrame({
        "Feature": ["Resume Preparation", "Interview Preparation", "Both Features"],
        "Candidates": [stats["resume_users"], stats["interview_users"], stats["both_users"]]
    }).set_index("Feature")

    c1, c2, c3 = st.columns([1, 10, 1])
    with c2:
        st.bar_chart(chart_df, y="Candidates", color="#10B981")

    st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)

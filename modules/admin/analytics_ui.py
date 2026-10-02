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
ANALYTICS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "platform_analytics.json")


def track_platform_visit():
    """Dynamically tracks app visits every time a user visits the platform."""
    if "session_visit_logged" not in st.session_state:
        st.session_state["session_visit_logged"] = True
        _increment_analytics_counter("total_visits")


def track_platform_action():
    """Dynamically tracks user actions across the platform."""
    _increment_analytics_counter("total_actions")


def _increment_analytics_counter(key: str):
    data = {"total_visits": 0, "total_actions": 0}
    if os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass
    data[key] = data.get(key, 0) + 1
    try:
        os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)
        with open(ANALYTICS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def _get_platform_stats():
    """Reads users.json and platform_analytics.json to compute real, truthful aggregated metrics."""
    stats = {
        "registered_candidates": 0,
        "resume_users": 0,
        "interview_users": 0,
        "both_users": 0,
        "total_resumes_created": 0,
        "total_interviews_practiced": 0,
        "total_visits": 0,
        "total_actions": 0,
    }
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                users = json.load(f)
                # Filter out founder account to reflect true external candidate registrations
                candidate_users = {uid: u for uid, u in users.items() if uid != "ALANKRITA-FOUNDER"}
                stats["registered_candidates"] = len(candidate_users)
                for uid, udata in candidate_users.items():
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
            
    if os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
                analytics_data = json.load(f)
                stats["total_visits"] = analytics_data.get("total_visits", 0)
                stats["total_actions"] = analytics_data.get("total_actions", 0)
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
            Real-time dynamic platform data updated on every user visit and action.
        </p>
    </div>
    """), unsafe_allow_html=True)

    # Real Metrics Row 1 (Candidates & Activity)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; padding:20px 16px; border-radius:16px; border:1px solid {t['border']}; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="font-size:1.6rem; margin-bottom:4px;">👥</div>
            <div style="font-size:0.78rem; color:{t['text_muted']}; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Registered Candidates</div>
            <div style="font-size:2.2rem; font-weight:800; color:{t['text_primary']};">{stats['registered_candidates']}</div>
        </div>
        """), unsafe_allow_html=True)
    with m2:
        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; padding:20px 16px; border-radius:16px; border:1px solid {t['border']}; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="font-size:1.6rem; margin-bottom:4px;">🌐</div>
            <div style="font-size:0.78rem; color:{t['text_muted']}; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Platform Visits</div>
            <div style="font-size:2.2rem; font-weight:800; color:{t['accent']};">{stats['total_visits']}</div>
        </div>
        """), unsafe_allow_html=True)
    with m3:
        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; padding:20px 16px; border-radius:16px; border:1px solid {t['border']}; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="font-size:1.6rem; margin-bottom:4px;">⚡</div>
            <div style="font-size:0.78rem; color:{t['text_muted']}; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Actions Performed</div>
            <div style="font-size:2.2rem; font-weight:800; color:{t['gold']};">{stats['total_actions']}</div>
        </div>
        """), unsafe_allow_html=True)
    with m4:
        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; padding:20px 16px; border-radius:16px; border:1px solid {t['border']}; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="font-size:1.6rem; margin-bottom:4px;">📄</div>
            <div style="font-size:0.78rem; color:{t['text_muted']}; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Resumes Created</div>
            <div style="font-size:2.2rem; font-weight:800; color:{t['text_primary']};">{stats['total_resumes_created']}</div>
        </div>
        """), unsafe_allow_html=True)

    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

    # Chart Section Header
    st.markdown(clean_html(f"""
    <div style="max-width:900px; margin: 0 auto;">
        <h3 style="font-family:'DM Sans', sans-serif; font-size:1.2rem; color:{t['text_primary']}; margin-bottom:14px;">
            Candidate Feature Focus Distribution
        </h3>
    </div>
    """), unsafe_allow_html=True)

    # Prepare data for Streamlit native bar chart
    chart_df = pd.DataFrame({
        "Feature": ["Resume Preparation", "Interview Preparation", "Both Features"],
        "Candidates": [stats["resume_users"], stats["interview_users"], stats["both_users"]]
    }).set_index("Feature")

    c1, c2, c3 = st.columns([1, 10, 1])
    with c2:
        st.bar_chart(chart_df, y="Candidates", color="#10B981")

    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

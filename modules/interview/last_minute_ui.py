"""
AchieveHire — Last-Minute Preparation Interview Router
Provides top-level navigation, theme styling, and routing across:
1. Setup & History (render_last_minute_setup)
2. Live Room (render_last_minute_live_session)
3. Diagnostic Report & Scorecard (render_last_minute_report)
"""

import streamlit as st
from modules.landing.ui import THEMES
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer
from modules.interview.last_minute.setup_ui import render_last_minute_setup
from modules.interview.last_minute.session_ui import render_last_minute_live_session
from modules.interview.last_minute.report_ui import render_last_minute_report


def render_last_minute_interview():
    """Renders the comprehensive Last-Minute Preparation Interview interface."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Interview › Last-Minute Preparation")

    view_mode = st.session_state.get("lm_view_mode", "setup")

    if view_mode == "setup":
        render_last_minute_setup()
    elif view_mode == "live":
        render_last_minute_live_session()
    elif view_mode == "report":
        att_id = st.session_state.get("lm_view_attempt_id")
        render_last_minute_report(att_id)
    else:
        render_last_minute_setup()

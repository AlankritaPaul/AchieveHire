"""
AscendCareer — Application Settings Page
Provides candidate settings:
1. On/Off Notifications (with notification logo)
2. Add this to Desktop (with desktop app logo)
3. Delete Account (with account deletion logo & safe confirmation flow)
"""

import streamlit as st
from modules.auth.user_service import get_current_user, delete_user_account, sign_out
from modules.landing.ui import THEMES, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer


def render_settings_page():
    """Renders the comprehensive, modern AscendCareer platform settings page."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Platform › Settings", show_signin=False, show_theme=False)

    user_id = st.session_state.get("user_id")
    current_user = get_current_user()
    username = st.session_state.get("username", "Candidate")

    st.markdown(clean_html(f"""
    <div style="max-width:880px; margin: 24px auto 20px; padding: 0 16px;">
        <div style="margin-bottom: 24px;">
            <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.80rem; font-weight:700; padding:4px 14px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
                Platform Preferences &amp; Controls
            </div>
            <h1 style="font-size: 2.1rem; font-weight: 800; color:{t['text_primary']}; margin:0 0 8px;">
                Application Settings
            </h1>
            <p style="font-size: 1.02rem; color:{t['text_secondary']}; line-height:1.65; max-width:760px; margin:0;">
                Customize notifications, configure desktop access, and manage your account and data controls.
            </p>
        </div>
    </div>
    """), unsafe_allow_html=True)

    st.markdown(clean_html(f"""
    <div style="max-width:880px; margin: 0 auto; padding: 0 16px;">
    </div>
    """), unsafe_allow_html=True)

    # ── 1. Notification Preferences (with Logo) ──
    with st.container(border=True):
        st.markdown(clean_html(f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <div style="width:36px; height:36px; border-radius:8px; background:{t['accent_soft']}; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">
                🔔
            </div>
            <div>
                <h3 style="font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin:0;">
                    Notification Preferences
                </h3>
            </div>
        </div>
        """), unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([68, 32])
        with col_n1:
            st.markdown(f"""
            <div style="font-weight:600; font-size:0.95rem; color:{t['text_primary']}; margin-bottom:2px;">
                Preparation &amp; Interview Reminders
            </div>
            <div style="font-size:0.84rem; color:{t['text_secondary']}; line-height:1.5;">
                Receive on-screen and browser notifications for scheduled practice sessions and pending resume reviews.
            </div>
            """, unsafe_allow_html=True)
        with col_n2:
            prep_notifs = st.toggle(
                "Preparation Notifications",
                value=st.session_state.get("notif_prep_enabled", True),
                key="toggle_notif_prep",
                label_visibility="collapsed"
            )
            st.session_state["notif_prep_enabled"] = prep_notifs

        st.markdown("<hr style='border:none; border-top:1px solid " + t["border"] + "; margin:12px 0;'>", unsafe_allow_html=True)

        col_m1, col_m2 = st.columns([68, 32])
        with col_m1:
            st.markdown(f"""
            <div style="font-weight:600; font-size:0.95rem; color:{t['text_primary']}; margin-bottom:2px;">
                Milestone &amp; Readiness Score Alerts
            </div>
            <div style="font-size:0.84rem; color:{t['text_secondary']}; line-height:1.5;">
                Get notified when your resume alignment score updates or when interview level evaluations are ready.
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            milestone_notifs = st.toggle(
                "Milestone Notifications",
                value=st.session_state.get("notif_milestones_enabled", True),
                key="toggle_notif_milestone",
                label_visibility="collapsed"
            )
            st.session_state["notif_milestones_enabled"] = milestone_notifs

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 2. Add this to Desktop (with Logo) ──
    with st.container(border=True):
        col_d1, col_d2 = st.columns([68, 32])
        with col_d1:
            st.markdown(clean_html(f"""
            <div style="display:flex; align-items:flex-start; gap:12px;">
                <div style="width:36px; height:36px; border-radius:8px; background:{t['gold_soft']}; display:flex; align-items:center; justify-content:center; font-size:1.2rem; flex-shrink:0;">
                    🖥️
                </div>
                <div>
                    <h3 style="font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin:0 0 4px;">
                        Add AscendCareer to Desktop
                    </h3>
                    <div style="font-size:0.84rem; color:{t['text_secondary']}; line-height:1.5;">
                        Create a desktop shortcut launcher to quickly open AscendCareer directly in your browser.
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)
        with col_d2:
            shortcut_data = "[InternetShortcut]\r\nURL=http://localhost:8501\r\nIconIndex=0\r\n"
            st.download_button(
                label="🖥️  Add to Desktop",
                data=shortcut_data,
                file_name="AscendCareer.url",
                mime="application/x-mswinurl",
                use_container_width=True,
                type="primary"
            )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 3. Sign Out of Account (with Logo) ──
    with st.container(border=True):
        col_s1, col_s2 = st.columns([68, 32])
        with col_s1:
            st.markdown(clean_html(f"""
            <div style="display:flex; align-items:flex-start; gap:12px;">
                <div style="width:36px; height:36px; border-radius:8px; background:{t['accent_soft']}; display:flex; align-items:center; justify-content:center; font-size:1.2rem; flex-shrink:0;">
                    🚪
                </div>
                <div>
                    <h3 style="font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin:0 0 4px;">
                        Sign Out of Account
                    </h3>
                    <div style="font-size:0.84rem; color:{t['text_secondary']}; line-height:1.5;">
                        This will not delete your account or your old data. You will be temporarily out. When you will again come back and you will click 'Sign In', use your existing user ID in the 'Existing User' option.
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)
        with col_s2:
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            if st.button("Yes", use_container_width=True, key="btn_execute_signout"):
                sign_out()
                st.session_state["nav_open"] = False
                st.success("You have signed out successfully.")
                st.rerun()

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 4. Delete Account (with Logo) ──
    with st.container(border=True):
        col_del1, col_del2 = st.columns([68, 32])
        with col_del1:
            st.markdown(clean_html(f"""
            <div style="display:flex; align-items:flex-start; gap:12px;">
                <div style="width:36px; height:36px; border-radius:8px; background:#FEE2E2; display:flex; align-items:center; justify-content:center; font-size:1.2rem; flex-shrink:0;">
                    🗑️
                </div>
                <div>
                    <h3 style="font-size:1.15rem; font-weight:700; color:#DC2626; margin:0 0 4px;">
                        Delete Account &amp; Associated Data
                    </h3>
                    <div style="font-size:0.84rem; color:{t['text_secondary']}; line-height:1.5;">
                        Permanently remove your candidate profile, unique User ID, saved resumes, and interview evaluations. This action cannot be undone.
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)
        with col_del2:
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            if st.button("Yes", key="btn_delete_account_yes", type="primary", use_container_width=True):
                if user_id:
                    delete_user_account(user_id)
                st.session_state.clear()
                st.session_state["ac_screen"] = "landing"
                st.session_state["nav_open"] = False
                st.success("Your account and all associated data have been permanently deleted.")
                st.rerun()

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── 5. Clear Session Cache (with Logo) ──
    with st.container(border=True):
        col_cs1, col_cs2 = st.columns([68, 32])
        with col_cs1:
            st.markdown(clean_html(f"""
            <div style="display:flex; align-items:flex-start; gap:12px;">
                <div style="width:36px; height:36px; border-radius:8px; background:{t['surface2']}; display:flex; align-items:center; justify-content:center; font-size:1.2rem; flex-shrink:0;">
                    🧹
                </div>
                <div>
                    <h3 style="font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin:0 0 4px;">
                        Clear Session Cache
                    </h3>
                    <div style="font-size:0.84rem; color:{t['text_secondary']}; line-height:1.5;">
                        Clear current browser session state and temporary cached data without deleting stored account records.
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)
        with col_cs2:
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            if st.button("Yes", key="btn_clear_session_yes", use_container_width=True):
                st.session_state.clear()
                st.session_state["ac_screen"] = "landing"
                st.session_state["nav_open"] = False
                st.success("Current session cache cleared successfully.")
                st.rerun()




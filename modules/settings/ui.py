"""
AscendCareer — Application Settings Page
Provides candidate settings:
1. On/Off Notifications (with notification logo)
2. Add this to Desktop (with desktop app logo)
3. Delete Account (with account deletion logo & safe confirmation flow)
"""

import streamlit as st
from modules.auth.user_service import get_current_user, delete_user_account
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
    st.markdown(clean_html(f"""
    <div style="max-width:880px; margin: 0 auto 20px; padding: 0 16px;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <div style="width:38px; height:38px; border-radius:10px; background:{t['accent_soft']}; display:flex; align-items:center; justify-content:center; font-size:1.3rem;">
                🔔
            </div>
            <div>
                <h3 style="font-size:1.2rem; font-weight:700; color:{t['text_primary']}; margin:0;">
                    Notification Preferences
                </h3>
                <div style="font-size:0.85rem; color:{t['text_muted']};">
                    Control interview alerts, resume analysis updates, and practice milestone reminders.
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    with st.container(border=True):
        col_n1, col_n2 = st.columns([75, 25])
        with col_n1:
            st.markdown(f"""
            <div style="font-weight:600; font-size:0.95rem; color:{t['text_primary']};">
                Preparation &amp; Interview Reminders
            </div>
            <div style="font-size:0.84rem; color:{t['text_secondary']};">
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

        col_m1, col_m2 = st.columns([75, 25])
        with col_m1:
            st.markdown(f"""
            <div style="font-weight:600; font-size:0.95rem; color:{t['text_primary']};">
                Milestone &amp; Readiness Score Alerts
            </div>
            <div style="font-size:0.84rem; color:{t['text_secondary']};">
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

    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

    # ── 2. Add this to Desktop (with Logo) ──
    st.markdown(clean_html(f"""
    <div style="max-width:880px; margin: 0 auto 20px; padding: 0 16px;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <div style="width:38px; height:38px; border-radius:10px; background:{t['gold_soft']}; display:flex; align-items:center; justify-content:center; font-size:1.3rem;">
                🖥️
            </div>
            <div>
                <h3 style="font-size:1.2rem; font-weight:700; color:{t['text_primary']}; margin:0;">
                    Add AscendCareer to Desktop
                </h3>
                <div style="font-size:0.85rem; color:{t['text_muted']};">
                    Install AscendCareer as a standalone desktop app for fast, focused preparation.
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(f"""
        <div style="font-size:0.92rem; color:{t['text_secondary']}; line-height:1.65; margin-bottom:14px;">
            You can launch AscendCareer directly from your desktop, dock, or taskbar in its own distraction-free window without browser tabs.
        </div>
        <div style="background:{t['surface2']}; border:1px solid {t['border']}; border-radius:10px; padding:16px 20px; margin-bottom:16px;">
            <div style="font-weight:700; font-size:0.90rem; color:{t['text_primary']}; margin-bottom:8px;">
                📌 How to Install to Desktop in 2 Steps:
            </div>
            <ol style="margin:0; padding-left:20px; font-size:0.86rem; color:{t['text_secondary']}; line-height:1.75;">
                <li>In Chrome or Edge, click the <strong>Install / App icon</strong> (<span style="font-family:monospace;">⊕</span> or monitor symbol) on the right side of the URL address bar.</li>
                <li>Or click browser <strong>Menu (⋮) → 'Cast, save, and share' / 'More tools' → 'Install AscendCareer' / 'Create shortcut...'</strong> and check <em>'Open as window'</em>.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        col_d1, col_d2 = st.columns([50, 50])
        with col_d1:
            if st.button("💻  Bookmark App (Ctrl + D)", key="btn_bookmark_app", use_container_width=True):
                st.info("💡 Press **Ctrl + D** (or **Cmd + D** on Mac) in your browser to instantly bookmark AscendCareer.")
        with col_d2:
            if st.button("🚀  Copy Platform Link", key="btn_copy_link", use_container_width=True):
                st.success("✅ Platform URL: http://localhost:8501 (Ready for desktop shortcut)")

    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)

    # ── 3. Delete Account (with Logo) ──
    st.markdown(clean_html(f"""
    <div style="max-width:880px; margin: 0 auto 20px; padding: 0 16px;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
            <div style="width:38px; height:38px; border-radius:10px; background:#FEE2E2; display:flex; align-items:center; justify-content:center; font-size:1.3rem;">
                🗑️
            </div>
            <div>
                <h3 style="font-size:1.2rem; font-weight:700; color:#DC2626; margin:0;">
                    Delete Account &amp; Associated Data
                </h3>
                <div style="font-size:0.85rem; color:{t['text_muted']};">
                    Permanently delete your profile, unique User ID, resumes, and interview evaluations.
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    with st.container(border=True):
        if user_id:
            st.markdown(f"""
            <div style="background:#FFF5F5; border:1px solid #FECACA; border-left:4px solid #EF4444; border-radius:8px; padding:14px 18px; margin-bottom:16px;">
                <div style="font-weight:700; font-size:0.92rem; color:#991B1B; margin-bottom:4px;">
                    ⚠️ Warning: This action cannot be undone
                </div>
                <div style="font-size:0.84rem; color:#7F1D1D; line-height:1.6;">
                    Deleting your account will permanently remove candidate <strong>{username}</strong> (ID: <code>{user_id}</code>), including all saved resume drafts, optimization history, mock interview recordings, and preparation analytics.
                </div>
            </div>
            """, unsafe_allow_html=True)

            confirm_check = st.checkbox(
                f"I understand that deleting my account ({user_id}) is permanent and cannot be reversed.",
                key="chk_confirm_delete"
            )

            if st.button("🗑️  Permanently Delete My Account", type="primary", disabled=not confirm_check, key="btn_execute_delete"):
                delete_user_account(user_id)
                st.session_state["ac_screen"] = "landing"
                st.session_state["nav_open"] = False
                st.success("Your account and all associated data have been permanently deleted.")
                st.rerun()
        else:
            st.markdown(f"""
            <div style="font-size:0.88rem; color:{t['text_secondary']}; line-height:1.6;">
                You are currently in <strong>Guest Mode</strong> without a registered User ID. There is no permanent account data stored on the server.
            </div>
            """, unsafe_allow_html=True)
            if st.button("🧹  Clear Current Session Cache", key="btn_clear_guest_session"):
                st.session_state.clear()
                st.session_state["ac_screen"] = "landing"
                st.rerun()

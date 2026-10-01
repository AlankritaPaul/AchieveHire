"""
AscendCareer — Candidate Profile Page
Clean, organized layout displaying candidate account, profile details,
profile picture management with default avatar fallback, and account settings.
"""

import base64
import streamlit as st
from modules.landing.ui import THEMES, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer, _get_avatar_uri


def render_user_profile():
    """Renders the comprehensive, organized candidate profile page."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="User Profile & Account", show_signin=False)

    # Defaults in session state
    if "username" not in st.session_state:
        st.session_state["username"] = "Alankrita Paul"
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = "candidate@ascendcareer.ai"
    if "user_headline" not in st.session_state:
        st.session_state["user_headline"] = "Senior Software Engineer · Distributed Systems"
    if "user_location" not in st.session_state:
        st.session_state["user_location"] = "India"
    if "user_bio" not in st.session_state:
        st.session_state["user_bio"] = "Focused on rigorous interview preparation, system design depth, and competitive career advancement."

    avatar_uri = _get_avatar_uri()

    st.markdown(clean_html(f"""
    <div style="max-width:980px; margin: 24px auto; padding: 0 16px;">
        <div style="display:flex; align-items:center; gap:24px; padding:24px; background:{t['surface']}; border:1px solid {t['border']}; border-radius:16px; box-shadow:{t['card_shadow']}; margin-bottom:28px;">
            <div style="position:relative; width:92px; height:92px; flex-shrink:0;">
                <img src="{avatar_uri}" alt="Profile Picture" style="width:92px; height:92px; border-radius:50%; object-fit:cover; border:2.5px solid {t['accent']};" />
            </div>
            <div style="flex:1;">
                <h1 style="font-size:1.8rem; font-weight:800; color:{t['text_primary']}; margin:0 0 4px;">
                    {st.session_state['username']}
                </h1>
                <div style="font-size:1.02rem; color:{t['text_secondary']}; font-weight:500;">
                    {st.session_state['user_headline']}
                </div>
                <div style="font-size:0.86rem; color:{t['text_muted']}; margin-top:6px;">
                    📍 {st.session_state['user_location']} &nbsp;·&nbsp; ✉️ {st.session_state['user_email']}
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    col_details, col_media = st.columns([62, 38], gap="large")

    with col_details:
        st.markdown(f"<h3 style='font-size:1.18rem; font-weight:700; color:{t['text_primary']}; margin-bottom:12px;'>Account & Personal Information</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            new_username = st.text_input("Username / Display Name", value=st.session_state["username"])
            new_email = st.text_input("Primary Email", value=st.session_state["user_email"])
            new_headline = st.text_input("Professional Headline", value=st.session_state["user_headline"])
            new_location = st.text_input("Location", value=st.session_state["user_location"])
            new_bio = st.text_area("Candidate Bio / Summary", value=st.session_state["user_bio"], height=100)

            if st.button("💾  Save Profile Changes", type="primary", use_container_width=True, key="btn_save_profile"):
                st.session_state["username"] = new_username.strip() if new_username.strip() else "Candidate"
                st.session_state["user_email"] = new_email.strip()
                st.session_state["user_headline"] = new_headline.strip()
                st.session_state["user_location"] = new_location.strip()
                st.session_state["user_bio"] = new_bio.strip()
                st.success("Profile updated successfully!")
                st.rerun()

    with col_media:
        st.markdown(f"<h3 style='font-size:1.18rem; font-weight:700; color:{t['text_primary']}; margin-bottom:12px;'>Profile Picture</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f"""
            <div style="font-size:0.86rem; color:{t['text_secondary']}; margin-bottom:12px; line-height:1.5;">
                You are not required to upload a profile photo. If not provided, a clean default avatar with an addition badge is displayed automatically.
            </div>
            """, unsafe_allow_html=True)

            uploaded_photo = st.file_uploader(
                "Upload Custom Profile Photo (PNG, JPG, WebP)",
                type=["png", "jpg", "jpeg", "webp"],
                key="uploader_profile_pic",
            )
            if uploaded_photo is not None:
                encoded = base64.b64encode(uploaded_photo.read()).decode("utf-8")
                mime = uploaded_photo.type or "image/png"
                st.session_state["user_profile_pic"] = f"data:{mime};base64,{encoded}"
                st.success("Custom profile photo uploaded!")
                st.rerun()

            if "user_profile_pic" in st.session_state and st.session_state["user_profile_pic"]:
                if st.button("🗑️  Remove Photo & Revert to Default Avatar", use_container_width=True, key="btn_remove_avatar"):
                    st.session_state["user_profile_pic"] = None
                    st.rerun()

        st.markdown(f"<h3 style='font-size:1.18rem; font-weight:700; color:{t['text_primary']}; margin:20px 0 12px;'>Platform Activity</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid {t['border']};">
                <span style="color:{t['text_secondary']}; font-size:0.9rem;">Resumes Created:</span>
                <strong style="color:{t['text_primary']}; font-size:0.9rem;">2</strong>
            </div>
            <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid {t['border']};">
                <span style="color:{t['text_secondary']}; font-size:0.9rem;">Resumes Analyzed:</span>
                <strong style="color:{t['text_primary']}; font-size:0.9rem;">5</strong>
            </div>
            <div style="display:flex; justify-content:space-between; padding:8px 0;">
                <span style="color:{t['text_secondary']}; font-size:0.9rem;">Interviews Practiced:</span>
                <strong style="color:{t['text_primary']}; font-size:0.9rem;">4</strong>
            </div>
            """, unsafe_allow_html=True)

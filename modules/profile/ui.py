"""
AscendCareer — Candidate Profile Page
Clean, organized layout displaying candidate account, unique User ID,
profile details, profile picture management with default avatar fallback, and account settings.
"""

import base64
import streamlit as st
from modules.auth.user_service import (
    get_current_user,
    update_user_record,
    register_user,
    PURPOSE_OPTIONS,
)
from modules.landing.ui import THEMES, _get_user_verified_symbol_uri, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer, _get_avatar_uri


def render_user_profile():
    """Renders the comprehensive, organized candidate profile page with unique User ID isolation."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="User Profile & Account", show_signin=False, show_theme=False)

    # Load active user or fallback
    current_user = get_current_user()
    user_id = st.session_state.get("user_id")
    verified_uri = _get_user_verified_symbol_uri()

    if not current_user:
        username = st.session_state.get("username", "Candidate")
        user_purpose = st.session_state.get("user_purpose", "Both")
        user_email = st.session_state.get("user_email", "candidate@ascendcareer.ai")
        user_headline = st.session_state.get("user_headline", "Candidate · Career Readiness")
        user_location = st.session_state.get("user_location", "India")
        user_bio = st.session_state.get("user_bio", "Focused on rigorous interview preparation, resume refinement, and career readiness.")
    else:
        username = current_user.get("name", "Candidate")
        user_purpose = current_user.get("purpose", "Both")
        user_email = current_user.get("email", "candidate@ascendcareer.ai")
        user_headline = current_user.get("headline", "Candidate · Career Readiness")
        user_location = current_user.get("location", "India")
        user_bio = current_user.get("bio", "")

    avatar_uri = _get_avatar_uri()

    verified_badge_html = f'''
        <span style="background:{t["surface2"]}; border:1.5px solid #10B981; color:#10B981; font-family:monospace; font-weight:700; font-size:0.88rem; padding:4px 12px; border-radius:8px; display:inline-flex; align-items:center; gap:6px;">
            <img src="{verified_uri}" style="height:20px; width:auto;" alt="Verified" />
            <span>🆔 {user_id} · Verified</span>
        </span>
    ''' if user_id else f'''
        <span style="background:{t['gold_soft']}; color:{t['gold']}; font-size:0.82rem; font-weight:700; padding:4px 12px; border-radius:6px;">
            Guest Mode · No ID Generated
        </span>
    '''

    st.markdown(clean_html(f"""
    <div style="max-width:980px; margin: 24px auto; padding: 0 16px;">
        <div style="display:flex; align-items:center; gap:24px; padding:24px; background:{t['surface']}; border:1px solid {t['border']}; border-radius:16px; box-shadow:{t['card_shadow']}; margin-bottom:28px;">
            <div style="position:relative; width:92px; height:92px; flex-shrink:0;">
                <img src="{avatar_uri}" alt="Profile Picture" style="width:92px; height:92px; border-radius:50%; object-fit:cover; border:2.5px solid {t['accent']};" />
            </div>
            <div style="flex:1;">
                <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:4px;">
                    <h1 style="font-size:1.8rem; font-weight:800; color:{t['text_primary']}; margin:0;">
                        {username}
                    </h1>
                    {verified_badge_html}
                </div>
                <div style="font-size:1.02rem; color:{t['text_secondary']}; font-weight:500;">
                    {user_headline}
                </div>
                <div style="font-size:0.86rem; color:{t['text_muted']}; margin-top:6px;">
                    📍 {user_location} &nbsp;·&nbsp; ✉️ {user_email} &nbsp;·&nbsp; 🎯 Focus: <strong>{user_purpose}</strong>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    col_details, col_media = st.columns([60, 40], gap="large")

    with col_details:
        st.markdown(f"<h3 style='font-size:1.18rem; font-weight:700; color:{t['text_primary']}; margin-bottom:12px;'>Account & Personal Information</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            new_username = st.text_input("Candidate Name", value=username, key="prof_input_name")
            new_email = st.text_input("Primary Email", value=user_email, key="prof_input_email")
            new_headline = st.text_input("Professional Headline", value=user_headline, key="prof_input_headline")
            new_location = st.text_input("Location", value=user_location, key="prof_input_location")
            new_purpose = st.selectbox(
                "Primary Preparation Focus",
                options=PURPOSE_OPTIONS,
                index=PURPOSE_OPTIONS.index(user_purpose) if user_purpose in PURPOSE_OPTIONS else 2,
                key="prof_select_purpose"
            )
            new_bio = st.text_area("Candidate Bio / Summary", value=user_bio, height=90, key="prof_input_bio")

            if st.button("💾  Save Profile Changes", type="primary", use_container_width=True, key="btn_save_profile"):
                updates = {
                    "name": new_username.strip() if new_username.strip() else "Candidate",
                    "email": new_email.strip(),
                    "headline": new_headline.strip(),
                    "location": new_location.strip(),
                    "purpose": new_purpose,
                    "bio": new_bio.strip(),
                }
                if user_id:
                    update_user_record(user_id, updates)
                st.session_state["username"] = updates["name"]
                st.session_state["user_email"] = updates["email"]
                st.session_state["user_headline"] = updates["headline"]
                st.session_state["user_location"] = updates["location"]
                st.session_state["user_purpose"] = updates["purpose"]
                st.session_state["user_bio"] = updates["bio"]
                st.success("Profile updated successfully!")
                st.rerun()

    with col_media:
        st.markdown(f"<h3 style='font-size:1.18rem; font-weight:700; color:{t['text_primary']}; margin-bottom:12px;'>Profile Picture</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f"""
            <div style="font-size:0.86rem; color:{t['text_secondary']}; margin-bottom:12px; line-height:1.5;">
                You are not required to upload a profile photo. If not provided, your verified user ID symbol is displayed automatically.
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
                avatar_data = f"data:{mime};base64,{encoded}"
                st.session_state["user_profile_pic"] = avatar_data
                if user_id:
                    update_user_record(user_id, {"profile_pic": avatar_data})
                st.success("Custom profile photo uploaded!")
                st.rerun()

            if "user_profile_pic" in st.session_state and st.session_state["user_profile_pic"]:
                if st.button("🗑️  Remove Photo & Revert to Verified Avatar", use_container_width=True, key="btn_remove_avatar"):
                    st.session_state["user_profile_pic"] = None
                    if user_id:
                        update_user_record(user_id, {"profile_pic": None})
                    st.rerun()

        st.markdown(f"<h3 style='font-size:1.18rem; font-weight:700; color:{t['text_primary']}; margin:20px 0 12px;'>Unique Identity & Isolation</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            if user_id:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px;">
                    <img src="{verified_uri}" style="height:36px; width:auto;" alt="Verified" />
                    <div>
                        <div style="font-weight:700; font-size:0.95rem; color:#10B981;">User ID Active &amp; Verified</div>
                        <div style="font-family:monospace; font-size:0.86rem; color:{t['text_primary']}; font-weight:700;">{user_id}</div>
                    </div>
                </div>
                <div style="font-size:0.88rem; color:{t['text_secondary']}; line-height:1.6; margin-bottom:12px;">
                    Your account is tied to <strong>{user_id}</strong>. All your resumes, interview recordings, and score reports are isolated from other candidates.
                </div>
                """, unsafe_allow_html=True)
                if st.button("🔄  Switch Account / Generate New ID", use_container_width=True, key="prof_btn_switch_id"):
                    st.session_state["ac_screen"] = "signin"
                    st.rerun()
            else:
                st.markdown(f"""
                <div style="font-size:0.88rem; color:{t['text_secondary']}; line-height:1.6; margin-bottom:12px;">
                    You are currently using AscendCareer in guest mode without a unique User ID.
                </div>
                """, unsafe_allow_html=True)
                if st.button("✨  Generate Unique User ID Now", type="primary", use_container_width=True, key="prof_btn_gen_id"):
                    st.session_state["ac_screen"] = "signin"
                    st.rerun()

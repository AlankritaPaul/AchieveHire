"""
AchieveHire — Main Navigation Drawer & Top Navigation Bar
Clean, modern, professional, minimal navigation structure.
"""

import base64
import streamlit as st
import streamlit.components.v1 as components
from modules.landing.ui import (
    THEMES,
    _get_theme_icon_data_uri,
    _get_signin_symbol_data_uri,
    _get_user_verified_symbol_uri,
    clean_html,
)


DEFAULT_AVATAR_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
  <circle cx="24" cy="24" r="23" fill="#EEF2FF" stroke="#818CF8" stroke-width="1.8"/>
  <circle cx="24" cy="18" r="8" fill="#4F46E5"/>
  <path d="M 10 38 C 10 30 17 28 24 28 C 31 28 38 30 38 38" fill="#4F46E5"/>
  <circle cx="38" cy="38" r="7" fill="#10B981" stroke="#FFFFFF" stroke-width="1.5"/>
  <line x1="38" y1="35" x2="38" y2="41" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>
  <line x1="35" y1="38" x2="41" y2="38" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>
</svg>"""


def _get_avatar_uri() -> str:
    """Return avatar URI: custom uploaded picture if available, otherwise second picture (verified user ID symbol) if user has ID, else default avatar."""
    if "user_profile_pic" in st.session_state and st.session_state["user_profile_pic"]:
        return st.session_state["user_profile_pic"]
    if st.session_state.get("user_id"):
        verified_uri = _get_user_verified_symbol_uri()
        if verified_uri:
            return verified_uri
    encoded = base64.b64encode(DEFAULT_AVATAR_SVG.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def render_top_nav_bar(t: dict, title: str = "", show_signin: bool = False, show_theme: bool = False):
    """
    Renders top navigation header row across pages:
    - Left: Hamburger Menu Icon (3 horizontal lines)
    - Center: Screen Title / Breadcrumb
    - Right: Sun/Moon Theme Toggle icon & optional Sign In button
    """
    theme_key = st.session_state.get("ac_theme", "light")
    other_key = "dark" if theme_key == "light" else "light"
    theme_icon_uri = _get_theme_icon_data_uri()
    signin_symbol_uri = _get_signin_symbol_data_uri()
    user_verified_uri = _get_user_verified_symbol_uri()

    st.markdown(clean_html(f"""
    <style>
    /* ── Top Bar Container Alignment & Click Guarantee ── */
    .ac-top-nav-row,
    div[data-testid="stHorizontalBlock"]:first-of-type,
    div[data-testid="stHorizontalBlock"]:has(.st-key-ac_hamburger_btn),
    div[data-testid="stHorizontalBlock"]:has(.st-key-ac_theme_toggle_btn) {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 16px;
        position: relative !important;
        z-index: 9999 !important;
        pointer-events: auto !important;
    }}

    .st-key-ac_hamburger_btn,
    .st-key-ac_top_signin_btn,
    .st-key-ac_theme_toggle_btn,
    .st-key-ac_top_verified_user_btn {{
        position: relative !important;
        z-index: 99999 !important;
        pointer-events: auto !important;
    }}

    /* ── Hamburger Button (Three Horizontal Lines) ── */
    .st-key-ac_hamburger_btn button {{
        position: relative !important;
        z-index: 99999 !important;
        pointer-events: auto !important;
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        max-width: 44px !important;
        min-height: 44px !important;
        max-height: 44px !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        margin: 0 !important;
        transition: transform 0.18s ease !important;
    }}
    .st-key-ac_hamburger_btn button:hover {{
        transform: scale(1.12) !important;
        background: {t["surface2"]} !important;
        border-radius: 8px !important;
    }}
    .st-key-ac_hamburger_btn button * {{
        display: none !important;
    }}
    .st-key-ac_hamburger_btn button::before {{
        content: "";
        display: block;
        width: 22px;
        height: 2.2px;
        background-color: {t["text_primary"]};
        box-shadow: 0 -7px 0 {t["text_primary"]}, 0 7px 0 {t["text_primary"]};
        border-radius: 2px;
        transition: background-color 0.2s;
    }}
    .st-key-ac_hamburger_btn button:hover::before {{
        background-color: {t["accent"]};
        box-shadow: 0 -7px 0 {t["accent"]}, 0 7px 0 {t["accent"]};
    }}

    /* ── Sign In Button (Top Right — First Picture Symbol) ── */
    .st-key-ac_top_signin_btn {{
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: 100% !important;
        margin-right: -6px !important;
    }}

    .st-key-ac_top_signin_btn div[data-testid="stButton"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: flex-end !important;
    }}

    html body div.stApp div[data-testid="stElementContainer"].st-key-ac_top_signin_btn div[data-testid="stButton"] button,
    html body div.stApp div.st-key-ac_top_signin_btn div[data-testid="stButton"] button,
    html body div.stApp .st-key-ac_top_signin_btn button,
    html body div.stApp div[class*="st-key-ac_top_signin_btn"] button,
    .st-key-ac_top_signin_btn button,
    div[class*="st-key-ac_top_signin_btn"] button {{
        background: transparent url('{signin_symbol_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        background-image: url('{signin_symbol_uri}') !important;
        background-size: contain !important;
        border: none !important;
        border-width: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        cursor: pointer !important;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        padding: 0 !important;
        min-height: 64px !important;
        height: 64px !important;
        width: 180px !important;
        min-width: 180px !important;
        max-width: 180px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    html body div.stApp div[data-testid="stElementContainer"].st-key-ac_top_signin_btn div[data-testid="stButton"] button:hover,
    html body div.stApp div.st-key-ac_top_signin_btn div[data-testid="stButton"] button:hover,
    html body div.stApp .st-key-ac_top_signin_btn button:hover,
    html body div.stApp div[class*="st-key-ac_top_signin_btn"] button:hover,
    .st-key-ac_top_signin_btn button:hover,
    div[class*="st-key-ac_top_signin_btn"] button:hover {{
        transform: scale(1.08) translateY(-1px) !important;
        background: transparent url('{signin_symbol_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        background-image: url('{signin_symbol_uri}') !important;
        box-shadow: none !important;
        border: none !important;
    }}

    html body div.stApp div[data-testid="stElementContainer"].st-key-ac_top_signin_btn div[data-testid="stButton"] button *,
    html body div.stApp div.st-key-ac_top_signin_btn div[data-testid="stButton"] button *,
    html body div.stApp .st-key-ac_top_signin_btn button *,
    .st-key-ac_top_signin_btn button * {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }}

    /* ── Verified User Badge (Top Right — Second Picture Symbol) ── */
    .st-key-ac_top_verified_user_btn {{
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: 100% !important;
    }}
    .st-key-ac_top_verified_user_btn div[data-testid="stButton"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: flex-end !important;
    }}
    .st-key-ac_top_verified_user_btn button {{
        background: {t["surface2"]} !important;
        border: 1.5px solid #10B981 !important;
        border-radius: 9999px !important;
        color: {t["text_primary"]} !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        padding: 6px 14px 6px 10px !important;
        min-height: 40px !important;
        height: 40px !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.20) !important;
        cursor: pointer !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}
    .st-key-ac_top_verified_user_btn button:hover {{
        transform: translateY(-2px) scale(1.03) !important;
        border-color: #059669 !important;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35) !important;
    }}

    /* ── Theme Toggle Button (Sun/Moon Split Icon) ── */
    .st-key-ac_theme_toggle_btn {{
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        width: auto !important;
    }}
    .st-key-ac_theme_toggle_btn div[data-testid="stButton"] {{
        display: inline-flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 56px !important;
        height: 56px !important;
    }}
    html body div.stApp div[data-testid="stElementContainer"].st-key-ac_theme_toggle_btn div[data-testid="stButton"] button,
    html body div.stApp div.st-key-ac_theme_toggle_btn div[data-testid="stButton"] button,
    html body div.stApp .st-key-ac_theme_toggle_btn button,
    html body div.stApp div[class*="st-key-ac_theme_toggle_btn"] button,
    .st-key-ac_theme_toggle_btn button,
    div[class*="st-key-ac_theme_toggle_btn"] button {{
        width: 56px !important;
        height: 56px !important;
        min-width: 56px !important;
        max-width: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        background: transparent url('{theme_icon_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        background-image: url('{theme_icon_uri}') !important;
        background-size: contain !important;
        border: none !important;
        border-width: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        border-radius: 50% !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }}
    html body div.stApp div[data-testid="stElementContainer"].st-key-ac_theme_toggle_btn div[data-testid="stButton"] button:hover,
    html body div.stApp div.st-key-ac_theme_toggle_btn div[data-testid="stButton"] button:hover,
    html body div.stApp .st-key-ac_theme_toggle_btn button:hover,
    html body div.stApp div[class*="st-key-ac_theme_toggle_btn"] button:hover,
    .st-key-ac_theme_toggle_btn button:hover,
    div[class*="st-key-ac_theme_toggle_btn"] button:hover {{
        transform: scale(1.15) !important;
        background: transparent url('{theme_icon_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
    html body div.stApp div[data-testid="stElementContainer"].st-key-ac_theme_toggle_btn div[data-testid="stButton"] button *,
    html body div.stApp div.st-key-ac_theme_toggle_btn div[data-testid="stButton"] button *,
    html body div.stApp .st-key-ac_theme_toggle_btn button *,
    html body div.stApp div[class*="st-key-ac_theme_toggle_btn"] button *,
    .st-key-ac_theme_toggle_btn button *,
    div[class*="st-key-ac_theme_toggle_btn"] button * {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }}
    </style>
    """), unsafe_allow_html=True)

    if show_signin:
        col_h, col_title, col_signin, col_theme = st.columns([6, 73, 14, 7])
        with col_h:
            if st.button(" ", key="ac_hamburger_btn", help="Open Main Navigation"):
                st.session_state["nav_open"] = not st.session_state.get("nav_open", False)
                st.rerun()
        with col_title:
            if title:
                bt_c1, bt_c2 = st.columns([18, 82])
                with bt_c1:
                    if st.button("← Back", key=f"ac_topnav_back_btn_s", use_container_width=True, help="Return to Landing Page"):
                        st.session_state["ac_screen"] = "landing"
                        st.rerun()
                with bt_c2:
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; height:100%; padding-top:4px;">
                        <span style="font-size:0.95rem; font-weight:700; color:{t['text_muted']};">
                            <strong style="color:{t['text_primary']};">AchieveHire</strong> &nbsp;›&nbsp; {title}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
        with col_signin:
            active_uid = st.session_state.get("user_id")
            if active_uid:
                if st.button(f"🆔 {active_uid}", key="ac_top_verified_user_btn", use_container_width=True, help="Verified User ID · View Profile"):
                    st.session_state["ac_screen"] = "profile"
                    st.rerun()
            else:
                top_signin_clicked = st.button(" ", key="ac_top_signin_btn", use_container_width=True, help="Sign In / Generate User ID")
                if top_signin_clicked:
                    st.session_state["ac_screen"] = "signin"
                    st.rerun()
        with col_theme:
            if st.button(" ", key="ac_theme_toggle_btn", help=f"Switch to {'Dark' if theme_key == 'light' else 'Light'} Theme"):
                st.session_state["auth_popup_open"] = False
                st.session_state["ac_theme"] = other_key
                st.query_params["theme"] = other_key
                st.rerun()
    else:
        col_h, col_title, col_theme = st.columns([6, 87, 7])
        with col_h:
            if st.button(" ", key="ac_hamburger_btn", help="Open Main Navigation"):
                st.session_state["nav_open"] = not st.session_state.get("nav_open", False)
                st.rerun()
        with col_title:
            if title:
                bt_c1, bt_c2 = st.columns([16, 84])
                with bt_c1:
                    if st.button("← Back", key=f"ac_topnav_back_btn_m", use_container_width=True, help="Return to Landing Page"):
                        st.session_state["ac_screen"] = "landing"
                        st.rerun()
                with bt_c2:
                    st.markdown(f"""
                    <div style="display:flex; align-items:center; height:100%; padding-top:4px;">
                        <span style="font-size:0.95rem; font-weight:700; color:{t['text_muted']};">
                            <strong style="color:{t['text_primary']};">AchieveHire</strong> &nbsp;›&nbsp; {title}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
        with col_theme:
            if show_theme:
                if st.button(" ", key="ac_theme_toggle_btn", help=f"Switch to {'Dark' if theme_key == 'light' else 'Light'} Theme"):
                    st.session_state["auth_popup_open"] = False
                    st.session_state["ac_theme"] = other_key
                    st.query_params["theme"] = other_key
                    st.rerun()



def render_navigation_drawer(t: dict):
    """
    Renders the modern, clean, slide-out navigation panel when nav_open is True.
    Contains:
    1. Resume (collapsible: Resume Create, Resume Analysis)
    2. Interview (collapsible: Specialized Interview, Job Related Interview)
    3. User Profile Area (circular avatar with + sign, username, click to view full profile)
    4. Privacy
    5. Terms and Conditions
    6. Brand Status Element (refined circular jewel, non-guarantee)
    """
    if not st.session_state.get("nav_open", False):
        return

    avatar_uri = _get_avatar_uri()
    username = st.session_state.get("username", "Candidate")

    # Expand/collapse states (default to expanded)
    if "nav_resume_open" not in st.session_state:
        st.session_state["nav_resume_open"] = True
    if "nav_interview_open" not in st.session_state:
        st.session_state["nav_interview_open"] = True

    resume_open = st.session_state["nav_resume_open"]
    interview_open = st.session_state["nav_interview_open"]
    is_dark = (t.get("bg") == "#0D0F1A") or (st.session_state.get("ac_theme") == "dark")
    neon_green = "#4ADE80" if is_dark else t["text_muted"]
    chip_border = "rgba(74, 222, 128, 0.35)" if is_dark else t["border"]

    st.markdown(clean_html(f"""
    <div id="ac-nav-backdrop-el" class="ac-nav-backdrop"></div>
    <style>
    /* ── Navigation Backdrop Blur ── */
    .ac-nav-backdrop {{
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(13, 15, 26, 0.55);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
        z-index: 100000;
        cursor: pointer;
    }}

    /* ── Navigation Drawer Box ── */
    [data-testid="stSidebar"] {{
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 330px !important;
        min-width: 330px !important;
        max-width: 86vw !important;
        height: 100vh !important;
        background: {t["surface"]} !important;
        border-right: 1px solid {t["border"]} !important;
        box-shadow: 8px 0 32px rgba(0, 0, 0, 0.25) !important;
        z-index: 100001 !important;
        overflow-y: auto !important;
        padding: 24px 20px 32px !important;
        display: flex !important;
        flex-direction: column !important;
        transform: translateX(0) !important;
        visibility: visible !important;
        animation: acSlideIn 0.24s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    
    /* Hide the native sidebar toggle buttons inside the drawer */
    [data-testid="stSidebarCollapseButton"], 
    [data-testid="stSidebarResizer"] {{
        display: none !important;
    }}
    @keyframes acSlideIn {{
        from {{ transform: translateX(-100%); }}
        to {{ transform: translateX(0); }}
    }}

    /* ── Drawer Header ── */
    .ac-drawer-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }}
    .ac-drawer-brand {{
        font-family: 'Cinzel Decorative', 'Palatino Linotype', Georgia, serif;
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: 0em !important;
        margin: 0;
    }}

    /* ── Brand Status Circular Jewel ── */
    .ac-brand-status-chip {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: {t["surface2"]};
        border: 1px solid {chip_border};
        border-radius: 9999px;
        padding: 4px 14px;
        margin-bottom: 20px;
        font-size: 0.88rem;
        font-weight: 600;
        color: {neon_green} !important;
        letter-spacing: 0.02em;
    }}
    .ac-brand-status-chip span {{
        color: {neon_green} !important;
    }}
    .ac-status-jewel {{
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.7);
        animation: acPulse 2.4s infinite ease-in-out;
    }}
    @keyframes acPulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.85; }}
        50% {{ transform: scale(1.28); opacity: 1; }}
    }}

    /* ── Navigation Section Category Headers ── */
    .ac-nav-category-title {{
        font-size: 0.88rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {neon_green} !important;
        margin: 18px 0 8px 6px;
    }}

    /* ── Navigation Buttons in Drawer (Exit Symbol >) ── */
    .st-key-nav_close_btn button,
    .st-key-nav_close_btn button *,
    .st-key-nav_close_btn button p,
    .st-key-nav_close_btn button div,
    .st-key-nav_close_btn button span {{
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        line-height: 1 !important;
        color: {t["text_primary"]} !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    .st-key-nav_close_btn button {{
        background: transparent !important;
        border: none !important;
        cursor: pointer !important;
        padding: 2px 8px !important;
        border-radius: 8px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    .st-key-nav_close_btn button:hover {{
        background: {t["surface2"]} !important;
        color: {t["accent"]} !important;
    }}

    /* Prevent Streamlit default focus/active layout shifts for all nav buttons */
    .st-key-nav_cat_resume button:focus, .st-key-nav_cat_resume button:active,
    .st-key-nav_cat_interview button:focus, .st-key-nav_cat_interview button:active,
    div[class*="st-key-nav_sub_"] button:focus, div[class*="st-key-nav_sub_"] button:active,
    div[class*="st-key-nav_btn_"] button:focus, div[class*="st-key-nav_btn_"] button:active {{
        box-shadow: none !important;
        outline: none !important;
        border-width: 1px !important;
    }}
    /* Category Accordion Header Buttons */
    .st-key-nav_cat_resume button,
    .st-key-nav_cat_interview button {{
        background: {t["surface2"]} !important;
        border: 1px solid {t["border"]} !important;
        color: {t["text_primary"]} !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        border-radius: 10px !important;
        padding: 11px 16px !important;
        text-align: left !important;
        width: 100% !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 4px !important;
        transition: all 0.18s ease !important;
    }}
    .st-key-nav_cat_resume button:hover,
    .st-key-nav_cat_interview button:hover {{
        border-color: {t["accent"]} !important;
        background: {t["accent_soft"]} !important;
    }}

    /* Indented Sub-option Buttons */
    .st-key-nav_sub_resume_create button,
    .st-key-nav_sub_resume_analysis button,
    .st-key-nav_sub_resume_saved button,
    .st-key-nav_sub_interview_spec button,
    .st-key-nav_sub_interview_job button,
    .st-key-nav_sub_interview_last_minute button {{
        background: transparent !important;
        border: 1px solid transparent !important;
        color: {t["text_secondary"]} !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        border-radius: 8px !important;
        padding: 9px 14px 9px 26px !important;
        text-align: left !important;
        width: 100% !important;
        display: block !important;
        margin: 2px 0 2px 8px !important;
        transition: all 0.15s ease !important;
    }}
    .st-key-nav_sub_resume_create button:hover,
    .st-key-nav_sub_resume_analysis button:hover,
    .st-key-nav_sub_resume_saved button:hover,
    .st-key-nav_sub_interview_spec button:hover,
    .st-key-nav_sub_interview_job button:hover,
    .st-key-nav_sub_interview_last_minute button:hover {{
        background: {t["surface2"]} !important;
        border-color: {t["border"]} !important;
        color: {t["text_primary"]} !important;
        transform: translateX(4px) !important;
    }}

    /* Profile, FAQ, Privacy, Terms, Home, Settings, Founder Analytics items */
    .st-key-nav_btn_profile button,
    .st-key-nav_btn_switch_user button,
    .st-key-nav_btn_generate_id_drawer button,
    .st-key-nav_btn_faq button,
    .st-key-nav_btn_privacy button,
    .st-key-nav_btn_terms button,
    .st-key-nav_btn_home button,
    .st-key-nav_btn_settings button,
    .st-key-nav_btn_founder_analytics button {{
        background: transparent !important;
        border: 1px solid {t["border"]} !important;
        color: {t["text_primary"]} !important;
        font-weight: 600 !important;
        font-size: 1.08rem !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        text-align: left !important;
        width: 100% !important;
        display: block !important;
        margin-bottom: 6px !important;
        transition: all 0.18s ease !important;
    }}
    .st-key-nav_btn_profile button:hover,
    .st-key-nav_btn_switch_user button:hover,
    .st-key-nav_btn_generate_id_drawer button:hover,
    .st-key-nav_btn_faq button:hover,
    .st-key-nav_btn_privacy button:hover,
    .st-key-nav_btn_terms button:hover,
    .st-key-nav_btn_home button:hover,
    .st-key-nav_btn_settings button:hover,
    .st-key-nav_btn_founder_analytics button:hover {{
        background: {t["surface2"]} !important;
        border-color: {t["accent"]} !important;
    }}

    /* Profile Avatar Item */
    .ac-nav-profile-card {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 12px;
        background: {t["surface2"]};
        border: 1px solid {t["border"]};
        border-radius: 12px;
        margin-top: 14px;
        margin-bottom: 6px;
    }}
    .ac-nav-avatar {{
        width: 44px;
        height: 44px;
        border-radius: 50%;
        object-fit: cover;
        flex-shrink: 0;
        border: 1.5px solid {t["accent"]};
    }}
    </style>
    """), unsafe_allow_html=True)

    # Render drawer container inside sidebar or fixed container
    with st.sidebar:
        # Exit / Close Button (placed cleanly above the brand text)
        close_col1, close_col2 = st.columns([82, 18])
        with close_col2:
            if st.button(">", key="nav_close_btn", help="Close Menu & Go to Home"):
                st.session_state["nav_open"] = False
                st.session_state["ac_screen"] = "landing"
                st.rerun()

        # Clean Brand Header Row (below exit button)
        st.markdown(clean_html(f"""
        <div id="ac-drawer-brand-logo" class="ac-drawer-header" style="margin-top:-6px; margin-bottom:12px; cursor:pointer;" title="Click to go to Home Page">
            <span class="ac-drawer-brand">
                <span style="color:{t['brand_ascend_color']};">Achieve</span><span style="color:{t['brand_career_color']};">Hire</span>
            </span>
        </div>
        """), unsafe_allow_html=True)

        # Status / Brand Element (Subtle, non-promise indicator)
        st.markdown(clean_html(f"""
        <div class="ac-brand-status-chip">
            <span class="ac-status-jewel"></span>
            <span>AchievePlatform · Ready</span>
        </div>
        """), unsafe_allow_html=True)

        st.markdown(clean_html(f'<div class="ac-nav-category-title">Core Preparation</div>'), unsafe_allow_html=True)

        # ── 1. Resume Category (Collapsible) ──
        resume_icon = "▾" if resume_open else "▸"
        if st.button(f"📄  Resume  {resume_icon}", key="nav_cat_resume", use_container_width=True):
            st.session_state["nav_resume_open"] = not resume_open
            st.rerun()

        def _guard_nav_access(feature_name: str, target_screen: str):
            if st.session_state.get("user_id"):
                st.session_state["ac_screen"] = target_screen
                st.session_state["nav_open"] = False
                st.rerun()
            else:
                st.session_state["auth_popup_open"] = True
                st.session_state["auth_popup_feature"] = feature_name
                st.session_state["nav_open"] = False
                st.rerun()

        if resume_open:
            if st.button("📝  Resume Create", key="nav_sub_resume_create", use_container_width=True):
                _guard_nav_access("Resume Create & Builder", "resume_create")
            if st.button("🔍  Resume Analysis", key="nav_sub_resume_analysis", use_container_width=True):
                _guard_nav_access("Resume Analysis & Audit", "resume_analysis")
            if st.button("📂  My Saved Resumes", key="nav_sub_resume_saved", use_container_width=True):
                _guard_nav_access("My Saved Resumes", "resume_saved")

        # ── 2. Interview Category (Collapsible) ──
        interview_icon = "▾" if interview_open else "▸"
        if st.button(f"🎙️  Interview  {interview_icon}", key="nav_cat_interview", use_container_width=True):
            st.session_state["nav_interview_open"] = not interview_open
            st.rerun()

        if interview_open:
            if st.button("🎯  Specialized Interview", key="nav_sub_interview_spec", use_container_width=True):
                _guard_nav_access("Specialized Voice Interview", "interview_specialized")
            if st.button("💼  Job Related Interview", key="nav_sub_interview_job", use_container_width=True):
                _guard_nav_access("Job Related Voice Interview", "interview_job")
            if st.button("⚡  Last-Minute Preparation", key="nav_sub_interview_last_minute", use_container_width=True):
                _guard_nav_access("Last-Minute Preparation Interview", "interview_last_minute")

        user_id = st.session_state.get("user_id")
        user_purpose = st.session_state.get("user_purpose")
        verified_uri = _get_user_verified_symbol_uri()

        user_status_color = "#10B981" if user_id else t["accent"]
        user_status_text = f"🆔 {user_id} · Verified" if user_id else "Guest · No ID Set"
        verified_badge_html = f'<img src="{verified_uri}" style="height:18px; width:auto;" title="Verified User ID" />' if user_id and verified_uri else ''

        # ── 3. User Profile Area ──
        st.markdown(clean_html(f"""
        <div class="ac-nav-profile-card">
            <img src="{avatar_uri}" alt="{username}" class="ac-nav-avatar" />
            <div style="overflow:hidden; flex:1;">
                <div style="display:flex; align-items:center; gap:6px; font-weight:700; font-size:0.95rem; color:{t['text_primary']}; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">
                    <span>{username}</span>
                    {verified_badge_html}
                </div>
                <div style="font-size:0.75rem; font-family:'Consolas', monospace; font-weight:600; color:{user_status_color}; margin-top:2px;">
                    {user_status_text}
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        if user_id:
            if st.button("👤  View Complete Profile", key="nav_btn_profile", use_container_width=True):
                st.session_state["ac_screen"] = "profile"
                st.session_state["nav_open"] = False
                st.rerun()
            if st.button("🔄  Switch / New User ID", key="nav_btn_switch_user", use_container_width=True):
                st.session_state["ac_screen"] = "signin"
                st.session_state["nav_open"] = False
                st.rerun()
        else:
            if st.button("✨  Generate Unique User ID", key="nav_btn_generate_id_drawer", use_container_width=True):
                st.session_state["ac_screen"] = "signin"
                st.session_state["nav_open"] = False
                st.rerun()

        # ── Founder Exclusive Dashboard ──
        if user_id == "ALANKRITA-FOUNDER":
            st.markdown(clean_html(f'<div class="ac-nav-category-title" style="margin-top:18px; color:{t["gold"]};">Founder Controls</div>'), unsafe_allow_html=True)
            if st.button("📊  Platform Analytics", key="nav_btn_founder_analytics", use_container_width=True):
                st.session_state["ac_screen"] = "founder_analytics"
                st.session_state["nav_open"] = False
                st.rerun()

        st.markdown(f'<div class="ac-nav-category-title" style="margin-top:18px;">Platform Policies</div>', unsafe_allow_html=True)

        # ── 4. FAQ ──
        if st.button("❓  FAQ", key="nav_btn_faq", use_container_width=True):
            st.session_state["ac_screen"] = "faq"
            st.session_state["nav_open"] = False
            st.rerun()

        # ── 5. Privacy Policy ──
        if st.button("🔒  Privacy Policy", key="nav_btn_privacy", use_container_width=True):
            st.session_state["ac_screen"] = "privacy"
            st.session_state["nav_open"] = False
            st.rerun()

        # ── 6. Terms and Conditions ──
        if st.button("📜  Terms & Conditions", key="nav_btn_terms", use_container_width=True):
            st.session_state["ac_screen"] = "terms"
            st.session_state["nav_open"] = False
            st.rerun()

        # ── 7. Home / Landing Screen ──
        st.markdown("<hr style='border:none; border-top:1px solid " + t["border"] + "; margin:16px 0 12px;'>", unsafe_allow_html=True)
        if st.button("🏠  Home Page", key="nav_btn_home", use_container_width=True):
            st.session_state["ac_screen"] = "landing"
            st.session_state["nav_open"] = False
            st.rerun()

        # ── 8. Platform Settings (at the very end) ──
        if st.button("⚙️  Settings", key="nav_btn_settings", use_container_width=True):
            st.session_state["ac_screen"] = "settings"
            st.session_state["nav_open"] = False
            st.rerun()

    components.html("""
    <script>
    (function run() {
        const parentDoc = window.parent.document;
        const backdrop = parentDoc.getElementById('ac-nav-backdrop-el');
        const brandLogo = parentDoc.getElementById('ac-drawer-brand-logo');
        const homeBtn = parentDoc.querySelector('.st-key-nav_btn_home button');

        if (!homeBtn) {
            setTimeout(run, 50);
            return;
        }

        if (backdrop && !backdrop.dataset.hasListener) {
            backdrop.dataset.hasListener = "true";
            backdrop.style.cursor = "pointer";
            backdrop.onclick = function() {
                homeBtn.click();
            };
        }

        if (brandLogo && !brandLogo.dataset.hasListener) {
            brandLogo.dataset.hasListener = "true";
            brandLogo.style.cursor = "pointer";
            brandLogo.onclick = function() {
                homeBtn.click();
            };
        }
    })();
    </script>
    """, height=0, scrolling=False)


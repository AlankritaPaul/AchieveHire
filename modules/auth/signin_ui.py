"""
AscendCareer — Candidate Sign In & User ID Generation UI
Flow: Sign In → Enter Name → Select Resume Preparation / Interview Preparation / Both → Generate Unique User ID.
"""

import streamlit as st
from modules.auth.user_service import (
    PURPOSE_OPTIONS,
    generate_unique_user_id,
    register_user,
    get_user_by_id,
    set_active_user,
)
from modules.landing.ui import THEMES, _get_user_verified_symbol_uri, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer


def render_signin_flow():
    """Renders the step-by-step candidate sign in and User ID generation interface."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Account › Sign In & User ID", show_signin=False, show_theme=False)

    # State tracking for generation confirmation
    if "just_generated_user" not in st.session_state:
        st.session_state["just_generated_user"] = None

    just_generated = st.session_state["just_generated_user"]

    st.markdown(clean_html(f"""
    <div style="max-width:520px; margin: 16px auto 12px; padding: 0 12px; text-align:center;">
        <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.75rem; font-weight:700; padding:3px 12px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
            Candidate Authentication &amp; Identity
        </div>
        <h1 style="font-size: 1.65rem; font-weight: 800; color:{t['text_primary']}; margin:0 0 6px;">
            AscendCareer Sign In
        </h1>
        <p style="font-size: 0.92rem; color:{t['text_secondary']}; line-height:1.5; max-width:460px; margin:0 auto 10px;">
            Generate your personal User ID or sign in with an existing User ID to keep your workspace private.
        </p>
    </div>
    """), unsafe_allow_html=True)

    # If user was just generated or loaded via direct access, show the Identity Confirmation Card
    if just_generated:
        _render_user_id_success_card(just_generated, t)
        return

    # Main Setup Container (Medium sized max-width 520px)
    st.markdown(clean_html(f"""
    <div style="max-width:520px; margin: 0 auto 24px; padding: 0 12px;">
    """), unsafe_allow_html=True)

    tab_new, tab_existing = st.tabs(["✨  New Candidate Setup", "🔑  Existing User ID"])

    with tab_new:
        with st.container(border=True):
            st.markdown(f"""
            <div style="font-size:1.08rem; font-weight:700; color:{t['text_primary']}; margin-bottom:10px;">
                1. Enter Your Full Name
            </div>
            """, unsafe_allow_html=True)

            candidate_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                key="input_candidate_name",
                label_visibility="collapsed"
            )

            st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="font-size:1.08rem; font-weight:700; color:{t['text_primary']}; margin-bottom:4px;">
                2. What would you like to use AscendCareer for?
            </div>
            <div style="font-size:0.90rem; font-weight:500; color:{t['text_muted']}; margin-bottom:10px;">
                Select your primary preparation focus.
            </div>
            """, unsafe_allow_html=True)

            selected_purpose = st.radio(
                "Intended Use",
                options=PURPOSE_OPTIONS,
                index=2,  # Default to 'Both'
                label_visibility="collapsed",
                horizontal=False,
                key="input_candidate_purpose"
            )

            st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

            is_founder = candidate_name and candidate_name.strip().lower() in ["founder alankrita pal", "founder alankrita paul", "founder alankrita"]

            if is_founder:
                btn_col1, btn_col2, btn_col3 = st.columns([40, 35, 25])
            else:
                btn_col1, btn_col3 = st.columns([65, 35])
                btn_col2 = None
                founder_clicked = False

            with btn_col1:
                generate_clicked = st.button(
                    "🚀  Generate ID",
                    type="primary",
                    use_container_width=True,
                    key="btn_generate_user_id"
                )
            
            if is_founder and btn_col2:
                with btn_col2:
                    founder_clicked = st.button(
                        "👑 Direct Access",
                        use_container_width=True,
                        key="btn_founder_bypass"
                    )
            
            with btn_col3:
                if st.button("← Back", use_container_width=True, key="btn_cancel_signin"):
                    st.session_state["ac_screen"] = "landing"
                    st.rerun()

            if generate_clicked:
                if not candidate_name or len(candidate_name.strip()) < 2:
                    st.error("Please enter your name (at least 2 characters) before generating your User ID.")
                else:
                    user_record = register_user(
                        name=candidate_name.strip(),
                        purpose=selected_purpose
                    )
                    st.session_state["just_generated_user"] = user_record
                    st.rerun()
                    
            if founder_clicked:
                if not candidate_name or len(candidate_name.strip()) < 2:
                    st.error("Please enter your name first.")
                elif candidate_name.strip().lower() in ["founder alankrita pal", "founder alankrita paul", "founder alankrita"]:
                    from modules.auth.user_service import ensure_founder_user_record
                    user_record = ensure_founder_user_record(selected_purpose)
                    st.session_state["just_generated_user"] = user_record
                    st.rerun()
                else:
                    st.error("Access Denied: Only the Founder can open an account without generating a User ID. Please click 'Generate User ID' instead.")

    with tab_existing:
        with st.container(border=True):
            st.markdown(f"""
            <div style="font-size:1.08rem; font-weight:700; color:{t['text_primary']}; margin-bottom:4px;">
                Sign In with Existing User ID
            </div>
            <div style="font-size:0.90rem; font-weight:500; color:{t['text_muted']}; margin-bottom:12px;">
                Enter your unique User ID to restore your workspace.
            </div>
            """, unsafe_allow_html=True)

            existing_id_input = st.text_input(
                "User ID",
                placeholder="Your unique User ID",
                key="input_existing_user_id",
                label_visibility="collapsed"
            )

            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

            c1, c2 = st.columns([60, 40])
            with c1:
                if st.button("🔑  Load Workspace", type="primary", use_container_width=True, key="btn_login_existing_id"):
                    if not existing_id_input.strip():
                        st.error("Please enter your User ID.")
                    elif existing_id_input.strip().lower() in ["founder alankrita pal", "founder alankrita paul", "founder alankrita", "alankrita-founder"]:
                        from modules.auth.user_service import ensure_founder_user_record
                        user_record = ensure_founder_user_record("Both")
                        st.session_state["just_generated_user"] = user_record
                        st.rerun()
                    else:
                        existing_user = get_user_by_id(existing_id_input.strip().upper())
                        if existing_user:
                            set_active_user(existing_user)
                            st.session_state["just_generated_user"] = existing_user
                            st.rerun()
                        else:
                            st.error("User ID not found in system. Please check the spelling or generate a new User ID.")
            with c2:
                if st.button("← Cancel", use_container_width=True, key="btn_cancel_existing"):
                    st.session_state["ac_screen"] = "landing"
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def _render_user_id_success_card(user: dict, t: dict):
    """Renders a prominent confirmation card showing the generated unique User ID."""
    user_id = user["user_id"]
    name = user["name"]
    purpose = user.get("purpose", "Both")
    is_founder_user = (user_id == "ALANKRITA-FOUNDER")
    verified_uri = _get_user_verified_symbol_uri()

    st.markdown(clean_html(f"""
    <div style="max-width:520px; margin: 12px auto 24px; padding: 0 12px;">
        <div style="background:{t['surface']}; border:2px solid {t['accent']}; border-radius:16px; padding:24px 20px; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="margin-bottom:8px;">
                <img src="{verified_uri}" alt="User ID Generated" style="height:64px; width:auto; filter:drop-shadow(0 4px 14px rgba(16,185,129,0.40));" />
            </div>
            <h2 style="font-size:1.45rem; font-weight:800; color:{t['text_primary']}; margin:0 0 4px;">
                Welcome, {name}! {' (Founder Access)' if is_founder_user else ''}
            </h2>
            <div style="font-size:0.90rem; color:{t['text_secondary']}; margin-bottom:16px;">
                Your unique AscendCareer user ID has been generated &amp; verified.
            </div>

            <!-- Unique User ID Display Card -->
            <div style="background:{t['surface2']}; border:1.5px dashed #10B981; border-radius:12px; padding:14px 20px; margin:0 auto 16px; display:inline-block;">
                <div style="font-size:0.72rem; font-weight:800; color:{t['text_muted']}; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:2px;">
                    Your Unique AscendCareer User ID
                </div>
                <div style="font-family:'Consolas', 'Courier New', monospace; font-size:1.65rem; font-weight:800; color:{t['accent']}; letter-spacing:0.06em;">
                    {user_id}
                </div>
            </div>

            <!-- Purpose & Isolation Guarantee -->
            <div style="background:{t['accent_soft']}; border-radius:10px; padding:10px 14px; margin-bottom:18px; text-align:left;">
                <div style="font-size:0.84rem; color:{t['text_primary']}; font-weight:600; margin-bottom:2px;">
                    🔒 Data Isolation &amp; Privacy:
                </div>
                <div style="font-size:0.82rem; color:{t['text_secondary']}; line-height:1.45;">
                    All resume drafts, evaluations, and mock interview attempts are strictly saved under <strong>{user_id}</strong>.
                </div>
            </div>

            <div style="display:inline-block; background:{t['gold_soft']}; color:{t['gold']}; font-size:0.80rem; font-weight:700; padding:3px 12px; border-radius:50px; margin-bottom:18px;">
                🎯 Target Focus: {purpose}
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    c1, c2 = st.columns([50, 50])

    with c1:
        if purpose == "Resume Preparation":
            next_label = "📝 Start Resume"
            target_screen = "resume_create"
        elif purpose == "Interview Preparation":
            next_label = "🎙️ Start Interview"
            target_screen = "interview_specialized"
        else:
            next_label = "🚀 Enter Workspace"
            target_screen = "resume_create"

        if st.button(next_label, type="primary", use_container_width=True, key="btn_continue_to_prep"):
            st.session_state["just_generated_user"] = None
            st.session_state["ac_screen"] = target_screen
            st.rerun()

    with c2:
        if is_founder_user:
            if st.button("📊 Founder Analytics", use_container_width=True, key="btn_founder_analytics_after_gen"):
                st.session_state["just_generated_user"] = None
                st.session_state["ac_screen"] = "founder_analytics"
                st.rerun()
        else:
            if st.button("👤 View Profile", use_container_width=True, key="btn_view_profile_after_gen"):
                st.session_state["just_generated_user"] = None
                st.session_state["ac_screen"] = "profile"
                st.rerun()

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    if st.button("← Back to Landing", use_container_width=True, key="btn_back_to_landing_after_gen"):
        st.session_state["just_generated_user"] = None
        st.session_state["ac_screen"] = "landing"
        st.rerun()

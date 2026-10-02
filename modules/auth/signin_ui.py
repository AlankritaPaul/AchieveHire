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
from modules.landing.ui import THEMES, clean_html
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
    <div style="max-width:760px; margin: 28px auto 16px; padding: 0 16px; text-align:center;">
        <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.80rem; font-weight:700; padding:4px 16px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;">
            Candidate Authentication &amp; Identity
        </div>
        <h1 style="font-size: 2.2rem; font-weight: 800; color:{t['text_primary']}; margin:0 0 8px;">
            AscendCareer Account Setup
        </h1>
        <p style="font-size: 1.05rem; color:{t['text_secondary']}; line-height:1.6; max-width:620px; margin:0 auto;">
            Generate your permanent, unique User ID to keep your resumes, interview practice sessions, evaluations, and progress reports completely separated and private.
        </p>
    </div>
    """), unsafe_allow_html=True)

    # If user was just generated, show the Identity Confirmation Card
    if just_generated:
        _render_user_id_success_card(just_generated, t)
        return

    # Main Setup Container
    st.markdown(clean_html(f"""
    <div style="max-width:680px; margin: 0 auto 32px; padding: 0 16px;">
    </div>
    """), unsafe_allow_html=True)

    tab_new, tab_existing = st.tabs(["✨  New Candidate Setup", "🔑  Existing User ID"])

    with tab_new:
        with st.container(border=True):
            st.markdown(f"""
            <div style="font-size:1.22rem; font-weight:700; color:{t['text_primary']}; margin-bottom:12px;">
                1. Enter Your Full Name
            </div>
            """, unsafe_allow_html=True)

            candidate_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                key="input_candidate_name",
                label_visibility="collapsed"
            )

            st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="font-size:1.22rem; font-weight:700; color:{t['text_primary']}; margin-bottom:6px;">
                2. What would you like to use AscendCareer for?
            </div>
            <div style="font-size:1.02rem; font-weight:500; color:{t['text_muted']}; margin-bottom:14px;">
                Select your intended preparation focus. You can practice all features at any time.
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

            st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

            is_founder = candidate_name and candidate_name.strip().lower() in ["founder alankrita pal", "founder alankrita paul", "founder alankrita"]

            if is_founder:
                btn_col1, btn_col2, btn_col3 = st.columns([40, 35, 25])
            else:
                btn_col1, btn_col3 = st.columns([65, 35])
                btn_col2 = None
                founder_clicked = False

            with btn_col1:
                generate_clicked = st.button(
                    "🚀  Generate User ID",
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
                    st.session_state["just_generated_user"] = None
                    st.session_state["ac_screen"] = "resume_create" if selected_purpose != "Interview Preparation" else "interview_specialized"
                    st.rerun()
                else:
                    st.error("Access Denied: Only the Founder can open an account without generating a User ID. Please click 'Generate User ID' instead.")

    with tab_existing:
        with st.container(border=True):
            st.markdown(f"""
            <div style="font-size:1.22rem; font-weight:700; color:{t['text_primary']}; margin-bottom:6px;">
                Sign In with Existing User ID
            </div>
            <div style="font-size:1.02rem; font-weight:500; color:{t['text_muted']}; margin-bottom:16px;">
                Enter your unique AscendCareer User ID to restore your personal resumes and interview attempts.
            </div>
            """, unsafe_allow_html=True)

            existing_id_input = st.text_input(
                "User ID",
                placeholder="Your unique User ID will appear here",
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


def _render_user_id_success_card(user: dict, t: dict):
    """Renders a prominent confirmation card showing the generated unique User ID."""
    user_id = user["user_id"]
    name = user["name"]
    purpose = user.get("purpose", "Both")

    st.markdown(clean_html(f"""
    <div style="max-width:680px; margin: 12px auto 32px; padding: 0 16px;">
        <div style="background:{t['surface']}; border:2px solid {t['accent']}; border-radius:18px; padding:32px 28px; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="font-size:2.8rem; margin-bottom:8px;">🎉</div>
            <h2 style="font-size:1.65rem; font-weight:800; color:{t['text_primary']}; margin:0 0 6px;">
                Welcome, {name}!
            </h2>
            <div style="font-size:0.95rem; color:{t['text_secondary']}; margin-bottom:20px;">
                Your unique AscendCareer identity has been successfully generated.
            </div>

            <!-- Unique User ID Display Card -->
            <div style="background:{t['surface2']}; border:1.5px dashed {t['accent']}; border-radius:12px; padding:18px 24px; margin:0 auto 20px; display:inline-block;">
                <div style="font-size:0.75rem; font-weight:800; color:{t['text_muted']}; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:4px;">
                    Your Unique AscendCareer User ID
                </div>
                <div style="font-family:'Consolas', 'Courier New', monospace; font-size:1.9rem; font-weight:800; color:{t['accent']}; letter-spacing:0.06em;">
                    {user_id}
                </div>
            </div>

            <!-- Purpose & Isolation Guarantee -->
            <div style="background:{t['accent_soft']}; border-radius:10px; padding:12px 16px; margin-bottom:24px; text-align:left;">
                <div style="font-size:0.86rem; color:{t['text_primary']}; font-weight:600; margin-bottom:4px;">
                    🔒 Data Separation &amp; Privacy Guarantee:
                </div>
                <div style="font-size:0.84rem; color:{t['text_secondary']}; line-height:1.55;">
                    This User ID is uniquely assigned to you. All your resume drafts, analysis scores, mock interview recordings, and progress analytics will be strictly isolated under <strong>{user_id}</strong>.
                </div>
            </div>

            <div style="display:inline-block; background:{t['gold_soft']}; color:{t['gold']}; font-size:0.82rem; font-weight:700; padding:4px 14px; border-radius:50px; margin-bottom:24px;">
                🎯 Target Focus: {purpose}
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([60, 40])
    with col_btn1:
        if purpose == "Resume Preparation":
            next_label = "📝  Start Resume Preparation"
            target_screen = "resume_create"
        elif purpose == "Interview Preparation":
            next_label = "🎙️  Start Interview Preparation"
            target_screen = "interview_specialized"
        else:
            next_label = "🚀  Enter AscendCareer Workspace"
            target_screen = "resume_create"

        if st.button(next_label, type="primary", use_container_width=True, key="btn_continue_to_prep"):
            st.session_state["just_generated_user"] = None
            st.session_state["ac_screen"] = target_screen
            st.rerun()

    with col_btn2:
        if st.button("👤  View Candidate Profile", use_container_width=True, key="btn_view_profile_after_gen"):
            st.session_state["just_generated_user"] = None
            st.session_state["ac_screen"] = "profile"
            st.rerun()

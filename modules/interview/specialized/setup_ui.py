"""
AchieveHire — Specialized Interview Setup Screen
Allows candidate to configure technical specialization (with manual entry support),
interview spoken language (English, Hindi, Hinglish), interviewer gender,
and review round session prerequisites.
"""

import streamlit as st
from modules.landing.ui import clean_html
from modules.interview.specialized.models import (
    ROUNDS_CONFIG,
    LANGUAGE_OPTIONS,
    INTERVIEWER_OPTIONS,
    PRESET_SPECIALIZATIONS,
)
from modules.interview.specialized.storage import (
    load_specialized_progress,
    is_round_unlocked,
)


def render_specialized_setup(t: dict, on_launch_session, on_view_reports):
    """Renders the setup interface for configuring specialization, language, and interviewer."""
    user_id = st.session_state.get("user_id", "guest")

    st.markdown(clean_html(f"""
    <div style="max-width:960px; margin: 0 auto 24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
                <div style="font-family:'Cinzel Decorative', Georgia, serif; font-size:1.4rem; font-weight:800;">
                    <span style="color:{t['brand_ascend_color']};">Achieve</span><span style="color:{t['brand_career_color']};">Hire</span>
                </div>
                <div style="font-size:0.86rem; color:{t['text_muted']}; font-style:italic;">Better Preparation. Stronger Presentation.</div>
            </div>
            <div style="display:inline-block; background:{t['surface2']}; border:1px solid {t['border']}; padding:6px 16px; border-radius:50px; font-size:0.86rem; font-weight:700; color:{t['text_primary']};">
                Candidate ID: <code>{user_id}</code>
            </div>
        </div>
        <h2 style="font-size:1.85rem; font-weight:800; color:{t['text_primary']}; margin:0 0 6px;">
            Specialized Interview Setup
        </h2>
        <p style="font-size:0.98rem; color:{t['text_secondary']}; margin:0;">
            Configure your technical domain specialization, interviewer, and preferred conversation language.
        </p>
    </div>
    """), unsafe_allow_html=True)

    col_main, col_rounds = st.columns([60, 40], gap="large")

    with col_main:
        # 1. Technical Specialization Selection
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-bottom:8px;'>1. Choose Technical Specialization</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            spec_mode = st.radio(
                "Selection Method",
                options=["Select from Supported List", "✍️ Write Your Specialization (Custom Entry)"],
                index=0,
                key="spec_mode_radio",
            )

            if "Write Your Specialization" in spec_mode:
                custom_spec = st.text_input(
                    "Write Your Specialization (e.g., Solidity, Haskell, Embedded Linux, Kotlin Multiplatform)",
                    value=st.session_state.get("specialized_custom_spec", ""),
                    placeholder="Enter your exact technical language or specialization...",
                    key="input_custom_spec",
                )
                active_specialization = custom_spec.strip() if custom_spec.strip() else "Python"
            else:
                preset_choice = st.selectbox(
                    "Select Specialization / Language",
                    options=PRESET_SPECIALIZATIONS,
                    index=0,
                    key="select_preset_spec",
                )
                active_specialization = preset_choice

            st.session_state["specialized_selected_domain"] = active_specialization
            st.markdown(f"<div style='font-size:0.84rem; color:{t['text_muted']}; margin-top:4px;'>Selected Specialization: <strong>{active_specialization}</strong></div>", unsafe_allow_html=True)

        # 2. Interview Language
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-top:16px; margin-bottom:8px;'>2. Interview Spoken Language</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            selected_lang = st.radio(
                "Interviewer Language",
                options=LANGUAGE_OPTIONS,
                index=0,
                key="radio_interview_lang",
                help="The language used by the interviewer. Technical terms remain in English.",
            )
            st.session_state["specialized_selected_language"] = selected_lang

            if selected_lang == "Hinglish":
                st.info("🎙️ **Hinglish Mode:** The interviewer will speak natural, conversational Indian Hinglish with standard English technical terms.")
            elif selected_lang == "Hindi":
                st.info("🎙️ **Hindi Mode:** The interviewer will speak clear, understandable Hindi while keeping technical terms recognizable.")
            else:
                st.info("🎙️ **English Mode:** The interviewer will speak clear, professional English.")

        # 3. Interviewer Selection
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-top:16px; margin-bottom:8px;'>3. Choose Interviewer</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            interviewer_choice = st.radio(
                "Interviewer Persona",
                options=["👨‍💼 Male Interviewer (David / Rohan)", "👩‍💼 Female Interviewer (Sarah / Priya)"],
                index=0,
                key="radio_interviewer_gender",
            )
            gender_id = "male" if "Male" in interviewer_choice else "female"
            st.session_state["specialized_interviewer_gender"] = gender_id

    with col_rounds:
        # 4. Round Selector & Progression Status
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-bottom:8px;'>4. Select Round to Attempt</h3>", unsafe_allow_html=True)
        progress = load_specialized_progress(user_id, active_specialization)
        completed_rounds = progress.get("rounds_completed", [])

        with st.container(border=True):
            round_options = [1, 2, 3, 4]
            current_selected_round = st.session_state.get(
                "specialized_selected_round", progress.get("current_unlocked_round", 1)
            )

            def _execute_launch(r_to_start: int):
                lang = (
                    st.session_state.get("specialized_selected_language")
                    or st.session_state.get("specialized_language")
                    or "English"
                )
                gender = (
                    st.session_state.get("specialized_interviewer_gender")
                    or st.session_state.get("specialized_interviewer")
                    or "male"
                )
                st.session_state["specialized_selected_domain"] = active_specialization
                st.session_state["specialized_selected_language"] = lang
                st.session_state["specialized_language"] = lang
                st.session_state["specialized_interviewer_gender"] = gender
                st.session_state["specialized_interviewer"] = gender
                st.session_state["specialized_selected_round"] = r_to_start

                on_launch_session(
                    specialization=active_specialization,
                    language=lang,
                    interviewer_gender=gender,
                    round_num=r_to_start,
                )
                st.rerun()

            for r_num in round_options:
                cfg = ROUNDS_CONFIG[r_num]
                is_unlocked = is_round_unlocked(user_id, active_specialization, r_num)
                is_done = r_num in completed_rounds
                is_selected = (current_selected_round == r_num)

                status_badge = "✅ Completed" if is_done else ("🔓 Unlocked" if is_unlocked else "🔒 Locked")
                border_color = t['accent'] if is_selected else (t['border'] if is_unlocked else t['border'])

                st.markdown(f"""
                <div style="border:2px solid {border_color}; background:{t['surface2'] if is_selected else t['surface']}; border-radius:10px; padding:12px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-weight:700; color:{t['text_primary']};">
                            {cfg['badge_icon']} {cfg['name']} ({cfg['duration_minutes']} Mins)
                        </div>
                        <span style="font-size:0.80rem; font-weight:700; color:{'#10B981' if is_done else ('#3B82F6' if is_unlocked else '#9CA3AF')};">
                            {status_badge}
                        </span>
                    </div>
                    <div style="font-size:0.84rem; color:{t['text_secondary']}; margin-top:4px;">
                        {cfg['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if is_unlocked:
                    c_act1, c_act2 = st.columns([1, 1], gap="small")
                    with c_act1:
                        sel_label = f"✓ Round {r_num} Active" if is_selected else f"Select Round {r_num}"
                        if st.button(
                            sel_label,
                            key=f"btn_select_round_{r_num}",
                            use_container_width=True,
                            disabled=is_selected,
                        ):
                            st.session_state["specialized_selected_round"] = r_num
                            st.rerun()
                    with c_act2:
                        if st.button(
                            f"🚀 Start R{r_num}",
                            key=f"btn_quick_launch_r_{r_num}",
                            type="primary" if is_selected else "secondary",
                            use_container_width=True,
                        ):
                            st.session_state["specialized_selected_round"] = r_num
                            _execute_launch(r_num)

            selected_r_num = st.session_state.get("specialized_selected_round", 1)
            selected_cfg = ROUNDS_CONFIG[selected_r_num]

            st.markdown("<hr style='margin:14px 0;'/>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:{t['surface2']}; border-left:4px solid #10B981; border-radius:8px; padding:10px 14px; margin-bottom:12px; font-size:0.86rem; color:{t['text_secondary']};">
                🎯 <strong>Ready for {selected_cfg['name']}:</strong> Complete session in one go. Leaving midway cancels the round without marks.
            </div>
            """, unsafe_allow_html=True)

            launch_btn = st.button(
                f"🚀  Start {selected_cfg['name']}",
                type="primary",
                use_container_width=True,
                key="btn_launch_live_specialized_round",
            )

            if launch_btn:
                _execute_launch(selected_r_num)

            if completed_rounds:
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("📊 View Past Performance Reports", use_container_width=True, key="btn_view_spec_past_reports"):
                    on_view_reports(active_specialization)
                    st.rerun()


# -*- coding: utf-8 -*-
"""
AchieveHire — Job Related Live Interview Session HUD
Features a 100% transparent, responsive Live Conversation Chat & Dual Input (Voice + Text + Submit Button).
"""

import streamlit as st
import time
from typing import Dict, Any, List, Optional
from modules.landing.ui import THEMES, clean_html
from modules.interview.job_related.models import (
    JOB_ROUNDS_CONFIG,
    JobQuestionRecord,
    JobInterviewRoundState,
)
from modules.interview.job_related.engine import (
    generate_round_questions,
    generate_clarification_response,
    generate_closing_qa_response,
)
from modules.interview.job_related.evaluator import (
    evaluate_candidate_answer,
    generate_round_evaluation,
)
from modules.interview.job_related.storage import (
    load_job_interview_session,
    save_round_evaluation,
)
from modules.interview.job_related.audio_ui import (
    render_voice_synthesis_player,
    render_voice_recognition_widget,
)


def _init_live_round_state(round_num: int, user_id: str) -> None:
    """Initializes the in-memory round state for a continuous interview session."""
    session = load_job_interview_session(user_id) or {}
    role = session.get("target_role", "Software Engineer")
    company = session.get("target_company", "Google")
    lang = session.get("language", "English")
    resume = session.get("resume_snapshot", {})

    questions, panel = generate_round_questions(
        job_role=role,
        company=company,
        resume=resume,
        language=lang,
        round_num=round_num,
    )

    state = JobInterviewRoundState(
        round_num=round_num,
        is_active=True,
        is_completed=False,
        start_timestamp=time.time(),
        elapsed_seconds=0,
        active_question_index=0,
        questions_list=questions,
        panel_members=panel,
        active_interviewer_index=0,
    )

    st.session_state["job_live_state"] = state
    st.session_state["job_round_start_time"] = time.time()
    st.session_state["job_current_speech_text"] = questions[0].question_text if questions else ""
    st.session_state["job_interviewer_reaction"] = ""


def render_job_live_interview_session(round_num: int):
    """Renders the realistic, transparent live interview room."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id") or "GUEST"

    session = load_job_interview_session(user_id) or {}
    role = session.get("target_role", "Software Engineer")
    company = session.get("target_company", "Google")
    lang = session.get("language", "English")

    if "job_live_state" not in st.session_state or st.session_state.get("job_active_round_num") != round_num:
        _init_live_round_state(round_num, user_id)
        st.session_state["job_active_round_num"] = round_num

    state: JobInterviewRoundState = st.session_state["job_live_state"]
    cfg = JOB_ROUNDS_CONFIG.get(round_num, JOB_ROUNDS_CONFIG[1])

    # Timer Calculation
    start_t = st.session_state.get("job_round_start_time", time.time())
    elapsed_sec = int(time.time() - start_t)
    time_allowed = cfg["duration_minutes"] * 60
    remaining_sec = max(0, time_allowed - elapsed_sec)

    mins_rem = remaining_sec // 60
    secs_rem = remaining_sec % 60
    timer_color = "#DC2626" if remaining_sec < 180 else t["accent"]

    total_q = len(state.questions_list)
    curr_idx = state.active_question_index

    # Check for session completion or thank you stage
    if remaining_sec <= 0 or curr_idx >= total_q:
        active_panelist = state.panel_members[0]
        thank_text = "Aaj ke is interview round ke liye aapka bohot bohot dhanyawad. Hamare panel ne aapke javab evaluate kar liye hain, aur aapka performance report tayar hai." if "hindi" in lang.lower() or "hinglish" in lang.lower() else "Thank you so much for your time and participation today. That concludes our interview round. We have evaluated your responses and your performance report is now ready."
        
        st.markdown(clean_html(f"""
        <div style="max-width:760px; margin: 30px auto; text-align:center; background:{t['surface']}; border:1.5px solid {t['accent']}; border-radius:18px; padding:32px; box-shadow:{t['card_shadow']};">
            <div style="width:90px; height:90px; border-radius:50%; background:{t['accent_soft']}; border:3px solid {t['accent']}; display:flex; align-items:center; justify-content:center; font-size:3rem; margin:0 auto 16px;">
                {active_panelist.avatar_emoji}
            </div>
            <h2 style="font-size:1.6rem; font-weight:800; color:{t['text_primary']}; margin:0 0 6px;">
                Thank You from {active_panelist.name} & Panel
            </h2>
            <div style="font-size:0.95rem; font-weight:600; color:{t['accent']}; margin-bottom:16px;">
                {active_panelist.title} · {company}
            </div>
            <p style="font-size:1.05rem; color:{t['text_secondary']}; max-width:620px; margin:0 auto 24px; line-height:1.6; font-style:italic;">
                "{thank_text}"
            </p>
        </div>
        """), unsafe_allow_html=True)
        
        render_voice_synthesis_player(
            text_to_speak=thank_text,
            language=lang,
            interviewer_gender=active_panelist.voice_gender,
            key=f"tts_job_thankyou_{round_num}",
        )
        
        st.markdown("<div style='max-width:400px; margin:0 auto;'>", unsafe_allow_html=True)
        if st.button("📊  View Performance & Improvement Report →", type="primary", use_container_width=True, key="btn_view_job_rep_thankyou"):
            _finalize_round(round_num, user_id, elapsed_sec, role, company, lang)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    current_q: JobQuestionRecord = state.questions_list[curr_idx]
    active_panelist = next((p for p in state.panel_members if p.id == current_q.interviewer_id), state.panel_members[0])

    # Top HUD
    st.markdown(clean_html(f"""
    <div style="max-width:960px; margin: 12px auto 16px; padding: 0 16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; background:{t['surface']}; border:1px solid {t['border']}; border-radius:14px; padding:14px 20px; box-shadow:{t['card_shadow']};">
            <div>
                <div style="font-size:0.78rem; font-weight:700; color:{t['accent']}; text-transform:uppercase; letter-spacing:0.06em;">
                    AchieveHire Live Room · {cfg['name']}
                </div>
                <div style="font-size:1.15rem; font-weight:800; color:{t['text_primary']}; margin-top:2px;">
                    {role} · {company}
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:18px;">
                <div style="text-align:right;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; font-weight:600; text-transform:uppercase;">
                        Progress
                    </div>
                    <div style="font-size:1.05rem; font-weight:800; color:{t['text_primary']};">
                        Question {curr_idx + 1} of {total_q}
                    </div>
                </div>
                <div style="border-left:1px solid {t['border']}; padding-left:18px; text-align:right;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; font-weight:600; text-transform:uppercase;">
                        Time Remaining
                    </div>
                    <div id="job-live-timer-display" style="font-size:1.35rem; font-weight:900; color:{timer_color}; font-family:monospace;">
                        {mins_rem:02d}:{secs_rem:02d}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # Main Canvas: Left Panel (Interviewer & Speech), Right Panel (Transcript & Answer)
    col_panel, col_candidate = st.columns([45, 55], gap="large")

    with col_panel:
        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:16px; padding:22px; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="width:84px; height:84px; border-radius:50%; background:{t['accent_soft']}; border:2.5px solid {t['accent']}; display:flex; align-items:center; justify-content:center; font-size:2.6rem; margin: 0 auto 12px;">
                {active_panelist.avatar_emoji}
            </div>
            <h3 style="font-size:1.25rem; font-weight:800; color:{t['text_primary']}; margin:0 0 4px;">
                {active_panelist.name}
            </h3>
            <div style="font-size:0.86rem; font-weight:600; color:{t['accent']}; margin-bottom:6px;">
                {active_panelist.title} · {company}
            </div>
            
            <div id="job-interviewer-status-text" style="background:{t['surface2']}; border:1px solid {t['border']}; border-radius:30px; padding:8px 16px; font-size:0.88rem; font-weight:700; color:{t['accent']}; display:inline-block; margin-bottom:12px;">
                🎙️ Interviewer Speaking... (Listen Carefully)
            </div>
        </div>
        """), unsafe_allow_html=True)

        speech_text = st.session_state.get("job_current_speech_text", current_q.question_text)

        st.markdown(clean_html(f"""
        <div style="background:{t['surface2']}; border:1.5px solid {t['accent']}; border-radius:12px; padding:14px 18px; margin-top:10px; text-align:left;">
            <div style="font-weight:700; font-size:0.82rem; color:{t['accent']}; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.04em;">
                🎙️ Live Interviewer Question &amp; Reaction:
            </div>
            <div style="font-size:0.98rem; font-style:italic; color:{t['text_primary']}; line-height:1.5;">
                "{speech_text}"
            </div>
        </div>
        """), unsafe_allow_html=True)

        render_voice_synthesis_player(
            text_to_speak=speech_text,
            language=lang,
            interviewer_gender=active_panelist.voice_gender,
            key=f"tts_q_{curr_idx}_{len(speech_text)}",
        )

    with col_candidate:
        st.markdown(clean_html(f"""
        <div style="margin-bottom:10px;">
            <div style="font-weight:700; font-size:1.05rem; color:{t['text_primary']};">
                Your Spoken Answer &amp; Live Transcript
            </div>
            <div style="font-size:0.82rem; color:{t['text_muted']};">
                Speak into your microphone or type below. Answer auto-submits when you finish speaking.
            </div>
        </div>
        """), unsafe_allow_html=True)

        # Voice listener
        render_voice_recognition_widget(prompt_key=f"stt_{curr_idx}", language=lang)

        # Hidden fields for JS voice auto-submit
        st.markdown("""
        <style>
        div[data-testid="stElementContainer"]:has(input[aria-label="hidden_ans"]),
        div[data-testid="stTextInput"]:has(input[aria-label="hidden_ans"]),
        div[data-testid="stElementContainer"]:has(input[aria-label="hidden_ans"]) + div[data-testid="stElementContainer"] {
            position: absolute !important;
            opacity: 0 !important;
            width: 1px !important;
            height: 1px !important;
            overflow: hidden !important;
            pointer-events: auto !important;
            z-index: -9999 !important;
            margin: 0px !important;
            padding: 0px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        hidden_ans = st.text_input("hidden_ans", key=f"hidden_ans_{curr_idx}", label_visibility="collapsed")
        hidden_submit = st.button("hidden_submit", key=f"hidden_sub_{curr_idx}")

        # Transparent visible Text Input & Submit Button
        candidate_input = st.text_area(
            "Your Answer (Auto-populates from Microphone):",
            key=f"ans_input_{curr_idx}",
            height=110,
            placeholder="Speak into your microphone or type your response here...",
            label_visibility="collapsed",
        )

        submit_btn = st.button("🚀 Submit Answer & Next Question →", type="primary", use_container_width=True, key=f"btn_sub_{curr_idx}")

        if submit_btn or hidden_submit:
            ans_val = hidden_ans.strip() if hidden_ans.strip() else (candidate_input.strip() if candidate_input.strip() else "Candidate spoken response recorded.")
            evaluated_q = evaluate_candidate_answer(current_q, ans_val, lang, role, company)
            state.questions_list[curr_idx] = evaluated_q
            state.active_question_index += 1

            if state.active_question_index < len(state.questions_list):
                next_q = state.questions_list[state.active_question_index]
                reaction = evaluated_q.reaction or "Good! Understood."
                combined_speech = f"{reaction} ... {next_q.question_text}"
                st.session_state["job_current_speech_text"] = combined_speech
            st.rerun()

    # Session Exit Option
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    with st.expander("⚠️ Session Emergency Exit", expanded=False):
        if st.button("Exit Interview Round", key="btn_exit_session_round"):
            del st.session_state["job_live_state"]
            st.session_state["job_view_mode"] = "setup"
            st.rerun()


def _finalize_round(round_num: int, user_id: str, elapsed_sec: int, role: str, company: str, lang: str):
    """Processes evaluations, saves results persistently, and transitions to report view."""
    state = st.session_state.get("job_live_state")
    if not state:
        return

    evaluation = generate_round_evaluation(
        round_num=round_num,
        questions=state.questions_list,
        actual_time_sec=elapsed_sec,
        job_role=role,
        company=company,
        language=lang,
    )

    save_round_evaluation(user_id, round_num, evaluation)

    if "job_live_state" in st.session_state:
        del st.session_state["job_live_state"]

    st.session_state["job_view_mode"] = "report"
    st.session_state["job_report_round"] = round_num

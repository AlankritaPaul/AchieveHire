"""
AchieveHire — Last-Minute Preparation Live Room HUD
Enforces:
1. Exact 30-minute countdown timer.
2. Hidden questions during live interview (voice only).
3. Question 1 is strictly 'Please introduce yourself.'
4. Alternating multi-interviewer panel with distinct personas.
5. Thinking time, repeat, clarify, and honest 'I don't know' handling.
6. Automatic attempt finalization and permanent persistence.
"""

import streamlit as st
import time
from typing import Dict, Any, List
from modules.landing.ui import THEMES, clean_html
from modules.interview.last_minute.models import (
    LAST_MINUTE_DURATION_SECONDS,
    LastMinuteQuestionRecord,
    LastMinutePanelMember,
    MODE_SPECIALIZED,
)
from modules.interview.last_minute.engine import (
    generate_last_minute_questions,
    generate_last_minute_clarification,
)
from modules.interview.last_minute.evaluator import (
    evaluate_last_minute_answer,
    synthesize_attempt_evaluation,
)
from modules.interview.last_minute.storage import save_new_attempt
from modules.interview.last_minute.audio_ui import (
    render_voice_synthesis_player,
    render_voice_recognition_widget,
)


def _init_lm_live_session(mode: str, topic: str, company: str, lang: str, resume: dict):
    """Initializes in-memory state for the 30-minute intensive interview."""
    questions, panel = generate_last_minute_questions(
        mode=mode,
        topic=topic,
        company=company,
        language=lang,
        resume=resume,
    )
    st.session_state["lm_questions"] = questions
    st.session_state["lm_panel"] = panel
    st.session_state["lm_active_q_idx"] = 0
    st.session_state["lm_start_time"] = time.time()
    st.session_state["lm_current_speech"] = questions[0].question_text if questions else ""
    st.session_state["lm_session_finalized"] = False


def render_last_minute_live_session():
    """Renders the intensive 30-minute live interview room."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id") or "GUEST"

    mode = st.session_state.get("lm_active_mode", MODE_SPECIALIZED)
    topic = st.session_state.get("lm_active_topic", "Technical Core")
    company = st.session_state.get("lm_active_company", "Technology Solutions")
    lang = st.session_state.get("lm_active_language", "English")
    resume = st.session_state.get("lm_resume_snapshot", {})

    # Initialize session if not active
    if "lm_questions" not in st.session_state:
        _init_lm_live_session(mode, topic, company, lang, resume)

    questions: List[LastMinuteQuestionRecord] = st.session_state["lm_questions"]
    panel: List[LastMinutePanelMember] = st.session_state["lm_panel"]
    curr_idx = st.session_state.get("lm_active_q_idx", 0)

    # 30-minute Timer Tracking
    start_t = st.session_state.get("lm_start_time", time.time())
    elapsed_sec = int(time.time() - start_t)
    remaining_sec = max(0, LAST_MINUTE_DURATION_SECONDS - elapsed_sec)

    mins_rem = remaining_sec // 60
    secs_rem = remaining_sec % 60
    timer_color = "#DC2626" if remaining_sec < 180 else t["accent"]

    # Conclude if timer expired or all questions completed
    if (remaining_sec <= 0 or curr_idx >= len(questions)) and not st.session_state.get("lm_session_finalized", False):
        st.session_state["lm_session_finalized"] = True
        st.warning("⏱️ 30-Minute session concluded. Finalizing your comprehensive scorecard...")
        _finalize_lm_session(mode, topic, company, lang, resume, questions, elapsed_sec, user_id)
        return

    current_q = questions[curr_idx]
    active_panelist = next((p for p in panel if p.id == current_q.interviewer_id), panel[0])

    # Top HUD
    st.markdown(clean_html(f"""
    <div style="max-width:940px; margin: 12px auto 16px; padding: 0 16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; background:{t['surface']}; border:1px solid {t['border']}; border-radius:14px; padding:14px 20px; box-shadow:{t['card_shadow']};">
            <div>
                <div style="font-size:0.78rem; font-weight:700; color:{t['accent']}; text-transform:uppercase; letter-spacing:0.06em;">
                    ⚡ Last-Minute Intensive Rehearsal · {mode}
                </div>
                <div style="font-size:1.15rem; font-weight:800; color:{t['text_primary']}; margin-top:2px;">
                    {topic} {f'at {company}' if mode != MODE_SPECIALIZED else ''}
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:18px;">
                <div style="text-align:right;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; font-weight:600; text-transform:uppercase;">
                        Progress ({current_q.difficulty})
                    </div>
                    <div style="font-size:1.05rem; font-weight:800; color:{t['text_primary']};">
                        Question {curr_idx + 1} of {len(questions)}
                    </div>
                </div>
                <div style="border-left:1px solid {t['border']}; padding-left:18px; text-align:right;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; font-weight:600; text-transform:uppercase;">
                        30-Min Countdown
                    </div>
                    <div style="font-size:1.35rem; font-weight:900; color:{timer_color}; font-family:monospace;">
                        {mins_rem:02d}:{secs_rem:02d}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # Core Panel & Voice HUD
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
                {active_panelist.title}
            </div>
            <div style="font-size:0.78rem; color:{t['text_muted']}; margin-bottom:16px;">
                Focus: {active_panelist.focus_area}
            </div>

            <div id="lm-interviewer-status-text" style="background:{t['surface2']}; border:1px solid {t['border']}; border-radius:30px; padding:8px 16px; font-size:0.88rem; font-weight:700; color:{t['accent']}; display:inline-block; margin-bottom:12px;">
                🎙️ Panel Interviewer Speaking... (Listen Carefully)
            </div>

            <div style="background:#F8FAFC; border:1px dashed {t['border']}; border-radius:10px; padding:12px 14px; font-size:0.80rem; color:{t['text_secondary']}; text-align:left; line-height:1.45;">
                🔒 <strong>Voice-Only Mode:</strong> To simulate actual live interview pressure, questions are asked via voice and are not printed on screen. Listen carefully and respond verbally.
            </div>
        </div>
        """), unsafe_allow_html=True)

        # Trigger TTS Speech synthesis
        speech_text = st.session_state.get("lm_current_speech", current_q.question_text)
        render_voice_synthesis_player(
            text_to_speak=speech_text,
            language=lang,
            interviewer_gender=active_panelist.voice_gender,
            key=f"tts_lm_{curr_idx}_{len(speech_text)}",
        )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        with st.expander(f"👥 Active Panel Members ({len(panel)})", expanded=False):
            for pm in panel:
                active_mark = " (Currently Speaking)" if pm.id == active_panelist.id else ""
                st.markdown(f"- **{pm.avatar_emoji} {pm.name}**: {pm.title}{active_mark}")

    with col_candidate:
        st.markdown(clean_html(f"""
        <div style="margin-bottom:10px;">
            <div style="font-weight:700; font-size:1.05rem; color:{t['text_primary']};">
                Candidate Spoken Response
            </div>
            <div style="font-size:0.82rem; color:{t['text_muted']};">
                Take reasonable thinking time. Speak clearly when you are ready.
            </div>
        </div>
        """), unsafe_allow_html=True)

        render_voice_recognition_widget(prompt_key=f"lm_stt_{curr_idx}", language=lang)

        candidate_answer = st.text_area(
            "Candidate Answer",
            value="",
            placeholder="Your spoken words will appear here automatically via speech recognition. You may review and finalize your answer before submitting...",
            height=130,
            key=f"input_lm_ans_{curr_idx}",
            label_visibility="collapsed",
        )

        # Controls
        col_c1, col_c2, col_c3 = st.columns([1, 1, 1], gap="small")
        with col_c1:
            if st.button("🔁 Repeat Question", use_container_width=True, key=f"btn_repeat_lm_{curr_idx}"):
                st.session_state["lm_current_speech"] = current_q.question_text
                st.rerun()

        with col_c2:
            if st.button("❓ Clarify Question", use_container_width=True, key=f"btn_clarify_lm_{curr_idx}"):
                clarif = generate_last_minute_clarification(current_q.question_text, active_panelist.name)
                st.session_state["lm_current_speech"] = clarif
                st.rerun()

        with col_c3:
            if st.button("🤷 I Don't Know", use_container_width=True, key=f"btn_dont_know_lm_{curr_idx}"):
                current_q = evaluate_last_minute_answer(current_q, "I don't know", topic)
                questions[curr_idx] = current_q
                st.session_state["lm_active_q_idx"] += 1
                if st.session_state["lm_active_q_idx"] < len(questions):
                    next_q = questions[st.session_state["lm_active_q_idx"]]
                    st.session_state["lm_current_speech"] = next_q.question_text
                st.rerun()

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        if st.button("Submit Answer & Next Question ›", type="primary", use_container_width=True, key=f"btn_submit_lm_{curr_idx}"):
            ans_to_eval = candidate_answer.strip() if candidate_answer.strip() else "Unanswered"
            evaluated_q = evaluate_last_minute_answer(current_q, ans_to_eval, topic)
            questions[curr_idx] = evaluated_q
            st.session_state["lm_active_q_idx"] += 1

            if st.session_state["lm_active_q_idx"] < len(questions):
                next_q = questions[st.session_state["lm_active_q_idx"]]
                st.session_state["lm_current_speech"] = f"{evaluated_q.reaction} ... {next_q.question_text}"
            st.rerun()

    # Cancel / Exit Control
    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    with st.expander("Session Controls", expanded=False):
        if st.button("Cancel & Exit Session", key="btn_cancel_lm_live"):
            _clean_lm_session_state()
            st.session_state["lm_view_mode"] = "setup"
            st.rerun()


def _finalize_lm_session(mode: str, topic: str, company: str, lang: str, resume: dict, questions: list, elapsed_sec: int, user_id: str):
    """Synthesizes evaluation, permanently saves the attempt under the user's account, and transitions to report."""
    config = {
        "mode": mode,
        "topic": topic,
        "company": company,
        "language": lang,
        "resume_summary": bool(resume),
    }
    evaluation = synthesize_attempt_evaluation(
        mode=mode,
        topic=topic,
        configuration=config,
        questions=questions,
        actual_time_sec=elapsed_sec,
    )
    attempt_id = save_new_attempt(user_id, evaluation)
    _clean_lm_session_state()
    st.session_state["lm_view_attempt_id"] = attempt_id
    st.session_state["lm_view_mode"] = "report"
    st.rerun()


def _clean_lm_session_state():
    """Removes live session transient state keys."""
    for k in ["lm_questions", "lm_panel", "lm_active_q_idx", "lm_start_time", "lm_current_speech", "lm_session_finalized"]:
        if k in st.session_state:
            del st.session_state[k]

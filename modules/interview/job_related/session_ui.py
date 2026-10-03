"""
AchieveHire — Job Related Live Interview Session HUD
Enforces all operational rules:
1. QUESTIONS ARE NOT DISPLAYED AS READABLE TEXT ON SCREEN DURING LIVE SESSIONS.
2. Interviewer asks questions exclusively through voice.
3. Multi-interviewer rotation with distinct personas & titles.
4. Thinking time without penalties.
5. Clarification requests ('Could you repeat the question?', 'Could you clarify that?').
6. Honest 'I don't know' handling without fake answers.
7. Round 6 closing stage: 'Do you have any questions for us?'
8. Single continuous session requirement.
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
    st.session_state["job_is_clarifying"] = False
    st.session_state["job_round_6_in_closing"] = False


def render_job_live_interview_session(round_num: int):
    """Renders the realistic voice-first live interview room."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id") or "GUEST"

    session = load_job_interview_session(user_id) or {}
    role = session.get("target_role", "Software Engineer")
    company = session.get("target_company", "Google")
    lang = session.get("language", "English")

    cfg = JOB_ROUNDS_CONFIG.get(round_num, JOB_ROUNDS_CONFIG[1])
    max_duration_sec = cfg.get("duration_seconds", 20 * 60)

    # Initialize state if starting new round
    if "job_live_state" not in st.session_state or st.session_state["job_live_state"].round_num != round_num:
        _init_live_round_state(round_num, user_id)

    state: JobInterviewRoundState = st.session_state["job_live_state"]

    # Calculate elapsed and remaining time
    current_time = time.time()
    elapsed_sec = int(current_time - st.session_state.get("job_round_start_time", current_time))
    remaining_sec = max(0, max_duration_sec - elapsed_sec)

    mins_rem = remaining_sec // 60
    secs_rem = remaining_sec % 60
    timer_color = "#DC2626" if remaining_sec < 180 else t["accent"]

    # Auto-conclude if timer hits zero
    if remaining_sec <= 0 and not state.is_completed:
        st.warning("⏱️ Round duration completed. Processing your Performance & Improvement Report...")
        _finalize_round(round_num, user_id, elapsed_sec, role, company, lang)
        return

    # Check if all questions are finished
    total_q = len(state.questions_list)
    curr_idx = state.active_question_index

    # ── ROUND 6 CLOSING STAGE: 'Do you have any questions for us?' ───────────
    if round_num == 6 and curr_idx >= total_q and not state.candidate_asked_closing_question:
        _render_round_6_closing_stage(state, t, role, company, lang, user_id, elapsed_sec)
        return

    if curr_idx >= total_q:
        _finalize_round(round_num, user_id, elapsed_sec, role, company, lang)
        return

    current_q: JobQuestionRecord = state.questions_list[curr_idx]
    active_panelist = next((p for p in state.panel_members if p.id == current_q.interviewer_id), state.panel_members[0])

    # ── Top HUD: Navigation, Role & Timer ─────────────────────────────────────
    st.markdown(clean_html(f"""
    <div style="max-width:940px; margin: 12px auto 16px; padding: 0 16px;">
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
                    <div style="font-size:1.35rem; font-weight:900; color:{timer_color}; font-family:monospace;">
                        {mins_rem:02d}:{secs_rem:02d}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # ── Core Live Room Canvas (Audio synthesis + Interviewer Voice Indicator) ─
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
                Department: {active_panelist.department}
            </div>
            
            <div id="job-interviewer-status-text" style="background:{t['surface2']}; border:1px solid {t['border']}; border-radius:30px; padding:8px 16px; font-size:0.88rem; font-weight:700; color:{t['accent']}; display:inline-block; margin-bottom:12px;">
                🎙️ Interviewer Speaking... (Listen Carefully)
            </div>

            <div style="background:#F8FAFC; border:1px dashed {t['border']}; border-radius:10px; padding:12px 14px; font-size:0.80rem; color:{t['text_secondary']}; text-align:left; line-height:1.45;">
                🔒 <strong>Voice-Only Mode Active:</strong> Questions are asked verbally to simulate realistic interviews. Questions will not be displayed on-screen until the post-round report.
            </div>
        </div>
        """), unsafe_allow_html=True)

        # Trigger TTS Speech synthesis via components.html
        speech_text = st.session_state.get("job_current_speech_text", current_q.question_text)
        render_voice_synthesis_player(
            text_to_speak=speech_text,
            language=lang,
            interviewer_gender=active_panelist.voice_gender,
            key=f"tts_q_{curr_idx}_{len(speech_text)}",
        )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        # Panel Member Roster
        with st.expander(f"👥 Panel Members in this Round ({len(state.panel_members)})", expanded=False):
            for pm in state.panel_members:
                active_mark = " (Currently Speaking)" if pm.id == active_panelist.id else ""
                st.markdown(f"- **{pm.avatar_emoji} {pm.name}**: {pm.title}{active_mark}")

    # ── Candidate Interaction Side (Microphone + Response Submission) ─────────
    with col_candidate:
        st.markdown(clean_html(f"""
        <div style="margin-bottom:10px;">
            <div style="font-weight:700; font-size:1.05rem; color:{t['text_primary']};">
                Your Spoken Response
            </div>
            <div style="font-size:0.82rem; color:{t['text_muted']};">
                Take your time to think. Speak clearly into your microphone when ready.
            </div>
        </div>
        """), unsafe_allow_html=True)

        # Audio Recognition Widget
        render_voice_recognition_widget(prompt_key=f"stt_{curr_idx}", language=lang)

        # Candidate Answer Capture Box
        user_response = st.text_area(
            "Candidate Answer",
            value="",
            placeholder="Your spoken words will appear here automatically via speech-to-text. You may also adjust or finalize your thoughts before submitting...",
            height=130,
            key=f"input_candidate_ans_{curr_idx}",
            label_visibility="collapsed",
        )

        # Candidate Clarification & Option Buttons
        col_opt1, col_opt2, col_opt3 = st.columns([1, 1, 1], gap="small")
        with col_opt1:
            if st.button("🔁 Repeat Question", use_container_width=True, key=f"btn_repeat_q_{curr_idx}"):
                st.session_state["job_current_speech_text"] = current_q.question_text
                st.rerun()

        with col_opt2:
            if st.button("❓ Clarify Question", use_container_width=True, key=f"btn_clarify_q_{curr_idx}"):
                clarification = generate_clarification_response(current_q.question_text, lang, active_panelist.name)
                st.session_state["job_current_speech_text"] = clarification
                st.session_state["job_is_clarifying"] = True
                st.rerun()

        with col_opt3:
            if st.button("🤷 I Don't Know", use_container_width=True, key=f"btn_dont_know_{curr_idx}"):
                # Mark honestly as unanswered
                current_q = evaluate_candidate_answer(current_q, "I don't know", lang, role, company)
                state.questions_list[curr_idx] = current_q
                state.active_question_index += 1
                if state.active_question_index < len(state.questions_list):
                    next_q = state.questions_list[state.active_question_index]
                    st.session_state["job_current_speech_text"] = next_q.question_text
                st.rerun()

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        # Submit Answer Button
        if st.button("Submit Answer & Next ›", type="primary", use_container_width=True, key=f"btn_submit_ans_{curr_idx}"):
            ans_to_evaluate = user_response.strip() if user_response.strip() else "Unanswered"
            evaluated_q = evaluate_candidate_answer(current_q, ans_to_evaluate, lang, role, company)
            state.questions_list[curr_idx] = evaluated_q
            state.active_question_index += 1

            if state.active_question_index < len(state.questions_list):
                next_q = state.questions_list[state.active_question_index]
                # Prepend interviewer reaction to next question audio
                combined_speech = f"{evaluated_q.reaction} ... {next_q.question_text}"
                st.session_state["job_current_speech_text"] = combined_speech
            st.rerun()

    # ── Bottom Safety Exit & Cancel Warning ──────────────────────────────────
    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    with st.expander("⚠️ Session Controls & Emergency Exit", expanded=False):
        st.markdown(
            "**Important Rule:** Once started, a round must be completed in the same continuous session. "
            "If you leave or stop midway, that round will be cancelled and no marks will be calculated."
        )
        if st.button("Cancel & Exit This Round", key="btn_cancel_round_action"):
            del st.session_state["job_live_state"]
            st.session_state["job_view_mode"] = "setup"
            st.rerun()


def _render_round_6_closing_stage(state, t, role, company, lang, user_id, elapsed_sec):
    """Handles the realistic Round 6 closing stage: 'Do you have any questions for us?'."""
    lead_panelist = state.panel_members[0]

    st.markdown(clean_html(f"""
    <div style="max-width:820px; margin: 20px auto; padding: 0 16px;">
        <div style="background:{t['surface']}; border:2px solid {t['accent']}; border-radius:16px; padding:28px; box-shadow:{t['card_shadow']}; text-align:center;">
            <div style="font-size:3rem; margin-bottom:8px;">
                🤝
            </div>
            <div style="font-size:0.85rem; font-weight:700; color:{t['accent']}; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:4px;">
                Round 6 Final Stage · Executive Closing
            </div>
            <h2 style="font-size:1.75rem; font-weight:800; color:{t['text_primary']}; margin:0 0 10px;">
                “Do you have any questions for us?”
            </h2>
            <p style="font-size:0.98rem; color:{t['text_secondary']}; max-width:640px; margin: 0 auto 20px; line-height:1.6;">
                In executive interviews at {company}, asking thoughtful questions about team culture, technical vision,
                or operational priorities demonstrates your strategic preparation and engagement.
            </p>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # Audio synthesis prompt
    closing_prompt = "Do you have any questions for us?" if lang == "English" else ("क्या आपके पास हमारे लिए कोई प्रश्न हैं?" if lang == "Hindi" else "Do you have any questions for us?")
    render_voice_synthesis_player(text_to_speak=closing_prompt, language=lang, key="r6_closing_prompt")

    st.markdown("<div style='max-width:820px; margin: 0 auto; padding: 0 16px;'>", unsafe_allow_html=True)
    candidate_q = st.text_input(
        "Ask the Executive Panel a Question:",
        placeholder="e.g. How does the engineering team at Google balance rapid feature releases with architectural stability?",
        key="r6_closing_cand_question",
    )

    col_ask, col_conclude = st.columns([1, 1], gap="medium")
    with col_ask:
        if st.button("Ask Panel & Hear Response", type="primary", use_container_width=True, key="btn_ask_panel_r6"):
            if candidate_q.strip():
                resp = generate_closing_qa_response(candidate_q, company, role, lang, lead_panelist)
                state.candidate_asked_closing_question = True
                state.closing_candidate_question = candidate_q
                state.closing_panel_response = resp
                st.session_state["job_current_speech_text"] = resp
                st.rerun()
            else:
                st.warning("Please type or speak a question to ask the panel.")

    with col_conclude:
        if st.button("Formally Conclude Interview & View Report ›", use_container_width=True, key="btn_conclude_r6"):
            state.candidate_asked_closing_question = True
            _finalize_round(6, user_id, elapsed_sec, role, company, lang)
            return

    if state.candidate_asked_closing_question and state.closing_panel_response:
        st.markdown(clean_html(f"""
        <div style="background:{t['surface2']}; border:1px solid {t['accent']}; border-radius:12px; padding:18px 22px; margin-top:20px;">
            <div style="font-weight:700; color:{t['accent']}; font-size:0.95rem; margin-bottom:6px;">
                Executive Panel Response:
            </div>
            <div style="font-size:0.95rem; color:{t['text_primary']}; line-height:1.6;">
                {state.closing_panel_response}
            </div>
        </div>
        """), unsafe_allow_html=True)

        if st.button("Proceed to Overall Performance & Improvement Report ›", type="primary", use_container_width=True, key="btn_finish_r6_overall"):
            _finalize_round(6, user_id, elapsed_sec, role, company, lang)
            return

    st.markdown("</div>", unsafe_allow_html=True)


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

    # Clean up live state
    del st.session_state["job_live_state"]
    st.session_state["job_view_mode"] = "report"
    st.session_state["job_report_round"] = round_num
    st.rerun()

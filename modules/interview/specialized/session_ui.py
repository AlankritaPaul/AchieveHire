"""
AchieveHire — Specialized Interview Live Session UI
Conducts the live conversational technical interview session.
Strictly follows the rule: Questions are spoken by voice and NEVER displayed as text on screen.
"""

import time
import datetime
import streamlit as st
from modules.landing.ui import clean_html
from modules.interview.specialized.models import (
    ROUNDS_CONFIG,
    QuestionItem,
    QuestionEvaluation,
)
from modules.interview.specialized.questions_bank import get_specialized_questions
from modules.interview.specialized.engine import evaluate_response, compute_round_result
from modules.interview.specialized.storage import (
    record_round_completion,
    record_round_cancellation,
    load_specialized_progress,
)
from modules.interview.specialized.report_generator import build_overall_specialized_report
from modules.interview.specialized.audio_ui import (
    render_voice_synthesis_player,
    render_voice_recognition_widget,
    render_audio_waveform_hud,
)


def init_specialized_session(specialization: str, language: str, interviewer_gender: str, round_num: int):
    """Initializes live session variables in st.session_state."""
    round_cfg = ROUNDS_CONFIG.get(round_num, ROUNDS_CONFIG[1])
    questions = get_specialized_questions(
        specialization=specialization,
        round_num=round_num,
        language=language,
        count=round_cfg["target_questions_count"],
    )

    st.session_state["spec_sess_active"] = True
    st.session_state["spec_sess_specialization"] = specialization
    st.session_state["spec_sess_language"] = language
    st.session_state["spec_sess_interviewer_gender"] = interviewer_gender
    st.session_state["spec_sess_round_num"] = round_num
    st.session_state["spec_sess_questions"] = questions
    st.session_state["spec_sess_current_q_idx"] = 0
    st.session_state["spec_sess_evaluations"] = []
    st.session_state["spec_sess_start_time"] = time.time()
    st.session_state["spec_sess_time_allowed_sec"] = round_cfg["duration_seconds"]
    st.session_state["spec_sess_status"] = "speaking"  # "speaking", "listening", "evaluating", "reacting"
    st.session_state["spec_sess_last_reaction"] = ""
    st.session_state["spec_sess_user_input"] = ""


def render_specialized_session(t: dict, on_complete_round, on_cancel_session):
    """Renders the live interview interface with voice synthesis, timer, and question masking."""
    if not st.session_state.get("spec_sess_active"):
        st.warning("No active interview session found.")
        return

    specialization = st.session_state["spec_sess_specialization"]
    language = st.session_state["spec_sess_language"]
    gender = st.session_state["spec_sess_interviewer_gender"]
    round_num = st.session_state["spec_sess_round_num"]
    questions = st.session_state["spec_sess_questions"]
    q_idx = st.session_state["spec_sess_current_q_idx"]
    round_cfg = ROUNDS_CONFIG.get(round_num, ROUNDS_CONFIG[1])
    time_allowed = st.session_state["spec_sess_time_allowed_sec"]
    start_time = st.session_state["spec_sess_start_time"]

    # Calculate remaining time
    elapsed = int(time.time() - start_time)
    remaining_sec = max(0, time_allowed - elapsed)
    rem_min, rem_s = remaining_sec // 60, remaining_sec % 60
    time_str = f"{rem_min:02d}:{rem_s:02d}"

    # Check for timer expiration
    if remaining_sec <= 0 and q_idx < len(questions):
        st.warning("⏱️ Round time limit reached! Concluding session safely...")
        _finalize_round(specialization, language, gender, round_num, elapsed, on_complete_round)
        st.rerun()
        return

    # Check if all questions completed
    if q_idx >= len(questions):
        _finalize_round(specialization, language, gender, round_num, elapsed, on_complete_round)
        st.rerun()
        return

    current_q: QuestionItem = questions[q_idx]
    q_spoken_text = current_q.get_text(language)
    interviewer_name = "David" if gender == "male" else "Sarah"
    interviewer_icon = "👨‍💼" if gender == "male" else "👩‍💼"

    # 1. Top Header: Branding, Session Badges, Timer, Exit
    st.markdown(clean_html(f"""
    <div style="max-width:980px; margin: 0 auto 20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-bottom:1px solid {t['border']}; padding-bottom:12px;">
            <div>
                <div style="font-family:'Cinzel Decorative', Georgia, serif; font-size:1.35rem; font-weight:800;">
                    <span style="color:{t['brand_ascend_color']};">Achieve</span><span style="color:{t['brand_career_color']};">Hire</span>
                </div>
                <div style="font-size:0.80rem; color:{t['text_muted']}; font-style:italic;">Better Preparation. Stronger Presentation.</div>
            </div>
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                <span style="background:{t['surface2']}; border:1px solid {t['border']}; padding:6px 14px; border-radius:50px; font-size:0.84rem; font-weight:700; color:{t['text_primary']};">
                    🎯 {specialization}
                </span>
                <span style="background:{t['surface2']}; border:1px solid {t['border']}; padding:6px 14px; border-radius:50px; font-size:0.84rem; font-weight:700; color:{t['text_primary']};">
                    {round_cfg['badge_icon']} {round_cfg['name']}
                </span>
                <span style="background:{t['surface2']}; border:1.5px solid {round_cfg['color']}; padding:6px 16px; border-radius:50px; font-size:0.92rem; font-family:monospace; font-weight:800; color:{round_cfg['color']};">
                    ⏱️ {time_str} Remaining
                </span>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # 2. Main Interviewer Stage (Questions are NEVER rendered as readable text!)
    col_hud, col_actions = st.columns([62, 38], gap="large")

    with col_hud:
        with st.container(border=True):
            st.markdown(clean_html(f"""
            <div style="text-align:center; padding: 20px 10px 14px;">
                <div style="font-size:3.8rem; margin-bottom:6px;">
                    {interviewer_icon}
                </div>
                <div style="font-size:1.25rem; font-weight:800; color:{t['text_primary']};">
                    {interviewer_name} · Lead Technical Interviewer
                </div>
                <div style="font-size:0.88rem; color:{t['text_muted']}; margin-top:2px;">
                    Conversing in <strong>{language}</strong>
                </div>

                <!-- Live Status Text (Updated dynamically by Web Speech Synthesis) -->
                <div id="ac-interviewer-status-text" style="display:inline-block; background:{t['surface2']}; border:1px solid {t['border']}; color:{t['text_primary']}; font-weight:700; font-size:0.90rem; padding:6px 18px; border-radius:50px; margin: 16px auto 8px;">
                    🎙️ Interviewer Speaking... (Listen Carefully)
                </div>
            </div>
            """), unsafe_allow_html=True)

            # Audio Waveform HUD
            render_audio_waveform_hud(t, is_speaking=True)

            # Masked Question Notice (Explicit user rule: Do not display question text)
            st.markdown(clean_html(f"""
            <div style="background:{t['surface2']}; border:1px dashed {t['border']}; border-radius:10px; padding:14px; text-align:center; margin: 10px 0;">
                <div style="font-size:0.92rem; font-weight:700; color:{t['text_primary']};">
                    🔒 Question Masked (Live Audio Mode)
                </div>
                <div style="font-size:0.82rem; color:{t['text_muted']}; margin-top:4px;">
                    Listen carefully to the interviewer's voice. Questions will be revealed in the final report after this round concludes.
                </div>
            </div>
            """), unsafe_allow_html=True)

            # Speak Question via Web Speech Synthesis
            render_voice_synthesis_player(
                text_to_speak=q_spoken_text,
                language=language,
                interviewer_gender=gender,
                key=f"tts_q_{q_idx}",
            )

    with col_actions:
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-bottom:8px;'>Question {q_idx + 1} of {len(questions)}</h3>", unsafe_allow_html=True)
        
        # Progress Bar
        progress_val = min(1.0, max(0.0, (q_idx) / float(len(questions))))
        st.progress(progress_val)

        with st.container(border=True):
            st.markdown(f"<div style='font-weight:700; font-size:0.92rem; color:{t['text_primary']}; margin-bottom:6px;'>Your Spoken / Recorded Answer:</div>", unsafe_allow_html=True)

            # Voice Recognition component (STT)
            render_voice_recognition_widget(
                prompt_key=f"rec_widget_{q_idx}",
                language=language,
            )

            # Interactive answer box
            user_response = st.text_area(
                "Verbal Answer Transcript",
                value=st.session_state.get("spec_sess_user_input", ""),
                height=110,
                placeholder="Speak using the microphone above, or type your answer here if preferred...",
                key=f"user_ans_input_{q_idx}",
            )

            # Submit Answer
            if st.button("🚀  Submit Answer & Continue", type="primary", use_container_width=True, key=f"btn_submit_ans_{q_idx}"):
                _process_answer(current_q, user_response, language, round_num)
                st.session_state["spec_sess_user_input"] = ""
                st.session_state["spec_sess_current_q_idx"] += 1
                st.rerun()

            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)

            # Auxiliary action buttons
            col_aux1, col_aux2 = st.columns(2)
            with col_aux1:
                if st.button("🔄 Repeat Question", use_container_width=True, key=f"btn_repeat_q_{q_idx}"):
                    # Re-trigger speech synthesis
                    render_voice_synthesis_player(
                        text_to_speak=f"Sure, let me repeat that for you. {q_spoken_text}",
                        language=language,
                        interviewer_gender=gender,
                        key=f"tts_repeat_{q_idx}_{int(time.time())}",
                    )
                    st.info("Repeating question audio...")

            with col_aux2:
                if st.button("❓ I Don't Know / Pass", use_container_width=True, key=f"btn_pass_q_{q_idx}"):
                    _process_answer(current_q, "I do not know the answer to this question.", language, round_num)
                    st.session_state["spec_sess_user_input"] = ""
                    st.session_state["spec_sess_current_q_idx"] += 1
                    st.rerun()

            st.markdown("<hr style='margin:12px 0;'/>", unsafe_allow_html=True)

            # Safe cancellation
            if st.button("⚠️ Cancel & Exit Round", use_container_width=True, key="btn_cancel_spec_round"):
                st.session_state["spec_confirm_cancel_modal"] = True
                st.rerun()

    # Cancel confirmation modal dialog
    if st.session_state.get("spec_confirm_cancel_modal"):
        st.markdown(clean_html(f"""
        <div style="background:{t['surface']}; border:2px solid #EF4444; border-radius:12px; padding:20px; margin-top:20px; box-shadow:0 8px 24px rgba(239,68,68,0.25);">
            <h4 style="color:#EF4444; margin:0 0 8px; font-size:1.15rem; font-weight:800;">⚠️ Confirm Round Cancellation</h4>
            <p style="font-size:0.92rem; color:{t['text_secondary']}; line-height:1.55; margin:0 0 14px;">
                Leaving midway will immediately cancel this round. <strong>No marks, scores, or performance report will be generated.</strong> Partial completion will not be recorded.
            </p>
        </div>
        """), unsafe_allow_html=True)
        c_yes, c_no = st.columns(2)
        with c_yes:
            if st.button("Yes, Cancel Round", type="primary", use_container_width=True, key="btn_confirm_cancel_yes"):
                user_id = st.session_state.get("user_id", "guest")
                record_round_cancellation(user_id, specialization, round_num)
                st.session_state["spec_sess_active"] = False
                st.session_state["spec_confirm_cancel_modal"] = False
                on_cancel_session()
                st.rerun()
        with c_no:
            if st.button("No, Continue Interview", use_container_width=True, key="btn_confirm_cancel_no"):
                st.session_state["spec_confirm_cancel_modal"] = False
                st.rerun()


def _process_answer(question: QuestionItem, user_answer: str, language: str, round_num: int):
    """Evaluates answer, registers evaluation, and speaks interviewer reaction."""
    eval_obj, reaction_text = evaluate_response(question, user_answer, language, round_num)
    st.session_state["spec_sess_evaluations"].append(eval_obj)
    st.session_state["spec_sess_last_reaction"] = reaction_text


def _finalize_round(specialization: str, language: str, gender: str, round_num: int, time_taken_sec: int, on_complete_round):
    """Computes round results, updates persistence, builds overall report if Round 4, and transitions."""
    user_id = st.session_state.get("user_id", "guest")
    evaluations = st.session_state.get("spec_sess_evaluations", [])
    time_allowed = st.session_state.get("spec_sess_time_allowed_sec", 1200)

    round_result = compute_round_result(
        round_num=round_num,
        specialization=specialization,
        language=language,
        interviewer_gender=gender,
        time_allowed_sec=time_allowed,
        time_taken_sec=time_taken_sec,
        evaluations=evaluations,
        completed_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    # Save to user storage
    progress = load_specialized_progress(user_id, specialization)
    progress_results = progress.get("round_results", {})
    progress_results[str(round_num)] = round_result.to_dict()

    overall_report = None
    if round_num == 4 or len(progress_results) == 4:
        overall_report = build_overall_specialized_report(
            user_id=user_id,
            specialization=specialization,
            language=language,
            round_results=progress_results,
        )

    record_round_completion(
        user_id=user_id,
        specialization=specialization,
        round_num=round_num,
        round_result=round_result.to_dict(),
        overall_report=overall_report,
    )

    st.session_state["spec_sess_active"] = False
    st.session_state["spec_viewing_report_round"] = round_num
    st.session_state["spec_viewing_report_data"] = round_result.to_dict()
    st.session_state["spec_viewing_overall_report"] = overall_report
    on_complete_round(round_num, round_result.to_dict(), overall_report)

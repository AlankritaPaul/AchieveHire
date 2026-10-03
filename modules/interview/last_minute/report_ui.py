"""
AchieveHire — Last-Minute Preparation Report UI
Interactive on-screen tabs for:
1. Executive Scorecard & Diagnostics
2. Question-by-Question Evaluation (Recorded vs Model Answer)
3. Performance Radar Chart (with official AchieveHire stamp at bottom)
4. Improvement Roadmap
5. Downloadable Official PDF Report
6. Attempt Progression & Growth Comparison (if multiple attempts exist)
"""

import streamlit as st
import plotly.graph_objects as go
import base64
from pathlib import Path
from typing import Dict, Any, Optional
from modules.landing.ui import THEMES, clean_html
from modules.interview.last_minute.models import EVALUATION_CRITERIA
from modules.interview.last_minute.storage import (
    load_user_attempts,
    get_attempt_by_id,
    get_attempt_comparison_data,
)
from modules.interview.last_minute.report_generator import generate_last_minute_pdf

STAMP_PATH = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "achievehire_official_stamp.png"


def _get_stamp_base64() -> str:
    if STAMP_PATH.exists():
        data = STAMP_PATH.read_bytes()
        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    return ""


def render_last_minute_report(attempt_id: Optional[str] = None):
    """Renders the comprehensive, publication-grade Last-Minute Preparation report."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id") or "GUEST"

    attempts = load_user_attempts(user_id)
    if not attempts:
        st.error("No completed Last-Minute Preparation attempts found.")
        if st.button("Start a Practice Session", key="btn_start_new_first"):
            st.session_state["lm_view_mode"] = "setup"
            st.rerun()
        return

    # Select target attempt (default to latest or specified by ID)
    if attempt_id:
        target_attempt = get_attempt_by_id(user_id, attempt_id) or attempts[-1]
    else:
        target_attempt = attempts[-1]

    # Header Branding
    st.markdown(clean_html(f"""
    <div style="max-width:960px; margin: 16px auto 20px; text-align:center;">
        <div style="font-size:2.1rem; font-weight:900; letter-spacing:-0.03em; color:{t['text_primary']}; margin-bottom:2px;">
            AchieveHire
        </div>
        <div style="font-size:0.98rem; font-weight:600; color:{t['accent']}; letter-spacing:0.04em; margin-bottom:12px;">
            Better Preparation. Stronger Presentation.
        </div>
        <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.80rem; font-weight:700; padding:4px 14px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
            ⚡ 30-Minute Intensive Preparation Audit
        </div>
        <h1 style="font-size:1.8rem; font-weight:800; color:{t['text_primary']}; margin:0 0 6px;">
            {target_attempt.get('topic_title', 'Preparation')} — Attempt #{target_attempt.get('attempt_number', 1)}
        </h1>
        <p style="font-size:0.95rem; color:{t['text_secondary']}; max-width:680px; margin: 0 auto; line-height:1.55;">
            {target_attempt.get('mode', '')} &nbsp;·&nbsp; Completed on {target_attempt.get('completion_date', '')}
        </p>
    </div>
    """), unsafe_allow_html=True)

    tab_summary, tab_breakdown, tab_chart, tab_roadmap, tab_download, tab_compare = st.tabs([
        "📋 Scorecard & Summary",
        "🔍 Question Breakdown",
        "📊 Criteria Radar Chart",
        "💡 Improvement Roadmap",
        "📥 Download PDF Report",
        f"📈 Attempt History & Growth ({len(attempts)})",
    ])

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 1: Scorecard & Summary
    # ─────────────────────────────────────────────────────────────────────────
    with tab_summary:
        score = target_attempt.get("overall_score", 0)
        time_taken = target_attempt.get("actual_time_taken_sec", 0)

        st.markdown(clean_html(f"""
        <div style="max-width:900px; margin: 10px auto;">
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:12px; margin-bottom:20px;">
                <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; text-transform:uppercase; font-weight:700;">Rehearsal Score</div>
                    <div style="font-size:2rem; font-weight:900; color:{t['accent']}; margin-top:4px;">{score}/100</div>
                </div>
                <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; text-transform:uppercase; font-weight:700;">Attempt Number</div>
                    <div style="font-size:1.5rem; font-weight:800; color:{t['text_primary']}; margin-top:8px;">#{target_attempt.get('attempt_number', 1)}</div>
                </div>
                <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; text-transform:uppercase; font-weight:700;">Time Taken</div>
                    <div style="font-size:1.5rem; font-weight:800; color:{t['text_primary']}; margin-top:8px;">{time_taken // 60}m {time_taken % 60}s</div>
                </div>
                <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; text-transform:uppercase; font-weight:700;">Time Limit</div>
                    <div style="font-size:1.5rem; font-weight:800; color:{t['text_muted']}; margin-top:8px;">30 Minutes</div>
                </div>
            </div>

            <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:14px; padding:22px; box-shadow:{t['card_shadow']}; margin-bottom:20px;">
                <h3 style="font-size:1.15rem; font-weight:800; color:{t['text_primary']}; margin:0 0 8px;">
                    Executive Rehearsal Summary
                </h3>
                <p style="font-size:0.95rem; color:{t['text_secondary']}; line-height:1.65; margin:0;">
                    {target_attempt.get('executive_summary', '')}
                </p>
                <div style="font-size:0.80rem; color:{t['text_muted']}; margin-top:12px;">
                    Attempt Identifier: <code>{target_attempt.get('attempt_id', '')}</code>
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        col_b1, col_b2 = st.columns([1, 1], gap="medium")
        with col_b1:
            if st.button("‹ Back to Preparation Setup", use_container_width=True, key="btn_lm_back_setup"):
                st.session_state["lm_view_mode"] = "setup"
                st.rerun()
        with col_b2:
            if st.button("⚡ Start Another Rehearsal Attempt ›", type="primary", use_container_width=True, key="btn_lm_new_attempt"):
                st.session_state["lm_view_mode"] = "setup"
                st.rerun()

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 2: Question Breakdown
    # ─────────────────────────────────────────────────────────────────────────
    with tab_breakdown:
        questions = target_attempt.get("questions", [])
        for idx, q in enumerate(questions, 1):
            cls_name = q.get("classification", "Unanswered")
            badge_color = "#10B981" if cls_name == "Correct" else ("#F59E0B" if "Partially" in cls_name or "Incomplete" in cls_name else "#EF4444")
            u_ans = q.get("user_answer", "") or "Unanswered"

            with st.container(border=True):
                st.markdown(clean_html(f"""
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:8px;">
                    <div>
                        <div style="font-size:0.80rem; font-weight:700; color:{t['accent']}; text-transform:uppercase;">
                            Q{idx} ({q.get('difficulty', '')}) · {q.get('interviewer_name', 'Interviewer')} ({q.get('interviewer_title', '')})
                        </div>
                        <h4 style="font-size:1.05rem; font-weight:800; color:{t['text_primary']}; margin:4px 0 0;">
                            {q.get('question_text', '')}
                        </h4>
                    </div>
                    <span style="background:{badge_color}22; color:{badge_color}; border:1px solid {badge_color}; font-weight:700; font-size:0.80rem; padding:3px 10px; border-radius:50px; flex-shrink:0;">
                        {cls_name}
                    </span>
                </div>

                <div style="background:{t['surface2']}; border:1px solid {t['border']}; border-radius:10px; padding:12px 14px; margin-bottom:10px;">
                    <div style="font-size:0.80rem; font-weight:700; color:{t['text_muted']}; text-transform:uppercase; margin-bottom:4px;">
                        Candidate's Spoken Response
                    </div>
                    <div style="font-size:0.92rem; color:{t['text_primary']}; font-style:italic; line-height:1.5;">
                        "{u_ans}"
                    </div>
                </div>

                <div style="margin-bottom:8px; font-size:0.88rem; color:{t['text_secondary']};">
                    <strong>Diagnostic Feedback:</strong> {q.get('feedback', '')}
                </div>

                <div style="margin-bottom:8px; font-size:0.88rem; color:{t['text_muted']};">
                    <strong>Technical Concept:</strong> {q.get('correct_explanation', '')}
                </div>

                <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:10px; padding:12px 14px; margin-top:8px;">
                    <div style="font-size:0.80rem; font-weight:700; color:#047857; text-transform:uppercase; margin-bottom:3px;">
                        Better Possible Answer (Model Example)
                    </div>
                    <div style="font-size:0.90rem; color:#065F46; line-height:1.5;">
                        {q.get('better_possible_answer', '')}
                    </div>
                </div>
                """), unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 3: Criteria Radar Chart (With Official Stamp at Bottom)
    # ─────────────────────────────────────────────────────────────────────────
    with tab_chart:
        crit_scores = target_attempt.get("criteria_scores", {})
        categories = list(crit_scores.keys())
        values = list(crit_scores.values())

        if categories:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(79, 70, 229, 0.25)',
                line=dict(color='#4F46E5', width=2.5),
                name='Competency Score',
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
                ),
                showlegend=False,
                margin=dict(l=40, r=40, t=30, b=30),
                height=420,
            )
            st.plotly_chart(fig, use_container_width=True)

        stamp_uri = _get_stamp_base64()
        stamp_img_html = f'<img src="{stamp_uri}" style="width:110px; height:110px; object-fit:contain;" alt="Official Stamp" />' if stamp_uri else '<div style="font-weight:900; color:#4F46E5;">★ OFFICIAL AUDIT ★</div>'

        st.markdown(clean_html(f"""
        <div style="max-width:760px; margin: 24px auto 10px; padding: 18px 24px; background:{t['surface']}; border:1px solid {t['border']}; border-radius:14px; box-shadow:{t['card_shadow']}; display:flex; align-items:center; gap:24px;">
            <div style="flex-shrink:0;">
                {stamp_img_html}
            </div>
            <div>
                <div style="font-size:0.80rem; font-weight:700; color:{t['accent']}; text-transform:uppercase; letter-spacing:0.06em;">
                    AchieveHire Verified Intensive Rehearsal
                </div>
                <div style="font-size:1.05rem; font-weight:800; color:{t['text_primary']}; margin:2px 0 4px;">
                    Official Last-Minute Performance Scorecard
                </div>
                <div style="font-size:0.82rem; color:{t['text_secondary']}; line-height:1.5;">
                    Verified diagnostic evaluation generated by the AchieveHire Last-Minute Preparation Simulation Engine.
                    This document serves as an authentic candidate rehearsal record.
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 4: Improvement Roadmap
    # ─────────────────────────────────────────────────────────────────────────
    with tab_roadmap:
        col_w1, col_w2 = st.columns([1, 1], gap="large")
        with col_w1:
            st.markdown(clean_html(f"""
            <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:12px; padding:18px; margin-bottom:16px;">
                <h4 style="font-size:1.05rem; font-weight:800; color:#065F46; margin:0 0 10px;">
                    ✓ What You Did Well
                </h4>
            """), unsafe_allow_html=True)
            for item in target_attempt.get("what_went_well", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(clean_html(f"""
            <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:18px;">
                <h4 style="font-size:1.05rem; font-weight:800; color:#1E40AF; margin:0 0 10px;">
                    🛠️ How to Improve
                </h4>
            """), unsafe_allow_html=True)
            for item in target_attempt.get("how_to_improve", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_w2:
            st.markdown(clean_html(f"""
            <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:12px; padding:18px; margin-bottom:16px;">
                <h4 style="font-size:1.05rem; font-weight:800; color:#991B1B; margin:0 0 10px;">
                    ⚠️ What Needs Improvement
                </h4>
            """), unsafe_allow_html=True)
            for item in target_attempt.get("what_needs_improvement", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(clean_html(f"""
            <div style="background:#FFFBEB; border:1px solid #FDE68A; border-radius:12px; padding:18px;">
                <h4 style="font-size:1.05rem; font-weight:800; color:#92400E; margin:0 0 10px;">
                    🎯 What to Practise Before Your Next Rehearsal
                </h4>
            """), unsafe_allow_html=True)
            for item in target_attempt.get("what_to_practise_next", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 5: Download Official PDF
    # ─────────────────────────────────────────────────────────────────────────
    with tab_download:
        st.markdown(clean_html(f"""
        <div style="max-width:760px; margin: 16px auto; text-align:center;">
            <h3 style="font-size:1.3rem; font-weight:800; color:{t['text_primary']}; margin-bottom:6px;">
                Export Official Last-Minute Preparation Report
            </h3>
            <p style="font-size:0.92rem; color:{t['text_secondary']}; margin-bottom:20px;">
                Download a clean, publication-grade PDF report containing your complete 30-minute diagnostic scorecard,
                transcribed questions, model answers, and official AchieveHire audit stamp.
            </p>
        </div>
        """), unsafe_allow_html=True)

        pdf_bytes = generate_last_minute_pdf(target_attempt)
        fname = f"AchieveHire_LastMinute_{target_attempt.get('topic_title','Prep')}_Attempt_{target_attempt.get('attempt_number',1)}.pdf".replace(" ", "_")

        st.markdown("<div style='max-width:380px; margin: 0 auto 20px;'>", unsafe_allow_html=True)
        st.download_button(
            label=f"📥 Download Attempt #{target_attempt.get('attempt_number',1)} PDF Report",
            data=pdf_bytes,
            file_name=fname,
            mime="application/pdf",
            type="primary",
            use_container_width=True,
            key=f"dl_pdf_lm_{target_attempt.get('attempt_id')}",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 6: Attempt History & Growth Comparison
    # ─────────────────────────────────────────────────────────────────────────
    with tab_compare:
        st.markdown(clean_html(f"""
        <div style="max-width:900px; margin: 10px auto;">
            <h3 style="font-size:1.2rem; font-weight:800; color:{t['text_primary']}; margin-bottom:6px;">
                Permanent Rehearsal Attempt History
            </h3>
            <p style="font-size:0.90rem; color:{t['text_secondary']}; margin-bottom:18px;">
                Every completed rehearsal is stored under your unique User ID. Previous attempts are never overwritten.
            </p>
        </div>
        """), unsafe_allow_html=True)

        if len(attempts) >= 2:
            st.markdown(f"<div style='font-weight:700; font-size:1rem; color:{t['text_primary']}; margin-bottom:6px;'>Score Progression Across Attempts</div>", unsafe_allow_html=True)
            labels = [f"Attempt {a.get('attempt_number', i+1)}: {a.get('topic_title', '')[:16]}" for i, a in enumerate(attempts)]
            scores = [a.get("overall_score", 0) for a in attempts]

            fig_p = go.Figure()
            fig_p.add_trace(go.Scatter(
                x=labels,
                y=scores,
                mode='lines+markers+text',
                text=[f"{s}%" for s in scores],
                textposition='top center',
                line=dict(color='#4F46E5', width=3),
                marker=dict(size=10, color='#4338CA'),
            ))
            fig_p.update_layout(
                yaxis=dict(range=[0, 105], title="Readiness Score (0-100)"),
                margin=dict(l=40, r=40, t=30, b=40),
                height=300,
            )
            st.plotly_chart(fig_p, use_container_width=True)

        # List all past attempts
        for att in reversed(attempts):
            is_active = (att.get("attempt_id") == target_attempt.get("attempt_id"))
            border_c = t['accent'] if is_active else t['border']
            bg_c = t['accent_soft'] if is_active else t['surface']

            with st.container(border=True):
                c_inf, c_act = st.columns([75, 25])
                with c_inf:
                    active_label = " (Viewing Current)" if is_active else ""
                    st.markdown(f"**Attempt #{att.get('attempt_number', 1)} — {att.get('topic_title', 'Preparation')}**{active_label}")
                    st.markdown(f"Score: **{att.get('overall_score', 0)}/100** · {att.get('mode', '')} · {att.get('completion_date', '')}")
                with c_act:
                    if not is_active:
                        if st.button("View This Report", key=f"btn_switch_rep_{att.get('attempt_id')}", use_container_width=True):
                            st.session_state["lm_view_attempt_id"] = att.get("attempt_id")
                            st.rerun()
                    else:
                        st.markdown("<div style='color:#10B981; font-weight:700; font-size:0.85rem; padding-top:8px;'>✓ Active Report</div>", unsafe_allow_html=True)

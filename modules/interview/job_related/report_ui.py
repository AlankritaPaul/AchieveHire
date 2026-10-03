"""
AchieveHire — Job Related Interview Report UI
Interactive on-screen tabs for:
1. Executive Summary & Diagnostic Metrics
2. Question-by-Question Evaluation (Transcribed Answer, Classification, Model Answer)
3. Performance Criteria Chart (with official transparent AchieveHire stamp at bottom)
4. Actionable Improvement Roadmap
5. Downloadable Official PDF Reports (Single Round & Overall 6-Round)
"""

import streamlit as st
import plotly.graph_objects as go
import base64
from pathlib import Path
from typing import Dict, Any, Optional
from modules.landing.ui import THEMES, clean_html
from modules.interview.job_related.models import JOB_ROUNDS_CONFIG, EVALUATION_CRITERIA
from modules.interview.job_related.storage import load_job_interview_session
from modules.interview.job_related.report_generator import (
    generate_job_round_pdf,
    generate_job_overall_pdf,
)

STAMP_PATH = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "achievehire_official_stamp.png"


def _get_stamp_base64() -> str:
    """Returns the base64 encoded data URI of the official circular AchieveHire stamp."""
    if STAMP_PATH.exists():
        data = STAMP_PATH.read_bytes()
        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:image/png;base64,{b64}"
    return ""


def render_job_round_report(round_num: int):
    """Renders the comprehensive, interactive post-round Performance & Improvement Report."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id") or "GUEST"

    session = load_job_interview_session(user_id) or {}
    evals = session.get("round_evaluations", {})
    report_data = evals.get(str(round_num))

    if not report_data:
        st.error(f"No completed evaluation data found for Round {round_num}.")
        if st.button("Return to Setup", key="err_back_setup"):
            st.session_state["job_view_mode"] = "setup"
            st.rerun()
        return

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
            📊 Performance &amp; Improvement Report
        </div>
        <h1 style="font-size:1.8rem; font-weight:800; color:{t['text_primary']}; margin:0 0 6px;">
            {report_data.get('round_name', f'Round {round_num}')} Evaluation
        </h1>
        <p style="font-size:0.98rem; color:{t['text_secondary']}; max-width:680px; margin: 0 auto; line-height:1.55;">
            {session.get('target_role', 'Software Engineer')} &nbsp;·&nbsp; {session.get('target_company', 'Technology Solutions')} &nbsp;·&nbsp; Spoken Language: {session.get('language', 'English')}
        </p>
    </div>
    """), unsafe_allow_html=True)

    tab_summary, tab_breakdown, tab_chart, tab_roadmap, tab_download = st.tabs([
        "📋 Executive Summary",
        "🔍 Question-by-Question Analysis",
        "📊 Criteria Performance Chart",
        "💡 Improvement Roadmap",
        "📥 Download Official PDF",
    ])

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 1: Executive Summary
    # ─────────────────────────────────────────────────────────────────────────
    with tab_summary:
        st.markdown(clean_html(f"""
        <div style="max-width:900px; margin: 10px auto;">
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:12px; margin-bottom:20px;">
                <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; text-transform:uppercase; font-weight:700;">Readiness Score</div>
                    <div style="font-size:2rem; font-weight:900; color:{t['accent']}; margin-top:4px;">{report_data.get('overall_score', 0)}/100</div>
                </div>
                <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; text-transform:uppercase; font-weight:700;">Difficulty</div>
                    <div style="font-size:1.4rem; font-weight:800; color:{t['text_primary']}; margin-top:8px;">{report_data.get('difficulty', 'Moderate')}</div>
                </div>
                <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; text-transform:uppercase; font-weight:700;">Time Taken</div>
                    <div style="font-size:1.4rem; font-weight:800; color:{t['text_primary']}; margin-top:8px;">{report_data.get('actual_time_taken_sec', 0) // 60}m {report_data.get('actual_time_taken_sec', 0) % 60}s</div>
                </div>
                <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:16px; text-align:center;">
                    <div style="font-size:0.75rem; color:{t['text_muted']}; text-transform:uppercase; font-weight:700;">Time Limit</div>
                    <div style="font-size:1.4rem; font-weight:800; color:{t['text_muted']}; margin-top:8px;">{report_data.get('duration_allowed_sec', 0) // 60} Minutes</div>
                </div>
            </div>

            <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:14px; padding:22px; box-shadow:{t['card_shadow']}; margin-bottom:20px;">
                <h3 style="font-size:1.15rem; font-weight:800; color:{t['text_primary']}; margin:0 0 8px;">
                    Diagnostic Executive Summary
                </h3>
                <p style="font-size:0.95rem; color:{t['text_secondary']}; line-height:1.65; margin:0;">
                    {report_data.get('executive_summary', '')}
                </p>
                <div style="font-size:0.80rem; color:{t['text_muted']}; margin-top:12px;">
                    Completed on: {report_data.get('completion_date', '')}
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        col_next1, col_next2 = st.columns([1, 1], gap="medium")
        with col_next1:
            if st.button("‹ Back to Setup & Rounds", use_container_width=True, key="btn_rep_back_setup"):
                st.session_state["job_view_mode"] = "setup"
                st.rerun()

        with col_next2:
            if round_num < 6:
                next_num = round_num + 1
                if st.button(f"Proceed to Round {next_num} ›", type="primary", use_container_width=True, key=f"btn_proceed_r{next_num}"):
                    st.session_state["job_active_round_num"] = next_num
                    st.session_state["job_view_mode"] = "live"
                    st.rerun()
            else:
                if st.button("View Final Overall Report ›", type="primary", use_container_width=True, key="btn_view_overall_rep"):
                    st.session_state["job_view_mode"] = "overall_report"
                    st.rerun()

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 2: Question-by-Question Analysis
    # ─────────────────────────────────────────────────────────────────────────
    with tab_breakdown:
        st.markdown(clean_html(f"""
        <div style="max-width:900px; margin: 10px auto;">
            <p style="color:{t['text_secondary']}; font-size:0.92rem; margin-bottom:16px;">
                Detailed diagnostic audit of every question asked. Clearly distinguishes between your recorded answer,
                the evaluation, and the recommended model answer.
            </p>
        </div>
        """), unsafe_allow_html=True)

        questions = report_data.get("questions", [])
        for idx, q in enumerate(questions, 1):
            cls_name = q.get("classification", "Unanswered")
            badge_color = "#10B981" if cls_name == "Correct" else ("#F59E0B" if "Partially" in cls_name or "Incomplete" in cls_name else "#EF4444")
            u_ans = q.get("user_answer", "") or "Unanswered"

            with st.container(border=True):
                st.markdown(clean_html(f"""
                <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:8px;">
                    <div>
                        <div style="font-size:0.80rem; font-weight:700; color:{t['accent']}; text-transform:uppercase;">
                            Question {idx} · {q.get('interviewer_name', 'Interviewer')} ({q.get('interviewer_title', '')})
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
                        Candidate's Recorded Response
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
    # TAB 3: Performance Criteria Chart (With Official Stamp at Bottom)
    # ─────────────────────────────────────────────────────────────────────────
    with tab_chart:
        crit_scores = report_data.get("criteria_scores", {})
        categories = list(crit_scores.keys())
        values = list(crit_scores.values())

        if categories:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(37, 99, 235, 0.25)',
                line=dict(color='#2563EB', width=2.5),
                name='Criteria Score',
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

        # Official AchieveHire Circular Stamp placed cleanly at the bottom
        stamp_uri = _get_stamp_base64()
        stamp_img_html = f'<img src="{stamp_uri}" style="width:110px; height:110px; object-fit:contain;" alt="Official Stamp" />' if stamp_uri else '<div style="font-weight:900; color:#2563EB;">★ OFFICIAL AUDIT ★</div>'

        st.markdown(clean_html(f"""
        <div style="max-width:760px; margin: 24px auto 10px; padding: 18px 24px; background:{t['surface']}; border:1px solid {t['border']}; border-radius:14px; box-shadow:{t['card_shadow']}; display:flex; align-items:center; gap:24px;">
            <div style="flex-shrink:0;">
                {stamp_img_html}
            </div>
            <div>
                <div style="font-size:0.80rem; font-weight:700; color:{t['accent']}; text-transform:uppercase; letter-spacing:0.06em;">
                    AchieveHire Verified Evaluation
                </div>
                <div style="font-size:1.05rem; font-weight:800; color:{t['text_primary']}; margin:2px 0 4px;">
                    Official Performance &amp; Diagnostic Audit
                </div>
                <div style="font-size:0.82rem; color:{t['text_secondary']}; line-height:1.5;">
                    This radar assessment reflects verified candidate responses analyzed by the AchieveHire Job Related Voice Interview Engine.
                    Serves as an authentic continuous career improvement record.
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 4: Improvement Roadmap
    # ─────────────────────────────────────────────────────────────────────────
    with tab_roadmap:
        st.markdown(clean_html(f"""
        <div style="max-width:900px; margin: 10px auto;">
            <p style="color:{t['text_secondary']}; font-size:0.95rem; margin-bottom:16px;">
                Actionable improvement guidance connected to your specific answers in this round.
            </p>
        </div>
        """), unsafe_allow_html=True)

        col_w1, col_w2 = st.columns([1, 1], gap="large")
        with col_w1:
            st.markdown(clean_html(f"""
            <div style="background:#ECFDF5; border:1px solid #A7F3D0; border-radius:12px; padding:18px; margin-bottom:16px;">
                <h4 style="font-size:1.05rem; font-weight:800; color:#065F46; margin:0 0 10px;">
                    ✓ What You Did Well
                </h4>
            """), unsafe_allow_html=True)
            for item in report_data.get("what_went_well", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(clean_html(f"""
            <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:18px;">
                <h4 style="font-size:1.05rem; font-weight:800; color:#1E40AF; margin:0 0 10px;">
                    🛠️ How to Improve
                </h4>
            """), unsafe_allow_html=True)
            for item in report_data.get("how_to_improve", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_w2:
            st.markdown(clean_html(f"""
            <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:12px; padding:18px; margin-bottom:16px;">
                <h4 style="font-size:1.05rem; font-weight:800; color:#991B1B; margin:0 0 10px;">
                    ⚠️ What Needs Improvement
                </h4>
            """), unsafe_allow_html=True)
            for item in report_data.get("what_needs_improvement", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown(clean_html(f"""
            <div style="background:#FFFBEB; border:1px solid #FDE68A; border-radius:12px; padding:18px;">
                <h4 style="font-size:1.05rem; font-weight:800; color:#92400E; margin:0 0 10px;">
                    🎯 What to Practise Before Next Round
                </h4>
            """), unsafe_allow_html=True)
            for item in report_data.get("what_to_practise_next", []):
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 5: Download Official PDF
    # ─────────────────────────────────────────────────────────────────────────
    with tab_download:
        st.markdown(clean_html(f"""
        <div style="max-width:760px; margin: 16px auto; text-align:center;">
            <h3 style="font-size:1.3rem; font-weight:800; color:{t['text_primary']}; margin-bottom:6px;">
                Export Official Performance &amp; Improvement Document
            </h3>
            <p style="font-size:0.92rem; color:{t['text_secondary']}; margin-bottom:20px;">
                Generate a publication-grade PDF report complete with AchieveHire branding, full question-by-question breakdown,
                criteria evaluation, and official circular audit stamp.
            </p>
        </div>
        """), unsafe_allow_html=True)

        # Build PDF payload
        report_data_augmented = dict(report_data)
        report_data_augmented["target_role"] = session.get("target_role", "Software Engineer")
        report_data_augmented["target_company"] = session.get("target_company", "Technology Solutions")
        report_data_augmented["language"] = session.get("language", "English")

        pdf_bytes = generate_job_round_pdf(report_data_augmented)

        st.markdown("<div style='max-width:360px; margin: 0 auto 20px;'>", unsafe_allow_html=True)
        st.download_button(
            label=f"📥 Download Round {round_num} PDF Report",
            data=pdf_bytes,
            file_name=f"AchieveHire_Job_{session.get('target_role','Role')}_Round_{round_num}_Report.pdf".replace(" ", "_"),
            mime="application/pdf",
            type="primary",
            use_container_width=True,
            key=f"dl_pdf_r{round_num}",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(clean_html(f"""
        <div style="max-width:680px; margin: 0 auto; background:#F8FAFC; border:1px solid {t['border']}; border-radius:10px; padding:14px 18px; text-align:center; font-size:0.82rem; color:{t['text_muted']};">
            🔒 <em>AchieveHire Compliance: This diagnostic report is an authentic evaluation of your live session. In accordance with platform integrity rules, this document does not constitute an external certificate.</em>
        </div>
        """), unsafe_allow_html=True)


def render_job_overall_report():
    """Renders the comprehensive 6-Round Overall Performance & Improvement Report."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    user_id = st.session_state.get("user_id") or "GUEST"

    session = load_job_interview_session(user_id) or {}
    evals = session.get("round_evaluations", {})

    st.markdown(clean_html(f"""
    <div style="max-width:960px; margin: 16px auto 20px; text-align:center;">
        <div style="font-size:2.2rem; font-weight:900; letter-spacing:-0.03em; color:{t['text_primary']}; margin-bottom:2px;">
            AchieveHire
        </div>
        <div style="font-size:1.02rem; font-weight:600; color:{t['accent']}; letter-spacing:0.04em; margin-bottom:14px;">
            Better Preparation. Stronger Presentation.
        </div>
        <div style="display:inline-block; background:#ECFDF5; color:#047857; font-size:0.82rem; font-weight:800; padding:5px 16px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;">
            🏆 6-Round Panel Completed · Overall Audit
        </div>
        <h1 style="font-size:1.95rem; font-weight:800; color:{t['text_primary']}; margin:0 0 6px;">
            Overall Performance &amp; Improvement Report
        </h1>
        <p style="font-size:1.02rem; color:{t['text_secondary']}; max-width:720px; margin: 0 auto; line-height:1.6;">
            {session.get('target_role', 'Software Engineer')} &nbsp;·&nbsp; {session.get('target_company', 'Technology Solutions')} &nbsp;·&nbsp; {session.get('language', 'English')}
        </p>
    </div>
    """), unsafe_allow_html=True)

    # 6-Round Trajectory Chart
    round_labels = [f"R{i}: {JOB_ROUNDS_CONFIG[i]['difficulty']}" for i in range(1, 7)]
    round_scores = [evals.get(str(i), {}).get("overall_score", 0) for i in range(1, 7)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=round_labels,
        y=round_scores,
        mode='lines+markers+text',
        text=[f"{s}%" for s in round_scores],
        textposition='top center',
        line=dict(color='#2563EB', width=3),
        marker=dict(size=10, color='#1D4ED8'),
        name='Readiness Score',
    ))
    fig.update_layout(
        yaxis=dict(range=[0, 105], title="Readiness Score (0-100)"),
        xaxis=dict(title="Progressive Interview Rounds"),
        margin=dict(l=40, r=40, t=30, b=40),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Trajectory Analysis
    col_t1, col_t2 = st.columns([1, 1], gap="large")
    with col_t1:
        with st.container(border=True):
            st.markdown(f"<h4 style='font-size:1.05rem; font-weight:800; color:{t['text_primary']}; margin-bottom:8px;'>Continuous Progression Trajectory</h4>", unsafe_allow_html=True)
            st.markdown(
                f"From foundational introductions in Round 1 through architectural stress-testing in Rounds 4–5 "
                f"and executive Q&A in Round 6, you demonstrated systematic growth in managing ambiguity and articulating "
                f"high-leverage technical decisions for {session.get('target_company', 'your target company')}."
            )

    with col_t2:
        with st.container(border=True):
            st.markdown(f"<h4 style='font-size:1.05rem; font-weight:800; color:{t['text_primary']}; margin-bottom:8px;'>Strategic Recommendations</h4>", unsafe_allow_html=True)
            st.markdown(
                "- Continue grounding your architectural proposals in concrete trade-offs (latency vs. consistency).\n"
                "- Maintain concise, executive-level summaries (under 90 seconds) before diving into deep technical mechanics.\n"
                "- Lead with customer and business impact in enterprise panel discussions."
            )

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # Download Overall PDF
    overall_pdf = generate_job_overall_pdf(session)
    col_dl, col_back = st.columns([1, 1], gap="medium")
    with col_dl:
        st.download_button(
            label="📥 Download Final Overall PDF Report",
            data=overall_pdf,
            file_name=f"AchieveHire_{session.get('target_role','Role')}_Overall_Report.pdf".replace(" ", "_"),
            mime="application/pdf",
            type="primary",
            use_container_width=True,
            key="dl_overall_pdf_btn",
        )
    with col_back:
        if st.button("‹ Back to Interview Setup", use_container_width=True, key="btn_overall_back_setup"):
            st.session_state["job_view_mode"] = "setup"
            st.rerun()

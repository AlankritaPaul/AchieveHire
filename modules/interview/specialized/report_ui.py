"""
AchieveHire — Specialized Interview Report UI
Renders interactive in-app diagnostic reports and provides PDF report downloads.
"""

import streamlit as st
from modules.landing.ui import clean_html
from modules.interview.specialized.models import (
    ROUNDS_CONFIG,
    CLASSIFICATION_BADGES,
)
from modules.interview.specialized.report_generator import (
    generate_round_report_pdf,
    generate_overall_report_pdf,
)


def render_specialized_report_screen(
    t: dict,
    report_data: dict,
    overall_report: dict = None,
    on_next_round=None,
    on_return_overview=None,
):
    """Renders the comprehensive diagnostic performance and improvement report."""
    if not report_data:
        st.warning("No report data available.")
        return

    r_num = report_data.get("round_num", 1)
    r_name = report_data.get("round_name", f"Round {r_num}")
    spec = report_data.get("specialization", "Python")
    lang = report_data.get("language", "English")
    diff = report_data.get("difficulty", "Easy")
    score = report_data.get("overall_score", 0.0)
    t_allowed_min = report_data.get("time_allowed_sec", 1200) // 60
    t_taken_sec = report_data.get("time_taken_sec", 0)
    t_taken_str = f"{t_taken_sec // 60}m {t_taken_sec % 60}s"
    date_str = report_data.get("completed_at", "")
    evaluations = report_data.get("evaluations", [])

    # 1. Header & Official Branding
    st.markdown(clean_html(f"""
    <div style="max-width:980px; margin: 0 auto 24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-bottom:1px solid {t['border']}; padding-bottom:14px; margin-bottom:18px;">
            <div>
                <div style="font-family:'Cinzel Decorative', Georgia, serif; font-size:1.6rem; font-weight:800;">
                    <span style="color:{t['brand_ascend_color']};">Achieve</span><span style="color:{t['brand_career_color']};">Hire</span>
                </div>
                <div style="font-size:0.88rem; color:{t['text_muted']}; font-style:italic;">Better Preparation. Stronger Presentation.</div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="background:{t['accent_soft']}; color:{t['accent']}; font-size:0.86rem; font-weight:700; padding:6px 16px; border-radius:50px;">
                    {r_name} Report
                </span>
            </div>
        </div>

        <!-- Title & Metadata Grid -->
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:14px; margin-bottom:24px;">
            <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:14px; box-shadow:{t['card_shadow']};">
                <div style="font-size:0.80rem; color:{t['text_muted']}; font-weight:600; text-transform:uppercase;">Specialization</div>
                <div style="font-size:1.15rem; font-weight:800; color:{t['text_primary']}; margin-top:2px;">{spec}</div>
            </div>
            <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:14px; box-shadow:{t['card_shadow']};">
                <div style="font-size:0.80rem; color:{t['text_muted']}; font-weight:600; text-transform:uppercase;">Difficulty & Language</div>
                <div style="font-size:1.15rem; font-weight:800; color:{t['text_primary']}; margin-top:2px;">{diff} · {lang}</div>
            </div>
            <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:14px; box-shadow:{t['card_shadow']};">
                <div style="font-size:0.80rem; color:{t['text_muted']}; font-weight:600; text-transform:uppercase;">Time Allowed vs Taken</div>
                <div style="font-size:1.15rem; font-weight:800; color:{t['text_primary']}; margin-top:2px;">{t_taken_str} / {t_allowed_min}m</div>
            </div>
            <div style="background:{t['surface']}; border:1.5px solid {t['accent']}; border-radius:12px; padding:14px; box-shadow:0 4px 16px rgba(79,70,229,0.15);">
                <div style="font-size:0.80rem; color:{t['accent']}; font-weight:700; text-transform:uppercase;">Overall Score</div>
                <div style="font-size:1.45rem; font-weight:900; color:{t['accent']}; margin-top:2px;">{score}%</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # 2. Tabs
    tab_list = ["📋 Question-by-Question Analysis", "📊 Diagnostic Criteria Breakdown", "🚀 Improvement Roadmap"]
    if overall_report or r_num == 4:
        tab_list.append("🌟 4-Round Overall Progress & Introduction Evolution")

    tabs = st.tabs(tab_list)

    # ── TAB 1: Question-by-Question Analysis ────────────────────────────────
    with tabs[0]:
        st.markdown(f"<h3 style='font-size:1.25rem; font-weight:800; color:{t['text_primary']}; margin-bottom:14px;'>Detailed Question-by-Question Audit</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:0.92rem; color:{t['text_secondary']}; margin-bottom:18px;'>Here is the complete audit of questions spoken, your recorded responses, diagnostic breakdown, and recommended model answers:</p>", unsafe_allow_html=True)

        for idx, e in enumerate(evaluations, 1):
            q_text = e.get("question_text", "")
            u_ans = e.get("user_answer", "")
            cls_name = e.get("classification", "Correct")
            q_score = e.get("score", 0.0)
            badge_info = CLASSIFICATION_BADGES.get(cls_name, CLASSIFICATION_BADGES["Correct"])
            good_text = e.get("what_was_good", "N/A")
            missing_text = e.get("what_was_missing", "N/A")
            correct_text = e.get("correct_explanation", "N/A")
            better_text = e.get("better_possible_answer", "N/A")

            with st.expander(f"Question {idx}: {q_text[:70]}... — {badge_info['icon']} {cls_name} ({q_score}/10)", expanded=(idx == 1)):
                st.markdown(f"""
                <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:10px; padding:16px; margin-bottom:12px;">
                    <div style="font-size:1.02rem; font-weight:800; color:{t['text_primary']}; margin-bottom:8px;">
                        Q{idx}: {q_text}
                    </div>
                    <div style="display:inline-block; background:{badge_info['bg']}; color:{badge_info['color']}; border:1px solid {badge_info['color']}; font-weight:700; font-size:0.80rem; padding:3px 10px; border-radius:50px; margin-bottom:12px;">
                        {badge_info['icon']} {cls_name} &nbsp;·&nbsp; Score: {q_score}/10
                    </div>

                    <div style="margin-bottom:12px;">
                        <div style="font-weight:700; font-size:0.88rem; color:{t['text_muted']}; text-transform:uppercase;">Candidate's Recorded Answer:</div>
                        <div style="font-size:0.95rem; color:{t['text_primary']}; background:{t['surface2']}; padding:10px 14px; border-radius:8px; margin-top:4px; font-style:italic;">
                            "{u_ans}"
                        </div>
                    </div>

                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:12px;">
                        <div style="background:#ECFDF5; border:1px solid #10B981; border-radius:8px; padding:10px 14px;">
                            <div style="font-weight:700; font-size:0.82rem; color:#047857;">✅ What Went Well:</div>
                            <div style="font-size:0.88rem; color:#065F46; margin-top:2px;">{good_text}</div>
                        </div>
                        <div style="background:#FFFBEB; border:1px solid #F59E0B; border-radius:8px; padding:10px 14px;">
                            <div style="font-weight:700; font-size:0.82rem; color:#B45309;">⚠️ Areas Missing / Needs Polish:</div>
                            <div style="font-size:0.88rem; color:#92400E; margin-top:2px;">{missing_text}</div>
                        </div>
                    </div>

                    <div style="margin-bottom:10px;">
                        <div style="font-weight:700; font-size:0.84rem; color:{t['text_muted']};">Expected Technical Explanation:</div>
                        <div style="font-size:0.90rem; color:{t['text_secondary']}; margin-top:2px; line-height:1.5;">
                            {correct_text}
                        </div>
                    </div>

                    <div>
                        <div style="font-weight:700; font-size:0.84rem; color:#047857;">Better Possible Answer (Model Example):</div>
                        <div style="font-size:0.90rem; color:#047857; background:#ECFDF5; padding:10px 14px; border-radius:8px; margin-top:3px; font-style:italic; line-height:1.5;">
                            {better_text}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 2: Diagnostic Criteria Breakdown ───────────────────────────────
    with tabs[1]:
        st.markdown(f"<h3 style='font-size:1.25rem; font-weight:800; color:{t['text_primary']}; margin-bottom:14px;'>Performance Breakdown Across Criteria</h3>", unsafe_allow_html=True)
        criteria = report_data.get("criteria_breakdown", {})
        c_names = {
            "technical_correctness": "Technical Correctness & Accuracy",
            "relevance": "Question Relevance & Focus",
            "clarity": "Communication Clarity & Articulation",
            "completeness": "Completeness of Expected Points",
            "conciseness": "Conciseness (Avoiding Rambling)",
            "depth": "Technical Depth & Reasoning",
        }
        for key, label in c_names.items():
            val = criteria.get(key, 75.0)
            col_l, col_v = st.columns([75, 25])
            with col_l:
                st.markdown(f"**{label}**")
                st.progress(min(1.0, val / 100.0))
            with col_v:
                st.markdown(f"<div style='text-align:right; font-weight:800; font-size:1.15rem; color:{t['accent']}; padding-top:4px;'>{val}%</div>", unsafe_allow_html=True)
            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ── TAB 3: Improvement Roadmap ──────────────────────────────────────────
    with tabs[2]:
        st.markdown(f"<h3 style='font-size:1.25rem; font-weight:800; color:{t['text_primary']}; margin-bottom:14px;'>Targeted Improvement Roadmap</h3>", unsafe_allow_html=True)

        well = report_data.get("what_you_did_well", [])
        needs = report_data.get("what_needs_improvement", [])
        how = report_data.get("how_to_improve", [])
        practise = report_data.get("what_to_practise_before_next", [])

        col_imp1, col_imp2 = st.columns(2, gap="medium")
        with col_imp1:
            with st.container(border=True):
                st.markdown("<h4 style='color:#059669; font-size:1.05rem; margin:0 0 10px;'>✅ What You Did Well</h4>", unsafe_allow_html=True)
                for item in well:
                    st.markdown(f"• {item}")
            with st.container(border=True):
                st.markdown("<h4 style='color:#4F46E5; font-size:1.05rem; margin:0 0 10px;'>💡 How to Improve</h4>", unsafe_allow_html=True)
                for item in how:
                    st.markdown(f"• {item}")

        with col_imp2:
            with st.container(border=True):
                st.markdown("<h4 style='color:#D97706; font-size:1.05rem; margin:0 0 10px;'>⚠️ What Needs Improvement</h4>", unsafe_allow_html=True)
                for item in needs:
                    st.markdown(f"• {item}")
            with st.container(border=True):
                st.markdown("<h4 style='color:#8B5CF6; font-size:1.05rem; margin:0 0 10px;'>🎯 What to Practise Before Next Round</h4>", unsafe_allow_html=True)
                for item in practise:
                    st.markdown(f"• {item}")

    # ── TAB 4: Overall 4-Round Report (if available) ─────────────────────────
    if (overall_report or r_num == 4) and len(tabs) > 3:
        with tabs[3]:
            o_data = overall_report if overall_report else {}
            st.markdown(f"<h3 style='font-size:1.25rem; font-weight:800; color:{t['text_primary']}; margin-bottom:14px;'>4-Round Trajectory & Introduction Evolution</h3>", unsafe_allow_html=True)

            intro_c = o_data.get("intro_comparison", {})
            r1_in = intro_c.get("round_1_intro", "N/A")
            r4_in = intro_c.get("round_4_intro", "N/A")
            analysis = intro_c.get("analysis", "")

            st.markdown(clean_html(f"""
            <div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:12px; padding:18px; margin-bottom:20px; box-shadow:{t['card_shadow']};">
                <div style="font-weight:800; font-size:1.1rem; color:{t['text_primary']}; margin-bottom:10px;">
                    🔄 Self-Introduction Comparison: Round 1 (Baseline) vs Round 4 (Final)
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:14px; margin-bottom:12px;">
                    <div style="background:{t['surface2']}; border:1px solid {t['border']}; border-radius:8px; padding:12px;">
                        <div style="font-weight:700; font-size:0.84rem; color:{t['text_muted']};">Round 1 Opening (Baseline):</div>
                        <div style="font-size:0.90rem; color:{t['text_primary']}; margin-top:4px; font-style:italic;">"{r1_in}"</div>
                        <div style="font-weight:700; font-size:0.84rem; color:#4F46E5; margin-top:6px;">Score: {intro_c.get('round_1_score', 0)}/10</div>
                    </div>
                    <div style="background:#ECFDF5; border:1px solid #10B981; border-radius:8px; padding:12px;">
                        <div style="font-weight:700; font-size:0.84rem; color:#047857;">Round 4 Opening (Evolved):</div>
                        <div style="font-size:0.90rem; color:#065F46; margin-top:4px; font-style:italic;">"{r4_in}"</div>
                        <div style="font-weight:700; font-size:0.84rem; color:#10B981; margin-top:6px;">Score: {intro_c.get('round_4_score', 0)}/10</div>
                    </div>
                </div>
                <div style="font-size:0.90rem; color:{t['text_secondary']}; line-height:1.55;">
                    <strong>Evolution Analysis:</strong> {analysis}
                </div>
            </div>
            """), unsafe_allow_html=True)

            recs = o_data.get("final_recommendations", [])
            with st.container(border=True):
                st.markdown("<h4 style='color:#4F46E5; font-size:1.05rem; margin:0 0 10px;'>🏆 Final Career Readiness Recommendations</h4>", unsafe_allow_html=True)
                for r_item in recs:
                    st.markdown(f"• {r_item}")

    st.markdown("<hr style='margin:28px 0 20px;'/>", unsafe_allow_html=True)

    # 3. Action & Download Buttons
    c_act1, c_act2, c_act3 = st.columns([35, 35, 30], gap="medium")

    with c_act1:
        # Download Single Round PDF
        pdf_bytes = generate_round_report_pdf(report_data)
        st.download_button(
            label=f"📥 Download {r_name} Report (PDF)",
            data=pdf_bytes,
            file_name=f"AchieveHire_{spec}_{r_name.replace(' ', '_')}_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
            key=f"btn_dl_round_pdf_{r_num}",
        )

    with c_act2:
        # Download Overall PDF (if completed)
        if overall_report or r_num == 4:
            overall_pdf_bytes = generate_overall_report_pdf(overall_report if overall_report else {})
            st.download_button(
                label="🌟 Download Overall 4-Round Report (PDF)",
                data=overall_pdf_bytes,
                file_name=f"AchieveHire_{spec}_4Round_Overall_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="btn_dl_overall_pdf",
            )
        elif on_next_round and r_num < 4:
            next_r_cfg = ROUNDS_CONFIG.get(r_num + 1)
            if st.button(f"🚀 Proceed to {next_r_cfg['name']}", type="primary", use_container_width=True, key="btn_next_round_action"):
                on_next_round(r_num + 1)
                st.rerun()

    with c_act3:
        if st.button("🏠 Return to Interview Overview", use_container_width=True, key="btn_back_to_spec_overview"):
            if on_return_overview:
                on_return_overview()
            st.rerun()

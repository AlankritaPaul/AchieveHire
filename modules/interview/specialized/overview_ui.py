"""
AchieveHire — Specialized Interview Overview Page
Presents the clear, elegant vertical progression workflow, session rules,
progressive difficulty explanation, and entry points.
"""

import streamlit as st
from modules.landing.ui import clean_html
from modules.interview.specialized.storage import load_specialized_progress


def render_specialized_overview(t: dict, on_start_setup):
    """
    Renders the clean, visually understandable vertical flow overview page.
    """
    user_id = st.session_state.get("user_id", "guest")
    current_spec = st.session_state.get("specialized_selected_domain", "Python")
    progress = load_specialized_progress(user_id, current_spec)
    completed_rounds = progress.get("rounds_completed", [])
    current_unlocked = progress.get("current_unlocked_round", 1)

    # 1. Page Header & AchieveHire Branding
    st.markdown(clean_html(f"""
    <div style="max-width:860px; margin: 0 auto 28px; text-align:center;">
        <div style="font-family:'Cinzel Decorative', Georgia, serif; font-size:1.85rem; font-weight:800; margin-bottom:2px;">
            <span style="color:{t['brand_ascend_color']};">Achieve</span><span style="color:{t['brand_career_color']};">Hire</span>
        </div>
        <div style="font-size:0.92rem; font-weight:600; color:{t['text_muted']}; letter-spacing:0.05em; font-style:italic; margin-bottom:16px;">
            Better Preparation. Stronger Presentation.
        </div>
        <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.82rem; font-weight:700; padding:4px 16px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;">
            Specialized Interview Overview
        </div>
        <h1 style="font-size: clamp(1.8rem, 3.2vw, 2.5rem); font-weight: 800; color:{t['text_primary']}; margin: 0 0 10px;">
            Technical Domain Interview Simulation
        </h1>
        <p style="font-size: 1.05rem; color:{t['text_secondary']}; max-width:720px; margin: 0 auto; line-height: 1.65;">
            A 4-stage progressive technical interview designed to evaluate both deep technical knowledge and verbal communication.
            Each round increases in depth and duration to prepare you for real-world hiring rounds.
        </p>
    </div>
    """), unsafe_allow_html=True)

    # 2. Important Session Note Box
    st.markdown(clean_html(f"""
    <div style="max-width:860px; margin: 0 auto 32px; background:{t['surface']}; border-left: 4.5px solid #F59E0B; border-top: 1px solid {t['border']}; border-right: 1px solid {t['border']}; border-bottom: 1px solid {t['border']}; border-radius: 12px; padding: 18px 22px; box-shadow: {t['card_shadow']};">
        <div style="display:flex; align-items:flex-start; gap:14px;">
            <span style="font-size:1.4rem;">⚠️</span>
            <div>
                <div style="font-weight:800; font-size:1.02rem; color:{t['text_primary']}; margin-bottom:4px;">
                    Important Session Rule
                </div>
                <div style="font-size:0.93rem; color:{t['text_secondary']}; line-height:1.6;">
                    <strong>Once a round starts, it must be completed in the same session.</strong> If you leave or stop midway, that round will be cancelled and no marks or performance will be calculated. Partial completion will not be considered.
                </div>
                <div style="font-size:0.86rem; color:{t['text_muted']}; margin-top:8px;">
                    💡 <em>Note: You do not have to complete all four rounds on the same day. You can complete different rounds on different days at your own pace.</em>
                </div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # 3. Clean Vertical Workflow with Arrows
    st.markdown(clean_html(f"""
    <div style="max-width:680px; margin: 0 auto 36px;">
        <h3 style="font-size:1.22rem; font-weight:800; color:{t['text_primary']}; text-align:center; margin-bottom:20px;">
            Interview Progression Workflow
        </h3>

        <!-- Flow step helper styles -->
        <style>
        .ac-flow-card {{
            background: {t['surface']};
            border: 1.5px solid {t['border']};
            border-radius: 12px;
            padding: 14px 20px;
            text-align: center;
            font-weight: 700;
            font-size: 0.98rem;
            color: {t['text_primary']};
            box-shadow: {t['card_shadow']};
            transition: transform 0.18s ease;
        }}
        .ac-flow-arrow {{
            text-align: center;
            font-size: 1.5rem;
            color: {t['accent']};
            margin: 6px 0;
            line-height: 1;
        }}
        .ac-flow-round {{
            background: {t['surface2']};
            border: 1.5px solid {t['accent']};
            color: {t['text_primary']};
            border-radius: 12px;
            padding: 16px 20px;
            text-align: center;
            font-weight: 800;
            font-size: 1.05rem;
            box-shadow: 0 4px 14px rgba(79,70,229,0.12);
        }}
        .ac-flow-report {{
            background: {t['surface']};
            border: 1px dashed #10B981;
            border-radius: 10px;
            padding: 10px 16px;
            text-align: center;
            font-weight: 600;
            font-size: 0.88rem;
            color: #10B981;
        }}
        .ac-flow-final-report {{
            background: linear-gradient(135deg, {t['accent_soft']}, {t['surface']});
            border: 2px solid {t['accent']};
            border-radius: 14px;
            padding: 18px 24px;
            text-align: center;
            font-weight: 800;
            font-size: 1.12rem;
            color: {t['text_primary']};
            box-shadow: 0 6px 20px rgba(79,70,229,0.20);
        }}
        </style>

        <div class="ac-flow-card">1. Choose Specialization</div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-card">2. Choose Interview Language (English / Hindi / Hinglish)</div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-card">3. Choose Interviewer (Male / Female)</div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-round" style="border-color:#10B981;">
            🟢 Round 1 — Easy — 20 Minutes
            <div style="font-size:0.84rem; font-weight:500; color:{t['text_secondary']}; margin-top:3px;">
                Self-Introduction & Core Fundamentals
            </div>
        </div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-report">📊 Performance & Improvement Report (Round 1)</div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-round" style="border-color:#F59E0B;">
            🟡 Round 2 — Moderate — 30 Minutes
            <div style="font-size:0.84rem; font-weight:500; color:{t['text_secondary']}; margin-top:3px;">
                Technical Depth & Practical Application
            </div>
        </div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-report">📊 Performance & Improvement Report (Round 2)</div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-round" style="border-color:#EA580C;">
            🟠 Round 3 — Hard — 35 Minutes
            <div style="font-size:0.84rem; font-weight:500; color:{t['text_secondary']}; margin-top:3px;">
                Complex Scenarios, Edge Cases & Architecture
            </div>
        </div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-report">📊 Performance & Improvement Report (Round 3)</div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-round" style="border-color:#8B5CF6;">
            🏆 Round 4 — Final — 40 Minutes
            <div style="font-size:0.84rem; font-weight:500; color:{t['text_secondary']}; margin-top:3px;">
                Introduction Evolution, Master Evaluation & Candidate Inquiries
            </div>
        </div>
        <div class="ac-flow-arrow">↓</div>

        <div class="ac-flow-final-report">
            🌟 Overall Performance & Improvement Report
            <div style="font-size:0.86rem; font-weight:500; color:{t['text_secondary']}; margin-top:4px;">
                Comprehensive 4-round progression, strengths, recurring weaknesses & career readiness
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # 4. Action Button
    c_btn1, c_btn2, c_btn3 = st.columns([20, 60, 20])
    with c_btn2:
        btn_label = f"🚀  Proceed to Interview Setup (Round {current_unlocked})"
        if st.button(btn_label, type="primary", use_container_width=True, key="btn_proceed_to_spec_setup"):
            on_start_setup()
            st.rerun()

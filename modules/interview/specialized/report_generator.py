"""
AchieveHire — Specialized Interview Report Engine & PDF Generator
Builds detailed post-round diagnostic reports, final 4-round overall reports
(with Round 1 vs Round 4 Introduction comparison), and pixel-perfect downloadable PDFs.
"""

import io
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from modules.interview.specialized.models import ROUNDS_CONFIG, CLASSIFICATION_BADGES


# ─────────────────────────────────────────────────────────────────────────────
# Overall 4-Round Report Generator
# ─────────────────────────────────────────────────────────────────────────────

def build_overall_specialized_report(
    user_id: str,
    specialization: str,
    language: str,
    round_results: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Constructs a comprehensive 4-round progression summary:
    - Combines rounds 1, 2, 3, 4
    - Compares Round 1 vs Round 4 Introduction
    - Analyzes technical trajectory and communication evolution
    - Provides master strengths, recurring weaknesses, and final recommendations
    """
    r1 = round_results.get("1", {})
    r2 = round_results.get("2", {})
    r3 = round_results.get("3", {})
    r4 = round_results.get("4", {})

    scores = []
    for r in [r1, r2, r3, r4]:
        if r and "overall_score" in r:
            scores.append(r["overall_score"])

    final_aggregate_score = round(sum(scores) / len(scores), 1) if scores else 0.0

    # Extract Introduction from Round 1 and Round 4
    r1_intro_eval = next((e for e in r1.get("evaluations", []) if e.get("is_intro")), None)
    r4_intro_eval = next((e for e in r4.get("evaluations", []) if e.get("is_intro")), None)

    r1_intro_text = r1_intro_eval.get("user_answer", "N/A") if r1_intro_eval else "N/A"
    r4_intro_text = r4_intro_eval.get("user_answer", "N/A") if r4_intro_eval else "N/A"
    r1_intro_score = r1_intro_eval.get("score", 0.0) if r1_intro_eval else 0.0
    r4_intro_score = r4_intro_eval.get("score", 0.0) if r4_intro_eval else 0.0

    intro_comparison = {
        "round_1_intro": r1_intro_text,
        "round_1_score": r1_intro_score,
        "round_4_intro": r4_intro_text,
        "round_4_score": r4_intro_score,
        "score_delta": round(r4_intro_score - r1_intro_score, 1),
        "analysis": (
            "Clear evolution in self-presentation. The final introduction demonstrated greater executive confidence, "
            "sharper technical focus, and clearer architectural impact compared to foundational Round 1."
            if r4_intro_score >= r1_intro_score
            else "Candidate maintained consistent background delivery. Recommend polishing elevator pitch with more quantified metrics."
        ),
    }

    # Aggregate master strengths & recurring areas
    master_strengths = []
    recurring_weaknesses = []

    for r in [r1, r2, r3, r4]:
        if r:
            master_strengths.extend(r.get("summary_strengths", []))
            recurring_weaknesses.extend(r.get("summary_improvements", []))

    # De-duplicate
    master_strengths = list(dict.fromkeys(master_strengths))[:6]
    recurring_weaknesses = list(dict.fromkeys(recurring_weaknesses))[:6]

    total_time_taken = sum(r.get("time_taken_sec", 0) for r in [r1, r2, r3, r4] if r)
    total_time_allowed = sum(r.get("time_allowed_sec", 0) for r in [r1, r2, r3, r4] if r)

    return {
        "user_id": user_id,
        "specialization": specialization,
        "language": language,
        "completed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "final_aggregate_score": final_aggregate_score,
        "total_time_allowed_sec": total_time_allowed,
        "total_time_taken_sec": total_time_taken,
        "rounds_summary": {
            "round_1": {"name": "Round 1 — Easy", "score": r1.get("overall_score", 0.0), "time_sec": r1.get("time_taken_sec", 0)},
            "round_2": {"name": "Round 2 — Moderate", "score": r2.get("overall_score", 0.0), "time_sec": r2.get("time_taken_sec", 0)},
            "round_3": {"name": "Round 3 — Hard", "score": r3.get("overall_score", 0.0), "time_sec": r3.get("time_taken_sec", 0)},
            "round_4": {"name": "Round 4 — Final", "score": r4.get("overall_score", 0.0), "time_sec": r4.get("time_taken_sec", 0)},
        },
        "intro_comparison": intro_comparison,
        "master_strengths": master_strengths,
        "recurring_weaknesses": recurring_weaknesses,
        "final_recommendations": [
            f"Maintain daily practice on high-concurrency and edge-case scenarios in {specialization}.",
            "Structure complex technical explanations using the 'Concept → Mechanism → Production Trade-off' framework.",
            "Consistently time answers to stay between 60 and 90 seconds for optimal conciseness and impact.",
            "Continue refining candidate closing questions to demonstrate deep architectural interest.",
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# PDF Document Generator (ReportLab)
# ─────────────────────────────────────────────────────────────────────────────

def generate_round_report_pdf(report_data: Dict[str, Any]) -> bytes:
    """
    Generates a professional PDF document for a single round's Performance & Improvement Report.
    Adheres strictly to AchieveHire branding, layout rules, and stamp design.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=1,  # Center
    )
    tagline_style = ParagraphStyle(
        'DocTagline',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#D97706'),
        alignment=1,
    )
    section_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
    )
    bold_body = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#0F172A'),
    )

    story = []

    # 1. Header & Official Branding
    story.append(Paragraph("<b>AchieveHire</b>", title_style))
    story.append(Paragraph("Better Preparation. Stronger Presentation.", tagline_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"<b>SPECIALIZED INTERVIEW — PERFORMANCE & IMPROVEMENT REPORT</b>", ParagraphStyle('SubH', parent=title_style, fontSize=11, leading=15, textColor=colors.HexColor('#4F46E5'))))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#E2E8F0'), spaceAfter=14))

    # 2. Metadata Grid
    r_name = report_data.get("round_name", "Round 1 — Easy")
    spec = report_data.get("specialization", "Python")
    lang = report_data.get("language", "English")
    diff = report_data.get("difficulty", "Easy")
    score = report_data.get("overall_score", 0.0)
    t_allowed = report_data.get("time_allowed_sec", 1200) // 60
    t_taken = report_data.get("time_taken_sec", 0)
    t_taken_str = f"{t_taken // 60}m {t_taken % 60}s"
    date_str = report_data.get("completed_at", datetime.datetime.now().strftime("%Y-%m-%d"))

    meta_table_data = [
        [
            Paragraph(f"<b>Technical Specialization:</b> {spec}", body_style),
            Paragraph(f"<b>Round:</b> {r_name} ({diff})", body_style),
        ],
        [
            Paragraph(f"<b>Interview Language:</b> {lang}", body_style),
            Paragraph(f"<b>Completion Date:</b> {date_str}", body_style),
        ],
        [
            Paragraph(f"<b>Time Allowed:</b> {t_allowed} Minutes", body_style),
            Paragraph(f"<b>Actual Time Taken:</b> {t_taken_str}", body_style),
        ],
        [
            Paragraph(f"<b>Overall Round Score:</b> <font color='#4F46E5'><b>{score}%</b></font>", bold_body),
            Paragraph(f"<b>Status:</b> Verified Completed", body_style),
        ],
    ]

    t_meta = Table(meta_table_data, colWidths=[260, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # 3. Question-by-Question Analysis
    story.append(Paragraph("<b>Question-by-Question Diagnostic Analysis</b>", section_heading))
    story.append(Paragraph("Comprehensive audit of each question spoken, user's recorded response, diagnostic findings, and model answers:", body_style))
    story.append(Spacer(1, 8))

    evaluations = report_data.get("evaluations", [])
    for idx, e in enumerate(evaluations, 1):
        q_text = e.get("question_text", "")
        u_ans = e.get("user_answer", "")
        cls_name = e.get("classification", "Correct")
        q_score = e.get("score", 0.0)
        good_text = e.get("what_was_good", "N/A")
        missing_text = e.get("what_was_missing", "N/A")
        correct_text = e.get("correct_explanation", "N/A")
        better_text = e.get("better_possible_answer", "N/A")

        q_table_data = [
            [
                Paragraph(f"<b>Q{idx}: {q_text}</b>", bold_body),
                Paragraph(f"<b>Rating:</b> {q_score}/10 &nbsp;|&nbsp; <b>{cls_name}</b>", ParagraphStyle('R', parent=body_style, alignment=2, textColor=colors.HexColor('#4F46E5'))),
            ],
            [
                Paragraph(f"<b>Candidate's Recorded Answer:</b><br/><i>\"{u_ans}\"</i>", body_style),
                "",
            ],
            [
                Paragraph(f"<b>Diagnostic Feedback:</b><br/>• <b>What Went Well:</b> {good_text}<br/>• <b>Areas Missing / Needs Polish:</b> {missing_text}", body_style),
                "",
            ],
            [
                Paragraph(f"<b>Expected Technical Explanation:</b><br/>{correct_text}", body_style),
                "",
            ],
            [
                Paragraph(f"<b>Better Possible Answer (Model Example):</b><br/><i>{better_text}</i>", ParagraphStyle('M', parent=body_style, textColor=colors.HexColor('#047857'))),
                "",
            ],
        ]

        t_q = Table(q_table_data, colWidths=[400, 130])
        t_q.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('SPAN', (0, 4), (1, 4)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EEF2FF')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFFFFF')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#C7D2FE')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E7FF')),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(KeepTogether([t_q, Spacer(1, 10)]))

    # 4. Improvement Roadmap
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Improvement & Practice Roadmap</b>", section_heading))

    well_items = report_data.get("what_you_did_well", [])
    need_items = report_data.get("what_needs_improvement", [])
    practice_items = report_data.get("what_to_practise_before_next", [])

    imp_table_data = [
        [
            Paragraph("<b>What You Did Well</b>", bold_body),
            Paragraph("<b>What Needs Improvement & Practice</b>", bold_body),
        ],
        [
            Paragraph("<br/>".join([f"• {x}" for x in well_items]) if well_items else "• Strong technical engagement.", body_style),
            Paragraph("<br/>".join([f"• {x}" for x in (need_items + practice_items)]) if (need_items or practice_items) else "• Continue advanced edge-case drills.", body_style),
        ],
    ]

    t_imp = Table(imp_table_data, colWidths=[265, 265])
    t_imp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#ECFDF5')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#FEF3C7')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(t_imp)
    story.append(Spacer(1, 16))

    # 5. Official AchieveHire Branding Stamp (Non-certificate notice)
    stamp_img_path = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "achievehire_official_stamp.png"
    if stamp_img_path.exists():
        stamp_right = RLImage(str(stamp_img_path), width=72, height=72)
    else:
        stamp_right = Paragraph(
            "<font color='#4F46E5'><b>ACHIEVEHIRE</b></font><br/>"
            "<font size='7' color='#D97706'>★ OFFICIAL AUDIT ★</font><br/>"
            f"<font size='7' color='#64748B'>{date_str}</font>",
            ParagraphStyle('Stamp', parent=body_style, alignment=1, fontName='Helvetica-Bold')
        )

    stamp_data = [
        [
            Paragraph(
                "<font size='8' color='#64748B'><b>ACHIEVEHIRE PERFORMANCE AUDIT</b><br/>"
                "This document is an authentic diagnostic assessment generated by the AchieveHire Specialized Interview Simulation Engine. "
                "It serves as a professional improvement record and does not represent an external qualification.</font>",
                body_style
            ),
            stamp_right,
        ]
    ]
    t_stamp = Table(stamp_data, colWidths=[420, 110])
    t_stamp.setStyle(TableStyle([
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
    ]))
    story.append(t_stamp)

    doc.build(story)
    return buf.getvalue()


def generate_overall_report_pdf(overall_data: Dict[str, Any]) -> bytes:
    """
    Generates a professional PDF for the Final 4-Round Overall Performance & Improvement Report.
    Includes Round 1 vs Round 4 Introduction Comparison and master progression analysis.
    """
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=1,
    )
    tagline_style = ParagraphStyle(
        'DocTagline',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#D97706'),
        alignment=1,
    )
    section_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
    )
    bold_body = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#0F172A'),
    )

    story = []

    # 1. Header
    story.append(Paragraph("<b>AchieveHire</b>", title_style))
    story.append(Paragraph("Better Preparation. Stronger Presentation.", tagline_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>SPECIALIZED INTERVIEW — COMPREHENSIVE OVERALL REPORT (4 ROUNDS)</b>", ParagraphStyle('SubH', parent=title_style, fontSize=11, leading=15, textColor=colors.HexColor('#4F46E5'))))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#E2E8F0'), spaceAfter=14))

    # 2. Summary Grid
    spec = overall_data.get("specialization", "Python")
    lang = overall_data.get("language", "English")
    final_score = overall_data.get("final_aggregate_score", 0.0)
    t_tot_sec = overall_data.get("total_time_taken_sec", 0)
    t_tot_str = f"{t_tot_sec // 60}m {t_tot_sec % 60}s"
    date_str = overall_data.get("completed_at", datetime.datetime.now().strftime("%Y-%m-%d"))

    r_summary = overall_data.get("rounds_summary", {})
    if isinstance(r_summary, dict):
        r1_score = r_summary.get("round_1", {}).get("score", 0.0) if isinstance(r_summary.get("round_1"), dict) else 0.0
        r2_score = r_summary.get("round_2", {}).get("score", 0.0) if isinstance(r_summary.get("round_2"), dict) else 0.0
        r3_score = r_summary.get("round_3", {}).get("score", 0.0) if isinstance(r_summary.get("round_3"), dict) else 0.0
        r4_score = r_summary.get("round_4", {}).get("score", 0.0) if isinstance(r_summary.get("round_4"), dict) else 0.0
    elif isinstance(r_summary, list):
        r1_score = next((r.get("score", 0.0) for r in r_summary if isinstance(r, dict) and r.get("round_num") == 1), 0.0)
        r2_score = next((r.get("score", 0.0) for r in r_summary if isinstance(r, dict) and r.get("round_num") == 2), 0.0)
        r3_score = next((r.get("score", 0.0) for r in r_summary if isinstance(r, dict) and r.get("round_num") == 3), 0.0)
        r4_score = next((r.get("score", 0.0) for r in r_summary if isinstance(r, dict) and r.get("round_num") == 4), 0.0)
    else:
        r1_score, r2_score, r3_score, r4_score = 0.0, 0.0, 0.0, 0.0

    summary_grid = [
        [
            Paragraph(f"<b>Technical Specialization:</b> {spec}", body_style),
            Paragraph(f"<b>Final Aggregate Score:</b> <font color='#4F46E5'><b>{final_score}%</b></font>", bold_body),
        ],
        [
            Paragraph(f"<b>Interview Language:</b> {lang}", body_style),
            Paragraph(f"<b>Total Actual Interview Time:</b> {t_tot_str}", body_style),
        ],
        [
            Paragraph(f"<b>All 4 Rounds Verified:</b> Completed", body_style),
            Paragraph(f"<b>Completion Date:</b> {date_str}", body_style),
        ],
    ]
    t_sum = Table(summary_grid, colWidths=[260, 270])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 14))

    # 3. 4-Round Performance Trajectory
    story.append(Paragraph("<b>4-Round Progression & Difficulty Trajectory</b>", section_heading))
    trajectory_data = [
        [
            Paragraph("<b>Round 1 (Easy)</b>", bold_body),
            Paragraph("<b>Round 2 (Moderate)</b>", bold_body),
            Paragraph("<b>Round 3 (Hard)</b>", bold_body),
            Paragraph("<b>Round 4 (Final)</b>", bold_body),
        ],
        [
            Paragraph(f"<font color='#10B981'><b>{r1_score}%</b></font><br/>Fundamentals", body_style),
            Paragraph(f"<font color='#F59E0B'><b>{r2_score}%</b></font><br/>Application", body_style),
            Paragraph(f"<font color='#EA580C'><b>{r3_score}%</b></font><br/>Architecture", body_style),
            Paragraph(f"<font color='#8B5CF6'><b>{r4_score}%</b></font><br/>Comprehensive", body_style),
        ]
    ]
    t_traj = Table(trajectory_data, colWidths=[132, 132, 133, 133])
    t_traj.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EEF2FF')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#FFFFFF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_traj)
    story.append(Spacer(1, 14))

    # 4. Introduction Comparison: Round 1 vs Round 4
    story.append(Paragraph("<b>Candidate Introduction Evolution (Round 1 vs Round 4)</b>", section_heading))
    intro_comp = overall_data.get("intro_comparison", {})
    r1_in = intro_comp.get("round_1_intro", "N/A")
    r4_in = intro_comp.get("round_4_intro", "N/A")
    analysis = intro_comp.get("analysis", "")

    intro_table_data = [
        [
            Paragraph("<b>Round 1 Opening Introduction (Baseline)</b>", bold_body),
            Paragraph("<b>Round 4 Final Introduction (Evolved)</b>", bold_body),
        ],
        [
            Paragraph(f"<i>\"{r1_in}\"</i><br/><br/><b>Score:</b> {intro_comp.get('round_1_score', 0)}/10", body_style),
            Paragraph(f"<i>\"{r4_in}\"</i><br/><br/><b>Score:</b> {intro_comp.get('round_4_score', 0)}/10", body_style),
        ],
        [
            Paragraph(f"<b>Evolution Analysis:</b> {analysis}", body_style),
            "",
        ]
    ]
    t_intro = Table(intro_table_data, colWidths=[265, 265])
    t_intro.setStyle(TableStyle([
        ('SPAN', (0, 2), (1, 2)),
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#ECFDF5')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 14))

    # 5. Master Recommendations
    story.append(Paragraph("<b>Final Career Readiness & Placement Recommendations</b>", section_heading))
    recs = overall_data.get("final_recommendations", [])
    rec_text = "<br/>".join([f"• <b>{r}</b>" for r in recs])
    story.append(Paragraph(rec_text, body_style))
    story.append(Spacer(1, 18))

    # 6. Official Stamp & Disclaimer
    stamp_img_path = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "achievehire_official_stamp.png"
    if stamp_img_path.exists():
        stamp_right = RLImage(str(stamp_img_path), width=72, height=72)
    else:
        stamp_right = Paragraph(
            "<font color='#4F46E5'><b>ACHIEVEHIRE</b></font><br/>"
            "<font size='7' color='#D97706'>★ COMPREHENSIVE ★</font><br/>"
            f"<font size='7' color='#64748B'>{date_str}</font>",
            ParagraphStyle('Stamp2', parent=body_style, alignment=1, fontName='Helvetica-Bold')
        )

    stamp_data = [
        [
            Paragraph(
                "<font size='8' color='#64748B'><b>ACHIEVEHIRE COMPREHENSIVE CAREER AUDIT</b><br/>"
                "This overall report consolidates performance across all 4 rounds of the Specialized Interview. "
                "AchieveHire provides this diagnostic evaluation to accelerate placement readiness.</font>",
                body_style
            ),
            stamp_right,
        ]
    ]
    t_stamp = Table(stamp_data, colWidths=[420, 110])
    t_stamp.setStyle(TableStyle([
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
    ]))
    story.append(t_stamp)

    doc.build(story)
    return buf.getvalue()

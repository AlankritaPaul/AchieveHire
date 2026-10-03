"""
AchieveHire — Job Related Interview Report Generator & PDF Engine
Generates:
1. Single Round Performance & Improvement PDF Report
2. Final Overall 6-Round Performance & Improvement PDF Report
Features:
- Header: AchieveHire / Better Preparation. Stronger Presentation.
- Official AchieveHire Transparent Circular Stamp
- Question-by-Question breakdown (Exact question, candidate answer, classification, model answer)
- Visual performance criteria summary
- Improvement Roadmap (What You Did Well, What Needs Improvement, How to Improve, What to Practise Next)
- Strict rule: NO certificates.
"""

import io
from pathlib import Path
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    Image as RLImage,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

STAMP_PATH = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "achievehire_official_stamp.png"


def generate_job_round_pdf(report_data: Dict[str, Any]) -> bytes:
    """Generates a downloadable PDF for a single round's Performance & Improvement Report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    brand_title = ParagraphStyle('BrandTitle', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=colors.HexColor('#0F172A'), alignment=1)
    brand_sub = ParagraphStyle('BrandSub', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#2563EB'), alignment=1)
    sec_title = ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#1E293B'))
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor('#334155'))
    bold_body = ParagraphStyle('BoldBody', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.HexColor('#1E293B'))

    story = []

    # 1. Header & Branding
    story.append(Paragraph("AchieveHire", brand_title))
    story.append(Paragraph("Better Preparation. Stronger Presentation.", brand_sub))
    story.append(Spacer(1, 8))

    r_name = report_data.get("round_name", f"Round {report_data.get('round_num', 1)}")
    diff = report_data.get("difficulty", "Moderate")
    score = report_data.get("overall_score", 0)

    # 2. Metadata Table
    meta_data = [
        [
            Paragraph(f"<b>Assessment:</b> {r_name} ({diff})", bold_body),
            Paragraph(f"<b>Overall Readiness Score:</b> <font color='#2563EB'><b>{score}/100</b></font>", bold_body),
        ],
        [
            Paragraph(f"<b>Target Role:</b> {report_data.get('target_role', 'Software Engineer')}", body_style),
            Paragraph(f"<b>Target Company:</b> {report_data.get('target_company', 'Technology Solutions')}", body_style),
        ],
        [
            Paragraph(f"<b>Interview Language:</b> {report_data.get('language', 'English')}", body_style),
            Paragraph(f"<b>Completion Date:</b> {report_data.get('completion_date', '')}", body_style),
        ],
        [
            Paragraph(f"<b>Time Allowed:</b> {report_data.get('duration_allowed_sec', 0) // 60} Minutes", body_style),
            Paragraph(f"<b>Actual Time Taken:</b> {report_data.get('actual_time_taken_sec', 0) // 60}m {report_data.get('actual_time_taken_sec', 0) % 60}s", body_style),
        ],
    ]
    t_meta = Table(meta_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # 3. Executive Summary
    story.append(Paragraph("<b>Executive Summary</b>", sec_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph(report_data.get("executive_summary", ""), body_style))
    story.append(Spacer(1, 10))

    # 4. Criteria Breakdown
    story.append(Paragraph("<b>Criteria Performance Scores</b>", sec_title))
    story.append(Spacer(1, 4))

    crit_scores = report_data.get("criteria_scores", {})
    crit_rows = []
    items = list(crit_scores.items())
    for i in range(0, len(items), 3):
        row = []
        for j in range(3):
            if i + j < len(items):
                c_name, c_val = items[i + j]
                row.append(Paragraph(f"<b>{c_name}:</b> {c_val}%", body_style))
            else:
                row.append(Paragraph("", body_style))
        crit_rows.append(row)

    if crit_rows:
        t_crit = Table(crit_rows, colWidths=[180, 180, 180])
        t_crit.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(t_crit)
        story.append(Spacer(1, 10))

    # 5. Question-by-Question Evaluation Table
    story.append(Paragraph("<b>Question-by-Question Evaluation</b>", sec_title))
    story.append(Spacer(1, 4))

    questions = report_data.get("questions", [])
    for idx, q in enumerate(questions, 1):
        q_text = q.get("question_text", "")
        u_ans = q.get("user_answer", "") or "Unanswered"
        cls_name = q.get("classification", "Unanswered")
        better_ans = q.get("better_possible_answer", "")
        exp_text = q.get("correct_explanation", "")

        q_table = [
            [
                Paragraph(f"<b>Q{idx}: {q.get('interviewer_name', 'Interviewer')} ({q.get('interviewer_title', '')})</b>", bold_body),
                Paragraph(f"<b>Classification:</b> <font color='#2563EB'><b>{cls_name}</b></font>", ParagraphStyle('R', parent=bold_body, alignment=2)),
            ],
            [Paragraph(f"<b>Question Asked:</b> {q_text}", body_style), ""],
            [Paragraph(f"<b>Candidate's Answer:</b><br/><i>\"{u_ans}\"</i>", body_style), ""],
            [Paragraph(f"<b>Diagnostic Feedback:</b> {q.get('feedback', '')}", body_style), ""],
            [Paragraph(f"<b>Technical Explanation:</b> {exp_text}", body_style), ""],
            [Paragraph(f"<b>Better Possible Answer (Model Example):</b><br/><font color='#059669'><i>{better_ans}</i></font>", body_style), ""],
        ]
        t_q = Table(q_table, colWidths=[400, 140])
        t_q.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('SPAN', (0, 4), (1, 4)),
            ('SPAN', (0, 5), (1, 5)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EFF6FF')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFFFFF')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#BFDBFE')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DBEAFE')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(KeepTogether([t_q, Spacer(1, 8)]))

    # 6. Improvement Roadmap
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Improvement & Practice Roadmap</b>", sec_title))
    story.append(Spacer(1, 4))

    well_p = "<br/>".join([f"• {x}" for x in report_data.get("what_went_well", [])])
    need_p = "<br/>".join([f"• {x}" for x in report_data.get("what_needs_improvement", [])])
    how_p = "<br/>".join([f"• {x}" for x in report_data.get("how_to_improve", [])])
    next_p = "<br/>".join([f"• {x}" for x in report_data.get("what_to_practise_next", [])])

    imp_table = [
        [Paragraph("<b>What You Did Well</b>", bold_body), Paragraph("<b>What Needs Improvement</b>", bold_body)],
        [Paragraph(well_p, body_style), Paragraph(need_p, body_style)],
        [Paragraph("<b>How to Improve</b>", bold_body), Paragraph("<b>What to Practise Next</b>", bold_body)],
        [Paragraph(how_p, body_style), Paragraph(next_p, body_style)],
    ]
    t_imp = Table(imp_table, colWidths=[270, 270])
    t_imp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#ECFDF5')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#FEF2F2')),
        ('BACKGROUND', (0, 2), (0, 2), colors.HexColor('#EFF6FF')),
        ('BACKGROUND', (1, 2), (1, 2), colors.HexColor('#FFFBEB')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_imp)
    story.append(Spacer(1, 14))

    # 7. Official AchieveHire Circular Stamp & Non-Certificate Notice
    stamp_elem = RLImage(str(STAMP_PATH), width=68, height=68) if STAMP_PATH.exists() else Paragraph("★ OFFICIAL AUDIT ★", bold_body)
    stamp_table_data = [
        [
            Paragraph(
                "<font size='8' color='#64748B'><b>ACHIEVEHIRE OFFICIAL AUDIT RECORD</b><br/>"
                "This performance report is an authentic diagnostic assessment generated by the AchieveHire Job Related Voice Interview Engine. "
                "It serves as an intensive career readiness record. This document does not constitute a certificate.</font>",
                body_style,
            ),
            stamp_elem,
        ]
    ]
    t_stamp = Table(stamp_table_data, colWidths=[440, 100])
    t_stamp.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_stamp)

    doc.build(story)
    return buffer.getvalue()


def generate_job_overall_pdf(session: Dict[str, Any]) -> bytes:
    """Generates the downloadable PDF for the Final 6-Round Overall Performance & Improvement Report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    brand_title = ParagraphStyle('BrandTitle', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=colors.HexColor('#0F172A'), alignment=1)
    brand_sub = ParagraphStyle('BrandSub', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#2563EB'), alignment=1)
    sec_title = ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#1E293B'))
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor('#334155'))
    bold_body = ParagraphStyle('BoldBody', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.HexColor('#1E293B'))

    story = []

    # 1. Header & Branding
    story.append(Paragraph("AchieveHire", brand_title))
    story.append(Paragraph("Better Preparation. Stronger Presentation.", brand_sub))
    story.append(Spacer(1, 8))

    role = session.get("target_role", "Software Engineer")
    company = session.get("target_company", "Google")
    lang = session.get("language", "English")

    evals = session.get("round_evaluations", {})
    scores = [evals[str(r)].get("overall_score", 0) for r in range(1, 7) if str(r) in evals]
    avg_score = round(sum(scores) / max(1, len(scores)), 1) if scores else 0

    # 2. Overall Metadata
    meta_data = [
        [
            Paragraph(f"<b>Comprehensive Assessment:</b> 6-Round Job Interview Panel", bold_body),
            Paragraph(f"<b>Final Aggregate Readiness:</b> <font color='#2563EB'><b>{avg_score}/100</b></font>", bold_body),
        ],
        [
            Paragraph(f"<b>Target Role:</b> {role}", body_style),
            Paragraph(f"<b>Target Company:</b> {company}", body_style),
        ],
        [
            Paragraph(f"<b>Interview Language:</b> {lang}", body_style),
            Paragraph(f"<b>Completed Rounds:</b> {len(scores)} of 6", body_style),
        ],
    ]
    t_meta = Table(meta_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # 3. 6-Round Progression Table
    story.append(Paragraph("<b>6-Round Progression Trajectory</b>", sec_title))
    story.append(Spacer(1, 4))

    prog_rows = [
        [
            Paragraph("<b>Round</b>", bold_body),
            Paragraph("<b>Difficulty</b>", bold_body),
            Paragraph("<b>Panel Composition</b>", bold_body),
            Paragraph("<b>Duration</b>", bold_body),
            Paragraph("<b>Score</b>", bold_body),
        ]
    ]

    from modules.interview.job_related.models import JOB_ROUNDS_CONFIG
    for r_num in range(1, 7):
        cfg = JOB_ROUNDS_CONFIG.get(r_num, {})
        r_eval = evals.get(str(r_num), {})
        r_score = r_eval.get("overall_score", "N/A")
        r_time = f"{r_eval.get('actual_time_taken_sec', 0) // 60}m" if r_eval else f"{cfg.get('duration_minutes')}m (limit)"

        prog_rows.append([
            Paragraph(cfg.get("name", f"Round {r_num}"), body_style),
            Paragraph(cfg.get("difficulty", ""), body_style),
            Paragraph(f"{cfg.get('interviewer_count')} Interviewers", body_style),
            Paragraph(r_time, body_style),
            Paragraph(f"<b>{r_score}/100</b>" if r_score != "N/A" else "Pending", bold_body),
        ])

    t_prog = Table(prog_rows, colWidths=[150, 80, 140, 90, 80])
    t_prog.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EEF2FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_prog)
    story.append(Spacer(1, 12))

    # 4. Master Strengths & Strategic Areas
    story.append(Paragraph("<b>Executive Competency Evaluation</b>", sec_title))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        f"Across all six progressive rounds for the {role} role at {company}, the candidate progressed from initial background "
        "exploration to multi-stakeholder executive panel interrogation. Demonstrated consistent capacity for structured technical reasoning, "
        "resilience under simulated operational outages, and active engagement with senior leadership.",
        body_style,
    ))
    story.append(Spacer(1, 16))

    # 5. Official AchieveHire Circular Stamp
    stamp_elem = RLImage(str(STAMP_PATH), width=72, height=72) if STAMP_PATH.exists() else Paragraph("★ OFFICIAL AUDIT ★", bold_body)
    stamp_table_data = [
        [
            Paragraph(
                "<font size='8' color='#64748B'><b>ACHIEVEHIRE COMPREHENSIVE PERFORMANCE AUDIT</b><br/>"
                "This document records the full 6-round technical and leadership interview progression completed on AchieveHire. "
                "It serves as a permanent readiness portfolio. This document does not constitute a certificate.</font>",
                body_style,
            ),
            stamp_elem,
        ]
    ]
    t_stamp = Table(stamp_table_data, colWidths=[440, 100])
    t_stamp.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_stamp)

    doc.build(story)
    return buffer.getvalue()

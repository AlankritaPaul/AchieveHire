"""
AchieveHire — Last-Minute Preparation Report Generator & PDF Engine
Generates publication-grade PDF reports for 30-minute intensive rehearsals.
Features:
- AchieveHire Branding & Official Stamp
- Attempt ID & Permanent History Tracking
- Question-by-Question Diagnostic Evaluation
- Criteria Performance Breakdown
- Actionable Improvement Roadmap
- Strict rule: ZERO certificates generated.
"""

import io
from pathlib import Path
from typing import Dict, Any, List
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

STAMP_PATH = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "achievehire_official_stamp.png"


def generate_last_minute_pdf(attempt_data: Dict[str, Any]) -> bytes:
    """Generates a downloadable PDF for the 30-minute Last-Minute Preparation session."""
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
    brand_sub = ParagraphStyle('BrandSub', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor('#4F46E5'), alignment=1)
    sec_title = ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#1E293B'))
    body_style = ParagraphStyle('Body', fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor('#334155'))
    bold_body = ParagraphStyle('BoldBody', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.HexColor('#1E293B'))

    story = []

    # 1. Header & Branding
    story.append(Paragraph("AchieveHire", brand_title))
    story.append(Paragraph("Better Preparation. Stronger Presentation.", brand_sub))
    story.append(Spacer(1, 8))

    mode_title = attempt_data.get("mode", "Last-Minute Preparation")
    topic = attempt_data.get("topic_title", "Preparation")
    score = attempt_data.get("overall_score", 0)
    attempt_num = attempt_data.get("attempt_number", 1)

    # 2. Metadata Table
    meta_rows = [
        [
            Paragraph(f"<b>Assessment:</b> {mode_title}", bold_body),
            Paragraph(f"<b>Overall Score:</b> <font color='#4F46E5'><b>{score}/100</b></font>", bold_body),
        ],
        [
            Paragraph(f"<b>Topic / Target Focus:</b> {topic}", body_style),
            Paragraph(f"<b>Completion Date:</b> {attempt_data.get('completion_date', '')}", body_style),
        ],
        [
            Paragraph(f"<b>Time Allowed:</b> 30 Minutes (Fixed)", body_style),
            Paragraph(f"<b>Actual Time Taken:</b> {attempt_data.get('actual_time_taken_sec', 0) // 60}m {attempt_data.get('actual_time_taken_sec', 0) % 60}s", body_style),
        ],
        [
            Paragraph(f"<b>Attempt Identifier:</b> <font face='Courier'>{attempt_data.get('attempt_id', 'N/A')}</font>", body_style),
            Paragraph(f"<b>Session Type:</b> Real-Time Voice Simulation", body_style),
        ],
    ]
    t_meta = Table(meta_rows, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # 3. Executive Summary
    story.append(Paragraph("<b>Executive Summary</b>", sec_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph(attempt_data.get("executive_summary", ""), body_style))
    story.append(Spacer(1, 10))

    # 4. Criteria Performance Scores
    story.append(Paragraph("<b>Criteria Performance Scores</b>", sec_title))
    story.append(Spacer(1, 4))

    crit_scores = attempt_data.get("criteria_scores", {})
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

    questions = attempt_data.get("questions", [])
    for idx, q in enumerate(questions, 1):
        q_text = q.get("question_text", "")
        u_ans = q.get("user_answer", "") or "Unanswered"
        cls_name = q.get("classification", "Unanswered")
        better_ans = q.get("better_possible_answer", "")
        exp_text = q.get("correct_explanation", "")

        q_table = [
            [
                Paragraph(f"<b>Q{idx}: {q.get('interviewer_name', 'Interviewer')} ({q.get('interviewer_title', '')})</b>", bold_body),
                Paragraph(f"<b>Classification:</b> <font color='#4F46E5'><b>{cls_name}</b></font>", ParagraphStyle('R', parent=bold_body, alignment=2)),
            ],
            [Paragraph(f"<b>Question Asked:</b> {q_text}", body_style), ""],
            [Paragraph(f"<b>Candidate's Spoken Response:</b><br/><i>\"{u_ans}\"</i>", body_style), ""],
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
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EEF2FF')),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FFFFFF')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#C7D2FE')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E7FF')),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(KeepTogether([t_q, Spacer(1, 8)]))

    # 6. Improvement Roadmap
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Improvement & Practice Roadmap</b>", sec_title))
    story.append(Spacer(1, 4))

    well_p = "<br/>".join([f"• {x}" for x in attempt_data.get("what_went_well", [])])
    need_p = "<br/>".join([f"• {x}" for x in attempt_data.get("what_needs_improvement", [])])
    how_p = "<br/>".join([f"• {x}" for x in attempt_data.get("how_to_improve", [])])
    next_p = "<br/>".join([f"• {x}" for x in attempt_data.get("what_to_practise_next", [])])

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
                "<font size='8' color='#64748B'><b>ACHIEVEHIRE PERFORMANCE AUDIT</b><br/>"
                "This document is an authentic diagnostic assessment generated by the AchieveHire Last-Minute Preparation Interview Engine. "
                "It serves as a permanent improvement record and does not represent an external certificate.</font>",
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

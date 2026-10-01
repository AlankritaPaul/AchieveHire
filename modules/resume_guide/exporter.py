"""
Export utilities to generate downloadable PDF, DOCX, and TXT resumes from final compiled text.
"""

import io
from typing import Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
import docx
from docx.shared import Pt, Inches, RGBColor

def export_resume_to_pdf(resume_text: str, candidate_title: str = "Updated Resume") -> bytes:
    """Generate a clean, high-quality PDF resume using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "ResumeTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=6
    )
    
    section_heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        "ResumeBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        "ResumeBullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        leftIndent=14,
        firstLineIndent=-10,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=2
    )

    elements = []
    lines = resume_text.split("\n")
    
    is_first_header = True

    for line in lines:
        stripped = line.strip()
        if not stripped:
            elements.append(Spacer(1, 4))
            continue

        # Check if line looks like a major section heading
        is_heading = (
            stripped.isupper() and len(stripped) < 40 and not stripped.startswith("•")
        ) or any(stripped.startswith(prefix) for prefix in [
            "PROFESSIONAL SUMMARY", "WORK EXPERIENCE", "PROJECTS", "TECHNICAL SKILLS",
            "SKILLS", "EDUCATION", "CERTIFICATIONS", "PERSONAL / ADDITIONAL DETAILS"
        ])

        if is_first_header and not is_heading:
            elements.append(Paragraph(stripped, title_style))
            is_first_header = False
            continue

        if is_heading:
            elements.append(Spacer(1, 6))
            elements.append(Paragraph(stripped, section_heading_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=6))
        elif stripped.startswith(("•", "-", "*")):
            clean_b = stripped.lstrip("•-* ").strip()
            # Escape HTML characters for ReportLab Paragraph
            clean_b = clean_b.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            elements.append(Paragraph(f"&bull; {clean_b}", bullet_style))
        else:
            safe_text = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            elements.append(Paragraph(safe_text, body_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def export_resume_to_docx(resume_text: str) -> bytes:
    """Generate a clean Microsoft Word (.docx) resume."""
    doc = docx.Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    lines = resume_text.split("\n")
    is_first = True

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        is_heading = (
            stripped.isupper() and len(stripped) < 40 and not stripped.startswith("•")
        ) or any(stripped.startswith(prefix) for prefix in [
            "PROFESSIONAL SUMMARY", "WORK EXPERIENCE", "PROJECTS", "TECHNICAL SKILLS",
            "SKILLS", "EDUCATION", "CERTIFICATIONS", "PERSONAL / ADDITIONAL DETAILS"
        ])

        if is_first and not is_heading:
            p = doc.add_paragraph()
            run = p.add_run(stripped)
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(26, 54, 93)
            is_first = False
            continue

        if is_heading:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(stripped)
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(43, 108, 176)
        elif stripped.startswith(("•", "-", "*")):
            clean_b = stripped.lstrip("•-* ").strip()
            p = doc.add_paragraph(clean_b, style="List Bullet")
            p.paragraph_format.space_after = Pt(2)
        else:
            p = doc.add_paragraph(stripped)
            p.paragraph_format.space_after = Pt(3)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

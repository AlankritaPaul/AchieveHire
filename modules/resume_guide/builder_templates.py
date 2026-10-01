"""
Resume templates, visual previews, HTML rendering, and PDF generator for 'Create Resume' flow.
Supports 6 distinct templates:
1. Classic
2. Modern
3. Minimal
4. Professional
5. Creative
6. Technical
"""

from typing import Dict, Any, List
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, Image as RLImage

TEMPLATES_INFO = {
    "Classic": {
        "name": "Classic",
        "description": "Timeless, elegant layout with traditional typography and centered headers. Ideal for law, finance, academia, and traditional corporate sectors.",
        "accent_color": "#2C3E50",
        "preview_svg": """
        <div style="border: 2px solid #CBD5E0; border-radius: 8px; padding: 12px; background: #FFFDF9; font-family: Georgia, serif; height: 240px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); cursor: pointer;">
            <div style="text-align: center; border-bottom: 2px solid #2C3E50; padding-bottom: 6px; margin-bottom: 8px;">
                <div style="font-weight: bold; font-size: 14px; color: #1A202C;">JOHN DOE</div>
                <div style="font-size: 8px; color: #718096;">New York, NY • john@email.com • +1-555-0100</div>
            </div>
            <div style="font-size: 9px; font-weight: bold; color: #2C3E50; border-bottom: 1px solid #E2E8F0; margin-top: 6px;">EDUCATION</div>
            <div style="font-size: 7.5px; color: #4A5568; margin-top: 2px;">B.S. in Computer Science — State University (2020)</div>
            <div style="font-size: 9px; font-weight: bold; color: #2C3E50; border-bottom: 1px solid #E2E8F0; margin-top: 6px;">EXPERIENCE</div>
            <div style="font-size: 7.5px; color: #4A5568; margin-top: 2px;">• Software Engineer — TechCorp (2021-Present)</div>
            <div style="font-size: 9px; font-weight: bold; color: #2C3E50; border-bottom: 1px solid #E2E8F0; margin-top: 6px;">DECLARATION & SIGNATURE</div>
            <div style="font-size: 7px; color: #718096; margin-top: 2px;">I hereby declare... Date: ____ Sign: ____</div>
        </div>
        """
    },
    "Modern": {
        "name": "Modern",
        "description": "Contemporary two-tone design with an eye-catching header bar and crisp sans-serif structure. Perfect for tech companies, product teams, and startups.",
        "accent_color": "#2B6CB0",
        "preview_svg": """
        <div style="border: 2px solid #CBD5E0; border-radius: 8px; background: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, sans-serif; height: 240px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); overflow: hidden; cursor: pointer;">
            <div style="background: linear-gradient(135deg, #2B6CB0, #1A365D); color: white; padding: 12px 14px;">
                <div style="font-weight: 700; font-size: 14px;">JOHN DOE</div>
                <div style="font-size: 8.5px; opacity: 0.9;">Target: Software Developer</div>
                <div style="font-size: 7.5px; opacity: 0.75;">john@email.com | +1-555-0100</div>
            </div>
            <div style="padding: 10px;">
                <div style="font-size: 8.5px; font-weight: bold; color: #2B6CB0; text-transform: uppercase;">SKILLS & COMPETENCIES</div>
                <div style="font-size: 7px; color: #4A5568; margin-top: 2px;">Python • JavaScript • SQL • Cloud Architecture</div>
                <div style="font-size: 8.5px; font-weight: bold; color: #2B6CB0; text-transform: uppercase; margin-top: 6px;">WORK EXPERIENCE</div>
                <div style="font-size: 7px; color: #4A5568;">• Led engineering team to build scalable microservices.</div>
                <div style="font-size: 8.5px; font-weight: bold; color: #2B6CB0; text-transform: uppercase; margin-top: 6px;">DECLARATION</div>
                <div style="font-size: 6.5px; color: #718096;">Verified information. Date: ____ Sign: ____</div>
            </div>
        </div>
        """
    },
    "Minimal": {
        "name": "Minimal",
        "description": "Streamlined, clutter-free aesthetics maximizing readability and focus on core accomplishments. Preferred by recruiters who favor simplicity.",
        "accent_color": "#1A202C",
        "preview_svg": """
        <div style="border: 2px solid #CBD5E0; border-radius: 8px; padding: 14px; background: #FFFFFF; font-family: -apple-system, sans-serif; height: 240px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); cursor: pointer;">
            <div style="font-weight: 300; font-size: 15px; color: #1A202C; letter-spacing: 1px;">JOHN DOE</div>
            <div style="font-size: 7.5px; color: #A0AEC0; margin-bottom: 10px;">SOFTWARE DEVELOPER • NEW YORK, NY</div>
            <div style="font-size: 8px; font-weight: 600; color: #2D3748; letter-spacing: 0.5px;">EXPERIENCE</div>
            <div style="font-size: 7px; color: #718096; margin-bottom: 6px;">Senior Developer — Built robust backend data pipelines.</div>
            <div style="font-size: 8px; font-weight: 600; color: #2D3748; letter-spacing: 0.5px;">PROJECTS</div>
            <div style="font-size: 7px; color: #718096; margin-bottom: 6px;">AI Platform — Developed high-scale inference service.</div>
            <div style="font-size: 8px; font-weight: 600; color: #2D3748; letter-spacing: 0.5px;">DECLARATION</div>
            <div style="font-size: 6.5px; color: #A0AEC0;">Date: ________  Signature: ________</div>
        </div>
        """
    },
    "Professional": {
        "name": "Professional",
        "description": "Polished corporate layout featuring structured navy section headings, clean horizontal dividing rules, and balanced multi-column attributes.",
        "accent_color": "#1E3A8A",
        "preview_svg": """
        <div style="border: 2px solid #CBD5E0; border-radius: 8px; padding: 12px; background: #F8FAFC; font-family: 'Segoe UI', Tahoma, sans-serif; height: 240px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); cursor: pointer;">
            <div style="border-left: 4px solid #1E3A8A; padding-left: 8px; margin-bottom: 8px;">
                <div style="font-weight: 700; font-size: 13px; color: #1E3A8A;">JOHN DOE</div>
                <div style="font-size: 7.5px; color: #64748B;">john.doe@email.com | (555) 019-2834</div>
            </div>
            <div style="background: #E2E8F0; padding: 2px 6px; font-weight: bold; font-size: 8px; color: #1E3A8A;">CORE COMPETENCIES</div>
            <div style="font-size: 7px; color: #334155; margin: 3px 0 6px 4px;">Data Structures, Python, REST APIs, Team Leadership</div>
            <div style="background: #E2E8F0; padding: 2px 6px; font-weight: bold; font-size: 8px; color: #1E3A8A;">PROFESSIONAL EXPERIENCE</div>
            <div style="font-size: 7px; color: #334155; margin: 3px 0 6px 4px;">• Architected enterprise workflow automation modules.</div>
            <div style="background: #E2E8F0; padding: 2px 6px; font-weight: bold; font-size: 8px; color: #1E3A8A;">DECLARATION</div>
            <div style="font-size: 6.5px; color: #64748B; margin-top: 2px;">Date: ____________  Signature: ____________</div>
        </div>
        """
    },
    "Creative": {
        "name": "Creative",
        "description": "Distinctive layout with bold teal/emerald highlights, visual badges, and styled section tags. Excellent for designers, front-end engineers, and marketing.",
        "accent_color": "#0D9488",
        "preview_svg": """
        <div style="border: 2px solid #CBD5E0; border-radius: 8px; background: #FFFFFF; font-family: -apple-system, sans-serif; height: 240px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); overflow: hidden; cursor: pointer;">
            <div style="background: #0D9488; color: white; padding: 10px 12px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 800; font-size: 13px;">JOHN DOE</div>
                    <div style="font-size: 7.5px; opacity: 0.9;">Creative & UI/UX Engineer</div>
                </div>
            </div>
            <div style="padding: 10px;">
                <div style="font-size: 8px; font-weight: bold; color: #0D9488; text-transform: uppercase;">HIGHLIGHTED SKILLS</div>
                <div style="display: flex; gap: 4px; margin: 3px 0;">
                    <span style="background: #CCFBF1; color: #0F766E; font-size: 6.5px; padding: 1px 4px; border-radius: 4px;">Figma</span>
                    <span style="background: #CCFBF1; color: #0F766E; font-size: 6.5px; padding: 1px 4px; border-radius: 4px;">React</span>
                    <span style="background: #CCFBF1; color: #0F766E; font-size: 6.5px; padding: 1px 4px; border-radius: 4px;">CSS3</span>
                </div>
                <div style="font-size: 8px; font-weight: bold; color: #0D9488; text-transform: uppercase; margin-top: 6px;">KEY PROJECTS</div>
                <div style="font-size: 7px; color: #374151;">• Designed interactive design system for mobile app.</div>
                <div style="font-size: 8px; font-weight: bold; color: #0D9488; text-transform: uppercase; margin-top: 6px;">DECLARATION</div>
                <div style="font-size: 6.5px; color: #6B7280;">Date: ________ Signature: ________</div>
            </div>
        </div>
        """
    },
    "Technical": {
        "name": "Technical",
        "description": "Engineered for developers, engineers, and researchers. Prominently categorizes languages, frameworks, developer tools, algorithms, and GitHub links.",
        "accent_color": "#0F172A",
        "preview_svg": """
        <div style="border: 2px solid #CBD5E0; border-radius: 8px; padding: 12px; background: #0F172A; color: #F8FAFC; font-family: 'Consolas', 'Courier New', monospace; height: 240px; box-shadow: 0 2px 4px rgba(0,0,0,0.06); cursor: pointer;">
            <div style="border-bottom: 1px solid #334155; padding-bottom: 6px; margin-bottom: 6px;">
                <div style="font-weight: bold; font-size: 13px; color: #38BDF8;">&gt; JOHN_DOE</div>
                <div style="font-size: 7.5px; color: #94A3B8;">dev@terminal.sh | github.com/johndoe</div>
            </div>
            <div style="font-size: 8px; font-weight: bold; color: #34D399;">$ TECHNICAL_STACK</div>
            <div style="font-size: 7px; color: #CBD5E1; margin-bottom: 6px;">Languages: Python, Go, C++, SQL | Tools: Docker, Git</div>
            <div style="font-size: 8px; font-weight: bold; color: #34D399;">$ PROJECTS & ARCHITECTURE</div>
            <div style="font-size: 7px; color: #CBD5E1; margin-bottom: 6px;">* Distributed K/V Store: Raft consensus algorithm</div>
            <div style="font-size: 8px; font-weight: bold; color: #34D399;">$ DECLARATION</div>
            <div style="font-size: 6.5px; color: #64748B;">Date: [________]  Sign: [________]</div>
        </div>
        """
    }
}

def render_resume_html(data: Dict[str, Any], template_name: str = "Modern", photo_b64: str = "") -> str:
    """Generate rich responsive HTML representing the resume in the user's selected template."""
    accent = TEMPLATES_INFO.get(template_name, TEMPLATES_INFO["Modern"])["accent_color"]
    
    full_name = data.get("full_name", "").strip() or "YOUR NAME"
    contact_parts = []
    if data.get("email"): contact_parts.append(data["email"])
    if data.get("phone"): contact_parts.append(data["phone"])
    if data.get("location"): contact_parts.append(data["location"])
    contact_line = " &bull; ".join(contact_parts)

    # Handle photo mode
    photo_mode = data.get("photo_mode", "none")
    photo_tag = ""
    if (photo_mode == "upload" or photo_b64) and photo_b64:
        photo_tag = f'<img src="data:image/jpeg;base64,{photo_b64}" style="width: 85px; height: 85px; object-fit: cover; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.15);"/>'
    elif photo_mode == "box":
        photo_tag = '<div style="width: 95px; height: 115px; border: 2px dashed #718096; background: #F8FAFC; border-radius: 4px; display: inline-flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 4px; box-sizing: border-box;"><span style="font-size: 18px; color: #A0AEC0;">📷</span><span style="font-size: 8px; color: #4A5568; font-weight: 600; margin-top: 4px; line-height: 1.2;">Affix Passport Size Photo</span></div>'

    # Build sections HTML
    sections_html = []

    # Summary
    if data.get("summary"):
        sections_html.append(f"""<div class="resume-sec">
<div class="sec-title">PROFESSIONAL SUMMARY</div>
<div class="sec-content">{data['summary']}</div>
</div>""")

    # Skills
    if data.get("skills"):
        skills_text = data['skills']
        sections_html.append(f"""<div class="resume-sec">
<div class="sec-title">TECHNICAL & FUNCTIONAL SKILLS</div>
<div class="sec-content" style="white-space: pre-line;">{skills_text}</div>
</div>""")

    # Work Experience
    if data.get("experience") and data["experience"].strip():
        sections_html.append(f"""<div class="resume-sec">
<div class="sec-title">WORK EXPERIENCE</div>
<div class="sec-content" style="white-space: pre-line;">{data['experience']}</div>
</div>""")

    # Projects
    if data.get("projects"):
        sections_html.append(f"""<div class="resume-sec">
<div class="sec-title">PROJECTS</div>
<div class="sec-content" style="white-space: pre-line;">{data['projects']}</div>
</div>""")

    # Education and Qualifications
    if data.get("education"):
        sections_html.append(f"""<div class="resume-sec">
<div class="sec-title">EDUCATION AND QUALIFICATIONS</div>
<div class="sec-content" style="white-space: pre-line;">{data['education']}</div>
</div>""")

    # Certifications
    if data.get("certifications"):
        sections_html.append(f"""<div class="resume-sec">
<div class="sec-title">CERTIFICATIONS & COURSES</div>
<div class="sec-content" style="white-space: pre-line;">{data['certifications']}</div>
</div>""")

    # Custom / Other Sections
    for extra in data.get("custom_sections", []):
        if extra.get("title") and extra.get("content"):
            sections_html.append(f"""<div class="resume-sec">
<div class="sec-title">{extra['title'].upper()}</div>
<div class="sec-content" style="white-space: pre-line;">{extra['content']}</div>
</div>""")

    # Declaration & Signature (MANDATORY)
    declaration_text = data.get("declaration", "").strip() or "I hereby declare that all the information and details provided above are true, complete, and correct to the best of my knowledge and belief."
    date_val = data.get("date_val", "").strip() or "____________________"
    
    # Handle signature rendering (Write / Upload / Blank)
    sig_mode = data.get("signature_mode", "write")
    sig_img_b64 = data.get("signature_img_b64", "")
    sig_val = data.get("sig_val", "").strip()

    if sig_mode == "upload" and sig_img_b64:
        signature_element = f'''<div style="text-align: right; min-width: 170px;">
<img src="data:image/png;base64,{sig_img_b64}" style="max-height: 48px; max-width: 160px; object-fit: contain; margin-bottom: 2px; display: inline-block;" />
<div style="border-top: 1px solid #718096; width: 160px; margin-left: auto;"></div>
<div style="font-size: 0.85rem; color: #4A5568; margin-top: 2px;">Signature</div>
</div>'''
    elif sig_mode == "write" and sig_val:
        signature_element = f'''<div style="text-align: right; min-width: 170px;">
<div style="font-family: 'Brush Script MT', 'Dancing Script', 'Caveat', cursive, sans-serif; font-size: 1.55rem; color: #1A365D; line-height: 1.1; margin-bottom: 2px;">{sig_val}</div>
<div style="border-top: 1px solid #718096; width: 160px; margin-left: auto;"></div>
<div style="font-size: 0.85rem; color: #4A5568; margin-top: 2px;">Signature</div>
</div>'''
    else:
        signature_element = '''<div style="text-align: right; min-width: 170px;">
<div style="font-size: 0.85rem; color: #4A5568; margin-top: 2px;">Signature: ____________________</div>
</div>'''

    sections_html.append(f"""<div class="resume-sec" style="margin-top: 25px; border-top: 1px solid #E2E8F0; padding-top: 12px;">
<div class="sec-title">DECLARATION</div>
<div class="sec-content" style="font-size: 0.88rem; color: #4A5568; font-style: italic;">{declaration_text}</div>
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 25px;">
<div style="font-size: 0.9rem;"><strong>Date:</strong> {date_val}</div>
{signature_element}
</div>
</div>""")

    all_sections = "".join(sections_html)

    # Template-specific styling wrappers
    if template_name == "Classic":
        font_family = "Georgia, 'Times New Roman', serif"
        header_html = f"""
            <div style="text-align: center; border-bottom: 2px solid #2C3E50; padding-bottom: 12px; margin-bottom: 18px;">
                {f'<div style="margin-bottom: 10px;">{photo_tag}</div>' if photo_tag else ''}
                <h1 style="font-size: 1.8rem; margin: 0; color: #1A202C; letter-spacing: 1px;">{full_name.upper()}</h1>
                <p style="font-size: 0.9rem; color: #4A5568; margin-top: 4px;">{contact_line}</p>
                {f'<p style="font-size: 0.9rem; color: #2C3E50; font-weight: bold; margin-top: 2px;">{data.get("job_role", "")} &bull; {data.get("company", "")}</p>' if data.get("job_role") else ''}
            </div>
        """
    elif template_name == "Modern":
        font_family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        header_html = f"""
            <div style="background: linear-gradient(135deg, #2B6CB0, #1A365D); color: white; padding: 22px 26px; border-radius: 6px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="font-size: 1.8rem; margin: 0; font-weight: 700;">{full_name}</h1>
                    {f'<div style="font-size: 1rem; opacity: 0.95; font-weight: 500; margin-top: 2px;">{data.get("job_role", "")} &bull; {data.get("company", "")}</div>' if data.get("job_role") else ''}
                    <div style="font-size: 0.85rem; opacity: 0.85; margin-top: 6px;">{contact_line}</div>
                </div>
                {f'<div>{photo_tag}</div>' if photo_tag else ''}
            </div>
        """
    elif template_name == "Minimal":
        font_family = "-apple-system, BlinkMacSystemFont, 'Inter', sans-serif"
        header_html = f"""
            <div style="margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid #CBD5E0; display: flex; justify-content: space-between; align-items: flex-end;">
                <div>
                    <h1 style="font-size: 2rem; font-weight: 300; margin: 0; color: #1A202C; letter-spacing: 0.5px;">{full_name}</h1>
                    {f'<div style="font-size: 0.9rem; color: #718096; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">{data.get("job_role", "")} &bull; {data.get("company", "")}</div>' if data.get("job_role") else ''}
                    <div style="font-size: 0.85rem; color: #718096; margin-top: 4px;">{contact_line}</div>
                </div>
                {f'<div>{photo_tag}</div>' if photo_tag else ''}
            </div>
        """
    elif template_name == "Professional":
        font_family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        header_html = f"""
            <div style="border-left: 6px solid #1E3A8A; padding-left: 16px; margin-bottom: 22px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="font-size: 1.85rem; font-weight: 700; margin: 0; color: #1E3A8A;">{full_name}</h1>
                    {f'<div style="font-size: 0.95rem; font-weight: 600; color: #475569; margin-top: 2px;">{data.get("job_role", "")} &bull; {data.get("company", "")}</div>' if data.get("job_role") else ''}
                    <div style="font-size: 0.85rem; color: #64748B; margin-top: 4px;">{contact_line}</div>
                </div>
                {f'<div>{photo_tag}</div>' if photo_tag else ''}
            </div>
        """
    elif template_name == "Creative":
        font_family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        header_html = f"""
            <div style="background: #0D9488; color: white; padding: 20px 24px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="font-size: 1.8rem; font-weight: 800; margin: 0;">{full_name}</h1>
                    {f'<div style="font-size: 1rem; opacity: 0.95; font-weight: 500; margin-top: 3px;">{data.get("job_role", "")} &bull; {data.get("company", "")}</div>' if data.get("job_role") else ''}
                    <div style="font-size: 0.85rem; opacity: 0.9; margin-top: 4px;">{contact_line}</div>
                </div>
                {f'<div>{photo_tag}</div>' if photo_tag else ''}
            </div>
        """
    else:  # Technical
        font_family = "'Consolas', 'Monaco', 'Courier New', monospace"
        header_html = f"""
            <div style="background: #0F172A; color: #F8FAFC; padding: 18px 22px; border-radius: 6px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="font-size: 1.6rem; font-weight: 700; margin: 0; color: #38BDF8;">&gt; {full_name}</h1>
                    {f'<div style="font-size: 0.9rem; color: #34D399; margin-top: 3px;">Role: {data.get("job_role", "")} | Org: {data.get("company", "")}</div>' if data.get("job_role") else ''}
                    <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">{contact_line}</div>
                </div>
                {f'<div>{photo_tag}</div>' if photo_tag else ''}
            </div>
        """

    raw_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{
    margin: 0;
    padding: 20px 10px;
    background-color: #F8FAFC;
    font-family: {font_family};
    display: flex;
    justify-content: center;
}}
.resume-paper {{
    background: #FFFFFF;
    color: #2D3748;
    padding: 36px 40px;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    border: 1px solid #E2E8F0;
    max-width: 820px;
    width: 100%;
    box-sizing: border-box;
    line-height: 1.55;
}}
.resume-sec {{ margin-bottom: 20px; }}
.sec-title {{ font-weight: 700; font-size: 1.05rem; color: {accent}; border-bottom: 2px solid {accent}40; padding-bottom: 4px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px; }}
.sec-content {{ font-size: 0.94rem; color: #2D3748; line-height: 1.6; }}
</style>
</head>
<body>
<div class="resume-paper">
{header_html}
{all_sections}
</div>
</body>
</html>"""
    return "\n".join([line.strip() for line in raw_html.split("\n") if line.strip()])

def export_builder_resume_to_pdf(data: Dict[str, Any], template_name: str = "Modern") -> bytes:
    """Generate high-quality PDF specifically adhering to the selected template styling."""
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
    accent_hex = TEMPLATES_INFO.get(template_name, TEMPLATES_INFO["Modern"])["accent_color"]
    accent_color = colors.HexColor(accent_hex)

    title_style = ParagraphStyle(
        "BuilderTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=accent_color,
        spaceAfter=3
    )

    contact_style = ParagraphStyle(
        "BuilderContact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        "BuilderHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=accent_color,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        "BuilderBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        "BuilderBullet",
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

    # Title & Contact
    name = data.get("full_name", "").strip() or "YOUR NAME"

    contact_parts = []
    if data.get("email"): contact_parts.append(data["email"])
    if data.get("phone"): contact_parts.append(data["phone"])
    if data.get("location"): contact_parts.append(data["location"])
    if data.get("job_role"): contact_parts.append(f"{data['job_role']} - {data.get('company', '')}" if data.get('company') else data['job_role'])

    header_left = [
        Paragraph(name, title_style),
        Paragraph(" &bull; ".join(contact_parts), contact_style)
    ]

    photo_mode = data.get("photo_mode", "none")
    photo_b64 = data.get("photo_b64", "")

    if (photo_mode == "upload" or photo_b64) and photo_b64:
        try:
            photo_bytes = base64.b64decode(photo_b64)
            img_obj = RLImage(io.BytesIO(photo_bytes), width=70, height=70)
            hdr_table = Table([[header_left, img_obj]], colWidths=[440, 80])
            hdr_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN', (1,0), (1,0), 'RIGHT')
            ]))
            elements.append(hdr_table)
        except Exception:
            elements.extend(header_left)
    elif photo_mode == "box":
        box_style = ParagraphStyle(
            "PassportBoxText",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9.5,
            alignment=1,
            textColor=colors.HexColor("#718096")
        )
        box_content = [
            Spacer(1, 14),
            Paragraph("Affix<br/>Passport Size<br/>Photo", box_style)
        ]
        box_table = Table([[box_content]], colWidths=[70], rowHeights=[85])
        box_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A0AEC0")),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        hdr_table = Table([[header_left, box_table]], colWidths=[440, 80])
        hdr_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'RIGHT')
        ]))
        elements.append(hdr_table)
    else:
        elements.extend(header_left)

    elements.append(Spacer(1, 4))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=8))

    # Helper to add section
    def add_section(heading_text: str, content_text: str):
        if not content_text or not content_text.strip():
            return
        elements.append(Paragraph(heading_text.upper(), section_heading))
        for line in content_text.strip().split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            safe_l = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if safe_l in ("Education", "Qualifications"):
                elements.append(Paragraph(f"<b><u>{safe_l}</u></b>", body_style))
            elif safe_l.startswith(("•", "-", "*")):
                clean_b = safe_l.lstrip("•-* ").strip()
                elements.append(Paragraph(f"&bull; {clean_b}", bullet_style))
            else:
                elements.append(Paragraph(safe_l, body_style))
        elements.append(Spacer(1, 4))

    # Render all sections
    if data.get("summary"):
        add_section("Professional Summary", data["summary"])

    if data.get("skills"):
        add_section("Technical & Functional Skills", data["skills"])

    if data.get("experience") and data["experience"].strip():
        add_section("Work Experience", data["experience"])

    if data.get("projects"):
        add_section("Projects", data["projects"])

    if data.get("education"):
        add_section("Education and Qualifications", data["education"])

    if data.get("certifications"):
        add_section("Certifications & Courses", data["certifications"])

    for extra in data.get("custom_sections", []):
        if extra.get("title") and extra.get("content"):
            add_section(extra["title"], extra["content"])

    # Declaration & Signature (MANDATORY)
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("DECLARATION", section_heading))
    dec_text = data.get("declaration", "").strip() or "I hereby declare that all the information and details provided above are true, complete, and correct to the best of my knowledge and belief."
    safe_dec = dec_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    elements.append(Paragraph(f"<i>{safe_dec}</i>", body_style))
    elements.append(Spacer(1, 14))

    date_val = data.get("date_val", "").strip() or "____________________"
    sig_mode = data.get("signature_mode", "write")
    sig_img_b64 = data.get("signature_img_b64", "")
    sig_val = data.get("sig_val", "").strip()

    if sig_mode == "upload" and sig_img_b64:
        try:
            sig_bytes = base64.b64decode(sig_img_b64)
            sig_img = RLImage(io.BytesIO(sig_bytes), width=110, height=35)
            sig_table = Table([[
                Paragraph(f"<b>Date:</b> {date_val}", body_style),
                sig_img
            ]], colWidths=[320, 200])
            sig_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
                ('ALIGN', (1,0), (1,0), 'RIGHT')
            ]))
            elements.append(sig_table)
        except Exception:
            date_sig_html = f"<b>Date:</b> {date_val}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Signature:</b> ____________________"
            elements.append(Paragraph(date_sig_html, body_style))
    else:
        sig_str = sig_val if (sig_mode == "write" and sig_val) else "____________________"
        date_sig_html = f"<b>Date:</b> {date_val}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Signature:</b> {sig_str}"
        elements.append(Paragraph(date_sig_html, body_style))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

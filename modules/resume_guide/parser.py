"""
Resume parsing utilities for extracting text and segmenting sections from PDF, DOCX, and TXT files.
"""

import io
import re
from typing import Dict, List, Any
import pypdf
import docx

STANDARD_SECTION_PATTERNS = {
    "summary": re.compile(r"^(professional\s+summary|summary|profile|about\s+me|career\s+objective|objective)", re.IGNORECASE),
    "experience": re.compile(r"^(work\s+experience|professional\s+experience|experience|employment\s+history|work\s+history|internship\s+experience|career\s+history)", re.IGNORECASE),
    "projects": re.compile(r"^(projects|technical\s+projects|personal\s+projects|academic\s+projects|key\s+projects)", re.IGNORECASE),
    "skills": re.compile(r"^(skills|technical\s+skills|core\s+competencies|technologies|areas\s+of\s+expertise|tools\s+&\s+technologies|skills\s+&\s+abilities)", re.IGNORECASE),
    "education": re.compile(r"^(education|academic\s+background|educational\s+qualifications|academics)", re.IGNORECASE),
    "certifications": re.compile(r"^(certifications|licenses|courses|certificates|credentials|achievements|awards|honors)", re.IGNORECASE),
    "miscellaneous": re.compile(r"^(miscellaneous|additional\s+information|interests|hobbies|languages|volunteer\s+experience|publications)", re.IGNORECASE),
}

def extract_text_from_file(uploaded_file) -> str:
    """Extract clean string text from an uploaded file (PDF, DOCX, TXT/MD)."""
    filename = getattr(uploaded_file, "name", "").lower()
    
    # In Streamlit, uploaded_file is an UploadedFile buffer
    if hasattr(uploaded_file, "read"):
        content_bytes = uploaded_file.read()
        # Reset pointer for subsequent reads if needed
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
    elif isinstance(uploaded_file, bytes):
        content_bytes = uploaded_file
    elif isinstance(uploaded_file, str):
        return uploaded_file
    else:
        content_bytes = b""

    text = ""
    if filename.endswith(".pdf"):
        reader = pypdf.PdfReader(io.BytesIO(content_bytes))
        extracted_pages = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                extracted_pages.append(t)
        text = "\n".join(extracted_pages)
    elif filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    paragraphs.append(" | ".join(row_text))
        text = "\n".join(paragraphs)
    else:
        # Default text decode (try utf-8 then latin-1)
        try:
            text = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = content_bytes.decode("latin-1", errors="replace")

    return clean_text(text)

def clean_text(text: str) -> str:
    """Normalize linebreaks and spaces."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Replace multiple empty lines with maximum 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def parse_resume_sections(raw_text: str) -> Dict[str, str]:
    """
    Parse a raw resume string into structured standard sections:
    header, summary, experience, projects, skills, education, certifications, miscellaneous.
    """
    lines = raw_text.split("\n")
    sections: Dict[str, List[str]] = {
        "header": [],
        "summary": [],
        "experience": [],
        "projects": [],
        "skills": [],
        "education": [],
        "certifications": [],
        "miscellaneous": []
    }

    current_section = "header"
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_section in sections:
                sections[current_section].append(line)
            continue

        # Check if line is a section header (short line, matches header pattern)
        # Often headers are all caps or title case and <= 40 chars
        clean_header = re.sub(r"^[#\*\-_\s]+", "", stripped)
        clean_header = re.sub(r"[:\-_]+$", "", clean_header).strip()

        matched_section = None
        if len(clean_header) <= 45 and not clean_header.endswith("."):
            for sec_key, pattern in STANDARD_SECTION_PATTERNS.items():
                if pattern.search(clean_header):
                    matched_section = sec_key
                    break

        if matched_section:
            current_section = matched_section
            sections[current_section].append(stripped)
        else:
            sections[current_section].append(stripped)

    # Join lines back into text blocks
    return {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}

def extract_bullets_from_text(section_text: str) -> List[str]:
    """Extract individual bullet points or meaningful sentences from a section."""
    lines = section_text.split("\n")
    bullets = []
    current_bullet = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Check if line starts with a bullet marker or dash or number
        is_bullet_start = bool(re.match(r"^([•\-\*▪▫‣–—]|\d+\.|\([a-zA-Z0-9]\))\s*", stripped))
        clean_line = re.sub(r"^([•\-\*▪▫‣–—]|\d+\.|\([a-zA-Z0-9]\))\s*", "", stripped)

        if is_bullet_start:
            if current_bullet:
                bullets.append(" ".join(current_bullet))
            current_bullet = [clean_line]
        else:
            if current_bullet:
                current_bullet.append(clean_line)
            else:
                current_bullet = [clean_line]

    if current_bullet:
        bullets.append(" ".join(current_bullet))

    return [b.strip() for b in bullets if b.strip()]

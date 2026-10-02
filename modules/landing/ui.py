"""
AscendCareer — Landing Screen
Polished opening screen with animated background, theme switching,
branding, Core Principle, Privacy & Trust section, and Sign In entry point.

This module is intentionally self-contained and modular.
The Sign In button is an entry-point placeholder — sign-in logic
is implemented separately in the next step.
"""

import base64
from pathlib import Path
import textwrap
import streamlit as st
import streamlit.components.v1 as components
from modules.landing.content import CORE_PRINCIPLE


_CACHED_LOGO_URI = ""
def _get_logo_data_uri() -> str:
    """Return inline base64 data URI of the transparent logo so it always renders without 404s."""
    global _CACHED_LOGO_URI
    if _CACHED_LOGO_URI:
        return _CACHED_LOGO_URI
    p = Path(__file__).resolve().parent.parent.parent / "assets" / "logo.png"
    if p.exists():
        encoded = base64.b64encode(p.read_bytes()).decode("utf-8")
        _CACHED_LOGO_URI = f"data:image/png;base64,{encoded}"
        return _CACHED_LOGO_URI
    return ""


_CACHED_THEME_ICON_URI = ""
def _get_theme_icon_data_uri() -> str:
    """Return data URI of the Sun/Moon split theme icon."""
    global _CACHED_THEME_ICON_URI
    if _CACHED_THEME_ICON_URI:
        return _CACHED_THEME_ICON_URI
    p_png = Path(__file__).resolve().parent.parent.parent / "assets" / "theme_icon.png"
    if p_png.exists():
        encoded = base64.b64encode(p_png.read_bytes()).decode("ascii")
        _CACHED_THEME_ICON_URI = f"data:image/png;base64,{encoded}"
        return _CACHED_THEME_ICON_URI
    p = Path(__file__).resolve().parent.parent.parent / "assets" / "theme_icon.svg"
    if p.exists():
        import urllib.parse
        svg_text = p.read_text(encoding="utf-8")
        encoded = urllib.parse.quote(svg_text)
        _CACHED_THEME_ICON_URI = f"data:image/svg+xml;utf8,{encoded}"
        return _CACHED_THEME_ICON_URI
    return ""


def clean_html(html_str: str) -> str:
    """
    Strips 100% of leading & trailing whitespace from every line.
    This guarantees that Markdown parsers NEVER see 4 or more leading spaces,
    preventing any HTML block from being rendered as a preformatted code block.
    """
    return "\n".join(line.strip() for line in html_str.splitlines() if line.strip())



# ─────────────────────────────────────────────────────────────────────────────
# Theme Configuration
# ─────────────────────────────────────────────────────────────────────────────

THEMES = {
    "light": {
        "label": "Toggle Theme",
        "bg": "#F8FAFF",
        "surface": "#FFFFFF",
        "surface2": "#F0F4FF",
        "border": "#DDE3F0",
        "text_primary": "#1A1F36",
        "text_secondary": "#0B4619",        # Bottle Green (user specified)
        "text_muted": "#145A32",            # Clear medium Bottle Green (user specified)
        "accent": "#4F46E5",
        "accent_hover": "#4338CA",
        "accent_soft": "#EEF2FF",
        "gold": "#D97706",
        "gold_soft": "#FEF3C7",
        "card_shadow": "0 2px 16px rgba(79,70,229,0.08)",
        "btn_text": "#FFFFFF",
        "tag_bg": "#EEF2FF",
        "tag_text": "#4F46E5",
        "divider": "#DDE3F0",
        "qa_bg": "#F8FAFF",
        "qa_hover": "#EEF2FF",
        "qa_answer_bg": "#F0F4FF",
        "qa_border": "#DDE3F0",
        "principle_border": "#A7F3D0",
        "brand_ascend_color": "#4338CA",
        "brand_ascend_glow": "rgba(67, 56, 202, 0.16)",
        "brand_career_color": "#D97706",
        "brand_career_glow": "rgba(217, 119, 6, 0.20)",
    },
    "dark": {
        "label": "Toggle Theme",
        "bg": "#0D0F1A",
        "surface": "#141827",
        "surface2": "#1C2035",
        "border": "#2D3450",
        "text_primary": "#FFFFFF",
        "text_secondary": "#FDFBF7",        # Off Cream (user specified)
        "text_muted": "#EAE5D9",            # Soft warm Off Cream (user specified)
        "accent": "#818CF8",
        "accent_hover": "#A5B4FC",
        "accent_soft": "#1E2347",
        "gold": "#FCD34D",
        "gold_soft": "#2D2710",
        "card_shadow": "0 2px 24px rgba(0,0,0,0.45)",
        "btn_text": "#0D0F1A",
        "tag_bg": "#1E2347",
        "tag_text": "#818CF8",
        "divider": "#2D3450",
        "qa_bg": "#141827",
        "qa_hover": "#1C2035",
        "qa_answer_bg": "#1A1F36",
        "qa_border": "#2D3450",
        "principle_border": "#3730A3",
        "brand_ascend_color": "#818CF8",
        "brand_ascend_glow": "rgba(129, 140, 248, 0.38)",
        "brand_career_color": "#FCD34D",
        "brand_career_glow": "rgba(252, 211, 77, 0.42)",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# CSS Injection
# ─────────────────────────────────────────────────────────────────────────────

def _inject_css(t: dict):
    theme_icon_uri = _get_theme_icon_data_uri()
    is_dark = (t.get("bg") == "#0D0F1A")
    metal_primary = "#F1F5F9" if is_dark else "#334155"
    metal_secondary = "#CBD5E1" if is_dark else "#475569"
    metal_muted = "#94A3B8" if is_dark else "#64748B"
    # Fast asynchronous font loading (non-blocking)
    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    st.markdown(clean_html(f"""
    <style>
    /* ── Reset & Base ─────────────────────────────────────────────────── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {{
        background: {t["bg"]} !important;
        color: {t["text_primary"]} !important;
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
    }}

    /* Hide default Streamlit chrome on landing */
    #MainMenu, [data-testid="stFooter"], [data-testid="stToolbar"],
    [data-testid="stSidebarNav"], [data-testid="stSidebar"], header {{
        display: none !important;
    }}

    /* ── Scrollbar ────────────────────────────────────────────────────── */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: {t["bg"]}; }}
    ::-webkit-scrollbar-thumb {{ background: {t["border"]}; border-radius: 3px; }}

    /* ── Streamlit padding override ───────────────────────────────────── */
    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    [data-testid="stVerticalBlock"] > div {{ padding: 0; }}

    /* ── Animated canvas ──────────────────────────────────────────────── */
    #ac-anim-canvas {{
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 0;
        pointer-events: none;
    }}

    /* ── Content layer above canvas ───────────────────────────────────── */
    .ac-content {{
        position: relative;
        z-index: 1;
    }}

    /* ── Header Row Alignment ─────────────────────────────────────────── */
    div[data-testid="stHorizontalBlock"]:first-of-type {{
        align-items: center !important;
        padding: 8px 16px 0 !important;
    }}

    /* ── Hamburger Menu Button (Three Horizontal Lines) ─────────────────── */
    .st-key-ac_hamburger_btn button {{
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        max-width: 44px !important;
        min-height: 44px !important;
        max-height: 44px !important;
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        margin: 0 !important;
        transition: transform 0.18s ease !important;
    }}
    .st-key-ac_hamburger_btn button:hover {{
        transform: scale(1.14) !important;
        background: transparent !important;
    }}
    .st-key-ac_hamburger_btn button * {{
        display: none !important;
        visibility: hidden !important;
    }}
    .st-key-ac_hamburger_btn button::before {{
        content: "";
        display: block;
        width: 22px;
        height: 2.2px;
        background-color: {t["text_primary"]};
        box-shadow: 0 -7px 0 {t["text_primary"]}, 0 7px 0 {t["text_primary"]};
        border-radius: 2px;
        transition: background-color 0.2s;
    }}
    .st-key-ac_hamburger_btn button:hover::before {{
        background-color: {t["accent"]};
        box-shadow: 0 -7px 0 {t["accent"]}, 0 7px 0 {t["accent"]};
    }}

    /* ── Pink Sign In Option (Top Right — Vibrant & Visible in both themes) ─ */
    .st-key-ac_top_signin_btn {{
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: 100% !important;
    }}

    .st-key-ac_top_signin_btn div[data-testid="stButton"] {{
        width: 100% !important;
    }}

    .st-key-ac_top_signin_btn button {{
        background: linear-gradient(135deg, #EC4899 0%, #DB2777 50%, #BE185D 100%) !important;
        background-color: #DB2777 !important;
        color: #FFFFFF !important;
        border: 1.5px solid #F472B6 !important;
        border-radius: 50px !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 4px 18px rgba(236, 72, 153, 0.45) !important;
        cursor: pointer !important;
        transition: all 0.22s ease !important;
        padding: 8px 22px !important;
        font-size: 0.98rem !important;
        min-height: 44px !important;
        height: 44px !important;
        width: 100% !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
    }}

    .st-key-ac_top_signin_btn button:hover {{
        background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%) !important;
        background-color: #E11D48 !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(236, 72, 153, 0.65) !important;
        border-color: #FDA4AF !important;
    }}

    .st-key-ac_top_signin_btn button * {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        display: inline !important;
        visibility: visible !important;
        opacity: 1 !important;
    }}

    /* ── Instant Theme Toggle Button (Exact reference icon, 100% transparent) ── */
    .st-key-ac_theme_toggle_btn {{
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: auto !important;
    }}

    .st-key-ac_theme_toggle_btn div[data-testid="stButton"] {{
        display: inline-flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 48px !important;
        height: 48px !important;
    }}

    .st-key-ac_theme_toggle_btn button {{
        width: 48px !important;
        height: 48px !important;
        min-width: 48px !important;
        max-width: 48px !important;
        min-height: 48px !important;
        max-height: 48px !important;
        background: transparent url('{theme_icon_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        background-size: contain !important;
        border: none !important;
        border-width: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        border-radius: 50% !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }}

    .st-key-ac_theme_toggle_btn button:hover {{
        transform: scale(1.15) !important;
        background: transparent url('{theme_icon_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    .st-key-ac_theme_toggle_btn button:focus,
    .st-key-ac_theme_toggle_btn button:active {{
        background: transparent url('{theme_icon_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* Completely hide any inner text / icon inside ONLY the theme toggle button */
    .st-key-ac_theme_toggle_btn button * {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }}

    /* ── Typography ───────────────────────────────────────────────────── */
    .ac-brand-title {{
        font-family: 'Cinzel Decorative', 'Palatino Linotype', 'Book Antiqua', Georgia, serif;
        font-size: clamp(2.6rem, 5.8vw, 4.4rem);
        font-weight: 800;
        letter-spacing: 0em !important;
        line-height: 1.1;
        margin: 0 auto 8px;
        text-align: center;
        display: inline-block;
    }}
    .ac-brand-ascend {{
        color: {t["brand_ascend_color"]};
        text-shadow: 0 2px 16px {t["brand_ascend_glow"]};
        letter-spacing: 0em !important;
    }}
    .ac-brand-career {{
        color: {t["brand_career_color"]};
        text-shadow: 0 2px 16px {t["brand_career_glow"]};
        letter-spacing: 0em !important;
    }}
    .ac-tagline-main {{
        font-size: clamp(1rem, 2.2vw, 1.35rem);
        font-weight: 700;
        color: {t["text_primary"]};
        letter-spacing: 0.01em;
    }}
    .ac-tagline-sub {{
        font-size: clamp(1.05rem, 2vw, 1.3rem);
        color: {t["text_secondary"]};
        font-style: italic;
        font-weight: 500;
    }}
    .ac-section-title {{
        font-family: 'Playfair Display', 'Georgia', 'Times New Roman', serif !important;
        font-size: 1.55rem;
        font-weight: 800;
        color: {t["text_primary"]};
        letter-spacing: -0.01em;
        margin: 0 0 6px;
    }}
    .ac-divider {{
        border: none;
        border-top: 1px solid {t["divider"]};
        margin: 0;
    }}
    .ac-gold-badge {{
        display: inline-block;
        background: {t["gold_soft"]};
        color: {t["gold"]};
        border-radius: 50px;
        padding: 4px 18px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}
    .ac-tag {{
        display: inline-block;
        background: {t["tag_bg"]};
        color: {t["tag_text"]};
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }}

    /* ── Streamlit Expander styling ───────────────────────────────────── */
    [data-testid="stExpander"] {{
        background: {t["surface"]} !important;
        border: 1px solid {t["border"]} !important;
        border-radius: 12px !important;
        box-shadow: none !important;
        margin-bottom: 4px !important;
        overflow: hidden !important;
    }}
    [data-testid="stExpander"] > details > summary {{
        background: {t["surface"]} !important;
        color: {t["text_primary"]} !important;
        font-weight: 700 !important;
        font-size: 0.97rem !important;
        padding: 14px 18px !important;
        border-radius: 12px !important;
    }}
    [data-testid="stExpander"] > details > summary:hover {{
        background: {t["surface2"]} !important;
    }}
    [data-testid="stExpander"] > details[open] > summary {{
        border-bottom: 1px solid {t["border"]} !important;
        border-radius: 12px 12px 0 0 !important;
    }}
    [data-testid="stExpander"] > details > div {{
        background: {t["surface"]} !important;
        padding: 4px 18px 16px !important;
    }}

    /* ── Q&A details/summary (HTML native) ───────────────────────────── */
    .ac-qa-item {{
        border: 1px solid {t["qa_border"]};
        border-radius: 8px;
        margin: 6px 0;
        overflow: hidden;
        background: {t["qa_bg"]};
        transition: border-color 0.2s;
    }}
    .ac-qa-item:hover {{
        border-color: {t["accent"]};
    }}
    .ac-qa-item summary {{
        padding: 11px 16px;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.88rem;
        color: {t["text_primary"]};
        list-style: none;
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 12px;
        user-select: none;
        background: {t["qa_bg"]};
        transition: background 0.15s;
    }}
    .ac-qa-item summary::-webkit-details-marker {{ display: none; }}
    .ac-qa-item summary:hover {{
        background: {t["qa_hover"]};
    }}
    .ac-qa-item summary .ac-qa-icon {{
        flex-shrink: 0;
        font-size: 0.9rem;
        margin-top: 1px;
        color: {t["accent"]};
        transition: transform 0.2s;
        font-style: normal;
    }}
    .ac-qa-item .ac-qa-icon::before {{ content: '+'; }}
    .ac-qa-item[open] .ac-qa-icon::before {{ content: '\2212'; }}
    .ac-qa-item[open] summary .ac-qa-icon {{
        transform: none;
    }}
    .ac-qa-item[open] summary {{
        border-bottom: 1px solid {t["qa_border"]};
        background: {t["qa_hover"]};
    }}
    .ac-qa-answer {{
        padding: 14px 18px 16px;
        font-size: 1.05rem;
        color: {t["text_secondary"]};
        line-height: 1.85;
        background: {t["qa_answer_bg"]};
        border-top: none;
    }}

    /* ── Privacy & Trust top-level expander — larger header ─────────── */
    .ac-privacy-top > [data-testid="stExpander"] > details > summary {{
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        padding: 16px 20px !important;
        background: {t["surface2"]} !important;
    }}

    /* ── Core Principle block ────────────────────────────────────────── */
    .ac-principle-block {{
        background: {t["surface"]};
        border: 1px solid {t["principle_border"]};
        border-left: 5px solid {t["accent"]};
        border-radius: 12px;
        padding: 24px 28px;
        font-family: 'DM Sans', 'Inter', system-ui, -apple-system, sans-serif !important;
        font-size: 1.15rem;
        line-height: 1.90;
        color: {t["text_secondary"]};
        box-shadow: {t["card_shadow"]};
    }}

    /* ── Privacy statement banner ────────────────────────────────────── */
    .ac-privacy-statement {{
        background: {t["accent_soft"]};
        border: 1px solid {t["accent"]};
        border-radius: 10px;
        padding: 16px 20px;
        font-size: 1.05rem;
        font-weight: 600;
        color: {t["text_primary"]};
        margin-bottom: 18px;
        line-height: 1.65;
    }}

    /* ── Section number badge ────────────────────────────────────────── */
    .ac-sec-badge {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        background: {t["accent"]};
        color: white;
        border-radius: 50%;
        font-size: 0.72rem;
        font-weight: 800;
        margin-right: 8px;
        flex-shrink: 0;
        vertical-align: middle;
    }}

    /* ── Footer ──────────────────────────────────────────────────────── */
    .ac-footer-container {{
        width: 100% !important;
        max-width: 100% !important;
        background: {t["surface"]} !important;
        border-top: 1px solid {t["border"]} !important;
        box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.06) !important;
        padding: 32px 48px 36px !important;
        margin-top: 56px !important;
        box-sizing: border-box !important;
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
    }}
    .ac-footer-inner {{
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 32px;
        box-sizing: border-box;
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
    }}
    .ac-footer-col {{
        box-sizing: border-box;
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
    }}
    .ac-footer-left {{
        flex: 1 1 0;
        text-align: left;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
    }}
    .ac-footer-readiness {{
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
        font-size: 0.95rem;
        font-weight: 600;
        color: {metal_secondary} !important;
        line-height: 1.45;
        letter-spacing: -0.01em;
    }}
    .ac-footer-copyright-group {{
        display: flex;
        flex-direction: column;
        gap: 3px;
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
    }}
    .ac-footer-copy {{
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
        font-size: 0.88rem;
        font-weight: 600;
        color: {metal_secondary} !important;
        line-height: 1.4;
    }}
    .ac-footer-rights {{
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
        font-size: 0.80rem;
        font-weight: 400;
        color: {metal_muted} !important;
        line-height: 1.35;
    }}
    .ac-footer-center {{
        flex: 1 1 0;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
    }}
    .ac-footer-brand {{
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
        font-size: 1.30rem;
        font-weight: 800;
        color: {metal_primary} !important;
        letter-spacing: 0.02em;
        line-height: 1.2;
    }}
    .ac-footer-tagline {{
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
        font-size: 0.86rem;
        font-weight: 400;
        color: {metal_muted} !important;
        line-height: 1.45;
    }}
    .ac-footer-right {{
        flex: 1 1 0;
        text-align: right;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        justify-content: center;
    }}
    .ac-footer-creator {{
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
        font-size: 0.92rem;
        font-weight: 500;
        color: {metal_secondary} !important;
        line-height: 1.45;
        white-space: nowrap;
    }}
    .ac-footer-creator-name {{
        font-family: 'Consolas', 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace !important;
        font-weight: 800;
        color: {metal_primary} !important;
        letter-spacing: 0.02em;
    }}

    /* ── Mobile responsiveness ───────────────────────────────────────── */
    @media (max-width: 880px) and (min-width: 641px) {{
        .ac-footer-inner {{
            gap: 16px;
        }}
        .ac-footer-creator {{
            white-space: normal;
        }}
    }}
    @media (max-width: 640px) {{
        .ac-brand-name {{ font-size: 2.4rem; }}
        .ac-principle-block {{ padding: 16px 18px; font-size: 0.87rem; }}
        .ac-qa-item summary {{ font-size: 0.83rem; padding: 10px 13px; }}
        .ac-qa-answer {{ font-size: 0.82rem; padding: 10px 13px; }}

        /* Stacked left-aligned footer on mobile */
        .ac-footer-container {{
            padding: 28px 20px 32px !important;
            margin-top: 36px !important;
        }}
        .ac-footer-inner {{
            flex-direction: column !important;
            text-align: left !important;
            align-items: flex-start !important;
            gap: 20px !important;
        }}
        .ac-footer-col {{
            width: 100% !important;
        }}
        .ac-footer-left {{
            text-align: left !important;
            align-items: flex-start !important;
            order: 1 !important;
            width: 100% !important;
            gap: 6px !important;
        }}
        .ac-footer-copyright-group {{
            align-items: flex-start !important;
            gap: 2px !important;
        }}
        .ac-footer-center {{
            text-align: left !important;
            align-items: flex-start !important;
            order: 2 !important;
            width: 100% !important;
            gap: 4px !important;
        }}
        .ac-footer-right {{
            text-align: left !important;
            align-items: flex-start !important;
            order: 3 !important;
            width: 100% !important;
        }}
        .ac-footer-creator {{
            white-space: normal !important;
            text-align: left !important;
        }}
    }}
    </style>
    """), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Animated Backgrounds
# ─────────────────────────────────────────────────────────────────────────────

def _animated_background(theme_key: str, theme_icon_uri: str = ""):
    """Injects a canvas-based animated background per theme."""

    if theme_key == "light":
        # ── Light: Full-Screen Ambient Glow ───────────────────────────────
        # Glowing particles slowly rise across 100% full width & height of the light background
        anim_js = r"""
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width  = window.parent.innerWidth  || window.innerWidth;
        canvas.height = window.parent.innerHeight || window.innerHeight;
    }
    resize();
    window.parent.addEventListener('resize', resize);

    const MAX = 90;
    const particles = [];

    function spawn(spreadY) {
        return {
            x:        Math.random() * canvas.width,
            y:        spreadY !== undefined ? spreadY : canvas.height + 8,
            r:        1.2 + Math.random() * 2.8,
            vy:       0.45 + Math.random() * 1.0,
            vx:       (Math.random() - 0.5) * 0.25,
            hue:      210 + Math.random() * 50,
            life:     0,
            maxLife:  450 + Math.random() * 500,
            maxAlpha: 0.25 + Math.random() * 0.45,
            alpha:    0,
        };
    }

    for (let i = 0; i < MAX; i++) {
        const p = spawn(Math.random() * canvas.height);
        p.life = Math.random() * p.maxLife;
        particles.push(p);
    }

    function drawGlow() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#F8FAFF';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        while (particles.length < MAX) { particles.push(spawn()); }

        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.life++; p.x += p.vx; p.y -= p.vy;

            const fadeIn  = p.maxLife * 0.15;
            const fadeOut = p.maxLife * 0.85;
            if (p.life < fadeIn) {
                p.alpha = p.maxAlpha * (p.life / fadeIn);
            } else if (p.life < fadeOut) {
                p.alpha = p.maxAlpha;
            } else {
                p.alpha = p.maxAlpha * (1 - (p.life - fadeOut) / (p.maxLife - fadeOut));
            }

            if (p.life >= p.maxLife || p.y < -20) { particles.splice(i, 1); continue; }

            const glowR = p.r * 6;
            const glow  = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, glowR);
            glow.addColorStop(0,   `hsla(${p.hue}, 70%, 55%, ${p.alpha * 0.45})`);
            glow.addColorStop(0.4, `hsla(${p.hue}, 65%, 60%, ${p.alpha * 0.18})`);
            glow.addColorStop(1,   `hsla(${p.hue}, 60%, 65%, 0)`);
            ctx.beginPath(); ctx.arc(p.x, p.y, glowR, 0, Math.PI * 2);
            ctx.fillStyle = glow; ctx.fill();

            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `hsla(${p.hue}, 75%, 48%, ${Math.min(1, p.alpha * 1.4)})`;
            ctx.fill();
        }
        requestAnimationFrame(drawGlow);
    }
    drawGlow();
        """

    else:
        # ── Dark: Rising Glow ─────────────────────────────────────────────
        # Tiny glowing particles slowly rise; some fade away while new ones appear
        anim_js = r"""
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width  = window.parent.innerWidth  || window.innerWidth;
        canvas.height = window.parent.innerHeight || window.innerHeight;
    }
    resize();
    window.parent.addEventListener('resize', resize);

    const MAX = 90;
    const particles = [];

    function spawn(spreadY) {
        return {
            x:        Math.random() * canvas.width,
            y:        spreadY !== undefined ? spreadY : canvas.height + 8,
            r:        1.2 + Math.random() * 2.8,
            vy:       0.45 + Math.random() * 1.0,
            vx:       (Math.random() - 0.5) * 0.25,
            hue:      200 + Math.random() * 90,
            life:     0,
            maxLife:  450 + Math.random() * 500,
            maxAlpha: 0.35 + Math.random() * 0.55,
            alpha:    0,
        };
    }

    for (let i = 0; i < MAX; i++) {
        const p = spawn(Math.random() * canvas.height);
        p.life = Math.random() * p.maxLife;
        particles.push(p);
    }

    function drawGlow() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#0D0F1A';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        while (particles.length < MAX) { particles.push(spawn()); }

        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.life++; p.x += p.vx; p.y -= p.vy;

            const fadeIn  = p.maxLife * 0.15;
            const fadeOut = p.maxLife * 0.85;
            if (p.life < fadeIn) {
                p.alpha = p.maxAlpha * (p.life / fadeIn);
            } else if (p.life < fadeOut) {
                p.alpha = p.maxAlpha;
            } else {
                p.alpha = p.maxAlpha * (1 - (p.life - fadeOut) / (p.maxLife - fadeOut));
            }

            if (p.life >= p.maxLife || p.y < -20) { particles.splice(i, 1); continue; }

            const glowR = p.r * 6;
            const glow  = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, glowR);
            glow.addColorStop(0,   `hsla(${p.hue}, 80%, 70%, ${p.alpha * 0.55})`);
            glow.addColorStop(0.4, `hsla(${p.hue}, 75%, 65%, ${p.alpha * 0.22})`);
            glow.addColorStop(1,   `hsla(${p.hue}, 70%, 60%, 0)`);
            ctx.beginPath(); ctx.arc(p.x, p.y, glowR, 0, Math.PI * 2);
            ctx.fillStyle = glow; ctx.fill();

            ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `hsla(${p.hue}, 90%, 85%, ${Math.min(1, p.alpha * 1.6)})`;
            ctx.fill();
        }
        requestAnimationFrame(drawGlow);
    }
    drawGlow();
        """

    # Inject canvas element into parent Streamlit DOM
    st.markdown(
        '<canvas id="ac-anim-canvas" '
        'style="position:fixed;top:0;left:0;width:100%;height:100%;'
        'z-index:0;pointer-events:none;"></canvas>',
        unsafe_allow_html=True,
    )

    # Run the animation JS via components.html (which properly executes scripts).
    # The script uses window.parent.document to reach the canvas in the parent page,
    # since components.html runs inside an iframe that shares origin with Streamlit.
    components.html(
        f"""
        <script>
        (function run() {{
            // Retry until parent canvas is available
            const canvas = window.parent.document.getElementById('ac-anim-canvas');
            if (!canvas) {{ setTimeout(run, 50); return; }}
            {anim_js}
        }})();
        </script>
        """,
        height=0,
        scrolling=False,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Section: Hero / Branding
# ─────────────────────────────────────────────────────────────────────────────

def _render_hero(t: dict):
    logo_data_uri = _get_logo_data_uri()
    st.markdown(clean_html(f"""
    <div class="ac-content" style="text-align:center; padding: 48px 24px 36px;">

        <!-- Logo — transparent background with base64 data URI -->
        <div style="margin-bottom:24px;">
            <img src="{logo_data_uri}"
                 alt="AscendCareer Logo"
                 style="height:125px; width:auto;
                        filter: drop-shadow(0 8px 24px rgba(79,70,229,0.30))
                                drop-shadow(0 2px 10px rgba(212,175,55,0.25));" />
        </div>

        <!-- Brand name — stylish Cinzel dual-tone (Ascend in indigo/lavender, Career in radiant gold) -->
        <div class="ac-brand-title"><span class="ac-brand-ascend">Ascend</span><span class="ac-brand-career">Career</span></div>

        <!-- Tagline 1: Ascend with Preparation -->
        <div style="
            font-family: 'Cinzel Decorative', 'Palatino Linotype', Georgia, serif;
            font-size: clamp(0.95rem, 2.0vw, 1.25rem);
            font-weight: 600;
            letter-spacing: 0.16em;
            color: {t['text_primary']};
            margin-top: 14px;
            text-transform: uppercase;
        ">Ascend with Preparation</div>

        <!-- Tagline 2: Where Preparation Meets Opportunity -->
        <div style="margin-top:12px;">
            <span style="
                display: inline-block;
                background: {t['gold_soft']};
                color: {t['gold']};
                border-radius: 50px;
                padding: 6px 26px;
                font-size: clamp(0.85rem, 1.6vw, 1.05rem);
                font-weight: 600;
                letter-spacing: 0.05em;
                font-style: italic;
            ">Where Preparation Meets Opportunity.</span>
        </div>

        <!-- Description: Bottle Green in light, Off-Cream in dark, larger font size -->
        <p style="margin:24px auto 0; max-width:680px;
                  font-family:'DM Sans','Inter',system-ui,sans-serif;
                  font-size:1.22rem; color:{t['text_secondary']}; line-height:1.90; font-weight: 500;">
            A comprehensive, AI-powered career-readiness platform — build, analyse, and refine
            your resume with smart suggestions, and prepare for interviews with realistic
            voice-to-voice practice, multi-persona panels, and adaptive difficulty.
        </p>

        <!-- Feature pills -->
        <div style="margin-top:22px; display:flex; flex-wrap:wrap;
                    gap:8px; justify-content:center;">
            <span class="ac-tag">📄 Resume Analysis</span>
            <span class="ac-tag">🏗️ Resume Builder</span>
            <span class="ac-tag">🎙️ Voice Interviews</span>
            <span class="ac-tag">👥 Multi-Panel Simulations</span>
            <span class="ac-tag">📊 Progress Analytics</span>
            <span class="ac-tag">🏆 6-Stage Ladder</span>
        </div>
    </div>
    """), unsafe_allow_html=True)






# ─────────────────────────────────────────────────────────────────────────────
# Section: Core Principle
# ─────────────────────────────────────────────────────────────────────────────

def _render_core_principle(t: dict):
    st.markdown(clean_html(f"""
    <div class="ac-content" style="padding: 0 24px;">
        <hr class="ac-divider" style="margin-bottom:32px;" />
        <div style="text-align:center; margin-bottom:20px;">
            <div class="ac-section-title">💡 Core Principle</div>
            <p style="font-family:'DM Sans','Inter',system-ui,sans-serif; font-size:1.12rem; color:{t['text_muted']}; margin-top:6px; font-weight: 500;">
                The philosophy behind everything AscendCareer does.
            </p>
        </div>
        <div class="ac-principle-block">
            {CORE_PRINCIPLE}
        </div>
    </div>
    """), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────

def _render_footer(t: dict):
    st.markdown(clean_html(f"""
    <div class="ac-content ac-footer-container" role="contentinfo">
        <div class="ac-footer-inner">
            <!-- 1 & 2. Left Group: Career Readiness Line & Copyright -->
            <div class="ac-footer-col ac-footer-left">
                <div class="ac-footer-readiness">AI-Powered Career Readiness Audit, Optimise, Train</div>
                <div class="ac-footer-copyright-group">
                    <div class="ac-footer-copy">© 2026 AscendCareer</div>
                    <div class="ac-footer-rights">All rights reserved</div>
                </div>
            </div>

            <!-- 3. Center Group: Brand Statement -->
            <div class="ac-footer-col ac-footer-center">
                <div class="ac-footer-brand">AscendCareer</div>
                <div class="ac-footer-tagline">Built for candidates serious about their next step.</div>
            </div>

            <!-- 4. Right Group: Creator Credit -->
            <div class="ac-footer-col ac-footer-right">
                <div class="ac-footer-creator">The brainchild of <span class="ac-footer-creator-name">ALANKRITA PAL</span> 💛</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Main render entry point
# ─────────────────────────────────────────────────────────────────────────────

def render_landing() -> dict:
    """
    Render the AscendCareer landing screen.

    Returns:
        dict with keys:
            - 'proceed' : bool  — True if user clicked Sign In
            - 'theme'   : str   — current theme key ('light' or 'dark')

    The caller (app.py) checks 'proceed' to move to the next step.
    """
    # ── State initialisation ─────────────────────────────────────────────────
    if "ac_theme" not in st.session_state:
        if "theme" in st.query_params and st.query_params.get("theme") in THEMES:
            st.session_state["ac_theme"] = st.query_params.get("theme")
        else:
            st.session_state["ac_theme"] = "light"      # Light is default

    theme_key = st.session_state["ac_theme"]
    t         = THEMES[theme_key]
    other_key = "dark" if theme_key == "light" else "light"

    # ── CSS ──────────────────────────────────────────────────────────────────
    # Global CSS is now injected in app.py

    # ── Animated background ──────────────────────────────────────────────────
    theme_icon_uri = _get_theme_icon_data_uri()
    _animated_background(theme_key, theme_icon_uri)

    # ── Navigation Drawer (if open) ──────────────────────────────────────────
    from modules.navigation.panel import render_navigation_drawer
    render_navigation_drawer(t)

    # ── Top Bar: Hamburger (Left), Spacer, Sign In (Right) & Sun/Moon Theme Switcher ──
    top_col_h, top_col_spacer, top_col_signin, top_col_theme = st.columns([6, 66, 19, 9])
    with top_col_h:
        if st.button(" ", key="ac_hamburger_btn", help="Open Main Navigation"):
            st.session_state["nav_open"] = not st.session_state.get("nav_open", False)
            st.rerun()
    with top_col_signin:
        top_signin_clicked = st.button("👤  Sign In", key="ac_top_signin_btn", type="primary", use_container_width=True)
    with top_col_theme:
        if st.button(" ", key="ac_theme_toggle_btn", help=f"Switch to {'Dark' if theme_key == 'light' else 'Light'} Theme"):
            st.session_state["ac_theme"] = other_key
            st.query_params["theme"] = other_key
            st.rerun()

    # ── Content ──────────────────────────────────────────────────────────────
    _render_hero(t)
    _render_core_principle(t)
    _render_footer(t)

    return {
        "proceed": top_signin_clicked,
        "theme":   theme_key,
    }

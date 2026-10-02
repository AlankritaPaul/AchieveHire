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
    p_svg = Path(__file__).resolve().parent.parent.parent / "assets" / "theme_icon.svg"
    if p_svg.exists():
        encoded = base64.b64encode(p_svg.read_bytes()).decode("ascii")
        return f"data:image/svg+xml;base64,{encoded}"
    p_png = Path(__file__).resolve().parent.parent.parent / "assets" / "theme_icon.png"
    if p_png.exists():
        encoded = base64.b64encode(p_png.read_bytes()).decode("ascii")
        return f"data:image/png;base64,{encoded}"
    return ""


_CACHED_SIGNIN_SYMBOL_URI = ""
def _get_signin_symbol_data_uri() -> str:
    """Return inline base64 data URI of the Sign In symbol."""
    global _CACHED_SIGNIN_SYMBOL_URI
    if _CACHED_SIGNIN_SYMBOL_URI:
        return _CACHED_SIGNIN_SYMBOL_URI
    p = Path(__file__).resolve().parent.parent.parent / "assets" / "signin_symbol.png"
    if p.exists():
        encoded = base64.b64encode(p.read_bytes()).decode("utf-8")
        _CACHED_SIGNIN_SYMBOL_URI = f"data:image/png;base64,{encoded}"
        return _CACHED_SIGNIN_SYMBOL_URI
    return ""


_CACHED_USER_VERIFIED_URI = ""
def _get_user_verified_symbol_uri() -> str:
    """Return inline base64 data URI of the verified user ID avatar symbol."""
    global _CACHED_USER_VERIFIED_URI
    if _CACHED_USER_VERIFIED_URI:
        return _CACHED_USER_VERIFIED_URI
    p = Path(__file__).resolve().parent.parent.parent / "assets" / "user_verified_symbol.png"
    if p.exists():
        encoded = base64.b64encode(p.read_bytes()).decode("utf-8")
        _CACHED_USER_VERIFIED_URI = f"data:image/png;base64,{encoded}"
        return _CACHED_USER_VERIFIED_URI
    return ""


_CACHED_SUMMIT_URI = ""
def _get_summit_data_uri() -> str:
    """Return inline base64 data URI of the dark theme summit left hero image."""
    global _CACHED_SUMMIT_URI
    if _CACHED_SUMMIT_URI:
        return _CACHED_SUMMIT_URI
    p = Path(__file__).resolve().parent.parent.parent / "assets" / "summit_left_dark.png"
    if p.exists():
        encoded = base64.b64encode(p.read_bytes()).decode("utf-8")
        _CACHED_SUMMIT_URI = f"data:image/png;base64,{encoded}"
        return _CACHED_SUMMIT_URI
    return ""


@st.dialog("🔒 Sign In Required")
def render_signin_required_dialog(feature_name: str = "this feature"):
    """Pop-up modal displayed when unauthenticated users try to access protected modules."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]
    signin_uri = _get_signin_symbol_data_uri()

    st.markdown(clean_html(f"""
    <div style="text-align:center; padding: 4px 0 16px;">
        <div style="margin-bottom:14px;">
            <img src="{signin_uri}" alt="Sign In Symbol" style="height:56px; width:auto; filter:drop-shadow(0 4px 14px rgba(37,99,235,0.30));" />
        </div>
        <h2 style="font-size:1.35rem; font-weight:800; color:{t['text_primary']} !important; margin:0 0 8px;">
            Sign In to Get Started
        </h2>
        <p style="font-size:0.96rem; color:{t['text_secondary']} !important; line-height:1.55; margin:0 auto; max-width:420px;">
            Welcome! Please sign in or create your candidate User ID to unlock full access to <span style="color:{t['accent']}; font-weight:700;">{feature_name}</span> and track your progress.
        </p>
    </div>
    """), unsafe_allow_html=True)

    c1, c2 = st.columns([60, 40])
    with c1:
        if st.button("🚀  Sign In / Generate ID", type="primary", use_container_width=True, key="dlg_btn_signin_action"):
            st.session_state["auth_popup_open"] = False
            st.session_state["ac_screen"] = "signin"
            st.rerun()
    with c2:
        if st.button("Cancel", use_container_width=True, key="dlg_btn_cancel_action"):
            st.session_state["auth_popup_open"] = False
            st.rerun()


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
        "text_primary": "#000000",          # Pure Black for all primary text, form titles, labels
        "text_secondary": "#000000",        # Pure Black for all options, tabs, radio buttons
        "text_muted": "#1F2937",            # Dark Charcoal for muted instructions
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
        "principle_title_color": "#D97706",
        "principle_title_glow": "none",
        "principle_sub_color": "#475569",
        "principle_text_color": "#5B21B6",
        "principle_text_glow": "none",
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
        "text_primary": "#FFFFFF",          # Pure White for all primary text, form titles, labels
        "text_secondary": "#FFFFFF",        # Pure White for all options, tabs, radio buttons
        "text_muted": "#F3F4F6",            # Bright Off-White for muted instructions
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
        "principle_title_color": "#FCD34D",
        "principle_title_glow": "0 0 16px rgba(252, 211, 77, 0.45)",
        "principle_sub_color": "#FDE68A",
        "principle_text_color": "#38BDF8",
        "principle_text_glow": "0 0 12px rgba(56, 189, 248, 0.28)",
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
    signin_symbol_uri = _get_signin_symbol_data_uri()
    user_verified_uri = _get_user_verified_symbol_uri()
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

    /* ── Sign In Button (Top Right — First Picture Symbol) ── */
    .st-key-ac_top_signin_btn {{
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: 100% !important;
        margin-right: -6px !important;
    }}

    .st-key-ac_top_signin_btn div[data-testid="stButton"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: flex-end !important;
    }}

    html body div.stApp div[data-testid="stElementContainer"].st-key-ac_top_signin_btn div[data-testid="stButton"] button,
    html body div.stApp div.st-key-ac_top_signin_btn div[data-testid="stButton"] button,
    html body div.stApp .st-key-ac_top_signin_btn button,
    html body div.stApp div[class*="st-key-ac_top_signin_btn"] button,
    .st-key-ac_top_signin_btn button,
    div[class*="st-key-ac_top_signin_btn"] button {{
        background: transparent url('{signin_symbol_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        background-image: url('{signin_symbol_uri}') !important;
        background-size: contain !important;
        border: none !important;
        border-width: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        cursor: pointer !important;
        transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        padding: 0 !important;
        min-height: 64px !important;
        height: 64px !important;
        width: 180px !important;
        min-width: 180px !important;
        max-width: 180px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    html body div.stApp div[data-testid="stElementContainer"].st-key-ac_top_signin_btn div[data-testid="stButton"] button:hover,
    html body div.stApp div.st-key-ac_top_signin_btn div[data-testid="stButton"] button:hover,
    html body div.stApp .st-key-ac_top_signin_btn button:hover,
    html body div.stApp div[class*="st-key-ac_top_signin_btn"] button:hover,
    .st-key-ac_top_signin_btn button:hover,
    div[class*="st-key-ac_top_signin_btn"] button:hover {{
        transform: scale(1.08) translateY(-1px) !important;
        background: transparent url('{signin_symbol_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        background-image: url('{signin_symbol_uri}') !important;
        box-shadow: none !important;
        border: none !important;
    }}

    html body div.stApp div[data-testid="stElementContainer"].st-key-ac_top_signin_btn div[data-testid="stButton"] button *,
    html body div.stApp div.st-key-ac_top_signin_btn div[data-testid="stButton"] button *,
    html body div.stApp .st-key-ac_top_signin_btn button *,
    .st-key-ac_top_signin_btn button * {{
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }}

    /* ── Verified User Badge (Top Right — Second Picture Symbol) ── */
    .st-key-ac_top_verified_user_btn {{
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: 100% !important;
    }}
    .st-key-ac_top_verified_user_btn div[data-testid="stButton"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: flex-end !important;
    }}
    .st-key-ac_top_verified_user_btn button {{
        background: {t["surface2"]} !important;
        border: 1.5px solid #10B981 !important;
        border-radius: 9999px !important;
        color: {t["text_primary"]} !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 8px 16px 8px 12px !important;
        min-height: 48px !important;
        height: 48px !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.20) !important;
        cursor: pointer !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}
    .st-key-ac_top_verified_user_btn button:hover {{
        transform: translateY(-2px) scale(1.03) !important;
        border-color: #059669 !important;
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35) !important;
    }}

    /* ── Instant Theme Toggle Button (Exact reference icon, 100% transparent) ── */
    .st-key-ac_theme_toggle_btn {{
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        width: auto !important;
    }}

    .st-key-ac_theme_toggle_btn div[data-testid="stButton"] {{
        display: inline-flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 56px !important;
        height: 56px !important;
    }}

    .st-key-ac_theme_toggle_btn button,
    .st-key-ac_theme_toggle_btn button:hover,
    .st-key-ac_theme_toggle_btn button:focus,
    .st-key-ac_theme_toggle_btn button:focus-visible,
    .st-key-ac_theme_toggle_btn button:active,
    .st-key-ac_theme_toggle_btn button:disabled,
    .st-key-ac_theme_toggle_btn button[disabled] {{
        width: 56px !important;
        height: 56px !important;
        min-width: 56px !important;
        max-width: 56px !important;
        min-height: 56px !important;
        max-height: 56px !important;
        background: transparent url('{theme_icon_uri}') no-repeat center center / contain !important;
        background-color: transparent !important;
        background-image: url('{theme_icon_uri}') !important;
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
        opacity: 1 !important;
        visibility: visible !important;
        filter: none !important;
        transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }}

    .st-key-ac_theme_toggle_btn button:hover {{
        transform: scale(1.15) !important;
    }}

    /* Completely hide any inner text / icon inside ONLY the theme toggle button */
    .st-key-ac_theme_toggle_btn button *,
    .st-key-ac_theme_toggle_btn button:hover *,
    .st-key-ac_theme_toggle_btn button:focus *,
    .st-key-ac_theme_toggle_btn button:active * {{
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

    /* ── Right-Side Perpendicular Oval Length Boxes ───────────────────── */
    .ac-right-features-rail {{
        position: fixed;
        top: 56%;
        right: 28px;
        transform: translateY(-38%);
        display: flex;
        flex-direction: column;
        gap: 14px; /* Comfortable spacing between perpendicular boxes */
        z-index: 90;
        pointer-events: auto;
    }}
    .ac-feature-oval-pill {{
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: {t["surface"]} !important;
        border: 1.5px solid {t["border"]} !important;
        border-radius: 9999px !important;
        padding: 8px 18px 8px 10px !important;
        box-shadow: {t["card_shadow"]} !important;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: default;
        text-align: left;
    }}
    .ac-feature-oval-pill:hover {{
        transform: translateX(-6px);
        border-color: {t["accent"]} !important;
        background: {t["surface2"]} !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.18) !important;
    }}
    .ac-feature-oval-icon {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: {t["accent_soft"]};
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.05rem;
        flex-shrink: 0;
    }}
    .ac-feature-oval-text {{
        font-family: 'DM Sans', 'Inter', system-ui, sans-serif !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        color: {t["text_primary"]} !important;
        letter-spacing: 0.01em;
        white-space: nowrap;
    }}

    @media (max-width: 1024px) {{
        .ac-right-features-rail {{
            position: static;
            transform: none;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: center;
            margin: 24px auto 0;
            right: auto;
            top: auto;
        }}
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
    .ac-principle-title {{
        font-family: 'Playfair Display', 'Georgia', 'Times New Roman', serif !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: {t["principle_title_color"]} !important;
        text-shadow: {t["principle_title_glow"]} !important;
        letter-spacing: -0.01em !important;
        margin: 0 0 8px !important;
    }}

    .ac-principle-sub {{
        font-family: 'DM Sans', 'Inter', system-ui, sans-serif !important;
        font-size: 1.14rem !important;
        color: {t["principle_sub_color"]} !important;
        margin-top: 6px !important;
        font-weight: 500 !important;
    }}

    .ac-principle-block {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 16px 0 !important;
        max-width: 860px !important;
        margin: 0 auto !important;
        font-family: 'DM Sans', 'Inter', system-ui, -apple-system, sans-serif !important;
        font-size: 1.18rem !important;
        line-height: 1.95 !important;
        color: {t["principle_text_color"]} !important;
        text-shadow: {t["principle_text_glow"]} !important;
        text-align: justify !important;
        text-justify: inter-word !important;
        font-weight: 500 !important;
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
    }}

    /* ── Streamlit Generic & Secondary Button Overrides (High Visibility in Dark & Light) ── */
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) div[data-testid="stButton"] > button:not([kind="primary"]),
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[data-testid="baseButton-secondary"],
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[kind="secondary"] {{
        background: {"#1C2035" if is_dark else "#FFFFFF"} !important;
        background-color: {"#1C2035" if is_dark else "#FFFFFF"} !important;
        color: {"#FFFFFF" if is_dark else "#000000"} !important;
        border: 1.5px solid {"#2D3450" if is_dark else "#DDE3F0"} !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.18s ease !important;
    }}
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) div[data-testid="stButton"] > button:not([kind="primary"]):hover,
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[data-testid="baseButton-secondary"]:hover,
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[kind="secondary"]:hover {{
        background: {"#252B48" if is_dark else "#F0F4FF"} !important;
        background-color: {"#252B48" if is_dark else "#F0F4FF"} !important;
        border-color: {"#818CF8" if is_dark else "#4F46E5"} !important;
        color: {"#FFFFFF" if is_dark else "#4F46E5"} !important;
        box-shadow: 0 4px 14px {"rgba(129, 140, 248, 0.25)" if is_dark else "rgba(79, 70, 229, 0.15)"} !important;
    }}
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) div[data-testid="stButton"] > button:not([kind="primary"]) p,
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) div[data-testid="stButton"] > button:not([kind="primary"]) span,
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) div[data-testid="stButton"] > button:not([kind="primary"]) div,
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[data-testid="baseButton-secondary"] p,
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[data-testid="baseButton-secondary"] span,
    div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[data-testid="baseButton-secondary"] div {{
        color: {"#FFFFFF" if is_dark else "#000000"} !important;
        -webkit-text-fill-color: {"#FFFFFF" if is_dark else "#000000"} !important;
        font-weight: 600 !important;
        font-size: 1.02rem !important;
    }}

    /* ── Streamlit Primary Button Overrides ── */
    div[data-testid="stButton"] > button[kind="primary"],
    button[data-testid="baseButton-primary"],
    button[kind="primary"] {{
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.40) !important;
    }}
    div[data-testid="stButton"] > button[kind="primary"] p,
    div[data-testid="stButton"] > button[kind="primary"] span,
    div[data-testid="stButton"] > button[kind="primary"] div,
    button[data-testid="baseButton-primary"] p,
    button[data-testid="baseButton-primary"] span,
    button[data-testid="baseButton-primary"] div {{
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }}
    div[data-testid="stButton"] > button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.55) !important;
        transform: translateY(-1px) !important;
    }}

    /* ── Streamlit Border Containers ── */
    div[data-testid="stVerticalBlockBorderWrapper"] > div {{
        background: {"#141827" if is_dark else "#FFFFFF"} !important;
        background-color: {"#141827" if is_dark else "#FFFFFF"} !important;
        border: 1.5px solid {t["border"]} !important;
        border-radius: 12px !important;
        box-shadow: {t["card_shadow"]} !important;
    }}

    /* ── Streamlit Dialogs & Modals ── */
    div[data-testid="stModal"],
    div[data-baseweb="modal"],
    div[role="dialog"],
    div[data-testid="stDialog"] {{
        background-color: {"#141827" if is_dark else "#FFFFFF"} !important;
        border: 1.5px solid {t["border"]} !important;
        border-radius: 14px !important;
        color: {t["text_primary"]} !important;
    }}

    /* ── Streamlit Radio Buttons Overrides (Targeting ALL level paragraphs, labels & spans) ── */
    div[data-testid="stRadio"],
    div[data-testid="stRadio"] *,
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label *,
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] [data-baseweb="radio"] *,
    div[data-testid="stRadio"] [data-baseweb="radio"] p,
    div[data-testid="stRadio"] [data-baseweb="radio"] span,
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] *,
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p,
    div[role="radiogroup"],
    div[role="radiogroup"] *,
    div[role="radiogroup"] label,
    div[role="radiogroup"] label *,
    div[role="radiogroup"] label p,
    div[role="radiogroup"] p,
    div[role="radiogroup"] span {{
        color: {t["text_primary"]} !important;
        font-weight: 600 !important;
        font-size: 1.12rem !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    /* ── Streamlit Tabs Overrides (Active & Inactive headers, paragraphs & spans) ── */
    [data-testid="stTabs"],
    [data-testid="stTabs"] *,
    [data-testid="stTabs"] button,
    [data-testid="stTabs"] button *,
    [data-testid="stTabs"] button p,
    [data-testid="stTabs"] button span,
    [data-testid="stTabs"] [data-testid="stMarkdownContainer"] *,
    [data-testid="stTabs"] [data-testid="stMarkdownContainer"] p,
    button[data-baseweb="tab"],
    button[data-baseweb="tab"] *,
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span,
    div[data-baseweb="tab-list"] button,
    div[data-baseweb="tab-list"] button *,
    div[data-baseweb="tab-list"] button p {{
        color: {t["text_secondary"]} !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    /* Active Tab Header */
    [data-testid="stTabs"] button[aria-selected="true"],
    [data-testid="stTabs"] button[aria-selected="true"] *,
    [data-testid="stTabs"] button[aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"],
    button[data-baseweb="tab"][aria-selected="true"] *,
    button[data-baseweb="tab"][aria-selected="true"] p,
    div[data-baseweb="tab-list"] button[aria-selected="true"],
    div[data-baseweb="tab-list"] button[aria-selected="true"] *,
    div[data-baseweb="tab-list"] button[aria-selected="true"] p {{
        color: {"#FCD34D" if is_dark else "#000000"} !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        opacity: 1 !important;
    }}

    /* ── Form Labels, Selectboxes, Inputs & Captions ── */
    [data-testid="stTextInput"] label,
    [data-testid="stTextInput"] label *,
    [data-testid="stTextInput"] label p,
    [data-testid="stTextArea"] label,
    [data-testid="stTextArea"] label *,
    [data-testid="stTextArea"] label p,
    [data-testid="stSelectbox"] label,
    [data-testid="stSelectbox"] label *,
    [data-testid="stSelectbox"] label p,
    .stTextInput label,
    .stTextInput label p,
    .stTextArea label,
    .stTextArea label p {{
        color: {t["text_primary"]} !important;
        font-weight: 700 !important;
        font-size: 1.12rem !important;
        opacity: 1 !important;
    }}

    /* Captions */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] *,
    [data-testid="stCaptionContainer"] p,
    .stCaption,
    .stCaption * {{
        color: {t["text_muted"]} !important;
        font-size: 1.02rem !important;
        font-weight: 500 !important;
        opacity: 1 !important;
    }}

    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div {{
        background-color: {"#1C2035" if is_dark else "#FFFFFF"} !important;
        border-color: {t["border"]} !important;
        border-radius: 8px !important;
    }}

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] * {{
        color: {"#FFFFFF" if is_dark else "#000000"} !important;
        -webkit-text-fill-color: {"#FFFFFF" if is_dark else "#000000"} !important;
        background-color: transparent !important;
        font-weight: 600 !important;
        font-size: 1.08rem !important;
    }}
    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {{
        color: {"#94A3B8" if is_dark else "#64748B"} !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
        opacity: 1 !important;
    }}

    /* Selectbox dropdown menu & options */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"] {{
        background-color: {"#141827" if is_dark else "#FFFFFF"} !important;
        border: 1px solid {t["border"]} !important;
    }}
    li[role="option"] {{
        background-color: {"#141827" if is_dark else "#FFFFFF"} !important;
        color: {t["text_primary"]} !important;
    }}
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {{
        background-color: {"#1C2035" if is_dark else "#F0F4FF"} !important;
        color: {"#818CF8" if is_dark else "#4F46E5"} !important;
    }}

    /* Pills & Segmented Controls */
    div[data-testid="stPills"] button,
    div[data-testid="stSegmentedControl"] button {{
        background: {"#1C2035" if is_dark else "#FFFFFF"} !important;
        border: 1.5px solid {"#2D3450" if is_dark else "#DDE3F0"} !important;
        color: {"#FFFFFF" if is_dark else "#000000"} !important;
        border-radius: 9999px !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stPills"] button[aria-selected="true"],
    div[data-testid="stSegmentedControl"] button[aria-selected="true"] {{
        background: #4F46E5 !important;
        border-color: #818CF8 !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] div {{
        color: inherit;
        opacity: 1 !important;
    }}
    </style>
    """), unsafe_allow_html=True)

    # ── Parent DOM Style Injection (Guarantees 100% white/black contrast for BaseWeb/Emotion elements) ──
    target_color = "#FFFFFF" if is_dark else "#000000"
    active_tab_color = "#FCD34D" if is_dark else "#000000"
    muted_color = "#F3F4F6" if is_dark else "#1F2937"

    input_bg = "#1C2035" if is_dark else "#FFFFFF"
    input_text = "#FFFFFF" if is_dark else "#000000"
    input_placeholder = "#94A3B8" if is_dark else "#64748B"
    input_border = "#2D3450" if is_dark else "#D1D5DB"

    btn_sec_bg = "#1C2035" if is_dark else "#FFFFFF"
    btn_sec_text = "#FFFFFF" if is_dark else "#000000"
    btn_sec_border = "#2D3450" if is_dark else "#D1D5DB"
    btn_sec_hover_bg = "#252B48" if is_dark else "#F0F4FF"
    btn_sec_hover_border = "#818CF8" if is_dark else "#4F46E5"

    components.html(f"""
    <script>
    (function run() {{
        const parentDoc = window.parent.document;
        if (!parentDoc || !parentDoc.head) {{ setTimeout(run, 50); return; }}
        
        let styleEl = parentDoc.getElementById('ac-parent-force-styles');
        if (!styleEl) {{
            styleEl = parentDoc.createElement('style');
            styleEl.id = 'ac-parent-force-styles';
            parentDoc.head.appendChild(styleEl);
        }}

        styleEl.textContent = `
            /* Force Generic / Secondary Buttons Contrast */
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) div[data-testid="stButton"] > button:not([kind="primary"]),
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[data-testid="baseButton-secondary"],
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[kind="secondary"] {{
                background-color: {btn_sec_bg} !important;
                background: {btn_sec_bg} !important;
                color: {btn_sec_text} !important;
                border: 1.5px solid {btn_sec_border} !important;
                border-radius: 8px !important;
            }}
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) div[data-testid="stButton"] > button:not([kind="primary"]):hover,
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[data-testid="baseButton-secondary"]:hover,
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[kind="secondary"]:hover {{
                background-color: {btn_sec_hover_bg} !important;
                background: {btn_sec_hover_bg} !important;
                border-color: {btn_sec_hover_border} !important;
                color: {btn_sec_text} !important;
            }}
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) div[data-testid="stButton"] > button:not([kind="primary"]) p,
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) div[data-testid="stButton"] > button:not([kind="primary"]) span,
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[data-testid="baseButton-secondary"] p,
            div[data-testid="stElementContainer"]:not(.st-key-ac_top_signin_btn):not(.st-key-ac_theme_toggle_btn):not(.st-key-ac_hamburger_btn):not(.st-key-ac_top_verified_user_btn):not(.st-key-nav_close_btn) button[data-testid="baseButton-secondary"] span {{
                color: {btn_sec_text} !important;
                -webkit-text-fill-color: {btn_sec_text} !important;
            }}

            /* Force Radio Button Options Visibility */
            div[data-testid="stRadio"] *,
            div[data-testid="stRadio"] p,
            div[data-testid="stRadio"] span,
            div[data-testid="stRadio"] label,
            div[data-testid="stRadio"] div,
            div[data-baseweb="radio"] *,
            div[data-baseweb="radio"] p,
            div[data-baseweb="radio"] span,
            div[data-baseweb="radio"] label,
            label[data-baseweb="radio"] *,
            label[data-baseweb="radio"] p,
            label[data-baseweb="radio"] span,
            div[role="radiogroup"] *,
            div[role="radiogroup"] p,
            div[role="radiogroup"] span,
            div[role="radiogroup"] label {{
                color: {target_color} !important;
                fill: {target_color} !important;
                font-size: 1.12rem !important;
                font-weight: 600 !important;
                opacity: 1 !important;
                visibility: visible !important;
            }}

            /* Force Tab Headers Visibility (Active & Inactive) */
            [data-testid="stTabs"] *,
            [data-testid="stTabs"] p,
            [data-testid="stTabs"] span,
            [data-testid="stTabs"] button,
            button[data-baseweb="tab"],
            button[data-baseweb="tab"] *,
            button[data-baseweb="tab"] p,
            button[data-baseweb="tab"] span,
            div[data-baseweb="tab-list"] *,
            div[data-baseweb="tab-list"] p,
            div[data-baseweb="tab-list"] button {{
                color: {target_color} !important;
                fill: {target_color} !important;
                font-size: 1.15rem !important;
                font-weight: 600 !important;
                opacity: 1 !important;
                visibility: visible !important;
            }}

            /* Force Active Tab Color */
            button[data-baseweb="tab"][aria-selected="true"],
            button[data-baseweb="tab"][aria-selected="true"] *,
            button[data-baseweb="tab"][aria-selected="true"] p,
            [data-testid="stTabs"] button[aria-selected="true"],
            [data-testid="stTabs"] button[aria-selected="true"] * {{
                color: {active_tab_color} !important;
                font-weight: 700 !important;
            }}

            /* Force Captions & Muted Text */
            [data-testid="stCaptionContainer"],
            [data-testid="stCaptionContainer"] *,
            [data-testid="stCaptionContainer"] p,
            .stCaption,
            .stCaption * {{
                color: {muted_color} !important;
                font-size: 1.02rem !important;
                font-weight: 500 !important;
                opacity: 1 !important;
            }}

            /* Force Form Labels */
            [data-testid="stTextInput"] label,
            [data-testid="stTextInput"] label *,
            [data-testid="stTextArea"] label,
            [data-testid="stTextArea"] label *,
            [data-testid="stSelectbox"] label,
            [data-testid="stSelectbox"] label * {{
                color: {target_color} !important;
                font-weight: 700 !important;
                font-size: 1.12rem !important;
                opacity: 1 !important;
            }}

            /* Force Input Fields Background, Text Color & Webkit Fill Color */
            div[data-baseweb="input"],
            div[data-baseweb="textarea"],
            div[data-baseweb="select"] > div {{
                background-color: {input_bg} !important;
                border-color: {input_border} !important;
                border-radius: 8px !important;
            }}

            div[data-baseweb="input"] input,
            div[data-baseweb="textarea"] textarea,
            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea,
            div[data-baseweb="select"] * {{
                color: {input_text} !important;
                -webkit-text-fill-color: {input_text} !important;
                background-color: {input_bg} !important;
                font-weight: 600 !important;
                font-size: 1.08rem !important;
            }}

            div[data-baseweb="input"] input::placeholder,
            div[data-baseweb="textarea"] textarea::placeholder,
            [data-testid="stTextInput"] input::placeholder,
            [data-testid="stTextArea"] textarea::placeholder {{
                color: {input_placeholder} !important;
                -webkit-text-fill-color: {input_placeholder} !important;
                font-weight: 500 !important;
                font-size: 1.05rem !important;
                opacity: 1 !important;
            }}

            /* Ultra-High Specificity Theme Toggle Button Protection (Sun/Moon Split Icon on 100% Transparent BG) */
            html body div.stApp div[data-testid="stElementContainer"].st-key-ac_theme_toggle_btn div[data-testid="stButton"] button,
            html body div.stApp div.st-key-ac_theme_toggle_btn div[data-testid="stButton"] button,
            html body div.stApp .st-key-ac_theme_toggle_btn button,
            html body div.stApp div[class*="st-key-ac_theme_toggle_btn"] button,
            .st-key-ac_theme_toggle_btn button,
            div[class*="st-key-ac_theme_toggle_btn"] button,
            .st-key-ac_theme_toggle_btn button:hover,
            .st-key-ac_theme_toggle_btn button:focus,
            .st-key-ac_theme_toggle_btn button:focus-visible,
            .st-key-ac_theme_toggle_btn button:active,
            .st-key-ac_theme_toggle_btn button:disabled,
            .st-key-ac_theme_toggle_btn button[disabled] {{
                background: transparent url('{theme_icon_uri}') no-repeat center center / contain !important;
                background-color: transparent !important;
                background-image: url('{theme_icon_uri}') !important;
                background-size: contain !important;
                border: none !important;
                border-width: 0 !important;
                border-radius: 50% !important;
                box-shadow: none !important;
                outline: none !important;
                opacity: 1 !important;
                visibility: visible !important;
                filter: none !important;
                width: 56px !important;
                height: 56px !important;
                min-width: 56px !important;
                max-width: 56px !important;
                min-height: 56px !important;
                max-height: 56px !important;
            }}

            html body div.stApp div[data-testid="stElementContainer"].st-key-ac_theme_toggle_btn div[data-testid="stButton"] button *,
            html body div.stApp div.st-key-ac_theme_toggle_btn div[data-testid="stButton"] button *,
            html body div.stApp .st-key-ac_theme_toggle_btn button *,
            html body div.stApp div[class*="st-key-ac_theme_toggle_btn"] button *,
            .st-key-ac_theme_toggle_btn button *,
            div[class*="st-key-ac_theme_toggle_btn"] button *,
            .st-key-ac_theme_toggle_btn button:hover *,
            .st-key-ac_theme_toggle_btn button:focus *,
            .st-key-ac_theme_toggle_btn button:active * {{
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
            }}

            /* Core Principle Golden Heading & Soft Neon Text Override (No Background Box) */
            .ac-principle-title {{
                color: {t["principle_title_color"]} !important;
                text-shadow: {t["principle_title_glow"]} !important;
            }}
            .ac-principle-sub {{
                color: {t["principle_sub_color"]} !important;
            }}
            .ac-principle-block {{
                background: transparent !important;
                background-color: transparent !important;
                color: {t["principle_text_color"]} !important;
                text-shadow: {t["principle_text_glow"]} !important;
                text-align: justify !important;
                text-justify: inter-word !important;
                border: none !important;
                box-shadow: none !important;
            }}
        `;
    }})();
    </script>
    """, height=0, scrolling=False)


# ─────────────────────────────────────────────────────────────────────────────
# Animated Backgrounds
# ─────────────────────────────────────────────────────────────────────────────

def _animated_background(theme_key: str, theme_icon_uri: str = ""):
    """Injects a canvas-based animated background per theme."""

    if theme_key == "light":
        # ── Light: Realistic Rear-View Ladder Climbing Scene ──────────────
        # Grounded back-view candidate (matching user photo) climbing the left ladder.
        # Hand only arrives when person reaches the top to support the ladder switch,
        # strictly contained on the left side to prevent any overlap with center logo/text.
        anim_js = r"""
    const ctx = canvas.getContext('2d');

    if (window.parent._ac_anim_req) {
        window.parent.cancelAnimationFrame(window.parent._ac_anim_req);
    }

    function resize() {
        canvas.width  = window.parent.innerWidth  || window.innerWidth;
        canvas.height = window.parent.innerHeight || window.innerHeight;
    }
    resize();
    window.parent.addEventListener('resize', resize);

    // Drifting background clouds (subtle, soft)
    const clouds = [
        { x: 0.04, y: 0.08, s: 1.0, speed: 0.00010 },
        { x: 0.35, y: 0.15, s: 1.3, speed: 0.00008 },
        { x: 0.68, y: 0.06, s: 0.85, speed: 0.00012 },
        { x: 0.08, y: 0.48, s: 1.1, speed: 0.00009 },
        { x: 0.75, y: 0.38, s: 1.4, speed: 0.00007 },
        { x: 0.42, y: 0.68, s: 0.8, speed: 0.00010 },
    ];

    function drawCloud(cx, cy, scale) {
        ctx.fillStyle = 'rgba(220, 235, 252, 0.70)';
        ctx.beginPath();
        const r = 24 * scale;
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.arc(cx + r * 0.95, cy - r * 0.35, r * 1.15, 0, Math.PI * 2);
        ctx.arc(cx + r * 1.85, cy, r * 0.85, 0, Math.PI * 2);
        ctx.arc(cx + r * 0.95, cy + r * 0.22, r * 0.95, 0, Math.PI * 2);
        ctx.fill();
    }

    let startTime = performance.now();

    function drawScene(now) {
        const elapsed = (now - startTime) / 1000;
        const loopDuration = 11.0; // 11-second cycle
        const progress = (elapsed % loopDuration) / loopDuration;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Sky background
        const bgGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
        bgGrad.addColorStop(0, '#EBF4FD');
        bgGrad.addColorStop(0.45, '#F3F8FE');
        bgGrad.addColorStop(1, '#FAFCFF');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        const W = canvas.width;
        const H = canvas.height;
        const scale = Math.min(Math.max(W / 1280, 0.75), 1.20);

        // 1. Draw Clouds
        clouds.forEach(c => {
            c.x = (c.x + c.speed) % 1.25;
            const drawX = (c.x > 1.1 ? c.x - 1.2 : c.x) * W;
            drawCloud(drawX, c.y * H, c.s * scale);
        });

        // 2. Strict Left-Side Alignment (Zero overlap with center content)
        const sceneLeft = Math.max(28 * scale, W * 0.04);
        const ladderW = 42 * scale;
        const ladderGap = 58 * scale;
        const rungDist = 28 * scale;
        const railThick = 4.5 * scale;
        const rungThick = 3.5 * scale;
        const ladderColor = '#50282E';

        const leftLadderX = sceneLeft;
        const leftLadderBottom = H + 40;
        const leftLadderTop = H * 0.38;

        const rightLadderX = leftLadderX + ladderW + ladderGap;
        const rightLadderBottom = H * 0.42;
        const rightLadderTop = -40;

        // Draw Left Ladder
        ctx.fillStyle = ladderColor;
        ctx.strokeStyle = ladderColor;
        ctx.lineWidth = railThick;
        ctx.beginPath();
        ctx.moveTo(leftLadderX, leftLadderBottom);
        ctx.lineTo(leftLadderX, leftLadderTop);
        ctx.moveTo(leftLadderX + ladderW, leftLadderBottom);
        ctx.lineTo(leftLadderX + ladderW, leftLadderTop);
        ctx.stroke();

        ctx.lineWidth = rungThick;
        for (let y = leftLadderBottom; y >= leftLadderTop + 4; y -= rungDist) {
            ctx.beginPath();
            ctx.moveTo(leftLadderX, y);
            ctx.lineTo(leftLadderX + ladderW, y);
            ctx.stroke();
        }

        // Draw Right Ladder
        ctx.lineWidth = railThick;
        ctx.beginPath();
        ctx.moveTo(rightLadderX, rightLadderBottom);
        ctx.lineTo(rightLadderX, rightLadderTop);
        ctx.moveTo(rightLadderX + ladderW, rightLadderBottom);
        ctx.lineTo(rightLadderX + ladderW, rightLadderTop);
        ctx.stroke();

        ctx.lineWidth = rungThick;
        for (let y = rightLadderBottom; y >= rightLadderTop - 10; y -= rungDist) {
            ctx.beginPath();
            ctx.moveTo(rightLadderX, y);
            ctx.lineTo(rightLadderX + ladderW, y);
            ctx.stroke();
        }

        // 3. Ascend Career Supportive Hand (ONLY enters when person reaches the top!)
        // Appears at progress 0.36, fully in place by 0.46, stays through 0.72, retreats by 0.82
        let handSlide = 0; // 0 = fully hidden to right of scene, 1 = in place
        if (progress >= 0.36 && progress < 0.46) {
            // Smooth slide-in
            handSlide = (progress - 0.36) / 0.10;
        } else if (progress >= 0.46 && progress < 0.72) {
            // Fully supporting
            handSlide = 1.0;
        } else if (progress >= 0.72 && progress < 0.82) {
            // Smooth retreat
            handSlide = 1.0 - (progress - 0.72) / 0.10;
        } else {
            handSlide = 0;
        }

        if (handSlide > 0.01) {
            ctx.save();
            const handTargetX = rightLadderX - 22 * scale;
            const handTargetY = rightLadderBottom + 12 * scale;
            const handOffscreenX = handTargetX + 220 * scale;
            const currentHandX = handOffscreenX - handSlide * (handOffscreenX - handTargetX);
            const handAlpha = Math.min(1.0, handSlide * 1.5);
            ctx.globalAlpha = handAlpha;

            const armEndX = currentHandX + 125 * scale;

            // Arm Sleeve (Confined strictly to local left scene width)
            ctx.fillStyle = '#112240';
            ctx.beginPath();
            ctx.moveTo(armEndX, handTargetY - 22 * scale);
            ctx.lineTo(currentHandX + 90 * scale, handTargetY - 18 * scale);
            ctx.lineTo(currentHandX + 85 * scale, handTargetY + 38 * scale);
            ctx.lineTo(armEndX, handTargetY + 44 * scale);
            ctx.closePath();
            ctx.fill();

            // White Cuff
            ctx.fillStyle = '#FFFFFF';
            ctx.beginPath();
            ctx.moveTo(currentHandX + 90 * scale, handTargetY - 18 * scale);
            ctx.lineTo(currentHandX + 80 * scale, handTargetY - 16 * scale);
            ctx.lineTo(currentHandX + 75 * scale, handTargetY + 36 * scale);
            ctx.lineTo(currentHandX + 85 * scale, handTargetY + 38 * scale);
            ctx.closePath();
            ctx.fill();

            // Palm & Supporting Platform Fingers
            ctx.fillStyle = '#F4BA94';
            ctx.beginPath();
            ctx.moveTo(currentHandX + 80 * scale, handTargetY - 16 * scale);
            ctx.bezierCurveTo(currentHandX + 58 * scale, handTargetY - 24 * scale, currentHandX + 38 * scale, handTargetY - 30 * scale, currentHandX + 26 * scale, handTargetY - 22 * scale);
            ctx.bezierCurveTo(currentHandX + 30 * scale, handTargetY - 12 * scale, currentHandX + 46 * scale, handTargetY - 8 * scale, currentHandX + 54 * scale, handTargetY - 4 * scale);
            ctx.bezierCurveTo(currentHandX + 26 * scale, handTargetY - 8 * scale, currentHandX + 4 * scale, handTargetY - 6 * scale, currentHandX - 16 * scale, handTargetY + 4 * scale);
            ctx.bezierCurveTo(currentHandX - 22 * scale, handTargetY + 12 * scale, currentHandX - 14 * scale, handTargetY + 22 * scale, currentHandX + 4 * scale, handTargetY + 24 * scale);
            ctx.bezierCurveTo(currentHandX + 34 * scale, handTargetY + 28 * scale, currentHandX + 64 * scale, handTargetY + 32 * scale, currentHandX + 75 * scale, handTargetY + 36 * scale);
            ctx.closePath();
            ctx.fill();

            // Crease details
            ctx.strokeStyle = '#D89972';
            ctx.lineWidth = 1.6 * scale;
            ctx.beginPath();
            ctx.moveTo(currentHandX - 2 * scale, handTargetY + 12 * scale);
            ctx.lineTo(currentHandX + 32 * scale, handTargetY + 10 * scale);
            ctx.moveTo(currentHandX - 8 * scale, handTargetY + 19 * scale);
            ctx.lineTo(currentHandX + 28 * scale, handTargetY + 18 * scale);
            ctx.stroke();

            // Subtle empowering glow
            const handGlow = ctx.createRadialGradient(currentHandX + 18 * scale, handTargetY + 4 * scale, 0, currentHandX + 18 * scale, handTargetY + 4 * scale, 65 * scale);
            handGlow.addColorStop(0, 'rgba(79, 70, 229, 0.20)');
            handGlow.addColorStop(0.5, 'rgba(212, 175, 55, 0.15)');
            handGlow.addColorStop(1, 'rgba(255, 255, 255, 0)');
            ctx.fillStyle = handGlow;
            ctx.beginPath();
            ctx.arc(currentHandX + 18 * scale, handTargetY + 4 * scale, 65 * scale, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();
        }

        // 4. Character State Machine (Grounded Rear-View Climber)
        let climberCenterX = leftLadderX + ladderW * 0.5;
        let climberY = H * 0.90;
        let climbCycle = 0;
        let isTransferring = false;
        let charOpacity = 1.0;

        if (progress < 0.38) {
            // Climbing Left Ladder (Hard-working steady upward progress)
            const p = progress / 0.38;
            climberCenterX = leftLadderX + ladderW * 0.5;
            climberY = (H * 0.92) - p * (H * 0.92 - (leftLadderTop + 30 * scale));
            climbCycle = (progress * 14) % 1;
        } else if (progress < 0.48) {
            // At Top of Left Ladder (Waiting for support)
            climberCenterX = leftLadderX + ladderW * 0.5;
            climberY = leftLadderTop + 30 * scale;
            climbCycle = 0;
        } else if (progress < 0.68) {
            // Stepping Across on the Hand & Right Ladder Base
            const p = (progress - 0.48) / 0.20;
            const startX = leftLadderX + ladderW * 0.5;
            const targetX = rightLadderX + ladderW * 0.5;
            climberCenterX = startX + p * (targetX - startX);
            climberY = (leftLadderTop + 30 * scale) - Math.sin(p * Math.PI) * (10 * scale) - p * (16 * scale);
            isTransferring = true;
            climbCycle = p;
        } else if (progress < 0.92) {
            // Climbing Right Ladder upward into the clouds
            const p = (progress - 0.68) / 0.24;
            climberCenterX = rightLadderX + ladderW * 0.5;
            climberY = (rightLadderBottom + 4 * scale) - p * (rightLadderBottom + 4 * scale - (-35));
            climbCycle = ((progress - 0.68) * 14) % 1;
        } else {
            // Fade out at upper sky before reset
            const p = (progress - 0.92) / 0.08;
            charOpacity = Math.max(0, 1 - p);
            climberCenterX = rightLadderX + ladderW * 0.5;
            climberY = -35 - p * 20;
        }

        ctx.save();
        ctx.globalAlpha = charOpacity;

        // 5. Draw Person from REAR VIEW (Back View matching user photo)
        const pScale = 0.92 * scale;
        const stride = Math.sin(climbCycle * Math.PI * 2);

        // Body center points
        const bodyX = climberCenterX;
        const bodyY = climberY;

        // ── LEGS (Rear View with realistic knee bending outward like the photo) ──
        const legThickness = 7.0 * pScale;
        const hipY = bodyY + 18 * pScale;
        const leftHipX = bodyX - 7 * pScale;
        const rightHipX = bodyX + 7 * pScale;

        // One leg is straight support, other leg knee flares out and lifts (matching reference photo)
        const leftLegLift = isTransferring ? 0.3 : stride;
        const rightLegLift = isTransferring ? -0.3 : -stride;

        // Left Leg (Rear view)
        const leftKneeX = leftHipX - (leftLegLift > 0 ? 12 * pScale : 3 * pScale);
        const leftKneeY = hipY + (leftLegLift > 0 ? 14 * pScale : 22 * pScale);
        const leftFootX = leftHipX - (leftLegLift > 0 ? 4 * pScale : 2 * pScale);
        const leftFootY = leftKneeY + (leftLegLift > 0 ? 14 * pScale : 20 * pScale);

        ctx.strokeStyle = '#142035';
        ctx.lineWidth = legThickness;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.beginPath();
        ctx.moveTo(leftHipX, hipY);
        ctx.lineTo(leftKneeX, leftKneeY);
        ctx.lineTo(leftFootX, leftFootY);
        ctx.stroke();

        // Left Shoe Heel (Solid black dress shoe rear view)
        ctx.fillStyle = '#0A0E18';
        ctx.fillRect(leftFootX - 4 * pScale, leftFootY - 1, 9 * pScale, 6 * pScale);

        // Right Leg (Rear view)
        const rightKneeX = rightHipX + (rightLegLift > 0 ? 12 * pScale : 3 * pScale);
        const rightKneeY = hipY + (rightLegLift > 0 ? 14 * pScale : 22 * pScale);
        const rightFootX = rightHipX + (rightLegLift > 0 ? 4 * pScale : 2 * pScale);
        const rightFootY = rightKneeY + (rightLegLift > 0 ? 14 * pScale : 20 * pScale);

        ctx.beginPath();
        ctx.moveTo(rightHipX, hipY);
        ctx.lineTo(rightKneeX, rightKneeY);
        ctx.lineTo(rightFootX, rightFootY);
        ctx.stroke();

        // Right Shoe Heel
        ctx.fillStyle = '#0A0E18';
        ctx.fillRect(rightFootX - 4 * pScale, rightFootY - 1, 9 * pScale, 6 * pScale);

        // ── SUIT JACKET (Back View, tailored navy suit) ──
        const shoulderY = bodyY - 18 * pScale;
        const shoulderLeftX = bodyX - 16 * pScale;
        const shoulderRightX = bodyX + 16 * pScale;

        // Main jacket back panel
        ctx.fillStyle = '#16243D';
        ctx.beginPath();
        ctx.moveTo(shoulderLeftX, shoulderY);
        ctx.lineTo(shoulderRightX, shoulderY);
        ctx.lineTo(bodyX + 14 * pScale, bodyY + 18 * pScale); // Lower right jacket hem
        ctx.lineTo(bodyX - 14 * pScale, bodyY + 18 * pScale); // Lower left jacket hem
        ctx.closePath();
        ctx.fill();

        // Center Back Seam & Tailoring Shadow
        ctx.strokeStyle = '#0F1A2E';
        ctx.lineWidth = 1.4 * pScale;
        ctx.beginPath();
        ctx.moveTo(bodyX, shoulderY + 4 * pScale);
        ctx.lineTo(bodyX, bodyY + 18 * pScale);
        ctx.stroke();

        // White Shirt Collar (Visible at nape of neck)
        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath();
        ctx.moveTo(bodyX - 6 * pScale, shoulderY - 1);
        ctx.lineTo(bodyX + 6 * pScale, shoulderY - 1);
        ctx.lineTo(bodyX + 5 * pScale, shoulderY + 4 * pScale);
        ctx.lineTo(bodyX - 5 * pScale, shoulderY + 4 * pScale);
        ctx.closePath();
        ctx.fill();

        // ── ARMS & HANDS (Reaching forward to grip ladder rungs in front) ──
        const armThickness = 5.5 * pScale;

        // Left Arm (Reaching up/forward to grip rung)
        const leftHandGripY = shoulderY - (stride > 0 ? 18 * pScale : 6 * pScale);
        const leftHandGripX = bodyX - 12 * pScale;
        const leftElbowX = bodyX - 20 * pScale;
        const leftElbowY = shoulderY + 2 * pScale;

        ctx.strokeStyle = '#16243D';
        ctx.lineWidth = armThickness;
        ctx.beginPath();
        ctx.moveTo(shoulderLeftX, shoulderY + 2 * pScale);
        ctx.lineTo(leftElbowX, leftElbowY);
        ctx.lineTo(leftHandGripX, leftHandGripY);
        ctx.stroke();

        // Left Hand (Back of hand gripping rung)
        ctx.fillStyle = '#F4BA94';
        ctx.beginPath();
        ctx.arc(leftHandGripX, leftHandGripY, 4.0 * pScale, 0, Math.PI * 2);
        ctx.fill();

        // Right Arm (Reaching up/forward to grip rung)
        const rightHandGripY = shoulderY - (stride < 0 ? 18 * pScale : 6 * pScale);
        const rightHandGripX = bodyX + (isTransferring ? 18 * pScale : 12 * pScale);
        const rightElbowX = bodyX + (isTransferring ? 24 * pScale : 20 * pScale);
        const rightElbowY = shoulderY + 2 * pScale;

        ctx.beginPath();
        ctx.moveTo(shoulderRightX, shoulderY + 2 * pScale);
        ctx.lineTo(rightElbowX, rightElbowY);
        ctx.lineTo(rightHandGripX, rightHandGripY);
        ctx.stroke();

        // Right Hand (Back of hand gripping rung)
        ctx.fillStyle = '#F4BA94';
        ctx.beginPath();
        ctx.arc(rightHandGripX, rightHandGripY, 4.0 * pScale, 0, Math.PI * 2);
        ctx.fill();

        // ── HEAD & HAIR (Back View, matching photo) ──
        const headCenterY = shoulderY - 12 * pScale;

        // Neck (Visible at back)
        ctx.fillStyle = '#E8B08A';
        ctx.fillRect(bodyX - 4 * pScale, shoulderY - 6 * pScale, 8 * pScale, 6 * pScale);

        // Head Base
        ctx.fillStyle = '#E8B08A';
        ctx.beginPath();
        ctx.arc(bodyX, headCenterY, 8.5 * pScale, 0, Math.PI * 2);
        ctx.fill();

        // Short Business Haircut (Back view covering top/sides of head)
        ctx.fillStyle = '#422F22';
        ctx.beginPath();
        ctx.arc(bodyX, headCenterY - 1.5 * pScale, 9.0 * pScale, Math.PI * 0.9, Math.PI * 2.1);
        ctx.bezierCurveTo(bodyX + 7 * pScale, headCenterY + 4 * pScale, bodyX - 7 * pScale, headCenterY + 4 * pScale, bodyX - 8.5 * pScale, headCenterY);
        ctx.closePath();
        ctx.fill();

        ctx.restore();

        window.parent._ac_anim_req = requestAnimationFrame(drawScene);
    }

    window.parent._ac_anim_req = requestAnimationFrame(drawScene);
        """

    else:
        # ── Dark: Rising Glow ─────────────────────────────────────────────
        # Tiny glowing particles slowly rise; some fade away while new ones appear
        anim_js = r"""
    const ctx = canvas.getContext('2d');

    if (window.parent._ac_anim_req) {
        window.parent.cancelAnimationFrame(window.parent._ac_anim_req);
    }

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
        window.parent._ac_anim_req = requestAnimationFrame(drawGlow);
    }
    window.parent._ac_anim_req = requestAnimationFrame(drawGlow);
        """

    # Inject canvas element (and left summit picture for dark theme) into parent Streamlit DOM
    if theme_key == "dark":
        summit_uri = _get_summit_data_uri()
        st.markdown(textwrap.dedent(f"""
            <div id="ac-dark-summit-hero" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 440px;
                max-width: 36vw;
                height: 100vh;
                z-index: 0;
                pointer-events: none;
                overflow: hidden;
            ">
                <img src="{summit_uri}" alt="Summit Achiever" style="
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    object-position: left bottom;
                    opacity: 0.86;
                    -webkit-mask-image: radial-gradient(ellipse at 35% 55%, rgba(0,0,0,1) 40%, rgba(0,0,0,0.65) 65%, rgba(0,0,0,0) 95%),
                                        linear-gradient(to right, rgba(0,0,0,1) 45%, rgba(0,0,0,0) 100%),
                                        linear-gradient(to top, rgba(0,0,0,1) 60%, rgba(0,0,0,0) 100%),
                                        linear-gradient(to bottom, rgba(0,0,0,1) 75%, rgba(0,0,0,0) 100%);
                    -webkit-mask-composite: destination-in;
                    mask-image: radial-gradient(ellipse at 35% 55%, rgba(0,0,0,1) 40%, rgba(0,0,0,0.65) 65%, rgba(0,0,0,0) 95%),
                                linear-gradient(to right, rgba(0,0,0,1) 45%, rgba(0,0,0,0) 100%);
                    mask-composite: intersect;
                    filter: drop-shadow(0 0 24px rgba(245, 158, 11, 0.16));
                " />
            </div>
            <canvas id="ac-anim-canvas" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;"></canvas>
        """), unsafe_allow_html=True)
    else:
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
        <!-- AscendCareer Canvas Animation Engine v2 -->
        <script>
        (function run() {{
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
    <div class="ac-content" style="text-align:center; padding: 12px 24px 32px; margin-top: -6px;">

        <!-- Logo — enlarged and with balanced distance to AscendCareer -->
        <div style="margin-top: -52px; margin-bottom: 28px; position: relative; z-index: 2;">
            <img src="{logo_data_uri}"
                 alt="AscendCareer Logo"
                 style="height:172px; width:auto;
                        filter: drop-shadow(0 14px 34px rgba(79,70,229,0.36))
                                drop-shadow(0 3px 16px rgba(212,175,55,0.32));" />
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

        <!-- Right-Side Perpendicular Oval Length Boxes -->
        <div class="ac-right-features-rail">
            <div class="ac-feature-oval-pill">
                <span class="ac-feature-oval-icon">📄</span>
                <span class="ac-feature-oval-text">Resume Analysis</span>
            </div>
            <div class="ac-feature-oval-pill">
                <span class="ac-feature-oval-icon">🏗️</span>
                <span class="ac-feature-oval-text">Resume Builder</span>
            </div>
            <div class="ac-feature-oval-pill">
                <span class="ac-feature-oval-icon">🎙️</span>
                <span class="ac-feature-oval-text">Voice Interviews</span>
            </div>
            <div class="ac-feature-oval-pill">
                <span class="ac-feature-oval-icon">👥</span>
                <span class="ac-feature-oval-text">Multi-Panel Simulations</span>
            </div>
            <div class="ac-feature-oval-pill">
                <span class="ac-feature-oval-icon">📊</span>
                <span class="ac-feature-oval-text">Progress Analytics</span>
            </div>
            <div class="ac-feature-oval-pill">
                <span class="ac-feature-oval-icon">🏆</span>
                <span class="ac-feature-oval-text">6-Stage Ladder</span>
            </div>
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
            <div class="ac-principle-title">💡 Core Principle</div>
            <p class="ac-principle-sub">
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

    # ── Auth Required Pop-up Dialog Check (Only triggered when accessing protected Resume / Interview) ──
    if st.session_state.get("auth_popup_open", False):
        feature_name = st.session_state.get("auth_popup_feature", "this feature")
        st.session_state["auth_popup_open"] = False
        render_signin_required_dialog(feature_name)

    # ── Top Bar: Hamburger (Left), Spacer, Sign In (Right) & Sun/Moon Theme Switcher ──
    top_col_h, top_col_spacer, top_col_signin, top_col_theme = st.columns([6, 73, 14, 7])
    with top_col_h:
        if st.button(" ", key="ac_hamburger_btn", help="Open Main Navigation"):
            st.session_state["auth_popup_open"] = False
            st.session_state["nav_open"] = not st.session_state.get("nav_open", False)
            st.rerun()
    with top_col_signin:
        active_user_id = st.session_state.get("user_id")
        if active_user_id:
            top_signin_clicked = False
            if st.button(f"🆔 {active_user_id}", key="ac_top_verified_user_btn", use_container_width=True, help="Verified User ID · Click to View Profile"):
                st.session_state["auth_popup_open"] = False
                st.session_state["ac_screen"] = "profile"
                st.rerun()
        else:
            top_signin_clicked = st.button(" ", key="ac_top_signin_btn", use_container_width=True, help="Sign In / Generate User ID")
    with top_col_theme:
        if st.button(" ", key="ac_theme_toggle_btn", help=f"Switch to {'Dark' if theme_key == 'light' else 'Light'} Theme"):
            st.session_state["auth_popup_open"] = False
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

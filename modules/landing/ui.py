"""
AscendCareer — Landing Screen
Polished opening screen with animated background, theme switching,
branding, Core Principle, Privacy & Trust section, and Sign In entry point.

This module is intentionally self-contained and modular.
The Sign In button is an entry-point placeholder — sign-in logic
is implemented separately in the next step.
"""

import streamlit as st
import streamlit.components.v1 as components
from modules.landing.content import (
    CORE_PRINCIPLE,
    PRIVACY_STATEMENT,
    PRIVACY_SECTIONS,
)


# ─────────────────────────────────────────────────────────────────────────────
# Theme Configuration
# ─────────────────────────────────────────────────────────────────────────────

THEMES = {
    "light": {
        "label": "🌙 Dark",           # label shows what you'll SWITCH TO
        "bg": "#F8FAFF",
        "surface": "#FFFFFF",
        "surface2": "#F0F4FF",
        "border": "#DDE3F0",
        "text_primary": "#1A1F36",
        "text_secondary": "#4A5568",
        "text_muted": "#718096",
        "accent": "#4F46E5",
        "accent_hover": "#4338CA",
        "accent_soft": "#EEF2FF",
        "gold": "#D97706",
        "gold_soft": "#FEF3C7",
        "card_shadow": "0 2px 16px rgba(79,70,229,0.08)",
        "btn_text": "#FFFFFF",
        "tag_bg": "#EEF2FF",
        "tag_text": "#4F46E5",
        "divider": "#E2E8F0",
        "qa_bg": "#F8FAFF",
        "qa_hover": "#EEF2FF",
        "qa_answer_bg": "#F0F4FF",
        "qa_border": "#DDE3F0",
        "principle_border": "#C7D2FE",
    },
    "dark": {
        "label": "☀️ Light",          # label shows what you'll SWITCH TO
        "bg": "#0D0F1A",
        "surface": "#141827",
        "surface2": "#1C2035",
        "border": "#2D3450",
        "text_primary": "#E8ECF7",
        "text_secondary": "#A0AABF",
        "text_muted": "#6B7599",
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
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# CSS Injection
# ─────────────────────────────────────────────────────────────────────────────

def _inject_css(t: dict):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Reset & Base ─────────────────────────────────────────────────── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {{
        background: {t["bg"]} !important;
        color: {t["text_primary"]} !important;
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }}

    /* Hide default Streamlit chrome on landing */
    #MainMenu, footer, [data-testid="stToolbar"],
    [data-testid="stSidebarNav"], header {{
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

    /* ── Theme toggle & top bar ───────────────────────────────────────── */
    .stButton > button {{
        background: {t["surface2"]} !important;
        color: {t["text_primary"]} !important;
        border: 1.5px solid {t["border"]} !important;
        border-radius: 50px !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 6px 18px !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
    }}
    .stButton > button:hover {{
        border-color: {t["accent"]} !important;
        color: {t["accent"]} !important;
        background: {t["accent_soft"]} !important;
    }}

    /* ── Sign In button override ──────────────────────────────────────── */
    [data-testid="stButton"][key="ac_signin_btn"] > button,
    div[data-testid="column"]:nth-child(2) .stButton > button {{
        background: linear-gradient(135deg, {t["accent"]}, {t["accent_hover"]}) !important;
        color: {t["btn_text"]} !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 14px 0 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.04em !important;
        box-shadow: 0 6px 28px rgba(79,70,229,0.32) !important;
        transition: all 0.2s ease !important;
    }}

    /* ── Typography ───────────────────────────────────────────────────── */
    .ac-brand-name {{
        font-size: clamp(2.6rem, 5.5vw, 4.5rem);
        font-weight: 900;
        letter-spacing: -0.025em;
        line-height: 1.08;
        background: linear-gradient(135deg, {t["accent"]} 0%, {t["gold"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }}
    .ac-tagline-main {{
        font-size: clamp(1rem, 2.2vw, 1.35rem);
        font-weight: 700;
        color: {t["text_primary"]};
        letter-spacing: 0.01em;
    }}
    .ac-tagline-sub {{
        font-size: clamp(0.82rem, 1.6vw, 1.02rem);
        color: {t["text_secondary"]};
        font-style: italic;
        font-weight: 400;
    }}
    .ac-section-title {{
        font-size: 1.25rem;
        font-weight: 800;
        color: {t["text_primary"]};
        letter-spacing: -0.01em;
        margin: 0 0 4px;
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
        padding: 12px 16px 14px;
        font-size: 0.855rem;
        color: {t["text_secondary"]};
        line-height: 1.7;
        background: {t["qa_answer_bg"]};
        border-top: none;
    }}

    /* ── Privacy & Trust top-level expander — larger header ─────────── */
    .ac-privacy-top > [data-testid="stExpander"] > details > summary {{
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        padding: 16px 20px !important;
        background: {t["surface2"]} !important;
    }}

    /* ── Core Principle block ────────────────────────────────────────── */
    .ac-principle-block {{
        background: {t["surface"]};
        border: 1px solid {t["principle_border"]};
        border-left: 4px solid {t["accent"]};
        border-radius: 12px;
        padding: 22px 26px;
        font-size: 0.92rem;
        line-height: 1.8;
        color: {t["text_secondary"]};
        box-shadow: {t["card_shadow"]};
    }}

    /* ── Privacy statement banner ────────────────────────────────────── */
    .ac-privacy-statement {{
        background: {t["accent_soft"]};
        border: 1px solid {t["accent"]};
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 0.9rem;
        font-weight: 600;
        color: {t["text_primary"]};
        margin-bottom: 16px;
        line-height: 1.6;
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

    /* ── Mobile responsiveness ───────────────────────────────────────── */
    @media (max-width: 640px) {{
        .ac-brand-name {{ font-size: 2.4rem; }}
        .ac-principle-block {{ padding: 16px 18px; font-size: 0.87rem; }}
        .ac-qa-item summary {{ font-size: 0.83rem; padding: 10px 13px; }}
        .ac-qa-answer {{ font-size: 0.82rem; padding: 10px 13px; }}
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Animated Backgrounds
# ─────────────────────────────────────────────────────────────────────────────

def _animated_background(theme_key: str):
    """Injects a canvas-based animated background per theme."""

    if theme_key == "light":
        # ── Light: Thin Career Path ───────────────────────────────────────
        # Delicate curved bezier lines traveling upward; small dots moving along them
        anim_js = r"""
    const ctx = canvas.getContext('2d');

    function resize() {
        canvas.width  = window.parent.innerWidth  || window.innerWidth;
        canvas.height = window.parent.innerHeight || window.innerHeight;
    }
    resize();
    window.parent.addEventListener('resize', resize);

    const PATH_DEFS = [
        { cp: [[0.05,0.95],[0.20,0.60],[0.45,0.70],[0.65,0.30],[0.85,0.10]], hue: 230, a: 0.18 },
        { cp: [[0.15,1.00],[0.30,0.75],[0.50,0.55],[0.70,0.35],[0.92,0.05]], hue: 250, a: 0.12 },
        { cp: [[0.00,0.80],[0.25,0.65],[0.40,0.40],[0.60,0.25],[0.80,0.08]], hue: 210, a: 0.10 },
        { cp: [[0.25,1.00],[0.35,0.80],[0.55,0.60],[0.72,0.38],[0.95,0.12]], hue: 240, a: 0.09 },
    ];

    function evalPath(cp, t, W, H) {
        const n   = cp.length - 1;
        const seg = Math.min(Math.floor(t * n), n - 1);
        const lt  = t * n - seg;
        const p0  = cp[seg];
        const p1  = cp[seg + 1];
        return { x: (p0[0] + (p1[0] - p0[0]) * lt) * W,
                 y: (p0[1] + (p1[1] - p0[1]) * lt) * H };
    }

    const paths = PATH_DEFS.map(def => ({
        def,
        dots: Array.from({ length: 3 }, (_, i) => ({
            t:     (i / 3) + Math.random() * 0.2,
            speed: 0.0006 + Math.random() * 0.0008,
            r:     1.8  + Math.random() * 2.2,
            alpha: 0.55 + Math.random() * 0.35,
        })),
    }));

    function drawPath(def) {
        const W = canvas.width, H = canvas.height;
        ctx.beginPath();
        for (let i = 0; i <= 120; i++) {
            const pt = evalPath(def.cp, i / 120, W, H);
            i === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y);
        }
        ctx.strokeStyle = `hsla(${def.hue}, 60%, 55%, ${def.a})`;
        ctx.lineWidth   = 1.2;
        ctx.stroke();
    }

    function drawAnim() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#F8FAFF';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        const W = canvas.width, H = canvas.height;
        paths.forEach(({ def, dots }) => {
            drawPath(def);
            dots.forEach(dot => {
                dot.t += dot.speed;
                if (dot.t > 1) dot.t -= 1;
                const pt = evalPath(def.cp, dot.t, W, H);
                const glow = ctx.createRadialGradient(pt.x, pt.y, 0, pt.x, pt.y, dot.r * 5);
                glow.addColorStop(0, `hsla(${def.hue}, 70%, 60%, ${dot.alpha * 0.5})`);
                glow.addColorStop(1, `hsla(${def.hue}, 70%, 60%, 0)`);
                ctx.beginPath(); ctx.arc(pt.x, pt.y, dot.r * 5, 0, Math.PI * 2);
                ctx.fillStyle = glow; ctx.fill();
                ctx.beginPath(); ctx.arc(pt.x, pt.y, dot.r, 0, Math.PI * 2);
                ctx.fillStyle = `hsla(${def.hue}, 65%, 52%, ${dot.alpha})`; ctx.fill();
            });
        });
        requestAnimationFrame(drawAnim);
    }
    drawAnim();
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
            vy:       0.35 + Math.random() * 0.9,
            vx:       (Math.random() - 0.5) * 0.25,
            hue:      200 + Math.random() * 90,
            life:     0,
            maxLife:  180 + Math.random() * 260,
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

            const fadeIn  = p.maxLife * 0.30;
            const fadeOut = p.maxLife * 0.70;
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
    st.markdown(f"""
    <div class="ac-content" style="text-align:center; padding: 56px 24px 36px;">

        <!-- Logo -->
        <div style="margin-bottom:18px;">
            <img src="app/static/logo.png"
                 alt="AscendCareer Logo"
                 onerror="this.style.display='none'"
                 style="height:68px; width:auto;
                        filter: drop-shadow(0 4px 16px rgba(79,70,229,0.22));" />
        </div>

        <!-- Brand name -->
        <div class="ac-brand-name">AscendCareer</div>

        <!-- Where Preparation Meets Opportunity badge -->
        <div style="margin-top:14px;">
            <span class="ac-gold-badge">Where Preparation Meets Opportunity</span>
        </div>

        <!-- Taglines -->
        <div class="ac-tagline-main" style="margin-top:16px;">
            Better Preparation.&nbsp; Stronger Presentation.
        </div>
        <div class="ac-tagline-sub" style="margin-top:6px;">
            Prepare for the opportunity you've been waiting for.
        </div>

        <!-- Description -->
        <p style="margin:20px auto 0; max-width:560px;
                  font-size:0.92rem; color:{t['text_secondary']}; line-height:1.75;">
            A comprehensive, AI-powered interview preparation and career-readiness platform —
            realistic voice-to-voice interaction, multi-persona panels,
            adaptive difficulty, and deep role &amp; company tailoring.
        </p>

        <!-- Feature pills -->
        <div style="margin-top:18px; display:flex; flex-wrap:wrap;
                    gap:7px; justify-content:center;">
            <span class="ac-tag">📄 Resume Analysis</span>
            <span class="ac-tag">🏗️ Resume Builder</span>
            <span class="ac-tag">🎙️ Voice Interviews</span>
            <span class="ac-tag">👥 Multi-Panel Simulations</span>
            <span class="ac-tag">📊 Progress Analytics</span>
            <span class="ac-tag">🏆 6-Stage Ladder</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Section: Sign In CTA
# ─────────────────────────────────────────────────────────────────────────────

def _render_signin_cta(t: dict) -> bool:
    st.markdown(f"""
    <div class="ac-content" style="text-align:center; padding:0 24px 20px;">
        <hr class="ac-divider" style="max-width:300px; margin:0 auto 28px;" />
        <p style="font-size:0.88rem; color:{t['text_muted']}; margin-bottom:18px;">
            Your personalised career preparation journey starts here.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1.2, 1, 1.2])
    with col_m:
        clicked = st.button("🚀  Sign In to AscendCareer",
                            key="ac_signin_btn",
                            use_container_width=True)

    st.markdown(f"""
    <div class="ac-content" style="text-align:center; padding:6px 24px 0;">
        <p style="font-size:0.75rem; color:{t['text_muted']}; margin-top:8px;">
            By signing in, you agree to our Privacy &amp; Trust principles outlined below.
        </p>
    </div>
    """, unsafe_allow_html=True)

    return clicked


# ─────────────────────────────────────────────────────────────────────────────
# Section: Core Principle
# ─────────────────────────────────────────────────────────────────────────────

def _render_core_principle(t: dict):
    st.markdown(f"""
    <div class="ac-content" style="padding: 0 24px;">
        <hr class="ac-divider" style="margin-bottom:32px;" />
        <div style="text-align:center; margin-bottom:18px;">
            <div class="ac-section-title">💡 Core Principle</div>
            <p style="font-size:0.83rem; color:{t['text_muted']}; margin-top:4px;">
                The philosophy behind everything AscendCareer does.
            </p>
        </div>
        <div class="ac-principle-block">
            {CORE_PRINCIPLE}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Section: Privacy & Trust
# ─────────────────────────────────────────────────────────────────────────────

def _build_qa_html(qa_list: list, t: dict) -> str:
    """Build the HTML for a list of Q&A items using native <details>/<summary>."""
    items_html = ""
    for item in qa_list:
        q = item["q"].replace("'", "&#39;").replace('"', "&quot;")
        a = item["a"].replace("'", "&#39;").replace('"', "&quot;")
        items_html += f"""
        <details class="ac-qa-item">
            <summary>
                <span>{q}</span>
                <span class="ac-qa-icon">+</span>
            </summary>
            <div class="ac-qa-answer">{a}</div>
        </details>
        """
    return items_html


def _render_privacy_trust(t: dict):
    st.markdown(f"""
    <div class="ac-content" style="padding: 0 24px;">
        <hr class="ac-divider" style="margin-top:32px; margin-bottom:32px;" />
        <div style="text-align:center; margin-bottom:20px;">
            <div class="ac-section-title">🔒 Privacy &amp; Trust</div>
            <p style="font-size:0.83rem; color:{t['text_muted']}; margin-top:4px;">
                How AscendCareer handles your information — honestly and clearly.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Wrap in a div for top-level expander styling
    st.markdown('<div class="ac-content ac-privacy-top" style="padding: 0 24px;">', unsafe_allow_html=True)

    with st.expander("🔒  Privacy & Trust — Click to read", expanded=False):
        # Statement banner at top
        st.markdown(f"""
        <div class="ac-privacy-statement">
            💬 {PRIVACY_STATEMENT}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # Each of the 7 sections as a nested expander
        for section in PRIVACY_SECTIONS:
            label = f"{section['number']}.  {section['title']}"
            with st.expander(label, expanded=False):
                qa_html = _build_qa_html(section["qa"], t)
                st.markdown(f"""
                <div style="padding: 4px 0;">
                    {qa_html}
                </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────

def _render_footer(t: dict):
    st.markdown(f"""
    <div class="ac-content" style="
        text-align:center;
        padding: 36px 24px 52px;
        border-top: 1px solid {t['divider']};
        margin-top: 36px;
    ">
        <div style="font-size:0.8rem; color:{t['text_muted']};">
            <strong style="color:{t['text_secondary']};">AscendCareer</strong>
            &nbsp;·&nbsp; AI-Powered Career Readiness
            &nbsp;·&nbsp; Audit → Optimize → Train → Verify → Placement Readiness
        </div>
        <div style="font-size:0.73rem; color:{t['text_muted']}; margin-top:5px;">
            © AscendCareer — Built for the candidate who is serious about their next step.
        </div>
    </div>
    """, unsafe_allow_html=True)


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
        st.session_state["ac_theme"] = "light"      # Light is default

    theme_key = st.session_state["ac_theme"]
    t         = THEMES[theme_key]
    other_key = "dark" if theme_key == "light" else "light"

    # ── CSS ──────────────────────────────────────────────────────────────────
    _inject_css(t)

    # ── Theme toggle — top-right ─────────────────────────────────────────────
    _, top_right = st.columns([8, 1])
    with top_right:
        st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
        if st.button(THEMES[other_key]["label"], key="ac_theme_toggle"):
            st.session_state["ac_theme"] = other_key
            st.rerun()

    # ── Animated background ──────────────────────────────────────────────────
    _animated_background(theme_key)

    # ── Content ──────────────────────────────────────────────────────────────
    _render_hero(t)
    signin_clicked = _render_signin_cta(t)
    _render_core_principle(t)
    _render_privacy_trust(t)
    _render_footer(t)

    return {
        "proceed": signin_clicked,
        "theme":   theme_key,
    }

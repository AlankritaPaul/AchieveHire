"""
AscendCareer — Landing Screen
Polished opening screen with animated background, theme switching,
branding, Core Principles, Privacy info, and Sign In entry point.

This module is intentionally self-contained and modular.
The Sign In button is an entry-point placeholder — sign-in logic
is implemented separately in the next step.
"""

import streamlit as st
from modules.landing.content import CORE_PRINCIPLES, PRIVACY_POINTS


# ─────────────────────────────────────────────────────────────────────────────
# Theme Configuration
# ─────────────────────────────────────────────────────────────────────────────

THEMES = {
    "light": {
        "label": "☀️ Light",
        "bg": "#F8FAFF",
        "surface": "#FFFFFF",
        "surface2": "#F0F4FF",
        "border": "#DDE3F0",
        "text_primary": "#1A1F36",
        "text_secondary": "#4A5568",
        "text_muted": "#718096",
        "accent": "#4F46E5",          # Indigo
        "accent_hover": "#4338CA",
        "accent_soft": "#EEF2FF",
        "gold": "#D97706",
        "gold_soft": "#FEF3C7",
        "card_shadow": "0 2px 16px rgba(79,70,229,0.08)",
        "btn_text": "#FFFFFF",
        "tag_bg": "#EEF2FF",
        "tag_text": "#4F46E5",
        "divider": "#E2E8F0",
        "anim_id": "light",
    },
    "dark": {
        "label": "🌙 Dark",
        "bg": "#0D0F1A",
        "surface": "#141827",
        "surface2": "#1C2035",
        "border": "#2D3450",
        "text_primary": "#E8ECF7",
        "text_secondary": "#A0AABF",
        "text_muted": "#6B7599",
        "accent": "#818CF8",          # Soft indigo
        "accent_hover": "#A5B4FC",
        "accent_soft": "#1E2347",
        "gold": "#FCD34D",
        "gold_soft": "#2D2710",
        "card_shadow": "0 2px 24px rgba(0,0,0,0.45)",
        "btn_text": "#0D0F1A",
        "tag_bg": "#1E2347",
        "tag_text": "#818CF8",
        "divider": "#2D3450",
        "anim_id": "dark",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# CSS Injection
# ─────────────────────────────────────────────────────────────────────────────

def _inject_css(t: dict):
    st.markdown(f"""
    <style>
    /* ── Reset & Base ─────────────────────────────────────────────────── */
    html, body, [data-testid="stAppViewContainer"],
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
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: {t["bg"]}; }}
    ::-webkit-scrollbar-thumb {{ background: {t["border"]}; border-radius: 3px; }}

    /* ── Streamlit default padding override ───────────────────────────── */
    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    [data-testid="stVerticalBlock"] > div {{ padding: 0; }}

    /* ── Section Cards ────────────────────────────────────────────────── */
    .ac-card {{
        background: {t["surface"]} !important;
        border: 1px solid {t["border"]} !important;
        border-radius: 16px !important;
        box-shadow: {t["card_shadow"]} !important;
        color: {t["text_primary"]} !important;
    }}

    .ac-card-subtle {{
        background: {t["surface2"]} !important;
        border: 1px solid {t["border"]} !important;
        border-radius: 12px !important;
        color: {t["text_primary"]} !important;
    }}

    /* ── Sign In Button ───────────────────────────────────────────────── */
    .ac-signin-btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        background: linear-gradient(135deg, {t["accent"]}, {t["accent_hover"]});
        color: {t["btn_text"]};
        border: none;
        border-radius: 50px;
        padding: 16px 52px;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        cursor: pointer;
        text-decoration: none;
        box-shadow: 0 6px 28px rgba(79,70,229,0.35);
        transition: all 0.2s ease;
        margin: 8px 4px;
    }}
    .ac-signin-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 36px rgba(79,70,229,0.45);
    }}

    /* ── Theme toggle button ──────────────────────────────────────────── */
    .stButton > button {{
        background: {t["surface2"]} !important;
        color: {t["text_primary"]} !important;
        border: 1.5px solid {t["border"]} !important;
        border-radius: 50px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 6px 18px !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover {{
        border-color: {t["accent"]} !important;
        color: {t["accent"]} !important;
    }}

    /* ── Principle / Privacy Tags ─────────────────────────────────────── */
    .ac-tag {{
        display: inline-block;
        background: {t["tag_bg"]};
        color: {t["tag_text"]};
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }}

    /* ── Animated canvas container ────────────────────────────────────── */
    #ac-anim-canvas {{
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 0;
        pointer-events: none;
    }}

    /* ── Content above canvas ─────────────────────────────────────────── */
    .ac-content {{
        position: relative;
        z-index: 1;
    }}

    /* ── Typography ───────────────────────────────────────────────────── */
    .ac-brand-name {{
        font-size: clamp(2.8rem, 6vw, 4.8rem);
        font-weight: 900;
        letter-spacing: -0.02em;
        line-height: 1.1;
        background: linear-gradient(135deg, {t["accent"]} 0%, {t["gold"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .ac-tagline-main {{
        font-size: clamp(1.05rem, 2.5vw, 1.45rem);
        font-weight: 700;
        color: {t["text_primary"]};
        letter-spacing: 0.01em;
    }}
    .ac-tagline-sub {{
        font-size: clamp(0.85rem, 1.8vw, 1.1rem);
        color: {t["text_secondary"]};
        font-style: italic;
        font-weight: 400;
    }}
    .ac-section-title {{
        font-size: 1.35rem;
        font-weight: 800;
        color: {t["text_primary"]};
        letter-spacing: -0.01em;
    }}
    .ac-principle-title {{
        font-size: 1.0rem;
        font-weight: 700;
        color: {t["text_primary"]};
    }}
    .ac-principle-desc {{
        font-size: 0.88rem;
        color: {t["text_secondary"]};
        line-height: 1.6;
    }}
    .ac-divider {{
        border: none;
        border-top: 1px solid {t["divider"]};
        margin: 0;
    }}

    /* ── Gold accent for tagline badge ───────────────────────────────── */
    .ac-gold-badge {{
        display: inline-block;
        background: {t["gold_soft"]};
        color: {t["gold"]};
        border-radius: 50px;
        padding: 4px 18px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Animated Background (Canvas)
# ─────────────────────────────────────────────────────────────────────────────

def _animated_background(theme_key: str):
    """Injects a canvas-based animated background appropriate for the theme."""

    if theme_key == "light":
        # Light theme: soft floating orbs + gentle particle drift
        anim_js = """
        (function() {
            const canvas = document.getElementById('ac-anim-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');

            function resize() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }
            resize();
            window.addEventListener('resize', resize);

            // Floating orbs
            const orbs = Array.from({length: 7}, (_, i) => ({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                r: 120 + Math.random() * 180,
                dx: (Math.random() - 0.5) * 0.25,
                dy: (Math.random() - 0.5) * 0.25,
                hue: [220, 240, 260, 200, 210][i % 5],
                alpha: 0.055 + Math.random() * 0.04,
            }));

            // Particles
            const particles = Array.from({length: 55}, () => ({
                x: Math.random() * (typeof canvas !== 'undefined' ? canvas.width : 1200),
                y: Math.random() * (typeof canvas !== 'undefined' ? canvas.height : 800),
                r: 1 + Math.random() * 2,
                dx: (Math.random() - 0.5) * 0.3,
                dy: -0.15 - Math.random() * 0.25,
                alpha: 0.12 + Math.random() * 0.18,
                hue: 220 + Math.random() * 40,
            }));

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Background base
                ctx.fillStyle = '#F8FAFF';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                // Subtle grid
                ctx.strokeStyle = 'rgba(79,70,229,0.035)';
                ctx.lineWidth = 1;
                const step = 48;
                for (let x = 0; x < canvas.width; x += step) {
                    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
                }
                for (let y = 0; y < canvas.height; y += step) {
                    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
                }

                // Orbs
                orbs.forEach(o => {
                    o.x += o.dx; o.y += o.dy;
                    if (o.x < -o.r) o.x = canvas.width + o.r;
                    if (o.x > canvas.width + o.r) o.x = -o.r;
                    if (o.y < -o.r) o.y = canvas.height + o.r;
                    if (o.y > canvas.height + o.r) o.y = -o.r;
                    const g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
                    g.addColorStop(0, `hsla(${o.hue}, 70%, 70%, ${o.alpha})`);
                    g.addColorStop(1, `hsla(${o.hue}, 70%, 70%, 0)`);
                    ctx.beginPath();
                    ctx.arc(o.x, o.y, o.r, 0, Math.PI * 2);
                    ctx.fillStyle = g;
                    ctx.fill();
                });

                // Particles
                particles.forEach(p => {
                    p.x += p.dx; p.y += p.dy;
                    if (p.y < -5) { p.y = canvas.height + 5; p.x = Math.random() * canvas.width; }
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    ctx.fillStyle = `hsla(${p.hue}, 60%, 55%, ${p.alpha})`;
                    ctx.fill();
                });

                requestAnimationFrame(draw);
            }
            draw();
        })();
        """
    else:
        # Dark theme: deep space nebula with stars + aurora ribbons
        anim_js = """
        (function() {
            const canvas = document.getElementById('ac-anim-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');

            function resize() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }
            resize();
            window.addEventListener('resize', resize);

            // Stars
            const stars = Array.from({length: 160}, () => ({
                x: Math.random() * (typeof canvas !== 'undefined' ? canvas.width : 1200),
                y: Math.random() * (typeof canvas !== 'undefined' ? canvas.height : 800),
                r: 0.4 + Math.random() * 1.4,
                alpha: 0.3 + Math.random() * 0.7,
                twinkleSpeed: 0.008 + Math.random() * 0.02,
                twinklePhase: Math.random() * Math.PI * 2,
            }));

            // Nebula orbs
            const nebulae = Array.from({length: 5}, (_, i) => ({
                x: Math.random() * (typeof canvas !== 'undefined' ? canvas.width : 1200),
                y: Math.random() * (typeof canvas !== 'undefined' ? canvas.height : 800),
                r: 200 + Math.random() * 300,
                dx: (Math.random() - 0.5) * 0.12,
                dy: (Math.random() - 0.5) * 0.12,
                hue: [260, 200, 280, 220, 240][i],
                alpha: 0.06 + Math.random() * 0.06,
            }));

            // Aurora ribbons
            const ribbons = Array.from({length: 3}, (_, i) => ({
                phase: i * (Math.PI * 2 / 3),
                speed: 0.004 + i * 0.002,
                amp: 60 + i * 30,
                y: 0.2 + i * 0.28,
                hue: [180, 270, 210][i],
            }));

            let t = 0;

            function draw() {
                t += 0.01;
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Base
                ctx.fillStyle = '#0D0F1A';
                ctx.fillRect(0, 0, canvas.width, canvas.height);

                // Nebulae
                nebulae.forEach(n => {
                    n.x += n.dx; n.y += n.dy;
                    if (n.x < -n.r) n.x = canvas.width + n.r;
                    if (n.x > canvas.width + n.r) n.x = -n.r;
                    if (n.y < -n.r) n.y = canvas.height + n.r;
                    if (n.y > canvas.height + n.r) n.y = -n.r;
                    const g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r);
                    g.addColorStop(0, `hsla(${n.hue}, 70%, 55%, ${n.alpha})`);
                    g.addColorStop(1, `hsla(${n.hue}, 70%, 55%, 0)`);
                    ctx.beginPath();
                    ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
                    ctx.fillStyle = g;
                    ctx.fill();
                });

                // Aurora ribbons
                ribbons.forEach(r => {
                    ctx.beginPath();
                    const baseY = r.y * canvas.height;
                    ctx.moveTo(0, baseY + Math.sin(r.phase + t * r.speed * canvas.width * 0.002) * r.amp);
                    for (let x = 0; x <= canvas.width; x += 4) {
                        const y = baseY + Math.sin(r.phase + t * r.speed + x * 0.006) * r.amp
                                        + Math.sin(r.phase * 2 + x * 0.003 + t * 0.5) * (r.amp * 0.4);
                        ctx.lineTo(x, y);
                    }
                    ctx.strokeStyle = `hsla(${r.hue}, 80%, 70%, 0.06)`;
                    ctx.lineWidth = 40 + 20 * Math.sin(t * 0.3 + r.phase);
                    ctx.stroke();
                });

                // Stars
                stars.forEach(s => {
                    s.twinklePhase += s.twinkleSpeed;
                    const a = s.alpha * (0.5 + 0.5 * Math.sin(s.twinklePhase));
                    ctx.beginPath();
                    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                    ctx.fillStyle = `rgba(200, 210, 255, ${a})`;
                    ctx.fill();
                });

                requestAnimationFrame(draw);
            }
            draw();
        })();
        """

    st.markdown(f"""
    <canvas id="ac-anim-canvas"></canvas>
    <script>{anim_js}</script>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Section: Hero / Branding
# ─────────────────────────────────────────────────────────────────────────────

def _render_hero(t: dict):
    st.markdown(f"""
    <div class="ac-content" style="
        text-align: center;
        padding: 60px 24px 40px;
    ">
        <!-- Logo -->
        <div style="margin-bottom: 20px;">
            <img src="app/static/logo.png"
                 alt="AscendCareer Logo"
                 onerror="this.style.display='none'"
                 style="height: 72px; width: auto; filter: drop-shadow(0 4px 16px rgba(79,70,229,0.25));" />
        </div>

        <!-- Brand name -->
        <div class="ac-brand-name">AscendCareer</div>

        <!-- Tagline row -->
        <div style="margin-top: 12px; margin-bottom: 6px;">
            <span class="ac-gold-badge">Where Preparation Meets Opportunity</span>
        </div>

        <!-- Main taglines -->
        <div class="ac-tagline-main" style="margin-top: 14px;">
            Better Preparation. &nbsp;Stronger Presentation.
        </div>
        <div class="ac-tagline-sub" style="margin-top: 6px;">
            Prepare for the opportunity you've been waiting for.
        </div>

        <!-- Description -->
        <p style="
            margin: 22px auto 0;
            max-width: 580px;
            font-size: 0.95rem;
            color: {t['text_secondary']};
            line-height: 1.7;
        ">
            A comprehensive, AI-powered interview preparation and career-readiness platform —
            with realistic voice-to-voice interaction, multi-persona panels,
            adaptive difficulty, and deep role &amp; company tailoring.
        </p>

        <!-- Feature pills -->
        <div style="margin-top: 20px; display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;">
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
    """Renders the Sign In button and returns True if clicked."""
    st.markdown(f"""
    <div class="ac-content" style="text-align: center; padding: 8px 24px 40px;">
        <hr class="ac-divider" style="max-width: 320px; margin: 0 auto 32px;" />
        <p style="font-size: 0.9rem; color: {t['text_muted']}; margin-bottom: 20px;">
            Your personalised career preparation journey starts here.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        clicked = st.button("🚀  Sign In to AscendCareer", key="ac_signin_btn", use_container_width=True)

    st.markdown(f"""
    <div class="ac-content" style="text-align: center; padding: 8px 24px 0;">
        <p style="font-size: 0.78rem; color: {t['text_muted']}; margin-top: 10px;">
            By signing in, you agree to our Privacy principles outlined below.
        </p>
    </div>
    """, unsafe_allow_html=True)

    return clicked


# ─────────────────────────────────────────────────────────────────────────────
# Section: Core Principles
# ─────────────────────────────────────────────────────────────────────────────

def _render_core_principles(t: dict):
    st.markdown(f"""
    <div class="ac-content" style="padding: 12px 24px 0;">
        <hr class="ac-divider" />
        <div style="padding: 40px 0 20px; text-align: center;">
            <div class="ac-section-title">⚡ Core Principles</div>
            <p style="color: {t['text_muted']}; font-size: 0.88rem; margin-top: 6px;">
                The values that guide every decision AscendCareer makes.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3-column grid of principle cards
    cols = st.columns(3, gap="medium")
    for i, principle in enumerate(CORE_PRINCIPLES):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="ac-content ac-card" style="padding: 20px; margin-bottom: 16px; min-height: 150px;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">{principle['icon']}</div>
                <div class="ac-principle-title">{principle['title']}</div>
                <div class="ac-principle-desc" style="margin-top: 6px;">{principle['description']}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Section: Privacy Information
# ─────────────────────────────────────────────────────────────────────────────

def _render_privacy(t: dict):
    st.markdown(f"""
    <div class="ac-content" style="padding: 12px 24px 0;">
        <hr class="ac-divider" style="margin-top: 24px;" />
        <div style="padding: 36px 0 20px; text-align: center;">
            <div class="ac-section-title">🔒 Privacy Information</div>
            <p style="color: {t['text_muted']}; font-size: 0.88rem; margin-top: 6px;">
                How AscendCareer handles your information — simply and honestly.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2-col + 3-col split: 2 on top, 3 on bottom
    top_items = PRIVACY_POINTS[:2]
    bot_items = PRIVACY_POINTS[2:]

    top_cols = st.columns(2, gap="medium")
    for i, item in enumerate(top_items):
        with top_cols[i]:
            st.markdown(f"""
            <div class="ac-content ac-card-subtle" style="padding: 18px 20px; margin-bottom: 14px; border-left: 3px solid {t['accent']};">
                <span style="font-size: 1.4rem;">{item['icon']}</span>
                <span class="ac-principle-title" style="margin-left: 8px;">{item['heading']}</span>
                <div class="ac-principle-desc" style="margin-top: 8px;">{item['text']}</div>
            </div>
            """, unsafe_allow_html=True)

    bot_cols = st.columns(3, gap="medium")
    for i, item in enumerate(bot_items):
        with bot_cols[i]:
            st.markdown(f"""
            <div class="ac-content ac-card-subtle" style="padding: 18px 20px; margin-bottom: 14px; border-left: 3px solid {t['accent']};">
                <span style="font-size: 1.4rem;">{item['icon']}</span>
                <span class="ac-principle-title" style="margin-left: 8px;">{item['heading']}</span>
                <div class="ac-principle-desc" style="margin-top: 8px;">{item['text']}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────

def _render_footer(t: dict):
    st.markdown(f"""
    <div class="ac-content" style="
        text-align: center;
        padding: 32px 24px 48px;
        border-top: 1px solid {t['divider']};
        margin-top: 32px;
    ">
        <div style="font-size: 0.82rem; color: {t['text_muted']};">
            <strong style="color: {t['text_secondary']};">AscendCareer</strong>
            &nbsp;·&nbsp; AI-Powered Career Readiness
            &nbsp;·&nbsp; Audit → Optimize → Train → Verify → Placement Readiness
        </div>
        <div style="font-size: 0.75rem; color: {t['text_muted']}; margin-top: 6px;">
            &copy; AscendCareer — Built for the candidate who is serious about their next step.
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
            - 'proceed': bool — True if user clicked Sign In
            - 'theme': str — current theme key ('light' or 'dark')

    The caller (app.py) checks 'proceed' to decide whether to move
    to the next step (sign-in / profile setup).
    """

    # ── State initialisation ─────────────────────────────────────────────────
    if "ac_theme" not in st.session_state:
        st.session_state["ac_theme"] = "light"      # Light is the default

    theme_key = st.session_state["ac_theme"]
    t = THEMES[theme_key]
    other_key = "dark" if theme_key == "light" else "light"
    other_label = THEMES[other_key]["label"]

    # ── CSS ──────────────────────────────────────────────────────────────────
    _inject_css(t)

    # ── Theme toggle — top right ─────────────────────────────────────────────
    top_col_l, top_col_r = st.columns([6, 1])
    with top_col_r:
        st.markdown("<div style='padding-top: 12px;'></div>", unsafe_allow_html=True)
        if st.button(other_label, key="ac_theme_toggle"):
            st.session_state["ac_theme"] = other_key
            st.rerun()

    # ── Animated background ──────────────────────────────────────────────────
    _animated_background(theme_key)

    # ── Content ──────────────────────────────────────────────────────────────
    _render_hero(t)
    signin_clicked = _render_signin_cta(t)
    _render_core_principles(t)
    _render_privacy(t)
    _render_footer(t)

    return {
        "proceed": signin_clicked,
        "theme": theme_key,
    }

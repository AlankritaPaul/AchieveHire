"""
AscendCareer — Specialized Interview Flow
Deep domain technical assessment, core skills evaluation, algorithmic reasoning,
and architectural problem dissection.
"""

import streamlit as st
from modules.landing.ui import THEMES, clean_html
from modules.navigation.panel import render_top_nav_bar, render_navigation_drawer


SPECIALIZED_DOMAINS = [
    {
        "id": "swe_sys_design",
        "title": "Software Engineering & Distributed Systems",
        "icon": "⚡",
        "description": "High-concurrency architecture, API contracts, caching tiers, data modeling, and fault tolerance.",
        "topics": ["System Scalability", "Low-Latency Services", "Distributed Consensus", "Database Sharding"],
    },
    {
        "id": "ai_data_science",
        "title": "AI, Machine Learning & Data Engineering",
        "icon": "🧠",
        "description": "Deep learning models, inference pipelines, feature stores, LLM orchestration, and ETL workflows.",
        "topics": ["Model Evaluation", "Vector Indexing & RAG", "Data Pipelines", "Production Inference"],
    },
    {
        "id": "product_management",
        "title": "Product Management & Strategy",
        "icon": "📊",
        "description": "User problem discovery, MVP scoping, product roadmaps, metrics architecture, and stakeholder trade-offs.",
        "topics": ["Product Sense", "Execution & Metrics", "Go-to-Market Strategy", "Technical Feasibility"],
    },
    {
        "id": "cloud_devops",
        "title": "Cloud Architecture & Site Reliability",
        "icon": "☁️",
        "description": "Container orchestration (K8s), infrastructure-as-code, zero-trust security, and observability.",
        "topics": ["Kubernetes & CI/CD", "Cloud Networking", "Incident Management", "Security & IAM"],
    },
    {
        "id": "quantitative_finance",
        "title": "Quantitative Analysis & Financial Engineering",
        "icon": "📈",
        "description": "Statistical modeling, risk attribution, algorithmic execution, and financial instruments.",
        "topics": ["Statistical Arbitrage", "Stochastic Modeling", "Time-Series Forensics", "Risk Metrics"],
    },
    {
        "id": "embedded_systems",
        "title": "Embedded Systems & Hardware Engineering",
        "icon": "🔌",
        "description": "Microcontroller firmware, real-time operating systems (RTOS), hardware protocols (I2C, SPI), and power budgets.",
        "topics": ["Firmware Design", "RTOS Scheduling", "Memory Constraints", "Peripheral Bus Protocols"],
    },
]


def render_specialized_interview():
    """Renders the Specialized Interview preparation interface."""
    theme_key = st.session_state.get("ac_theme", "light")
    t = THEMES[theme_key]

    render_navigation_drawer(t)
    render_top_nav_bar(t, title="Interview › Specialized Interview")

    st.markdown(clean_html(f"""
    <div style="max-width:1080px; margin: 24px auto; padding: 0 16px;">
        <div style="margin-bottom: 24px;">
            <div style="display:inline-block; background:{t['accent_soft']}; color:{t['accent']}; font-size:0.80rem; font-weight:700; padding:4px 14px; border-radius:50px; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">
                Domain-Specific Technical Evaluation
            </div>
            <h1 style="font-size: 2.1rem; font-weight: 800; color:{t['text_primary']}; margin:0 0 6px;">
                Specialized Interview
            </h1>
            <p style="font-size: 1.02rem; color:{t['text_secondary']}; max-width:820px; line-height:1.65; margin:0;">
                Rigorous, domain-focused interview simulations designed to probe depth of understanding,
                architectural trade-offs, and subject-matter excellence.
            </p>
        </div>
    </div>
    """), unsafe_allow_html=True)

    if "specialized_selected_domain" not in st.session_state:
        st.session_state["specialized_selected_domain"] = SPECIALIZED_DOMAINS[0]["id"]
    if "specialized_difficulty" not in st.session_state:
        st.session_state["specialized_difficulty"] = "Intermediate"

    col_domains, col_config = st.columns([62, 38], gap="large")

    with col_domains:
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-bottom:14px;'>1. Select Technical Specialization</h3>", unsafe_allow_html=True)
        for dom in SPECIALIZED_DOMAINS:
            is_active = st.session_state["specialized_selected_domain"] == dom["id"]
            active_border = t["accent"] if is_active else t["border"]
            active_bg = t["accent_soft"] if is_active else t["surface"]

            st.markdown(f"""
            <div style="border: 1.5px solid {active_border}; background: {active_bg}; border-radius: 12px; padding: 14px 18px; margin-bottom: 12px; transition: border-color 0.2s;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span style="font-size:1.5rem;">{dom['icon']}</span>
                    <div style="flex:1;">
                        <div style="font-weight:700; font-size:1.02rem; color:{t['text_primary']};">{dom['title']}</div>
                        <div style="font-size:0.86rem; color:{t['text_secondary']}; margin-top:2px;">{dom['description']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Choose: {dom['title']}", key=f"btn_dom_{dom['id']}", use_container_width=True):
                st.session_state["specialized_selected_domain"] = dom["id"]
                st.rerun()

    with col_config:
        st.markdown(f"<h3 style='font-size:1.15rem; font-weight:700; color:{t['text_primary']}; margin-bottom:14px;'>2. Session Parameters</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            st.session_state["specialized_difficulty"] = st.select_slider(
                "Assessment Depth",
                options=["Fundamental", "Intermediate", "Advanced Architect", "Principal/Staff"],
                value=st.session_state["specialized_difficulty"],
            )
            mode = st.radio(
                "Interview Mode",
                options=["🎙️ Voice & Conversational Simulation", "✍️ Interactive Scenario & Code Probing"],
                index=0,
            )
            time_limit = st.slider("Duration (Minutes)", min_value=15, max_value=60, value=30, step=5)

            st.markdown(f"""
            <div style="background:{t['surface2']}; border:1px solid {t['border']}; border-radius:8px; padding:12px; margin:16px 0; font-size:0.82rem; color:{t['text_muted']};">
                <strong>Evaluation Scope:</strong> System design reasoning, trade-off clarity, debugging instinct, and communication under pressure.
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀  Launch Specialized Session", type="primary", use_container_width=True, key="btn_start_specialized"):
                st.session_state["specialized_session_active"] = True
                st.success("Specialized Interview environment initialized! Voice engine connecting...")

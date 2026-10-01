"""
AscendCareer - Comprehensive Voice-Based Interview Preparation & Career-Readiness Platform
Main Streamlit Application Entrypoint
"""

import streamlit as st
from modules.resume_guide.ui import render_resume_guide

# Page Configuration
st.set_page_config(
    page_title="AscendCareer | AI Career & Interview Readiness",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Sidebar Branding & Navigation
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h1 style="font-size: 1.8rem; margin: 0; color: #1A365D;">AscendCareer</h1>
                <p style="font-size: 0.85rem; color: #718096; margin-top: 4px;">Realistic AI Interview Preparation & Career Readiness</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Platform Modules")
        
        # Main section selection
        app_mode = st.radio(
            "Navigation",
            options=[
                "📄 Resume Guide",
                "🎙️ Voice Interview (Stage 1-6)",
                "📈 Preparation Analytics",
                "🏅 Certified Profile"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("""
            <div style="background-color: #EDF2F7; padding: 0.8rem; border-radius: 6px; font-size: 0.8rem; color: #4A5568;">
                <strong>Cycle of Improvement:</strong><br>
                Weakness → Training → Re-practice → Verification → Improvement
            </div>
        """, unsafe_allow_html=True)

    # Route navigation
    if app_mode == "📄 Resume Guide":
        render_resume_guide()
    elif app_mode == "🎙️ Voice Interview (Stage 1-6)":
        st.info("🎙️ **Voice Interview Simulator**: Real-time microphone-driven conversational engine across progressive Levels 1-6 will be activated in the upcoming milestone.")
    elif app_mode == "📈 Preparation Analytics":
        st.info("📈 **Preparation Analytics**: Historical progress, weakness tracking, and readiness metrics dashboard.")
    elif app_mode == "🏅 Certified Profile":
        st.info("🏅 **Certified Profile**: Verifiable completion certificates and public career profiles.")

if __name__ == "__main__":
    main()

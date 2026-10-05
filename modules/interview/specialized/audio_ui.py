# -*- coding: utf-8 -*-
"""
AchieveHire — Specialized Interview Audio & Interactive HUD Component
Integrates live voice synthesis (TTS), speech recognition (STT),
avatar state animation, timer, and strictly enforces the rule:
QUESTIONS ARE NEVER DISPLAYED AS READABLE TEXT ON SCREEN DURING LIVE SESSIONS.
"""

import streamlit as st
import streamlit.components.v1 as components
import json
from typing import Dict, Any, Optional
from modules.landing.ui import clean_html


def render_voice_synthesis_player(
    text_to_speak: str,
    language: str = "English",
    interviewer_gender: str = "male",
    speech_rate: float = 0.95,
    key: str = "tts_player",
):
    """
    Executes real-time browser text-to-speech using Web Speech API via components.html
    complying with user global Streamlit rules.
    """
    escaped_text = json.dumps(text_to_speak)
    lang_code = "hi-IN" if "hindi" in language.lower() or "hinglish" in language.lower() else "en-US"
    gender_pref = "male" if "male" in interviewer_gender.lower() else "female"

    components.html(f"""
    <script>
    (function runTTS() {{
        if (!('speechSynthesis' in window)) return;

        // Cancel ongoing speech
        window.speechSynthesis.cancel();

        const text = {escaped_text};
        if (!text || text.trim() === '') return;

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = {speech_rate};
        utterance.pitch = {1.0 if gender_pref == 'male' else 1.15};
        utterance.lang = '{lang_code}';

        // Select suitable voice
        const voices = window.speechSynthesis.getVoices();
        let chosenVoice = null;
        if (voices.length > 0) {{
            // Look for matching language and gender keyword
            chosenVoice = voices.find(v => v.lang.includes('{lang_code[:2]}') && v.name.toLowerCase().includes('{gender_pref}')) ||
                          voices.find(v => v.lang.includes('{lang_code[:2]}')) ||
                          voices[0];
            if (chosenVoice) utterance.voice = chosenVoice;
        }}

        // Notify parent Streamlit container when speech starts and finishes
        utterance.onstart = function() {{
            const statusEl = window.parent.document.getElementById('ac-interviewer-status-text');
            if (statusEl) statusEl.innerText = "🎙️ Interviewer Speaking... (Listen Carefully)";
        }};

        utterance.onend = function() {{
            const statusEl = window.parent.document.getElementById('ac-interviewer-status-text');
            if (statusEl) statusEl.innerText = "🎧 Listening... Click microphone or speak your answer.";
        }};

        window.speechSynthesis.speak(utterance);
    }})();
    </script>
    """, height=0, scrolling=False)


def render_voice_recognition_widget(
    prompt_key: str = "stt_box",
    language: str = "English",
):
    lang_code = "hi-IN" if "hindi" in language.lower() or "hinglish" in language.lower() else "en-IN"

    components.html(f"""
    <div style="display:flex; justify-content:center; margin: 10px 0;">
        <div style="display:flex; align-items:center; gap:8px; background:#FEF2F2; border:1px solid #F87171; padding:8px 16px; border-radius:50px; color:#DC2626; font-weight:700; font-size:0.9rem;">
            <span style="display:inline-block; width:10px; height:10px; background:#DC2626; border-radius:50%; animation:pulse 1.2s infinite;"></span>
            Live Listening... Speak your answer.
        </div>
    </div>
    <style>
    @keyframes pulse {{
        0% {{ transform: scale(0.85); opacity: 0.5; }}
        50% {{ transform: scale(1.2); opacity: 1; }}
        100% {{ transform: scale(0.85); opacity: 0.5; }}
    }}
    </style>

    <script>
    (function initSTT() {{
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) return;

        let recognition = new SpeechRec();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = '{lang_code}';

        recognition.onend = function() {{
            try {{ recognition.start(); }} catch(e) {{}}
        }};

        recognition.onresult = function(event) {{
            let finalTranscript = event.results[0][0].transcript;
            if (finalTranscript.trim().length > 0) {{
                recognition.onend = null;
                const hiddenInput = window.parent.document.querySelector('input[aria-label="hidden_ans"]');
                if (hiddenInput) {{
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                    nativeInputValueSetter.call(hiddenInput, finalTranscript);
                    hiddenInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    
                    setTimeout(() => {{
                        const submitBtn = Array.from(window.parent.document.querySelectorAll('button')).find(btn => btn.innerText === 'hidden_submit');
                        if (submitBtn) submitBtn.click();
                    }}, 200);
                }}
            }}
        }};

        try {{ recognition.start(); }} catch(e) {{}}
    }})();
    </script>
    """, height=60, scrolling=False)


def render_audio_waveform_hud(t: dict, is_speaking: bool = False):
    """Renders visual audio waveform animation during interview session."""
    st.markdown(clean_html(f"""
    <div style="display:flex; align-items:center; justify-content:center; gap:6px; height:48px; margin: 12px 0;">
        <div class="ac-wave-bar" style="height:14px; width:4px; background:{t['accent']}; border-radius:4px; animation: acWave 1.2s infinite ease-in-out;"></div>
        <div class="ac-wave-bar" style="height:26px; width:4px; background:{t['accent']}; border-radius:4px; animation: acWave 0.9s infinite ease-in-out 0.2s;"></div>
        <div class="ac-wave-bar" style="height:38px; width:4px; background:{t['gold']}; border-radius:4px; animation: acWave 1.4s infinite ease-in-out 0.4s;"></div>
        <div class="ac-wave-bar" style="height:22px; width:4px; background:{t['accent']}; border-radius:4px; animation: acWave 1.0s infinite ease-in-out 0.1s;"></div>
        <div class="ac-wave-bar" style="height:34px; width:4px; background:{t['gold']}; border-radius:4px; animation: acWave 1.3s infinite ease-in-out 0.3s;"></div>
        <div class="ac-wave-bar" style="height:16px; width:4px; background:{t['accent']}; border-radius:4px; animation: acWave 1.1s infinite ease-in-out 0.5s;"></div>
    </div>
    <style>
    @keyframes acWave {{
        0%, 100% {{ transform: scaleY(0.4); opacity: 0.6; }}
        50% {{ transform: scaleY(1.0); opacity: 1.0; }}
    }}
    </style>
    """), unsafe_allow_html=True)

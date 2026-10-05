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
    <script>
    (function runParentSTT() {{
        const pWin = window.parent;
        const pDoc = pWin.document;

        // Ensure all component iframes have microphone permission
        try {{
            const iframes = pDoc.querySelectorAll('iframe');
            iframes.forEach(f => f.setAttribute('allow', 'microphone; camera;'));
        }} catch(e) {{}}

        // Initialize Speech Recognition on top window
        const SpeechRec = pWin.SpeechRecognition || pWin.webkitSpeechRecognition;
        if (!SpeechRec) {{
            const label = pDoc.getElementById('stt-status-label');
            if (label) label.innerText = "❌ Speech Recognition not supported in browser";
            return;
        }}

        if (pWin._activeSTT) {{
            try {{ pWin._activeSTT.stop(); }} catch(e) {{}}
        }}

        const rec = new SpeechRec();
        pWin._activeSTT = rec;

        rec.continuous = true;
        rec.interimResults = true;
        rec.lang = '{lang_code}';

        let finalTranscript = "";
        let submitTimer = null;

        rec.onstart = function() {{
            const label = pDoc.getElementById('stt-status-label');
            if (label) label.innerText = "🔴 Listening... Speak your answer.";
        }};

        rec.onerror = function(event) {{
            console.warn("STT Parent Error:", event.error);
            const label = pDoc.getElementById('stt-status-label');
            const preview = pDoc.getElementById('stt-transcript-preview');
            if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {{
                if (label) label.innerText = "⚠️ Click here to enable Microphone";
                if (preview) preview.innerText = "(Browser blocked microphone access. Click this text to enable.)";
            }}
        }};

        rec.onresult = function(event) {{
            let interim = "";
            for (let i = event.resultIndex; i < event.results.length; ++i) {{
                if (event.results[i].isFinal) {{
                    finalTranscript += event.results[i][0].transcript + " ";
                }} else {{
                    interim += event.results[i][0].transcript;
                }}
            }}
            const currentText = (finalTranscript + " " + interim).trim();

            const preview = pDoc.getElementById('stt-transcript-preview');
            if (preview && currentText) {{
                preview.innerText = '"' + currentText + '"';
            }}

            if (currentText.length > 0) {{
                if (submitTimer) clearTimeout(submitTimer);

                // Wait 1.8 seconds of silence after user finishes speaking
                submitTimer = setTimeout(() => {{
                    rec.onend = null;
                    try {{ rec.stop(); }} catch(e) {{}}

                    const label = pDoc.getElementById('stt-status-label');
                    if (label) label.innerText = "🟢 Answer Captured! Submitting...";

                    const hiddenInput = pDoc.querySelector('input[aria-label="hidden_ans"]');
                    if (hiddenInput) {{
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(pWin.HTMLInputElement.prototype, 'value').set;
                        nativeInputValueSetter.call(hiddenInput, currentText);
                        hiddenInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        hiddenInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

                        setTimeout(() => {{
                            const btns = Array.from(pDoc.querySelectorAll('button'));
                            const submitBtn = btns.find(b => b.textContent && b.textContent.includes('hidden_submit'));
                            if (submitBtn) {{
                                submitBtn.click();
                            }}
                        }}, 150);
                    }}
                }}, 1800);
            }}
        }};

        // Global manual click trigger for top window
        pWin._forceStartSTT = function() {{
            try {{ rec.start(); }} catch(e) {{}}
        }};

        try {{ rec.start(); }} catch(e) {{}}
    }})();
    </script>
    """, height=0, scrolling=False)


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

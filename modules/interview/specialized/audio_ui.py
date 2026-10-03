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
    on_transcript_callback=None,
):
    """
    Renders browser speech recognition component via Web Speech API with live transcript capture.
    """
    lang_code = "hi-IN" if "hindi" in language.lower() or "hinglish" in language.lower() else "en-IN"

    components.html(f"""
    <div id="ac-stt-container" style="display:flex; align-items:center; justify-content:center; gap:12px; margin: 10px 0;">
        <button id="ac-mic-trigger-btn" style="
            background: linear-gradient(135deg, #4F46E5, #6366F1);
            color: #FFFFFF;
            border: none;
            border-radius: 50px;
            padding: 10px 24px;
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
            transition: transform 0.18s ease;
        ">
            <span id="ac-mic-icon">🎙️</span>
            <span id="ac-mic-label">Start Speaking (Mic On)</span>
        </button>
        <span id="ac-mic-live-indicator" style="font-size:0.86rem; color:#6B7280; font-style:italic;"></span>
    </div>

    <script>
    (function initSTT() {{
        const btn = document.getElementById('ac-mic-trigger-btn');
        const icon = document.getElementById('ac-mic-icon');
        const label = document.getElementById('ac-mic-label');
        const liveInd = document.getElementById('ac-mic-live-indicator');
        if (!btn) return;

        let recognition = null;
        let isListening = false;

        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) {{
            label.innerText = "Speech Recognition not supported in this browser";
            btn.disabled = true;
            return;
        }}

        recognition = new SpeechRec();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = '{lang_code}';

        btn.onclick = function() {{
            if (!isListening) {{
                try {{
                    recognition.start();
                    isListening = true;
                    btn.style.background = "linear-gradient(135deg, #EF4444, #DC2626)";
                    label.innerText = "Listening... Click to Stop & Submit";
                    liveInd.innerText = "🔴 Recording your voice...";
                }} catch (e) {{
                    console.log(e);
                }}
            }} else {{
                recognition.stop();
                isListening = false;
                btn.style.background = "linear-gradient(135deg, #4F46E5, #6366F1)";
                label.innerText = "Start Speaking (Mic On)";
                liveInd.innerText = "✅ Voice recorded.";
            }}
        }};

        recognition.onresult = function(event) {{
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {{
                if (event.results[i].isFinal) {{
                    finalTranscript += event.results[i][0].transcript;
                }}
            }}
            if (finalTranscript.trim().length > 0) {{
                // Populate parent Streamlit text input box if accessible
                const parentInputs = window.parent.document.querySelectorAll('textarea, input[type="text"]');
                for (let inp of parentInputs) {{
                    if (inp.getAttribute('aria-label') && inp.getAttribute('aria-label').includes('Answer')) {{
                        inp.value = (inp.value ? inp.value + ' ' : '') + finalTranscript;
                        inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        break;
                    }}
                }}
            }}
        }};

        recognition.onerror = function(event) {{
            console.warn('Speech recognition error:', event.error);
            isListening = false;
            btn.style.background = "linear-gradient(135deg, #4F46E5, #6366F1)";
            label.innerText = "Start Speaking (Mic On)";
            liveInd.innerText = "⚠️ Voice captured or microphone released.";
        }};
    }})();
    </script>
    """, height=65, scrolling=False)


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

"""
AchieveHire — Job Related Interview Audio & Voice Component
Enforces the core rule:
QUESTIONS ARE NEVER DISPLAYED AS READABLE TEXT ON SCREEN DURING LIVE SESSIONS.
Uses Web Speech API via components.html with retry logic complying with Streamlit global rules.
"""

import streamlit as st
import streamlit.components.v1 as components
import json


def render_voice_synthesis_player(
    text_to_speak: str,
    language: str = "English",
    interviewer_gender: str = "female",
    speech_rate: float = 0.95,
    key: str = "job_tts_player",
):
    """
    Synthesizes the interviewer's question or reaction via browser Web Speech API.
    """
    escaped_text = json.dumps(text_to_speak)
    lang_code = "hi-IN" if "hindi" in language.lower() or "hinglish" in language.lower() else "en-US"
    gender_pref = "male" if "male" in interviewer_gender.lower() else "female"

    components.html(f"""
    <script>
    (function runTTS() {{
        if (!('speechSynthesis' in window)) return;

        window.speechSynthesis.cancel();

        const text = {escaped_text};
        if (!text || text.trim() === '') return;

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = {speech_rate};
        utterance.pitch = {1.0 if gender_pref == 'male' else 1.15};
        utterance.lang = '{lang_code}';

        const voices = window.speechSynthesis.getVoices();
        let chosenVoice = null;
        if (voices.length > 0) {{
            chosenVoice = voices.find(v => v.lang.includes('{lang_code[:2]}') && v.name.toLowerCase().includes('{gender_pref}')) ||
                          voices.find(v => v.lang.includes('{lang_code[:2]}')) ||
                          voices[0];
            if (chosenVoice) utterance.voice = chosenVoice;
        }}

        utterance.onstart = function() {{
            const statusEl = window.parent.document.getElementById('job-interviewer-status-text');
            if (statusEl) statusEl.innerText = "🎙️ Interviewer is asking... (Listen Carefully)";
        }};

        utterance.onend = function() {{
            const statusEl = window.parent.document.getElementById('job-interviewer-status-text');
            if (statusEl) statusEl.innerText = "🎧 Listening... Click microphone or speak your answer.";
        }};

        window.speechSynthesis.speak(utterance);
    }})();
    </script>
    """, height=0, scrolling=False)


def render_voice_recognition_widget(
    prompt_key: str = "job_stt_box",
    language: str = "English",
):
    """
    Renders browser speech recognition component via Web Speech API with live transcript capture.
    """
    lang_code = "hi-IN" if "hindi" in language.lower() or "hinglish" in language.lower() else "en-IN"

    components.html(f"""
    <div id="job-stt-container" style="display:flex; align-items:center; justify-content:center; gap:12px; margin: 8px 0;">
        <button id="job-mic-trigger-btn" style="
            background: linear-gradient(135deg, #2563EB, #3B82F6);
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
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
            transition: transform 0.18s ease;
        ">
            <span id="job-mic-icon" style="font-size:1.2rem;">🎙️</span>
            <span id="job-mic-label">Click &amp; Speak Answer</span>
        </button>
        <span id="job-rec-indicator" style="display:none; color:#EF4444; font-weight:700; font-size:0.85rem; align-items:center; gap:6px;">
            <span style="display:inline-block; width:10px; height:10px; background:#EF4444; border-radius:50%; animation:pulse 1s infinite;"></span>
            Recording Active...
        </span>
    </div>

    <style>
    @keyframes pulse {{
        0% {{ transform: scale(0.9); opacity: 0.7; }}
        50% {{ transform: scale(1.3); opacity: 1; }}
        100% {{ transform: scale(0.9); opacity: 0.7; }}
    }}
    </style>

    <script>
    (function initSTT() {{
        const btn = document.getElementById('job-mic-trigger-btn');
        const icon = document.getElementById('job-mic-icon');
        const label = document.getElementById('job-mic-label');
        const indicator = document.getElementById('job-rec-indicator');

        if (!btn) return;

        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) {{
            label.innerText = "Speech API not supported in browser";
            btn.style.opacity = "0.6";
            btn.disabled = true;
            return;
        }}

        let recognition = new SpeechRec();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = '{lang_code}';

        let isRecording = false;
        let finalTranscript = "";

        btn.onclick = function() {{
            if (!isRecording) {{
                try {{
                    recognition.start();
                    isRecording = true;
                    label.innerText = "Stop Recording";
                    icon.innerText = "⏹️";
                    btn.style.background = "#DC2626";
                    indicator.style.display = "inline-flex";
                }} catch(e) {{
                    console.error(e);
                }}
            }} else {{
                recognition.stop();
                isRecording = false;
                label.innerText = "Click & Speak Answer";
                icon.innerText = "🎙️";
                btn.style.background = "linear-gradient(135deg, #2563EB, #3B82F6)";
                indicator.style.display = "none";
            }}
        }};

        recognition.onresult = function(event) {{
            let interim = "";
            for (let i = event.resultIndex; i < event.results.length; ++i) {{
                if (event.results[i].isFinal) {{
                    finalTranscript += event.results[i][0].transcript + " ";
                }} else {{
                    interim += event.results[i][0].transcript;
                }}
            }}

            const combined = (finalTranscript + " " + interim).trim();

            const parentDoc = window.parent.document;
            const textareas = parentDoc.querySelectorAll('textarea');
            for (let ta of textareas) {{
                if (ta.getAttribute('aria-label') && ta.getAttribute('aria-label').toLowerCase().includes('answer')) {{
                    ta.value = combined;
                    ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    break;
                }}
            }}
        }};

        recognition.onerror = function(event) {{
            console.warn("Speech recognition error: ", event.error);
            isRecording = false;
            label.innerText = "Click & Speak Answer";
            icon.innerText = "🎙️";
            btn.style.background = "linear-gradient(135deg, #2563EB, #3B82F6)";
            indicator.style.display = "none";
        }};

        recognition.onend = function() {{
            if (isRecording) {{
                try {{ recognition.start(); }} catch(e) {{}}
            }}
        }};
    }})();
    </script>
    """, height=56, scrolling=False)

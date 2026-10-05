# -*- coding: utf-8 -*-
"""
AchieveHire — Last-Minute Preparation Audio & Voice HUD
Enforces the core rule:
QUESTIONS ARE NEVER DISPLAYED AS READABLE TEXT ON SCREEN DURING LIVE SESSIONS.
"""

import streamlit as st
import streamlit.components.v1 as components
import json


def render_voice_synthesis_player(
    text_to_speak: str,
    language: str = "English",
    interviewer_gender: str = "female",
    speech_rate: float = 0.95,
    key: str = "lm_tts_player",
):
    """Synthesizes the interviewer's question or reaction via browser Web Speech API."""
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
            const statusEl = window.parent.document.getElementById('lm-interviewer-status-text');
            if (statusEl) statusEl.innerText = "🎙️ Panel Interviewer is asking... (Listen Carefully)";
        }};

        utterance.onend = function() {{
            const statusEl = window.parent.document.getElementById('lm-interviewer-status-text');
            if (statusEl) statusEl.innerText = "🎧 Listening... Click microphone or speak your response.";
        }};

        window.speechSynthesis.speak(utterance);
    }})();
    </script>
    """, height=0, scrolling=False)


def render_voice_recognition_widget(
    prompt_key: str = "lm_stt_box",
    language: str = "English",
):
    lang_code = "hi-IN" if "hindi" in language.lower() or "hinglish" in language.lower() else "en-IN"

    components.html(f"""
    <div id="stt-widget-box" style="display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; margin: 6px 0; cursor:pointer;" onclick="forceStartMic()">
        <div id="stt-status-pill" style="display:inline-flex; align-items:center; gap:8px; background:#FEF2F2; border:1px solid #F87171; padding:8px 20px; border-radius:50px; color:#DC2626; font-weight:700; font-size:0.92rem; box-shadow:0 2px 8px rgba(220,38,38,0.15); transition:all 0.3s ease;">
            <span id="stt-dot" style="display:inline-block; width:10px; height:10px; background:#DC2626; border-radius:50%; animation:pulse 1.2s infinite;"></span>
            <span id="stt-status-label">🔴 Listening... Speak your answer.</span>
        </div>
        <div id="stt-transcript-preview" style="font-size:0.82rem; color:#475569; font-style:italic; max-width:90%; text-align:center; min-height:18px;">
            (Speak into your microphone. Answer auto-submits when you pause.)
        </div>
    </div>
    <style>
    @keyframes pulse {{
        0% {{ transform: scale(0.85); opacity: 0.5; }}
        50% {{ transform: scale(1.25); opacity: 1; }}
        100% {{ transform: scale(0.85); opacity: 0.5; }}
    }}
    </style>

    <script>
    let recognition = null;

    function forceStartMic() {{
        if (recognition) {{
            try {{ recognition.start(); }} catch(e) {{}}
        }}
    }}

    (function initSTT() {{
        function startRealtimeCountdown() {{
            try {{
                const pDoc = window.parent.document;
                let timerEl = pDoc.getElementById('job-live-timer-display') || pDoc.getElementById('spec-live-timer-display') || pDoc.getElementById('live-timer-display');
                if (!timerEl) {{
                    const divs = pDoc.querySelectorAll('div');
                    for (let d of divs) {{
                        if (d.innerText && /^[0-9]{{2}}:[0-9]{{2}}$/.test(d.innerText.trim()) && d.children.length === 0) {{
                            timerEl = d;
                            break;
                        }}
                    }}
                }}
                if (timerEl && !timerEl.getAttribute('data-timer-running')) {{
                    timerEl.setAttribute('data-timer-running', 'true');
                    let text = timerEl.innerText.trim();
                    let parts = text.split(':');
                    if (parts.length === 2) {{
                        let totalSec = parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
                        if (!isNaN(totalSec) && totalSec > 0) {{
                            setInterval(() => {{
                                if (totalSec > 0) {{
                                    totalSec--;
                                    let m = Math.floor(totalSec / 60);
                                    let s = totalSec % 60;
                                    timerEl.innerText = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
                                }}
                            }}, 1000);
                        }}
                    }}
                }}
            }} catch(e) {{}}
        }}
        startRealtimeCountdown();
        setInterval(startRealtimeCountdown, 500);

        function hideFields() {{
            try {{
                const pDoc = window.parent.document;
                const inp = pDoc.querySelector('input[aria-label="hidden_ans"]');
                if (inp) {{
                    const inputContainer = inp.closest('div[data-testid="stElementContainer"]') || inp.closest('div[data-testid="stTextInput"]');
                    if (inputContainer) {{
                        inputContainer.style.setProperty('display', 'none', 'important');
                        inputContainer.style.setProperty('height', '0px', 'important');
                        const nextContainer = inputContainer.nextElementSibling;
                        if (nextContainer) {{
                            nextContainer.style.setProperty('display', 'none', 'important');
                            nextContainer.style.setProperty('height', '0px', 'important');
                        }}
                    }}
                }}
            }} catch(e) {{}}
        }}
        hideFields();
        setInterval(hideFields, 100);

        const label = document.getElementById('stt-status-label');
        const preview = document.getElementById('stt-transcript-preview');
        const pill = document.getElementById('stt-status-pill');
        const dot = document.getElementById('stt-dot');

        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) {{
            if (label) label.innerText = "❌ Speech API not supported in browser";
            return;
        }}

        recognition = new SpeechRec();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = '{lang_code}';

        let finalTranscript = "";

        recognition.onstart = function() {{
            if (label) label.innerText = "🔴 Listening... Speak your answer.";
            if (pill) {{ pill.style.background = "#FEF2F2"; pill.style.borderColor = "#F87171"; pill.style.color = "#DC2626"; }}
            if (dot) dot.style.background = "#DC2626";
        }};

        recognition.onerror = function(event) {{
            console.warn("STT Error:", event.error);
            if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {{
                if (label) label.innerText = "⚠️ Click to Enable Microphone";
                if (preview) preview.innerText = "(Browser blocked microphone. Click this box to enable permissions.)";
            }}
        }};

        recognition.onend = function() {{
            if (finalTranscript.trim().length === 0) {{
                try {{ recognition.start(); }} catch(e) {{}}
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
            const currentText = (finalTranscript + " " + interim).trim();
            if (preview && currentText) {{
                preview.innerText = '"' + currentText + '"';
            }}

            if (finalTranscript.trim().length > 0) {{
                recognition.onend = null;
                if (label) label.innerText = "🟢 Answer Captured! Submitting...";
                if (pill) {{ pill.style.background = "#ECFDF5"; pill.style.borderColor = "#10B981"; pill.style.color = "#047857"; }}
                if (dot) dot.style.background = "#10B981";

                const pDoc = window.parent.document;
                const hiddenInput = pDoc.querySelector('input[aria-label="hidden_ans"]');
                if (hiddenInput) {{
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                    nativeInputValueSetter.call(hiddenInput, finalTranscript.trim());
                    hiddenInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    hiddenInput.dispatchEvent(new Event('change', {{ bubbles: true }}));

                    setTimeout(() => {{
                        const btns = Array.from(pDoc.querySelectorAll('button'));
                        const submitBtn = btns.find(b => b.textContent && b.textContent.includes('hidden_submit'));
                        if (submitBtn) {{
                            submitBtn.click();
                            submitBtn.dispatchEvent(new MouseEvent('click', {{ bubbles: true, cancelable: true, view: window.parent }}));
                        }}
                    }}, 200);
                }}
            }}
        }};

        try {{ recognition.start(); }} catch(e) {{}}
    }})();
    </script>
    """, height=70, scrolling=False)
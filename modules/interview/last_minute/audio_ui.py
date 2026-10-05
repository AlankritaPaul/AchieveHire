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
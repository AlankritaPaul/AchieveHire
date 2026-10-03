/**
 * AchieveHire - Speech Synthesis & Voice Input Engine
 * Handles Text-to-Speech in English, Hindi, Hinglish, microphone capture, and audio waveforms.
 */
class SpeechEngine {
    constructor() {
        this.synth = window.speechSynthesis || null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.analyser = null;
        this.audioCtx = null;
        this.canvasCtx = null;
        this.animId = null;
    }

    /**
     * Speaks the interviewer's prompt verbally in the selected language.
     * @param {string} text - text to speak
     * @param {string} language - 'English', 'Hindi', or 'Hinglish'
     * @param {function} onEnd - callback when done speaking
     */
    speak(text, language = 'English', onEnd = null) {
        if (!this.synth) {
            console.warn('[SpeechEngine] SpeechSynthesis not supported in this browser.');
            if (onEnd) onEnd();
            return;
        }

        this.synth.cancel(); // Stop any pending speech

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.95;
        utterance.pitch = 1.0;

        // Language code mapping
        if (language === 'Hindi') {
            utterance.lang = 'hi-IN';
        } else if (language === 'Hinglish') {
            // Use en-IN for natural Indian conversational cadence
            utterance.lang = 'en-IN';
        } else {
            utterance.lang = 'en-US';
        }

        const voices = this.synth.getVoices();
        const matchedVoice = voices.find(v => v.lang.startsWith(utterance.lang)) || voices[0];
        if (matchedVoice) utterance.voice = matchedVoice;

        utterance.onend = () => {
            if (onEnd) onEnd();
        };

        this.synth.speak(utterance);
    }

    stopSpeaking() {
        if (this.synth) this.synth.cancel();
    }

    /**
     * Starts microphone recording with real-time waveform animation
     */
    async startRecording(canvasElement, onDataAvailable = null) {
        if (this.isRecording) return;
        this.audioChunks = [];

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);

            this.mediaRecorder.ondataavailable = e => {
                if (e.data.size > 0) this.audioChunks.push(e.data);
            };

            this.mediaRecorder.start(250);
            this.isRecording = true;

            // Start Canvas Waveform Visualization
            if (canvasElement) {
                this.startWaveformVisualizer(stream, canvasElement);
            }
        } catch (err) {
            console.error('[SpeechEngine] Microphone permission denied or unavailable:', err);
            throw err;
        }
    }

    stopRecording() {
        return new Promise(resolve => {
            if (!this.mediaRecorder || !this.isRecording) {
                resolve(null);
                return;
            }

            this.mediaRecorder.onstop = () => {
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
                this.isRecording = false;
                this.stopWaveformVisualizer();
                resolve(audioBlob);
            };

            this.mediaRecorder.stop();
            // Stop media stream tracks
            if (this.mediaRecorder.stream) {
                this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
            }
        });
    }

    startWaveformVisualizer(stream, canvas) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        this.audioCtx = new AudioCtx();
        this.analyser = this.audioCtx.createAnalyser();
        this.analyser.fftSize = 128;

        const source = this.audioCtx.createMediaStreamSource(stream);
        source.connect(this.analyser);

        this.canvasCtx = canvas.getContext('2d');
        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        const draw = () => {
            if (!this.isRecording) return;
            this.animId = requestAnimationFrame(draw);
            this.analyser.getByteFrequencyData(dataArray);

            this.canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
            const barWidth = (canvas.width / bufferLength) * 2;
            let x = 0;

            for (let i = 0; i < bufferLength; i++) {
                const barHeight = (dataArray[i] / 255) * canvas.height;
                this.canvasCtx.fillStyle = '#3B82F6';
                this.canvasCtx.fillRect(x, canvas.height - barHeight, barWidth - 1, barHeight);
                x += barWidth;
            }
        };

        draw();
    }

    stopWaveformVisualizer() {
        if (this.animId) cancelAnimationFrame(this.animId);
        if (this.audioCtx && this.audioCtx.state !== 'closed') {
            this.audioCtx.close().catch(() => {});
        }
    }
}

window.speechEngine = new SpeechEngine();

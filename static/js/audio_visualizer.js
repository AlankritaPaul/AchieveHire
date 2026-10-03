/**
 * AchieveHire - Web Audio API Real-time Waveform & Speech Visualizer
 * Animates interactive frequency bars during candidate microphone responses.
 */
class AudioWaveformVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.canvasCtx = this.canvas ? this.canvas.getContext('2d') : null;
        this.audioCtx = null;
        this.analyser = null;
        this.source = null;
        this.animationId = null;
        this.isVisualizing = false;
        this.colorGradient = null;
    }

    async start(stream) {
        if (!this.canvas || !this.canvasCtx) return;
        if (!stream) return;

        try {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            this.audioCtx = new AudioContextClass();
            this.analyser = this.audioCtx.createAnalyser();
            this.analyser.fftSize = 256;

            this.source = this.audioCtx.createMediaStreamSource(stream);
            this.source.connect(this.analyser);

            this.isVisualizing = true;
            this.draw();
        } catch (err) {
            console.warn('[AudioVisualizer] Could not start audio visualizer:', err);
        }
    }

    draw() {
        if (!this.isVisualizing || !this.analyser || !this.canvasCtx) return;

        this.animationId = requestAnimationFrame(() => this.draw());

        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        this.analyser.getByteFrequencyData(dataArray);

        const width = this.canvas.width;
        const height = this.canvas.height;

        this.canvasCtx.clearRect(0, 0, width, height);

        const barWidth = (width / bufferLength) * 2.5;
        let barHeight;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            barHeight = (dataArray[i] / 255) * height;

            // Generate clean modern gradient
            const r = Math.round(59 + (barHeight / height) * (239 - 59));
            const g = Math.round(130 - (barHeight / height) * (130 - 68));
            const b = Math.round(246 - (barHeight / height) * (246 - 68));

            this.canvasCtx.fillStyle = `rgb(${r},${g},${b})`;
            this.canvasCtx.fillRect(x, height - barHeight, barWidth - 1, barHeight);

            x += barWidth + 1;
        }
    }

    stop() {
        this.isVisualizing = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        if (this.audioCtx && this.audioCtx.state !== 'closed') {
            this.audioCtx.close().catch(() => {});
        }
        if (this.canvasCtx && this.canvas) {
            this.canvasCtx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AudioWaveformVisualizer };
} else {
    window.AudioWaveformVisualizer = AudioWaveformVisualizer;
}

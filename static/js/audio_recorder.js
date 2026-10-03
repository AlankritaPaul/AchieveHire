/**
 * AchieveHire — Real-Time Web Audio API Voice Recorder & Audio Pipeline
 * Handles microphone permissions, real-time waveform visualization,
 * AudioContext gain calibration, and WAV blob generation for AI evaluation.
 */

class AchieveHireAudioRecorder {
  constructor(options = {}) {
    this.audioContext = null;
    this.mediaStream = null;
    this.mediaRecorder = null;
    this.audioChunks = [];
    this.analyserNode = null;
    this.gainNode = null;
    this.isRecording = false;
    this.isPaused = false;
    this.sampleRate = options.sampleRate || 44100;
    this.onVolumeChange = options.onVolumeChange || null;
    this.onStateChange = options.onStateChange || null;
  }

  async initializeMicrophone() {
    try {
      const constraints = {
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          channelCount: 1,
          sampleRate: this.sampleRate,
        },
      };

      this.mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this.audioContext = new AudioCtx({ sampleRate: this.sampleRate });

      const sourceNode = this.audioContext.createMediaStreamSource(this.mediaStream);
      this.analyserNode = this.audioContext.createAnalyser();
      this.analyserNode.fftSize = 256;
      this.analyserNode.smoothingTimeConstant = 0.8;

      this.gainNode = this.audioContext.createGain();
      this.gainNode.gain.value = 1.0;

      sourceNode.connect(this.gainNode);
      this.gainNode.connect(this.analyserNode);

      this.setupRecorder();
      return true;
    } catch (err) {
      console.error("[AchieveHire Audio] Microphone initialization failed:", err);
      throw new Error("Microphone permission denied or device not found.");
    }
  }

  setupRecorder() {
    let mimeType = "audio/webm;codecs=opus";
    if (!MediaRecorder.isTypeSupported(mimeType)) {
      mimeType = MediaRecorder.isTypeSupported("audio/mp4")
        ? "audio/mp4"
        : "audio/ogg";
    }

    this.mediaRecorder = new MediaRecorder(this.mediaStream, { mimeType });
    this.mediaRecorder.ondataavailable = (event) => {
      if (event.data && event.data.size > 0) {
        this.audioChunks.push(event.data);
      }
    };
  }

  startRecording() {
    if (!this.mediaRecorder) return;
    this.audioChunks = [];
    this.mediaRecorder.start(250);
    this.isRecording = true;
    this.isPaused = false;
    this.startVolumeMonitoring();
    if (this.onStateChange) this.onStateChange("recording");
  }

  pauseRecording() {
    if (this.mediaRecorder && this.isRecording && !this.isPaused) {
      this.mediaRecorder.pause();
      this.isPaused = true;
      if (this.onStateChange) this.onStateChange("paused");
    }
  }

  resumeRecording() {
    if (this.mediaRecorder && this.isRecording && this.isPaused) {
      this.mediaRecorder.resume();
      this.isPaused = false;
      if (this.onStateChange) this.onStateChange("recording");
    }
  }

  async stopRecording() {
    return new Promise((resolve) => {
      if (!this.mediaRecorder) {
        resolve(null);
        return;
      }

      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, {
          type: this.mediaRecorder.mimeType,
        });
        this.isRecording = false;
        this.isPaused = false;
        this.cleanupAudioContext();
        if (this.onStateChange) this.onStateChange("stopped");
        resolve(audioBlob);
      };

      this.mediaRecorder.stop();
    });
  }

  startVolumeMonitoring() {
    const dataArray = new Uint8Array(this.analyserNode.frequencyBinCount);
    const monitor = () => {
      if (!this.isRecording || this.isPaused) return;
      this.analyserNode.getByteFrequencyData(dataArray);
      let sum = 0;
      for (let i = 0; i < dataArray.length; i++) {
        sum += dataArray[i];
      }
      const avg = sum / dataArray.length;
      const normalizedVolume = Math.min(100, Math.round((avg / 255) * 100));
      if (this.onVolumeChange) {
        this.onVolumeChange(normalizedVolume);
      }
      requestAnimationFrame(monitor);
    };
    requestAnimationFrame(monitor);
  }

  cleanupAudioContext() {
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach((track) => track.stop());
      this.mediaStream = null;
    }
    if (this.audioContext && this.audioContext.state !== "closed") {
      this.audioContext.close();
      this.audioContext = null;
    }
  }
}

window.AchieveHireAudioRecorder = AchieveHireAudioRecorder;

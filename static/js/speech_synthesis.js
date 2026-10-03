/**
 * AchieveHire — Real-Time Web Speech API Interviewer Voice Engine
 * Handles natural vocal delivery across English, Hindi, and Hinglish.
 * Features rate regulation, gender matching, and sentence-boundary chunking.
 */

class AchieveHireSpeechEngine {
  constructor(options = {}) {
    this.synth = window.speechSynthesis || null;
    this.voices = [];
    this.preferredLanguage = options.language || "English";
    this.interviewerGender = options.gender || "Female";
    this.isSpeaking = false;
    this.onBoundary = options.onBoundary || null;
    this.onEnd = options.onEnd || null;

    if (this.synth) {
      this.loadVoices();
      if (this.synth.onvoiceschanged !== undefined) {
        this.synth.onvoiceschanged = () => this.loadVoices();
      }
    }
  }

  loadVoices() {
    if (!this.synth) return;
    this.voices = this.synth.getVoices();
  }

  getBestVoice(language, gender) {
    if (!this.voices || this.voices.length === 0) {
      this.loadVoices();
    }

    const langLower = (language || "english").toLowerCase();
    const isMale = (gender || "female").toLowerCase() === "male";

    let targetLangCode = "en";
    if (langLower === "hindi" || langLower === "hinglish") {
      targetLangCode = "hi";
    }

    // 1. Filter by language code
    let matching = this.voices.filter((v) =>
      v.lang.toLowerCase().startsWith(targetLangCode)
    );

    if (matching.length === 0) {
      matching = this.voices.filter((v) =>
        v.lang.toLowerCase().startsWith("en")
      );
    }

    // 2. Filter by gender if available in name
    const genderMatcher = isMale
      ? /(male|david|mark|george|ravi|madhav|guy)/i
      : /(female|zira|samantha|kavita|priya|swara|natural)/i;

    const genderMatched = matching.find((v) => genderMatcher.test(v.name));
    if (genderMatched) return genderMatched;

    return matching[0] || this.voices[0] || null;
  }

  speak(text, options = {}) {
    if (!this.synth || !text) return;

    this.stop();

    const utterance = new SpeechSynthesisUtterance(text);
    const selectedVoice = this.getBestVoice(
      options.language || this.preferredLanguage,
      options.gender || this.interviewerGender
    );

    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }

    utterance.rate = options.rate || 0.95;
    utterance.pitch = options.pitch || (options.gender === "Male" ? 0.95 : 1.05);
    utterance.volume = options.volume || 1.0;

    utterance.onstart = () => {
      this.isSpeaking = true;
    };

    utterance.onend = () => {
      this.isSpeaking = false;
      if (this.onEnd) this.onEnd();
    };

    utterance.onerror = (e) => {
      console.warn("[AchieveHire Speech] Utterance error:", e);
      this.isSpeaking = false;
      if (this.onEnd) this.onEnd();
    };

    this.synth.speak(utterance);
  }

  stop() {
    if (this.synth && this.synth.speaking) {
      this.synth.cancel();
      this.isSpeaking = false;
    }
  }

  pause() {
    if (this.synth && this.synth.speaking) {
      this.synth.pause();
    }
  }

  resume() {
    if (this.synth && this.synth.paused) {
      this.synth.resume();
    }
  }
}

window.AchieveHireSpeechEngine = AchieveHireSpeechEngine;

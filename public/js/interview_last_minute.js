/**
 * AchieveHire - Last-Minute Preparation Interview Module
 * Rapid, intensive 30-minute interview simulation with panel interviewers.
 * Features Strategy Advisory dialog: Left: "Back & Practice", Right: "Anyway Continue".
 */

class LastMinuteManager {
    constructor() {
        this.durationSeconds = 1800; // 30 minutes
        this.remainingSeconds = 1800;
        this.timerId = null;
        this.mode = 'Specialized'; // 'Specialized' or 'Job Related'
        this.topic = '';
        this.company = '';
        this.language = 'English';
        this.qaList = [];
        this.currentStage = 'Introduction'; // Introduction -> Easy -> Moderate -> Hard
        this.panel = [
            { name: 'Arjun Mehta', title: 'Lead System Architect', avatar: '👨‍💼' },
            { name: 'Priya Sharma', title: 'Senior Engineering Manager', avatar: '👩‍💻' },
            { name: 'Rohan Gupta', title: 'Domain Specialist', avatar: '👨‍🔬' }
        ];
        this.currentSpeakerIdx = 0;
    }

    startTimer(onTick, onComplete) {
        if (this.timerId) clearInterval(this.timerId);
        this.remainingSeconds = this.durationSeconds;

        this.timerId = setInterval(() => {
            if (this.remainingSeconds <= 0) {
                clearInterval(this.timerId);
                this.timerId = null;
                if (onComplete) onComplete();
                return;
            }
            this.remainingSeconds--;
            if (onTick) onTick(this.getFormattedTime(), this.remainingSeconds);
        }, 1000);
    }

    stopTimer() {
        if (this.timerId) {
            clearInterval(this.timerId);
            this.timerId = null;
        }
    }

    getFormattedTime() {
        const mins = Math.floor(this.remainingSeconds / 60);
        const secs = this.remainingSeconds % 60;
        return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    getCurrentSpeaker() {
        return this.panel[this.currentSpeakerIdx % this.panel.length];
    }

    getNextQuestion() {
        const speaker = this.getCurrentSpeaker();
        this.currentSpeakerIdx++;

        let questionText = '';
        if (this.qaList.length === 0) {
            this.currentStage = 'Introduction';
            questionText = 'Please introduce yourself, your core technical experience, and key accomplishments.';
        } else if (this.qaList.length === 1) {
            this.currentStage = 'Easy';
            questionText = `Let us dive into ${this.topic}. Can you explain the core fundamentals and design principles you rely on most frequently?`;
        } else if (this.qaList.length === 2) {
            this.currentStage = 'Moderate';
            questionText = `How do you apply these concepts in a practical production environment when handling latency and scaling challenges?`;
        } else {
            this.currentStage = 'Hard';
            questionText = `Describe a complex failure scenario or architectural trade-off you encountered with ${this.topic}. How did you resolve it under pressure?`;
        }

        return {
            speaker,
            stage: this.currentStage,
            questionText
        };
    }

    recordAnswer(question, answerText) {
        const score = Math.floor(80 + Math.random() * 16);
        this.qaList.push({
            question,
            answer: answerText || '(Voice Response Captured)',
            score
        });

        // Determine if rehearsal should conclude (4 rigorous questions over 30 min)
        const isDone = this.qaList.length >= 4 || this.remainingSeconds <= 60;
        return { isDone, score };
    }

    finalizeAttempt() {
        this.stopTimer();
        const total = this.qaList.reduce((acc, q) => acc + q.score, 0);
        const overallScore = Math.round(total / (this.qaList.length || 1));

        const attemptRecord = {
            mode: `Last-Minute Prep for ${this.mode}`,
            topic: this.topic,
            company: this.company || 'Technical Panel',
            language: this.language,
            duration: '30 Minutes',
            overallScore,
            qaList: this.qaList
        };

        // Save under persistent candidate user profile
        if (window.state) {
            window.state.saveInterviewAttempt(attemptRecord);
        }

        return attemptRecord;
    }
}

window.lastMinuteManager = new LastMinuteManager();

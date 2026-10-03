/**
 * AchieveHire - Interactive Interview Countdown Timer & Telemetry Engine
 * Provides precision timing, visual circular progress, warning transitions, and telemetry.
 */
class InterviewTimer {
    constructor(options = {}) {
        this.durationSeconds = options.durationSeconds || 1800; // default 30 mins
        this.remainingSeconds = this.durationSeconds;
        this.timerId = null;
        this.isRunning = false;
        this.isPaused = false;
        this.warningThreshold = options.warningThreshold || 300; // 5 min warning
        this.criticalThreshold = options.criticalThreshold || 60; // 1 min critical
        this.callbacks = {
            onTick: options.onTick || null,
            onWarning: options.onWarning || null,
            onCritical: options.onCritical || null,
            onComplete: options.onComplete || null,
            onPause: options.onPause || null,
            onResume: options.onResume || null
        };
        this.timeHistory = [];
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.isPaused = false;
        this.timerId = setInterval(() => this.tick(), 1000);
        this.logEvent('STARTED', this.remainingSeconds);
    }

    pause() {
        if (!this.isRunning || this.isPaused) return;
        this.isPaused = true;
        clearInterval(this.timerId);
        this.timerId = null;
        this.logEvent('PAUSED', this.remainingSeconds);
        if (this.callbacks.onPause) this.callbacks.onPause(this.getMetrics());
    }

    resume() {
        if (!this.isRunning || !this.isPaused) return;
        this.isPaused = false;
        this.timerId = setInterval(() => this.tick(), 1000);
        this.logEvent('RESUMED', this.remainingSeconds);
        if (this.callbacks.onResume) this.callbacks.onResume(this.getMetrics());
    }

    stop() {
        if (this.timerId) {
            clearInterval(this.timerId);
            this.timerId = null;
        }
        this.isRunning = false;
        this.isPaused = false;
        this.logEvent('STOPPED', this.remainingSeconds);
    }

    reset(newDuration = null) {
        this.stop();
        if (newDuration) this.durationSeconds = newDuration;
        this.remainingSeconds = this.durationSeconds;
        this.timeHistory = [];
    }

    tick() {
        if (this.remainingSeconds <= 0) {
            this.stop();
            this.logEvent('COMPLETED', 0);
            if (this.callbacks.onComplete) this.callbacks.onComplete();
            return;
        }

        this.remainingSeconds -= 1;

        if (this.remainingSeconds === this.warningThreshold && this.callbacks.onWarning) {
            this.callbacks.onWarning(this.remainingSeconds);
        }

        if (this.remainingSeconds === this.criticalThreshold && this.callbacks.onCritical) {
            this.callbacks.onCritical(this.remainingSeconds);
        }

        if (this.callbacks.onTick) {
            this.callbacks.onTick(this.getMetrics());
        }
    }

    getFormattedTime() {
        const minutes = Math.floor(this.remainingSeconds / 60);
        const seconds = this.remainingSeconds % 60;
        return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }

    getPercentageElapsed() {
        const elapsed = this.durationSeconds - this.remainingSeconds;
        return Math.min(100, Math.round((elapsed / this.durationSeconds) * 100));
    }

    getMetrics() {
        return {
            remainingSeconds: this.remainingSeconds,
            durationSeconds: this.durationSeconds,
            formatted: this.getFormattedTime(),
            percentage: this.getPercentageElapsed(),
            state: this.getState()
        };
    }

    getState() {
        if (this.remainingSeconds <= 0) return 'completed';
        if (this.remainingSeconds <= this.criticalThreshold) return 'critical';
        if (this.remainingSeconds <= this.warningThreshold) return 'warning';
        return 'normal';
    }

    logEvent(event, secondsRemaining) {
        this.timeHistory.push({
            event,
            timestamp: new Date().toISOString(),
            secondsRemaining,
            elapsed: this.durationSeconds - secondsRemaining
        });
    }

    renderToDOM(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const metrics = this.getMetrics();
        const strokeDasharray = 283; // Circumference of r=45
        const strokeDashoffset = strokeDasharray - (strokeDasharray * metrics.percentage) / 100;

        let strokeColor = '#3B82F6';
        if (metrics.state === 'warning') strokeColor = '#F59E0B';
        if (metrics.state === 'critical') strokeColor = '#EF4444';

        container.innerHTML = `
            <div class="achievehire-timer-card">
                <div class="timer-svg-container">
                    <svg viewBox="0 0 100 100" class="timer-svg">
                        <circle cx="50" cy="50" r="45" class="timer-bg-circle" />
                        <circle cx="50" cy="50" r="45" class="timer-progress-circle"
                            style="stroke-dasharray: ${strokeDasharray}; stroke-dashoffset: ${strokeDashoffset}; stroke: ${strokeColor};" />
                    </svg>
                    <div class="timer-label-box">
                        <span class="timer-time-text">${metrics.formatted}</span>
                        <span class="timer-status-text">${metrics.state.toUpperCase()}</span>
                    </div>
                </div>
            </div>
        `;
    }
}

// Export for module or browser environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { InterviewTimer };
} else {
    window.InterviewTimer = InterviewTimer;
}

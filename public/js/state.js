/**
 * AchieveHire - Persistent Client-Side State Manager
 * Ensures User ID, candidate profile, resumes, and interview scorecards are permanently stored.
 * The system NEVER forgets the user on reload or restart.
 */
class StateManager {
    constructor() {
        this.STORAGE_PREFIX = 'achievehire_';
        this.USER_KEY = this.STORAGE_PREFIX + 'active_user';
        this.USERS_REGISTRY_KEY = this.STORAGE_PREFIX + 'users_registry';
        this.THEME_KEY = this.STORAGE_PREFIX + 'theme';
        this.ACTIVE_SCREEN_KEY = this.STORAGE_PREFIX + 'screen';

        this.currentUser = this.loadUser();
        this.theme = localStorage.getItem(this.THEME_KEY) || 'light';
        this.currentScreen = localStorage.getItem(this.ACTIVE_SCREEN_KEY) || 'landing';
    }

    // ── User ID & Profile Persistence ─────────────────────────────────────────

    loadUser() {
        try {
            const raw = localStorage.getItem(this.USER_KEY);
            return raw ? JSON.parse(raw) : null;
        } catch (e) {
            console.error('[StateManager] Failed to parse active user:', e);
            return null;
        }
    }

    saveUser(userRecord) {
        if (!userRecord || !userRecord.user_id) return;
        this.currentUser = userRecord;
        localStorage.setItem(this.USER_KEY, JSON.stringify(userRecord));

        // Also update registry
        const registry = this.getUsersRegistry();
        registry[userRecord.user_id] = userRecord;
        localStorage.setItem(this.USERS_REGISTRY_KEY, JSON.stringify(registry));
        this.emit('userChanged', userRecord);
    }

    generateUserId(purpose = 'Both') {
        const prefix = purpose === 'Resume Preparation' ? 'RES' : purpose === 'Interview Preparation' ? 'INT' : 'CAND';
        const randomNum = Math.floor(1000 + Math.random() * 9000);
        return `${prefix}${randomNum}`;
    }

    createAccount(name, purpose) {
        const userId = this.generateUserId(purpose);
        const newUser = {
            user_id: userId,
            name: name || 'Candidate',
            purpose: purpose,
            created_at: new Date().toISOString(),
            headline: `Candidate · ${purpose}`,
            email: `${userId.toLowerCase()}@achievehire.ai`,
            location: 'India',
            resumes: [],
            interview_attempts: []
        };
        this.saveUser(newUser);
        return newUser;
    }

    getUsersRegistry() {
        try {
            const raw = localStorage.getItem(this.USERS_REGISTRY_KEY);
            return raw ? JSON.parse(raw) : {};
        } catch (e) {
            return {};
        }
    }

    signOut() {
        localStorage.removeItem(this.USER_KEY);
        this.currentUser = null;
        this.emit('userChanged', null);
    }

    deleteAccount() {
        if (!this.currentUser) return;
        const userId = this.currentUser.user_id;
        const registry = this.getUsersRegistry();
        delete registry[userId];
        localStorage.setItem(this.USERS_REGISTRY_KEY, JSON.stringify(registry));
        this.signOut();
    }

    // ── Resumes Management (Multiple Resumes) ──────────────────────────────────

    saveResume(resumeObj) {
        if (!this.currentUser) return false;
        if (!this.currentUser.resumes) this.currentUser.resumes = [];
        
        const resumeId = resumeObj.id || `RES-${Date.now()}`;
        const newResume = {
            ...resumeObj,
            id: resumeId,
            updated_at: new Date().toISOString()
        };

        const existingIdx = this.currentUser.resumes.findIndex(r => r.id === resumeId);
        if (existingIdx >= 0) {
            this.currentUser.resumes[existingIdx] = newResume;
        } else {
            this.currentUser.resumes.push(newResume);
        }

        this.saveUser(this.currentUser);
        return resumeId;
    }

    getResumes() {
        return (this.currentUser && this.currentUser.resumes) ? this.currentUser.resumes : [];
    }

    // ── Attempt History Management ────────────────────────────────────────────

    saveInterviewAttempt(attemptRecord) {
        if (!this.currentUser) return;
        if (!this.currentUser.interview_attempts) this.currentUser.interview_attempts = [];

        const attemptId = `ATT-${Date.now()}`;
        const attempt = {
            attempt_id: attemptId,
            timestamp: new Date().toISOString(),
            ...attemptRecord
        };

        this.currentUser.interview_attempts.push(attempt);
        this.saveUser(this.currentUser);
        return attempt;
    }

    getAttempts() {
        return (this.currentUser && this.currentUser.interview_attempts) ? this.currentUser.interview_attempts : [];
    }

    // ── Theme & Navigation ───────────────────────────────────────────────────

    setTheme(theme) {
        this.theme = theme;
        localStorage.setItem(this.THEME_KEY, theme);
        document.documentElement.setAttribute('data-theme', theme);
        this.emit('themeChanged', theme);
    }

    toggleTheme() {
        const next = this.theme === 'dark' ? 'light' : 'dark';
        this.setTheme(next);
        return next;
    }

    setScreen(screenId) {
        this.currentScreen = screenId;
        localStorage.setItem(this.ACTIVE_SCREEN_KEY, screenId);
        this.emit('screenChanged', screenId);
    }

    // ── Event Bus ────────────────────────────────────────────────────────────

    emit(event, data) {
        window.dispatchEvent(new CustomEvent(`achievehire:${event}`, { detail: data }));
    }
}

// Global state instance
window.state = new StateManager();

/**
 * AchieveHire - Main Frontend Application Controller
 * Handles view switching, authentication dialogs, strategy advisory, and report generation.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Theme
    const savedTheme = window.state.theme || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeBtn = document.getElementById('theme-toggle-btn');
    if (themeBtn) {
        themeBtn.textContent = savedTheme === 'dark' ? '☀️ Light' : '🌙 Dark';
        themeBtn.addEventListener('click', () => {
            const next = window.state.toggleTheme();
            themeBtn.textContent = next === 'dark' ? '☀️ Light' : '🌙 Dark';
        });
    }

    // 2. Setup Navigation
    setupNavigation();

    // 3. Setup Authentication Modals & Guards
    setupAuth();

    // 4. Update Header User Badge
    updateUserBadge();

    // 5. Setup Last Minute Strategy Advisory Dialog
    setupStrategyAdvisoryDialog();
});

function setupNavigation() {
    document.querySelectorAll('[data-nav]').forEach(el => {
        el.addEventListener('click', (e) => {
            e.preventDefault();
            const targetScreen = el.getAttribute('data-nav');
            navigateTo(targetScreen);
        });
    });
}

function navigateTo(screenId) {
    // Guard check: Resume Guide and Interviews require authenticated User ID
    const protectedScreens = ['view-resume', 'view-specialized', 'view-job', 'view-last-minute'];
    if (protectedScreens.includes(screenId) && !window.state.currentUser) {
        openAuthModal('Please sign in or create an account with a unique User ID to access this feature.');
        return;
    }

    document.querySelectorAll('.ah-view').forEach(view => view.classList.remove('active'));
    const target = document.getElementById(screenId);
    if (target) {
        target.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function updateUserBadge() {
    const badgeContainer = document.getElementById('nav-user-container');
    if (!badgeContainer) return;

    const user = window.state.currentUser;
    if (user) {
        badgeContainer.innerHTML = `
            <div class="ah-user-badge">
                <span>👤</span>
                <span>${user.user_id}</span>
            </div>
            <button class="ah-nav-btn" id="btn-signout" title="Sign Out">Sign Out</button>
        `;
        document.getElementById('btn-signout').addEventListener('click', () => {
            openConfirmModal(
                'Confirm Sign Out',
                'Are you sure you want to sign out? Your unique User ID is saved on this browser and can be re-accessed anytime.',
                () => {
                    window.state.signOut();
                    updateUserBadge();
                    navigateTo('view-landing');
                }
            );
        });
    } else {
        badgeContainer.innerHTML = `
            <button class="ah-nav-btn primary" id="btn-open-signin">Sign In / Register</button>
        `;
        document.getElementById('btn-open-signin').addEventListener('click', () => openAuthModal());
    }
}

function setupAuth() {
    const authModal = document.getElementById('modal-auth');
    const authForm = document.getElementById('form-register');
    const guestBtn = document.getElementById('btn-quick-founder');

    if (authForm) {
        authForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('input-candidate-name').value.trim();
            const purpose = document.getElementById('select-purpose').value;
            const user = window.state.createAccount(name, purpose);
            closeModal('modal-auth');
            updateUserBadge();
            navigateTo('view-landing');
        });
    }

    if (guestBtn) {
        guestBtn.addEventListener('click', () => {
            const founderUser = {
                user_id: 'ACHIEVE_FOUNDER_001',
                name: 'Alankrita Pal',
                purpose: 'Both',
                created_at: new Date().toISOString(),
                headline: 'Platform Founder & Leader · Career Readiness',
                resumes: [],
                interview_attempts: []
            };
            window.state.saveUser(founderUser);
            closeModal('modal-auth');
            updateUserBadge();
            navigateTo('view-landing');
        });
    }
}

function openAuthModal(noticeText = '') {
    const modal = document.getElementById('modal-auth');
    const noticeEl = document.getElementById('auth-notice-text');
    if (noticeEl) noticeEl.textContent = noticeText;
    if (modal) modal.classList.add('open');
}

function openConfirmModal(title, message, onConfirm) {
    const modal = document.getElementById('modal-confirm');
    document.getElementById('modal-confirm-title').textContent = title;
    document.getElementById('modal-confirm-body').textContent = message;

    const confirmBtn = document.getElementById('modal-confirm-btn-yes');
    const newConfirmBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);

    newConfirmBtn.addEventListener('click', () => {
        closeModal('modal-confirm');
        if (onConfirm) onConfirm();
    });

    if (modal) modal.classList.add('open');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('open');
}

function setupStrategyAdvisoryDialog() {
    const modal = document.getElementById('modal-advisory');
    const btnBack = document.getElementById('btn-advisory-back');
    const btnAnyway = document.getElementById('btn-advisory-anyway');

    if (btnBack) {
        btnBack.addEventListener('click', () => {
            closeModal('modal-advisory');
            // Navigate back to stage practice
            const target = btnBack.getAttribute('data-target') || 'view-specialized';
            navigateTo(target);
        });
    }

    if (btnAnyway) {
        btnAnyway.addEventListener('click', () => {
            closeModal('modal-advisory');
            // Directly start last minute prep session
            startLastMinuteLiveSession();
        });
    }
}

function showStrategyAdvisory(modeName, targetScreen) {
    const modal = document.getElementById('modal-advisory');
    const stageLabel = modeName.includes('Specialized') ? '4 levels' : '6 rounds';
    document.getElementById('advisory-question-text').textContent = 
        `Would you like to proceed with Last-Minute Prep before completing the ${stageLabel}?`;
    
    const btnBack = document.getElementById('btn-advisory-back');
    if (btnBack) btnBack.setAttribute('data-target', targetScreen);

    if (modal) modal.classList.add('open');
}

function startLastMinuteLiveSession() {
    navigateTo('view-lm-live');
    const timerDisplay = document.getElementById('lm-timer-digits');
    const qText = document.getElementById('lm-question-text');
    const speakerName = document.getElementById('lm-speaker-name');

    window.lastMinuteManager.startTimer((formattedTime) => {
        if (timerDisplay) timerDisplay.textContent = formattedTime;
    }, () => {
        alert('30-minute rapid session completed! Generating your performance scorecard.');
        const attempt = window.lastMinuteManager.finalizeAttempt();
        renderScorecard(attempt);
    });

    const firstQ = window.lastMinuteManager.getNextQuestion();
    if (qText) qText.textContent = firstQ.questionText;
    if (speakerName) speakerName.textContent = firstQ.speaker.name;

    // Speak first question
    window.speechEngine.speak(firstQ.questionText, window.lastMinuteManager.language);
}

function renderScorecard(reportData) {
    navigateTo('view-report');
    document.getElementById('rep-title').textContent = `${reportData.mode || reportData.type} Performance Report`;
    document.getElementById('rep-score').textContent = `${reportData.overallScore}%`;
    document.getElementById('rep-candidate').textContent = window.state.currentUser ? window.state.currentUser.name : 'Candidate';
    document.getElementById('rep-date').textContent = new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' });
}

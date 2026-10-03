/**
 * AchieveHire - Theme Manager & High-Contrast Mode Controller
 * Handles light/dark theme switching, accessibility contrast, and persistent preferences.
 */
class ThemeManager {
    constructor() {
        this.storageKey = 'achievehire_preferred_theme';
        this.contrastKey = 'achievehire_high_contrast';
        this.currentTheme = localStorage.getItem(this.storageKey) || this.detectSystemPreference();
        this.isHighContrast = localStorage.getItem(this.contrastKey) === 'true';
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.applyContrast(this.isHighContrast);
        this.listenToSystemChanges();
    }

    detectSystemPreference() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    listenToSystemChanges() {
        if (!window.matchMedia) return;
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (!localStorage.getItem(this.storageKey)) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    applyTheme(theme) {
        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(this.storageKey, theme);
        window.dispatchEvent(new CustomEvent('achievehire:themeChanged', { detail: { theme } }));
    }

    toggleTheme() {
        const nextTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(nextTheme);
        return nextTheme;
    }

    applyContrast(enable) {
        this.isHighContrast = enable;
        if (enable) {
            document.documentElement.classList.add('achievehire-high-contrast');
        } else {
            document.documentElement.classList.remove('achievehire-high-contrast');
        }
        localStorage.setItem(this.contrastKey, enable ? 'true' : 'false');
    }

    toggleContrast() {
        this.applyContrast(!this.isHighContrast);
        return this.isHighContrast;
    }
}

// Global initialization
if (typeof window !== 'undefined') {
    window.achieveHireTheme = new ThemeManager();
    document.addEventListener('DOMContentLoaded', () => {
        window.achieveHireTheme.init();
    });
}

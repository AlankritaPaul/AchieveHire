/**
 * AchieveHire - Client-Side Resume ATS Highlighter & Inspector
 * Scans resume text or rendered DOM for ATS keywords, action verbs, and formatting checks.
 */
class ResumeHighlighter {
    constructor(targetElementId) {
        this.targetElement = document.getElementById(targetElementId);
        this.matchedKeywords = new Set();
        this.weakVerbs = ['handled', 'worked on', 'helped', 'assisted', 'responsible for', 'tried'];
        this.impactVerbs = ['architected', 'spearheaded', 'engineered', 'optimized', 'accelerated', 'orchestrated', 'delivered', 'automated'];
    }

    /**
     * Highlights keywords in the target element with custom CSS badges
     * @param {Array<string>} targetKeywords
     */
    highlightKeywords(targetKeywords = []) {
        if (!this.targetElement) return;

        let content = this.targetElement.innerHTML;
        this.matchedKeywords.clear();

        targetKeywords.forEach(kw => {
            const regex = new RegExp(`\\b(${this.escapeRegex(kw)})\\b`, 'gi');
            if (regex.test(content)) {
                this.matchedKeywords.add(kw);
                content = content.replace(regex, `<mark class="ats-matched-keyword" title="ATS Target Keyword: $1">$1</mark>`);
            }
        });

        // Highlight impact verbs in green
        this.impactVerbs.forEach(verb => {
            const regex = new RegExp(`\\b(${this.escapeRegex(verb)})\\b`, 'gi');
            content = content.replace(regex, `<span class="ats-impact-verb" title="Strong Action Verb: $1">$1</span>`);
        });

        // Flag weak verbs in amber
        this.weakVerbs.forEach(verb => {
            const regex = new RegExp(`\\b(${this.escapeRegex(verb)})\\b`, 'gi');
            content = content.replace(regex, `<span class="ats-weak-verb" title="Opportunity for Stronger Action Verb: $1">$1</span>`);
        });

        this.targetElement.innerHTML = content;
    }

    escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    computeAtsScore(expectedKeywords = []) {
        if (!expectedKeywords.length) return 85;
        const matchCount = this.matchedKeywords.size;
        const coverageRatio = matchCount / expectedKeywords.length;
        const baseScore = Math.round(coverageRatio * 70); // 70% based on keywords
        const structureScore = 25; // standard clean structure points
        return Math.min(100, baseScore + structureScore);
    }

    renderSummaryBadge(badgeContainerId, expectedKeywords = []) {
        const badgeContainer = document.getElementById(badgeContainerId);
        if (!badgeContainer) return;

        const score = this.computeAtsScore(expectedKeywords);
        const matchCount = this.matchedKeywords.size;
        const total = expectedKeywords.length;

        let ratingClass = 'ats-rating-high';
        let ratingLabel = 'Excellent Match';
        if (score < 60) {
            ratingClass = 'ats-rating-low';
            ratingLabel = 'Needs Improvement';
        } else if (score < 80) {
            ratingClass = 'ats-rating-med';
            ratingLabel = 'Good Alignment';
        }

        badgeContainer.innerHTML = `
            <div class="ats-summary-card ${ratingClass}">
                <div class="ats-score-badge">
                    <span class="score-number">${score}</span>
                    <span class="score-denominator">/ 100</span>
                </div>
                <div class="ats-score-meta">
                    <div class="ats-rating-title">${ratingLabel}</div>
                    <div class="ats-matches-count">${matchCount} of ${total} Target Role Keywords Matched</div>
                </div>
            </div>
        `;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ResumeHighlighter };
} else {
    window.ResumeHighlighter = ResumeHighlighter;
}

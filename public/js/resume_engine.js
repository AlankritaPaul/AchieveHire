/**
 * AchieveHire - Resume Intelligence & ATS Builder Engine
 * Provides ATS analysis, 6 industry-tailored templates, and multi-resume management.
 */

const RESUME_TEMPLATES = [
    { id: 'classic_executive', name: 'Classic Executive', desc: 'Timeless single-column layout with serif headers, optimized for leadership and senior roles.' },
    { id: 'modern_minimalist', name: 'Modern Minimalist', desc: 'Clean sans-serif design with subtle dividers, high ATS compliance and crisp readability.' },
    { id: 'tech_lead', name: 'Tech Lead / Architect', desc: 'Highlights system architecture, technical stacks, quantitative impact, and patents.' },
    { id: 'compact_technical', name: 'Compact Technical', desc: 'High-density format maximizing content space for extensive projects and core competencies.' },
    { id: 'elegant_academic', name: 'Elegant Academic', desc: 'Scholarly structure emphasizing publications, research, credentials, and honors.' },
    { id: 'creative_professional', name: 'Creative Professional', desc: 'Contemporary dual-tone accent styling with balanced visual hierarchy and ATS safety.' }
];

const STRONG_ACTION_VERBS = [
    'architected', 'spearheaded', 'engineered', 'optimized', 'accelerated', 'orchestrated',
    'delivered', 'automated', 'streamlined', 'pioneered', 'implemented', 'scaled', 'mentored'
];

const WEAK_VERBS = [
    'handled', 'worked on', 'helped', 'assisted', 'responsible for', 'tried', 'participated in', 'did'
];

class ResumeEngine {
    /**
     * Analyzes resume text against ATS rules and returns a structured scorecard.
     */
    analyzeResume(text, targetRole = '') {
        const words = text.toLowerCase().split(/\s+/);
        const totalWords = words.length;

        // 1. Section Completeness Check
        const sections = [
            { name: 'Contact & Personal Details', regex: /(email|phone|linkedin|github|portfolio)/i },
            { name: 'Professional Summary', regex: /(summary|profile|about me|objective)/i },
            { name: 'Work Experience', regex: /(experience|employment|work history|career)/i },
            { name: 'Education', regex: /(education|degree|bachelor|master|university|college)/i },
            { name: 'Skills & Competencies', regex: /(skills|technologies|tools|competencies)/i },
            { name: 'Projects & Implementations', regex: /(projects|portfolio|achievements)/i }
        ];

        let presentSections = 0;
        const sectionBreakdown = sections.map(s => {
            const isPresent = s.regex.test(text);
            if (isPresent) presentSections++;
            return {
                section: s.name,
                status: isPresent ? 'Optimal' : 'Needs Addition',
                score: isPresent ? 100 : 30
            };
        });

        // 2. Action Verb Strength Audit
        let strongCount = 0;
        let weakCount = 0;
        const detectedStrong = [];
        const detectedWeak = [];

        STRONG_ACTION_VERBS.forEach(v => {
            const regex = new RegExp(`\\b${v}\\b`, 'gi');
            const matches = text.match(regex);
            if (matches) {
                strongCount += matches.length;
                detectedStrong.push(v);
            }
        });

        WEAK_VERBS.forEach(v => {
            const regex = new RegExp(`\\b${v}\\b`, 'gi');
            const matches = text.match(regex);
            if (matches) {
                weakCount += matches.length;
                detectedWeak.push(v);
            }
        });

        // 3. Score Calculation
        const sectionScore = (presentSections / sections.length) * 40;
        const verbScore = Math.min(30, strongCount * 5) - Math.min(15, weakCount * 3);
        const lengthScore = totalWords >= 250 && totalWords <= 850 ? 30 : 15;
        const overallScore = Math.max(20, Math.min(98, Math.round(sectionScore + Math.max(5, verbScore) + lengthScore)));

        return {
            overallScore,
            totalWords,
            sectionBreakdown,
            strongVerbs: detectedStrong,
            weakVerbs: detectedWeak,
            recommendations: this.generateRecommendations(presentSections, strongCount, weakCount, totalWords)
        };
    }

    generateRecommendations(presentSections, strongCount, weakCount, totalWords) {
        const recs = [];
        if (presentSections < 6) {
            recs.push('Add missing sections to ensure comprehensive coverage across automated ATS parsers.');
        }
        if (weakCount > 0) {
            recs.push(`Replace weak passive phrases (e.g., "${WEAK_VERBS[0]}") with high-impact action verbs (e.g., "Architected", "Engineered").`);
        }
        if (strongCount < 4) {
            recs.push('Quantify technical accomplishments with measurable percentages and performance metrics.');
        }
        if (totalWords < 250) {
            recs.push('Resume length is too brief. Expand on technical project contributions and system scale.');
        }
        return recs;
    }

    /**
     * Renders a chosen template into responsive HTML
     */
    renderTemplate(templateId, resumeData) {
        const r = resumeData || {};
        const name = r.fullName || 'Candidate Name';
        const title = r.title || 'Software Engineering Professional';
        const email = r.email || 'candidate@achievehire.ai';
        const phone = r.phone || '+91 98765 43210';
        const summary = r.summary || 'Results-driven engineer with deep experience in scalable distributed architecture, API design, and cloud systems.';
        const experience = r.experience || '• Architected resilient microservices handling high traffic throughput.\n• Streamlined continuous integration pipelines, cutting build latency by 45%.';
        const skills = r.skills || 'Python, JavaScript, React, Next.js, FastAPI, PostgreSQL, Docker, AWS';
        const education = r.education || 'Bachelor of Technology in Computer Science (2020 - 2024)';

        return `
            <div class="resume-preview-document ${templateId}">
                <header class="resume-hdr">
                    <h1 class="resume-name">${name}</h1>
                    <div class="resume-title">${title}</div>
                    <div class="resume-contact">${email} &nbsp;·&nbsp; ${phone}</div>
                </header>
                <hr style="margin: 16px 0; border: none; border-top: 1px solid #CBD5E1;" />
                <section class="resume-sec">
                    <h3 class="sec-hdr">Professional Summary</h3>
                    <p>${summary}</p>
                </section>
                <section class="resume-sec">
                    <h3 class="sec-hdr">Core Competencies & Skills</h3>
                    <p>${skills}</p>
                </section>
                <section class="resume-sec">
                    <h3 class="sec-hdr">Professional Experience</h3>
                    <p style="white-space: pre-line;">${experience}</p>
                </section>
                <section class="resume-sec">
                    <h3 class="sec-hdr">Education & Credentials</h3>
                    <p>${education}</p>
                </section>
            </div>
        `;
    }
}

window.resumeEngine = new ResumeEngine();

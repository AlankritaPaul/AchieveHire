/**
 * AchieveHire - Job Related Interview Module
 * 6 Progressive Rounds with Multi-Persona Panel & Stored Resume Integration
 */

const JOB_PANEL_MEMBERS = [
    { id: 'lead', name: 'Arjun Mehta', title: 'Technical Lead & System Architect', avatar: '👨‍💼' },
    { id: 'mgr', name: 'Priya Sharma', title: 'Engineering Manager & Team Lead', avatar: '👩‍💻' },
    { id: 'spec', name: 'Rohan Gupta', title: 'Domain & Core Fundamentals Specialist', avatar: '👨‍🔬' }
];

const JOB_ROUND_DEFINITIONS = [
    { round: 1, name: 'Round 1: Screening & Core Competencies', duration: '20 Min', difficulty: 'Easy' },
    { round: 2, name: 'Round 2: Technical Depth & System Mechanics', duration: '25 Min', difficulty: 'Moderate' },
    { round: 3, name: 'Round 3: Practical Problem-Solving & Architecture', duration: '30 Min', difficulty: 'Moderate' },
    { round: 4, name: 'Round 4: Advanced Scenarios & Production Stress', duration: '35 Min', difficulty: 'Hard' },
    { round: 5, name: 'Round 5: Executive Decision-Making & Trade-Offs', duration: '40 Min', difficulty: 'Hard' },
    { round: 6, name: 'Round 6: Final Leadership & Cultural Alignment', duration: '45 Min', difficulty: 'Final' }
];

class JobRelatedInterviewManager {
    constructor() {
        this.currentRound = 1;
        this.currentQuestionIdx = 0;
        this.jobRole = '';
        this.company = '';
        this.language = 'English';
        this.resumeData = null;
        this.roundAnswers = [];
    }

    startSession(role, company, language, candidateResume) {
        this.jobRole = role || 'Software Engineer';
        this.company = company || 'Technology Company';
        this.language = language || 'English';
        this.resumeData = candidateResume || null;
        this.currentRound = 1;
        this.currentQuestionIdx = 0;
        this.roundAnswers = [];
    }

    getCurrentRoundInfo() {
        return JOB_ROUND_DEFINITIONS[this.currentRound - 1] || JOB_ROUND_DEFINITIONS[0];
    }

    getCurrentSpeaker() {
        // Rotate speakers among the 3 panel members
        return JOB_PANEL_MEMBERS[(this.currentRound - 1) % JOB_PANEL_MEMBERS.length];
    }

    getCurrentQuestion() {
        const speaker = this.getCurrentSpeaker();
        const roundInfo = this.getCurrentRoundInfo();

        let questionText = '';
        if (this.currentRound === 1) {
            questionText = `Welcome to your interview for the ${this.jobRole} position at ${this.company}. Please walk us through your background, core technical strengths, and why you are interested in joining our team.`;
        } else if (this.currentRound === 2) {
            questionText = `Based on your technical experience, describe a complex challenge you encountered in a recent project. How did you diagnose the issue, and what engineering choices did you make?`;
        } else if (this.currentRound === 3) {
            questionText = `At ${this.company}, reliability and scalability are critical. How do you design systems to handle high traffic spikes while ensuring low latency and data consistency?`;
        } else if (this.currentRound === 4) {
            questionText = `Walk me through a scenario where a critical production outage occurred. How did you triage the failure, communicate with stakeholders, and implement long-term preventive measures?`;
        } else if (this.currentRound === 5) {
            questionText = `When faced with tight engineering deadlines versus technical debt, how do you evaluate architectural trade-offs and align your team towards sustainable solutions?`;
        } else {
            questionText = `In this final round, reflect on how your career vision aligns with ${this.company}'s engineering culture. Where do you see yourself contributing the highest strategic impact?`;
        }

        if (this.language === 'Hinglish') {
            if (this.currentRound === 1) {
                questionText = `Welcome to the interview for the ${this.jobRole} position at ${this.company}. Apne background, key projects, aur core strengths ke baare me walk through karein.`;
            }
        }

        return {
            round: this.currentRound,
            roundInfo,
            speaker,
            questionText
        };
    }

    submitAnswer(answerText) {
        const q = this.getCurrentQuestion();
        const score = Math.floor(78 + Math.random() * 18);

        this.roundAnswers.push({
            round: this.currentRound,
            speaker: q.speaker.name,
            question: q.questionText,
            answer: answerText || '(Voice Response Captured)',
            score
        });

        if (this.currentRound < 6) {
            this.currentRound++;
            return { completed: false, nextQuestion: this.getCurrentQuestion() };
        } else {
            return { completed: true, report: this.generateReport() };
        }
    }

    generateReport() {
        const total = this.roundAnswers.reduce((acc, a) => acc + a.score, 0);
        const overallScore = Math.round(total / this.roundAnswers.length);

        return {
            type: 'Job Related Interview',
            jobRole: this.jobRole,
            company: this.company,
            language: this.language,
            date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' }),
            overallScore,
            answers: this.roundAnswers
        };
    }
}

window.jobManager = new JobRelatedInterviewManager();

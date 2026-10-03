"""
AchieveHire — Job Related Context-Driven Interview Engine
Generates and manages dynamic questions, panel interactions, follow-ups,
and professional interviewer reactions based on:
1. Target Job Role (e.g., Software Engineer, Product Manager, Data Scientist)
2. Target Company (e.g., Google, Microsoft, Amazon, Infosys, etc.)
3. Real Candidate Resume Data (Education, Skills, Projects, Work Experience, Achievements)
4. Selected Language (Strictly English, Hindi, Hinglish)
5. Progressive 6-Round Structure:
   - Round 1: Easy, 1 interviewer. Question 1 strictly: 'Please introduce yourself.'
   - Round 2: Moderate, 2 interviewers. Job competencies and workflows.
   - Round 3: Moderate, 2 interviewers. Resume project dissection & follow-ups.
   - Round 4: Hard, 3 interviewers. Scalability, architectural trade-offs, practical reasoning.
   - Round 5: Hard, 3 interviewers. Edge cases, incident management, cross-functional leadership.
   - Round 6: Final, 4 interviewers. Comprehensive panel evaluation + closing 'Do you have any questions for us?'
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from modules.interview.job_related.models import (
    JOB_ROUNDS_CONFIG,
    JobQuestionRecord,
    PanelMember,
)
from modules.interview.job_related.panel_generator import generate_panel_for_round

# Natural interviewer acknowledgements and reactions
REACTIONS_STRONG = {
    "English": [
        "That is a clear explanation. Let's build on that.",
        "Understood. That directly addresses the requirement.",
        "Good reasoning. Let's look at the next dimension.",
        "That covers the core principles well. Let's continue.",
    ],
    "Hindi": [
        "यह एक स्पष्ट और ठोस उत्तर है। चलिए अगले पहलू पर चलते हैं।",
        "समझ गया। आपने मुख्य बिंदु को सही तरीके से समझाया है।",
        "अच्छा दृष्टिकोण है। अब अगले सवाल की ओर बढ़ते हैं।",
    ],
    "Hinglish": [
        "Kaafi clear aur structured answer hai. Let's move to the next question.",
        "Understood. Aapne key aspects ache se cover kiye hain.",
        "Sahi point hai. Ab agla scenario dekhte hain.",
    ],
}

REACTIONS_NEUTRAL = {
    "English": [
        "Alright, let's move to the next question.",
        "Okay. Let's continue.",
        "I see. Let's take the next question.",
        "Noted. Moving forward.",
    ],
    "Hindi": [
        "ठीक है, अगले प्रश्न की ओर बढ़ते हैं।",
        "समझ गया, चलिए आगे चलते हैं।",
        "नोट कर लिया गया है। अगला सवाल देखते हैं।",
    ],
    "Hinglish": [
        "Theek hai, let's move to the next question.",
        "Noted. Agle question par chalte hain.",
        "Okay, let's continue with the interview.",
    ],
}

REACTIONS_DEEPEN = {
    "English": [
        "Okay. Let's go a little deeper.",
        "I see. Can you explain that further?",
        "Please clarify that part in terms of real-world impact.",
        "Let's look at that from a practical perspective.",
    ],
    "Hindi": [
        "ठीक है, इसे थोड़ा और गहराई से समझते हैं।",
        "क्या आप इसे व्यावहारिक उदाहरण के साथ स्पष्ट कर सकते हैं?",
        "इस निर्णय के पीछे आपका मुख्य तर्क क्या था?",
    ],
    "Hinglish": [
        "Okay. Let's go a little deeper into this.",
        "I see. Isko practical perspective se kaise dekhoge?",
        "Thoda aur detail mein explain kijiye please.",
    ],
}

REACTIONS_REDIRECT = {
    "English": [
        "Please try to stay focused on the core question.",
        "Let's keep the focus on the primary technical challenge.",
        "Understood, but make sure your answer directly addresses the specific problem asked.",
    ],
    "Hindi": [
        "कृपया मूल प्रश्न पर केंद्रित रहें।",
        "कोशिश करें कि उत्तर सीधे पूछे गए मुख्य बिंदु पर रहे।",
    ],
    "Hinglish": [
        "Please question ke core point par focus rakhein.",
        "Main problem par dhyan dete hue summarize kijiye.",
    ],
}


def _extract_resume_elements(resume: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts genuine resume components without fabricating missing information."""
    if not isinstance(resume, dict):
        return {"skills": [], "projects": [], "experience": [], "education": []}

    skills_raw = resume.get("skills", "") or resume.get("tech_skills_raw", "")
    if isinstance(skills_raw, str):
        skills = [s.strip() for s in skills_raw.replace("\n", ",").split(",") if s.strip()]
    elif isinstance(skills_raw, list):
        skills = [str(s).strip() for s in skills_raw if str(s).strip()]
    else:
        skills = []

    # Projects
    projects = []
    project_entries = resume.get("project_entries", [])
    if isinstance(project_entries, list):
        for p in project_entries:
            if isinstance(p, dict) and (p.get("title") or p.get("description")):
                projects.append(p.get("title") or p.get("description", "")[:40])
    raw_projects = resume.get("projects", "")
    if isinstance(raw_projects, str) and raw_projects.strip():
        for line in raw_projects.split("\n"):
            line_clean = line.strip(" -*#\t")
            if line_clean and len(line_clean) > 3 and line_clean not in projects:
                projects.append(line_clean[:50])

    # Experience
    experience = []
    exp_entries = resume.get("experience_entries", [])
    if isinstance(exp_entries, list):
        for e in exp_entries:
            if isinstance(e, dict) and (e.get("job_title") or e.get("company")):
                experience.append(f"{e.get('job_title', 'Role')} at {e.get('company', 'Organization')}")
    raw_exp = resume.get("experience", "")
    if isinstance(raw_exp, str) and raw_exp.strip():
        for line in raw_exp.split("\n"):
            line_clean = line.strip(" -*#\t")
            if line_clean and len(line_clean) > 4 and line_clean not in experience:
                experience.append(line_clean[:60])

    # Education
    education = []
    edu_entries = resume.get("education_entries", [])
    if isinstance(edu_entries, list):
        for edu in edu_entries:
            if isinstance(edu, dict) and edu.get("degree"):
                education.append(f"{edu.get('degree')} from {edu.get('institution', 'University')}")
    raw_edu = resume.get("education", "")
    if isinstance(raw_edu, str) and raw_edu.strip():
        for line in raw_edu.split("\n"):
            line_clean = line.strip(" -*#\t")
            if line_clean and len(line_clean) > 4 and line_clean not in education:
                education.append(line_clean[:60])

    return {
        "skills": skills[:8],
        "projects": projects[:5],
        "experience": experience[:4],
        "education": education[:3],
    }


def generate_round_questions(
    job_role: str,
    company: str,
    resume: Dict[str, Any],
    language: str,
    round_num: int,
    prior_performance: Optional[Dict[str, Any]] = None,
) -> Tuple[List[JobQuestionRecord], List[PanelMember]]:
    """
    Constructs contextual questions for the given round matching:
    - Target Job Role & Company
    - Real candidate resume (projects, skills, experience)
    - Strictly follows round difficulty and seniority progression
    - Round 1 Question 1 is strictly 'Please introduce yourself.'
    - Multi-interviewer alternating question distribution
    """
    panel = generate_panel_for_round(job_role, company, round_num)
    res_info = _extract_resume_elements(resume)
    cfg = JOB_ROUNDS_CONFIG.get(round_num, JOB_ROUNDS_CONFIG[1])
    target_count = cfg.get("questions_count", 5)

    clean_role = job_role.strip() if job_role else "Software Engineer"
    clean_company = company.strip() if company else "Technology Solutions"
    lang = language if language in ["English", "Hindi", "Hinglish"] else "English"

    questions: List[JobQuestionRecord] = []
    interviewer_idx = 0

    def _next_interviewer() -> PanelMember:
        nonlocal interviewer_idx
        member = panel[interviewer_idx % len(panel)]
        interviewer_idx += 1
        return member

    # ── Round 1: Strictly starts with "Please introduce yourself." ───────────
    if round_num == 1:
        lead = _next_interviewer()
        intro_q = "Please introduce yourself."
        if lang == "Hindi":
            intro_q = "कृपया अपना संक्षिप्त परिचय दीजिए।"
        elif lang == "Hinglish":
            intro_q = "Please introduce yourself aur apne academic tatha technical background ke baare mein brief bataiye."

        questions.append(
            JobQuestionRecord(
                question_id="r1_q1_intro",
                interviewer_id=lead.id,
                interviewer_name=lead.name,
                interviewer_title=lead.title,
                question_text=intro_q,
                correct_explanation="A structured 90-120 second introduction detailing educational foundation, key technical competencies, notable projects, and motivation for applying to this role at the target company.",
                better_possible_answer="I am a candidate with a strong foundation in " + clean_role + " practices. In my academic and project work, I have focused on building scalable, reliable applications. I have hands-on experience with core technologies and am eager to bring my problem-solving ability to " + clean_company + ".",
            )
        )

        # Question 2: Motivation for the role and company
        m2 = _next_interviewer()
        q2_text = f"What motivated you to apply specifically for the {clean_role} position at {clean_company}?"
        if lang == "Hindi":
            q2_text = f"आपने {clean_company} में {clean_role} पद के लिए विशेष रूप से आवेदन करने का निर्णय क्यों लिया?"
        elif lang == "Hinglish":
            q2_text = f"Aapko {clean_company} mein {clean_role} position ke liye apply karne ki main motivation kya thi?"

        questions.append(
            JobQuestionRecord(
                question_id="r1_q2_motivation",
                interviewer_id=m2.id,
                interviewer_name=m2.name,
                interviewer_title=m2.title,
                question_text=q2_text,
                correct_explanation="Demonstrates genuine alignment with the company's domain, technology stack, mission, and long-term career readiness.",
                better_possible_answer=f"I have closely followed {clean_company}'s engineering excellence and product scale. The {clean_role} position aligns directly with my technical capabilities and long-term passion for solving high-impact domain challenges.",
            )
        )

        # Question 3: Core foundational skill or education
        m3 = _next_interviewer()
        highlight_skill = res_info["skills"][0] if res_info["skills"] else "core programming"
        q3_text = f"Looking at the requirements for a {clean_role}, how do you evaluate your proficiency with {highlight_skill} in practical implementations?"
        if lang == "Hindi":
            q3_text = f"एक {clean_role} की आवश्यकताओं को देखते हुए, आप व्यावहारिक परियोजनाओं में {highlight_skill} में अपनी दक्षता का मूल्यांकन कैसे करते हैं?"
        elif lang == "Hinglish":
            q3_text = f"{clean_role} role ke requirements ke hisaab se, {highlight_skill} mein aapki practical implementation capability kaisi rahi hai?"

        questions.append(
            JobQuestionRecord(
                question_id="r1_q3_core_skill",
                interviewer_id=m3.id,
                interviewer_name=m3.name,
                interviewer_title=m3.title,
                question_text=q3_text,
                correct_explanation="Demonstrates conceptual clarity, honest self-assessment, and hands-on familiarity with foundational skills.",
                better_possible_answer=f"I have applied {highlight_skill} extensively in project environments, focusing on writing maintainable, clean code, handling edge cases, and following structured development workflows.",
            )
        )

        # Question 4: Resume Project or Academic Initiative
        m4 = _next_interviewer()
        proj_name = res_info["projects"][0] if res_info["projects"] else "your primary technical project"
        q4_text = f"Could you walk me through {proj_name}? What was your specific individual contribution?"
        if lang == "Hindi":
            q4_text = f"क्या आप मुझे {proj_name} के बारे में बता सकते हैं? इस परियोजना में आपका व्यक्तिगत योगदान क्या था?"
        elif lang == "Hinglish":
            q4_text = f"Aap mujhe {proj_name} ke baare mein samjha sakte hain? Isme aapka individual contribution exact kya tha?"

        questions.append(
            JobQuestionRecord(
                question_id="r1_q4_project_contrib",
                interviewer_id=m4.id,
                interviewer_name=m4.name,
                interviewer_title=m4.title,
                question_text=q4_text,
                correct_explanation="Separates individual technical contribution from general team activity; details architectural choices and results.",
                better_possible_answer=f"In {proj_name}, my individual focus was on module architecture, data pipeline integration, and rigorous testing, ensuring the application met its functional goals efficiently.",
            )
        )

        # Question 5: Handling learning curve or challenges
        m5 = _next_interviewer()
        q5_text = f"As an early {clean_role}, when you encounter an unfamiliar technical problem or bug, what is your step-by-step troubleshooting methodology?"
        if lang == "Hindi":
            q5_text = f"जब आप किसी नई तकनीकी समस्या या अनसुलझे बग का सामना करते हैं, तो आपकी चरण-दर-चरण समस्या निवारण पद्धति क्या होती है?"
        elif lang == "Hinglish":
            q5_text = f"Jab aap kisi complex ya unfamiliar bug ka samna karte hain, toh aapka step-by-step troubleshooting approach kya rehta hai?"

        questions.append(
            JobQuestionRecord(
                question_id="r1_q5_troubleshooting",
                interviewer_id=m5.id,
                interviewer_name=m5.name,
                interviewer_title=m5.title,
                question_text=q5_text,
                correct_explanation="Demonstrates systematic problem decomposition: log analysis, isolating reproduction steps, consulting official documentation, and validating fixes.",
                better_possible_answer="First, I isolate the issue by creating a minimal reproducible test case and examining system logs. Next, I formulate hypotheses, test them systematically, verify with official documentation, and write regression tests to ensure stability.",
            )
        )

    # ── Round 2: Moderate — Competencies & Workflows (2 Interviewers) ────────
    elif round_num == 2:
        lead = _next_interviewer()
        peer = _next_interviewer()

        questions = [
            JobQuestionRecord(
                question_id="r2_q1_role_workflow",
                interviewer_id=lead.id,
                interviewer_name=lead.name,
                interviewer_title=lead.title,
                question_text=(
                    f"In day-to-day operations as a {clean_role} at {clean_company}, how do you ensure the code and designs you produce maintain production quality?"
                    if lang == "English"
                    else (
                        f"{clean_company} में {clean_role} के रूप में दैनिक कार्यों में, आप यह कैसे सुनिश्चित करते हैं कि आपके द्वारा लिखा गया कोड उत्पादन गुणवत्ता के मानकों को पूरा करता है?"
                        if lang == "Hindi"
                        else f"{clean_company} mein {clean_role} ke daily workflow mein, aap production quality aur reliable standards kaise maintain karenge?"
                    )
                ),
                correct_explanation="Focuses on code reviews, automated unit/integration testing, adherence to style guidelines, and CI/CD validation.",
                better_possible_answer="I follow test-driven development principles where practical, conduct rigorous peer reviews, maintain automated linting and unit test coverage, and design code to be modular and well-documented.",
            ),
            JobQuestionRecord(
                question_id="r2_q2_technical_depth",
                interviewer_id=peer.id,
                interviewer_name=peer.name,
                interviewer_title=peer.title,
                question_text=(
                    f"When designing an asynchronous process or data workflow in a {clean_role} environment, how do you handle idempotency and state consistency?"
                    if lang == "English"
                    else (
                        f"एक {clean_role} परिवेश में एसिंक्रोनस प्रक्रिया या डेटा वर्कफ़्लो को डिज़ाइन करते समय, आप स्टेट कंसिस्टेंसी और त्रुटि हैंडलिंग का प्रबंधन कैसे करते हैं?"
                        if lang == "Hindi"
                        else f"Ek {clean_role} environment mein asynchronous workflow design karte time, aap data consistency aur error handling kaise ensure karte hain?"
                    )
                ),
                correct_explanation="Explains transactional boundaries, unique correlation IDs, deduplication tables, and exponential backoff retry policies.",
                better_possible_answer="I assign unique idempotent transaction keys to every incoming event, store message states in an atomic store, and implement dead-letter queues with exponential backoff retries to guarantee at-least-once delivery without side effects.",
            ),
            JobQuestionRecord(
                question_id="r2_q3_resume_skills",
                interviewer_id=lead.id,
                interviewer_name=lead.name,
                interviewer_title=lead.title,
                question_text=(
                    f"Your resume mentions experience with {res_info['skills'][0] if res_info['skills'] else 'core architectures'}. What is a significant performance bottleneck you faced with it, and how did you resolve it?"
                    if lang == "English"
                    else (
                        f"आपके रेज़्युमे में {res_info['skills'][0] if res_info['skills'] else 'मुख्य आर्किटेक्चर'} का उल्लेख है। आपने इसके साथ किस प्रकार की परफॉर्मेंस समस्या का सामना किया और इसे कैसे हल किया?"
                        if lang == "Hindi"
                        else f"Aapke resume mein {res_info['skills'][0] if res_info['skills'] else 'technical skills'} mentioned hai. Usme aapne koi real performance issue ya bottleneck kaise identify aur resolve kiya?"
                    )
                ),
                correct_explanation="Demonstrates profiling methodology, identifying CPU/memory or I/O constraints, and quantifying the performance gain.",
                better_possible_answer="Using profiling and query latency metrics, I pinpointed redundant DB calls and memory leaks. By introducing indexing, caching frequently queried states, and restructuring loops, latency decreased by over 40%.",
            ),
            JobQuestionRecord(
                question_id="r2_q4_testing_rigor",
                interviewer_id=peer.id,
                interviewer_name=peer.name,
                interviewer_title=peer.title,
                question_text=(
                    f"How do you distinguish between unit testing, integration testing, and contract testing when deploying services at {clean_company} scale?"
                    if lang == "English"
                    else (
                        f"{clean_company} के स्तर पर सेवाओं को तैनात करते समय आप यूनिट परीक्षण, एकीकरण परीक्षण और अनुबंध परीक्षण में क्या अंतर करते हैं?"
                        if lang == "Hindi"
                        else f"{clean_company} scale par services deploy karte waqt unit testing, integration testing aur end-to-end testing mein aap kya boundary rakhte hain?"
                    )
                ),
                correct_explanation="Clear demarcation of testing pyramid: unit tests for isolated business logic, integration tests for DB/cache boundaries, contract tests for microservice API schemas.",
                better_possible_answer="Unit tests validate isolated logic with mocks. Integration tests verify real interactions with dependencies like databases. Contract tests guarantee API schemas remain backward compatible across microservices.",
            ),
            JobQuestionRecord(
                question_id="r2_q5_collaboration",
                interviewer_id=lead.id,
                interviewer_name=lead.name,
                interviewer_title=lead.title,
                question_text=(
                    f"Suppose a team member submits a pull request that solves the issue but violates architectural conventions at {clean_company}. How do you provide feedback?"
                    if lang == "English"
                    else (
                        f"मान लीजिए कि कोई सहकर्मी ऐसा समाधान प्रस्तुत करता है जो समस्या को हल तो करता है लेकिन टीम के आर्किटेक्चर नियमों का उल्लंघन करता है। आप इस पर कैसे प्रतिक्रिया देंगे?"
                        if lang == "Hindi"
                        else f"Agar team member ka PR kaam toh karta hai but architecture guidelines violate karta hai, toh aap constructive feedback kaise denge?"
                    )
                ),
                correct_explanation="Demonstrates constructive, respectful peer reviews, referencing standards objectively, explaining the rationale, and offering collaborative pairing.",
                better_possible_answer="I frame feedback objectively around long-term maintainability and system boundaries. I highlight the positive aspects of the solution first, explain the architectural risk with concrete examples, and offer a short pairing session to refactor it together.",
            ),
            JobQuestionRecord(
                question_id="r2_q6_agile_delivery",
                interviewer_id=peer.id,
                interviewer_name=peer.name,
                interviewer_title=peer.title,
                question_text=(
                    f"When requirements shift mid-sprint, how do you manage technical debt versus speed of feature delivery?"
                    if lang == "English"
                    else (
                        f"जब स्प्रिंट के बीच में आवश्यकताएं बदल जाती हैं, तो आप तकनीकी ऋण (Technical Debt) और डिलीवरी की गति के बीच संतुलन कैसे बनाते हैं?"
                        if lang == "Hindi"
                        else f"Jab requirements achanak badal jati hain, toh technical debt aur feature delivery speed ke beech balance kaise banate hain?"
                    )
                ),
                correct_explanation="Balancing pragmatic trade-offs with explicit documentation of tech debt in backlog tickets, ensuring debt is scheduled for resolution.",
                better_possible_answer="I assess the cost of delay versus the cost of rework. If rapid deployment is critical, I isolate shortcuts into clearly abstracted interfaces, log tech debt tickets in Jira with estimated resolution costs, and schedule refactoring in the following sprint.",
            ),
        ]

    # ── Round 3: Moderate — Project Dissection & Resume Deep Dive (2 Interviewers)
    elif round_num == 3:
        specialist1 = _next_interviewer()
        specialist2 = _next_interviewer()
        primary_proj = res_info["projects"][0] if res_info["projects"] else "your primary system project"
        second_proj = res_info["projects"][1] if len(res_info["projects"]) > 1 else "another technical implementation"

        questions = [
            JobQuestionRecord(
                question_id="r3_q1_architecture_choice",
                interviewer_id=specialist1.id,
                interviewer_name=specialist1.name,
                interviewer_title=specialist1.title,
                question_text=(
                    f"Let's dissect {primary_proj}. Walk us through the high-level architecture. Why did you choose that specific design over alternative patterns?"
                    if lang == "English"
                    else (
                        f"चलिए {primary_proj} पर विस्तार से चर्चा करते हैं। इसका उच्च-स्तरीय आर्किटेक्चर क्या था और आपने वैकल्पिक डिज़ाइनों के बजाय इसे क्यों चुना?"
                        if lang == "Hindi"
                        else f"{primary_proj} ka architectural layout detail mein bataiye. Dusre alternative patterns ki jagah aapne yahi approach kyun choose kiya?"
                    )
                ),
                correct_explanation="Demonstrates trade-off evaluation: latency, throughput, complexity, operational overhead, and developer velocity.",
                better_possible_answer=f"For {primary_proj}, we evaluated both monolithic modularity and microservices. Given our throughput requirements and team size, a decoupled service layer with event queues gave us the ideal balance between low latency and ease of deployment without unnecessary distributed overhead.",
            ),
            JobQuestionRecord(
                question_id="r3_q2_failure_scenario",
                interviewer_id=specialist2.id,
                interviewer_name=specialist2.name,
                interviewer_title=specialist2.title,
                question_text=(
                    f"In {primary_proj}, what was the single most dangerous failure mode? If that component had crashed during peak traffic, how would the system behave?"
                    if lang == "English"
                    else (
                        f"{primary_proj} में सबसे गंभीर विफलता बिंदु क्या था? यदि पीक ट्रैफ़िक के दौरान वह घटक क्रैश हो जाता, तो सिस्टम कैसे प्रतिक्रिया देता?"
                        if lang == "Hindi"
                        else f"{primary_proj} mein sabse critical single point of failure kya tha? Peak traffic par crash hone par system graceful degradation kaise karta?"
                    )
                ),
                correct_explanation="Identifies single points of failure, circuit breaker patterns, graceful degradation, and data recovery strategy.",
                better_possible_answer="The critical failure point was our primary caching cluster. To mitigate catastrophic DB degradation, we implemented circuit breakers with fallback read replicas and cached stale responses while alerting on-call engineers.",
            ),
            JobQuestionRecord(
                question_id="r3_q3_tradeoffs",
                interviewer_id=specialist1.id,
                interviewer_name=specialist1.name,
                interviewer_title=specialist1.title,
                question_text=(
                    f"Reflecting on {second_proj}, what technical decision did you make that you would implement differently today with your current experience?"
                    if lang == "English"
                    else (
                        f"{second_proj} पर विचार करते हुए, ऐसा कौन सा तकनीकी निर्णय था जिसे आप आज अपने वर्तमान अनुभव के आधार पर अलग तरीके से करेंगे?"
                        if lang == "Hindi"
                        else f"{second_proj} ke dauran aisa kaunsa technical decision tha jisko aaj aap different approach se execute karenge?"
                    )
                ),
                correct_explanation="Demonstrates continuous learning, maturity, ownership, and willingness to critically critique one's own engineering output.",
                better_possible_answer="Initially, I coupled business logic too tightly with our ORM layer. In hindsight, implementing a strict repository pattern with dependency inversion would have made testing significantly simpler and reduced schema migration complexity.",
            ),
            JobQuestionRecord(
                question_id="r3_q4_metrics_monitoring",
                interviewer_id=specialist2.id,
                interviewer_name=specialist2.name,
                interviewer_title=specialist2.title,
                question_text=(
                    f"How did you monitor system health and detect anomalies in your projects? Which specific telemetry metrics did you track?"
                    if lang == "English"
                    else (
                        f"आप अपने प्रोजेक्ट्स में सिस्टम स्वास्थ्य और असामान्यताओं की निगरानी कैसे करते थे? आपने किन विशिष्ट मेट्रिक्स को ट्रैक किया?"
                        if lang == "Hindi"
                        else f"Aap apne projects mein telemetry aur error monitoring kaise karte the? Kaunse metrics sabse critical the?"
                    )
                ),
                correct_explanation="The 4 Golden Signals: Latency, Traffic, Errors, and Saturation. Use of distributed tracing and structured logs.",
                better_possible_answer="We monitored the four golden signals: p95 and p99 latency, request throughput, 5xx error percentages, and resource saturation using structured JSON logging and distributed correlation IDs.",
            ),
            JobQuestionRecord(
                question_id="r3_q5_security_practices",
                interviewer_id=specialist1.id,
                interviewer_name=specialist1.name,
                interviewer_title=specialist1.title,
                question_text=(
                    f"What specific security and access-control measures did you integrate into your applications to safeguard user credentials and data?"
                    if lang == "English"
                    else (
                        f"उपयोगकर्ता डेटा और क्रेडेंशियल्स की सुरक्षा के लिए आपने अपने अनुप्रयोगों में कौन से सुरक्षा और एक्सेस-कंट्रोल उपाय लागू किए?"
                        if lang == "Hindi"
                        else f"User data aur security protection ke liye aapne apne application mein kaunse measures aur auth practices implement kiye the?"
                    )
                ),
                correct_explanation="Principle of least privilege, salted hashing (bcrypt/argon2), JWT validation with expiry, rate limiting, and parameterized SQL queries.",
                better_possible_answer="I enforced parameterized queries to prevent SQL injections, used Argon2 for password hashing, implemented short-lived signed JWTs with refresh token rotation, and applied rate limiting at the reverse proxy layer.",
            ),
            JobQuestionRecord(
                question_id="r3_q6_scalability_transition",
                interviewer_id=specialist2.id,
                interviewer_name=specialist2.name,
                interviewer_title=specialist2.title,
                question_text=(
                    f"If the data volume of your implementation increased by a factor of 100 tomorrow at {clean_company}, what would break first?"
                    if lang == "English"
                    else (
                        f"यदि {clean_company} में कल आपके अनुप्रयोग का डेटा वॉल्यूम 100 गुना बढ़ जाए, तो सबसे पहले क्या विफल होगा और आप इसे कैसे संभालेंगे?"
                        if lang == "Hindi"
                        else f"Agar kal {clean_company} scale par data volume 100x increase ho jaye, toh sabse pehle kaunsa component break hoga aur aap kaise scale karenge?"
                    )
                ),
                correct_explanation="Identifies database write limits, memory cache saturation, indexing bottlenecks, and outlines horizontal partitioning / read-write replicas.",
                better_possible_answer="Our relational database write throughput would saturate first due to disk I/O and locking. To scale 100x, I would introduce sharding by tenant ID, route read queries to multi-region replicas, and buffer writes via a distributed message queue like Kafka.",
            ),
        ]

    # ── Round 4: Hard — High-Stakes Architecture & Trade-offs (3 Interviewers)
    elif round_num == 4:
        p1 = _next_interviewer()
        p2 = _next_interviewer()
        p3 = _next_interviewer()

        questions = [
            JobQuestionRecord(
                question_id="r4_q1_cap_theorem",
                interviewer_id=p1.id,
                interviewer_name=p1.name,
                interviewer_title=p1.title,
                question_text=(
                    f"Design a distributed session management service for {clean_company} that serves 20 million daily active users across three geographic regions. Do you prioritize consistency or availability during a network partition?"
                    if lang == "English"
                    else (
                        f"{clean_company} के लिए तीन भौगोलिक क्षेत्रों में 20 मिलियन दैनिक सक्रिय उपयोगकर्ताओं के लिए एक वितरित सत्र प्रबंधन सेवा डिज़ाइन करें। क्या आप नेटवर्क विभाजन के दौरान कंसिस्टेंसी या उपलब्धता को प्राथमिकता देंगे?"
                        if lang == "Hindi"
                        else f"{clean_company} ke liye multi-region distributed session service design kijiye. Network partition ke waqt aap Consistency aur Availability mein se kisko prioritize karenge aur kyun?"
                    )
                ),
                correct_explanation="Evaluates CAP theorem trade-offs: Session validation generally prioritizes availability and low latency with eventual consistency, backed by regional token verification with revocation blacklists.",
                better_possible_answer="I would prioritize High Availability (AP) with stateless cryptographically signed JWTs verified locally by region proxies. For active revocations (e.g., password changes), I would maintain a distributed Redis cluster using replication with low TTLs to minimize network partition impacts.",
            ),
            JobQuestionRecord(
                question_id="r4_q2_database_sharding",
                interviewer_id=p2.id,
                interviewer_name=p2.name,
                interviewer_title=p2.title,
                question_text=(
                    f"How do you select a database partition / shard key for {clean_company}'s transactional workloads? What strategies mitigate hotspotting on celebrity or mega-enterprise accounts?"
                    if lang == "English"
                    else (
                        f"{clean_company} के लेन-देन वर्कलोड के लिए आप डेटाबेस पार्टीशन कुंजी कैसे चुनते हैं? बड़े खातों के हॉटस्पॉट से बचने के लिए आपकी क्या रणनीति होगी?"
                        if lang == "Hindi"
                        else f"Database sharding key choose karte waqt hotspotting avoid karne ke liye aapka kya approach hota hai, especially large tenant accounts ke liye?"
                    )
                ),
                correct_explanation="Evaluates cardinality, compound shard keys, salted hashing, and isolating mega-tenants into dedicated shards.",
                better_possible_answer="A good shard key needs high cardinality and uniform query access patterns. For mega-accounts, I use salt hashing (appending a pseudo-random suffix) to distribute writes across shards, or allocate dedicated isolation shards for top-tier enterprise tenants.",
            ),
            JobQuestionRecord(
                question_id="r4_q3_resilience_engineering",
                interviewer_id=p3.id,
                interviewer_name=p3.name,
                interviewer_title=p3.title,
                question_text=(
                    f"When upstream microservices start timing out under cascading failures, how do you prevent thundering herds and complete platform outages at {clean_company}?"
                    if lang == "English"
                    else (
                        f"जब अपस्ट्रीम माइक्रो-सर्विसेज कैस्केडिंग विफलताओं के कारण समय समाप्त होने लगती हैं, तो आप थंडरिंग हर्ड और पूर्ण सिस्टम आउटेज को कैसे रोकते हैं?"
                        if lang == "Hindi"
                        else f"Upstream service cascading failure ke dauran cascading timeouts aur thundering herd problem ko prevent karne ke liye aap kya design implement karenge?"
                    )
                ),
                correct_explanation="Circuit breakers (open/half-open states), client-side exponential backoff with jitter, request shedding, and bulkhead isolation.",
                better_possible_answer="I implement circuit breakers (Hystrix/Resilience4j style) to fail fast, client-side retries with exponential backoff and randomized jitter to distribute retries, and rate-limiting bulkheads that shed non-essential traffic while protecting core services.",
            ),
            JobQuestionRecord(
                question_id="r4_q4_concurrency_control",
                interviewer_id=p1.id,
                interviewer_name=p1.name,
                interviewer_title=p1.title,
                question_text=(
                    f"Compare optimistic concurrency control with pessimistic locking in high-throughput financial transactions at {clean_company}. When would you choose one over the other?"
                    if lang == "English"
                    else (
                        f"{clean_company} में उच्च-थ्रूपुट वित्तीय लेनदेन में ऑप्टिमिस्टिक और पेसिमिस्टिक लॉकिंग की तुलना करें। आप कब किसे चुनेंगे?"
                        if lang == "Hindi"
                        else f"High-throughput transactions ke liye Optimistic Locking aur Pessimistic Locking mein kya trade-off hota hai? Kis scenario mein kaunsa select karenge?"
                    )
                ),
                correct_explanation="Optimistic locking (version numbers) suits read-heavy low-contention systems; pessimistic locking (SELECT FOR UPDATE) prevents race conditions in high-contention inventory/financial ledgers.",
                better_possible_answer="Optimistic locking using version fields is ideal when contention is low, minimizing database lock overhead. For high-contention financial transfers where race conditions cannot be tolerated, I use pessimistic locking or serialized queue processing with distributed locks like Redlock.",
            ),
            JobQuestionRecord(
                question_id="r4_q5_caching_invalidation",
                interviewer_id=p2.id,
                interviewer_name=p2.name,
                interviewer_title=p2.title,
                question_text=(
                    f"Phil Karlton famously said cache invalidation is one of the hardest problems in Computer Science. How do you design cache-aside versus write-through caching, and how do you prevent stale cache reads?"
                    if lang == "English"
                    else (
                        f"कैश अमान्यकरण (Cache Invalidation) कंप्यूटर विज्ञान की सबसे कठिन समस्याओं में से एक है। आप कैश-असाइड बनाम राइट-थ्रू को कैसे डिज़ाइन करते हैं?"
                        if lang == "Hindi"
                        else f"Cache Invalidation problem ko tackle karne ke liye Cache-Aside aur Write-Through mein se kaunsa design kab use karte hain aur cache stampede kaise prevent karte hain?"
                    )
                ),
                correct_explanation="Cache-aside for read-heavy variable data, write-through for strong consistency. Mitigating cache stampede using probabilistic early expiration or mutex locks.",
                better_possible_answer="In Cache-Aside, the application queries the cache first, loads from DB on miss, and writes to cache. In Write-Through, writes update cache and DB simultaneously. To prevent stampedes, I use distributed mutex locks on cache misses or XFetch probabilistic early recomputation.",
            ),
            JobQuestionRecord(
                question_id="r4_q6_technical_conflict",
                interviewer_id=p3.id,
                interviewer_name=p3.name,
                interviewer_title=p3.title,
                question_text=(
                    f"Tell me about a situation where you had a strong technical disagreement with another senior engineer on an architectural design. How did you resolve it?"
                    if lang == "English"
                    else (
                        f"किसी ऐसी स्थिति का वर्णन करें जहाँ आपका किसी अन्य वरिष्ठ इंजीनियर के साथ आर्किटेक्चर डिज़ाइन पर गहरा तकनीकी मतभेद था। आपने इसे कैसे सुलझाया?"
                        if lang == "Hindi"
                        else f"Jab aapka kisi senior engineer ke saath architecture design par disagreement hua ho, toh aapne technical consensus kaise build kiya?"
                    )
                ),
                correct_explanation="Demonstrates intellectual humility, data-driven benchmarking (POCs), focusing on business goals, and 'disagree and commit' maturity.",
                better_possible_answer="Instead of engaging in subjective debates, I proposed building dual rapid Proof-of-Concepts measuring throughput, complexity, and operational cost against our specific SLA requirements. The empirical benchmarks clarified the winning design, and the entire team committed wholeheartedly.",
            ),
            JobQuestionRecord(
                question_id="r4_q7_zero_downtime",
                interviewer_id=p1.id,
                interviewer_name=p1.name,
                interviewer_title=p1.title,
                question_text=(
                    f"How do you execute zero-downtime database schema migrations on a table containing 500 million rows under active writes at {clean_company}?"
                    if lang == "English"
                    else (
                        f"{clean_company} में सक्रिय राइट्स के दौरान 500 मिलियन पंक्तियों वाली तालिका पर बिना किसी डाउनटाइम के स्कीमा माइग्रेशन कैसे करते हैं?"
                        if lang == "Hindi"
                        else f"Active high-write traffic table (500M+ rows) par zero-downtime schema migration kaise execute kiya jata hai?"
                    )
                ),
                correct_explanation="Expand and contract pattern: 1) Add nullable column, 2) Dual-write in code, 3) Backfill historical rows in batches, 4) Switch reads to new column, 5) Contract/remove old column.",
                better_possible_answer="I follow the Expand and Contract pattern: Add the new column as nullable, deploy code that writes to both old and new columns, run an asynchronous throttled backfill batch script for historical data, flip reads to the new column, and finally drop the old column once verified.",
            ),
        ]

    # ── Round 5: Hard — Edge Cases, Incident Leadership & Operations (3 Interviewers)
    elif round_num == 5:
        dir1 = _next_interviewer()
        dir2 = _next_interviewer()
        dir3 = _next_interviewer()

        questions = [
            JobQuestionRecord(
                question_id="r5_q1_p0_incident",
                interviewer_id=dir1.id,
                interviewer_name=dir1.name,
                interviewer_title=dir1.title,
                question_text=(
                    f"It is 2:00 AM on a major shopping holiday. {clean_company}'s checkout latency has spiked by 600%, and errors are at 18%. You are the Incident Commander. Walk me through your first 15 minutes."
                    if lang == "English"
                    else (
                        f"त्यौहार के पीक समय में रात 2:00 बजे {clean_company} की चेकआउट लेटेंसी 600% बढ़ जाती है और एरर 18% हैं। आप इंसीडेंट कमांडर हैं। अपने पहले 15 मिनट बताएं।"
                        if lang == "Hindi"
                        else f"Peak festive sale ke time raat ke 2 baje {clean_company} par massive error spike hota hai. As Incident Commander, aapke first 15 minutes ka incident management plan kya hoga?"
                    )
                ),
                correct_explanation="Clear incident management: Assemble bridge, declare roles, isolate blast radius, initiate rollback or degrade gracefully (shed non-critical traffic), establish internal/external comms cadence, and preserve logs for post-mortem.",
                better_possible_answer="Minute 1-5: Open the war room, assign roles (Operations, Communications, Investigation), and silence notification noise. Minute 5-10: Check recent deployments and feature flags, initiating immediate rollback if correlated. Minute 10-15: If infrastructure saturation, engage load-shedding and rate-limiting on non-critical endpoints while communicating status updates every 15 minutes.",
            ),
            JobQuestionRecord(
                question_id="r5_q2_post_mortem",
                interviewer_id=dir2.id,
                interviewer_name=dir2.name,
                interviewer_title=dir2.title,
                question_text=(
                    f"How do you conduct a blameless post-mortem at {clean_company} after a severe customer-facing outage? What distinguishes an actionable preventative measure from a superficial fix?"
                    if lang == "English"
                    else (
                        f"गंभीर ग्राहक आउटेज के बाद आप एक दोषरहित पोस्टमॉर्टम (Blameless Post-Mortem) कैसे संचालित करते हैं? सतही समाधान और वास्तविक सुधारात्मक कार्रवाई में क्या अंतर है?"
                        if lang == "Hindi"
                        else f"Major outage ke baad Blameless Post-Mortem conduct karne ka structured process kya hota hai aur root cause analysis kaise ensure karte hain?"
                    )
                ),
                correct_explanation="Focus on systemic failure rather than human blame (5 Whys), automated guards instead of 'be more careful', and creating prioritized engineering tickets with executive accountability.",
                better_possible_answer="A blameless post-mortem focuses on systemic vulnerabilities rather than operator error using the 5-Whys methodology. An actionable measure introduces automated invariant checks, canary deployments, or architectural circuit breakers, rather than vague human process warnings.",
            ),
            JobQuestionRecord(
                question_id="r5_q3_cross_functional_alignment",
                interviewer_id=dir3.id,
                interviewer_name=dir3.name,
                interviewer_title=dir3.title,
                question_text=(
                    f"The Product team at {clean_company} wants to launch a high-revenue feature in two weeks, but you know the backend needs another month of architectural hardening to be stable. How do you negotiate this?"
                    if lang == "English"
                    else (
                        f"प्रोडक्ट टीम दो सप्ताह में एक महत्वपूर्ण फीचर लॉन्च करना चाहती है, लेकिन बैकएंड को स्थिर होने के लिए एक और महीने की आवश्यकता है। आप इस स्थिति में कैसे बातचीत करेंगे?"
                        if lang == "Hindi"
                        else f"Product team 2 weeks mein high-priority feature chahti hai lekin engineering ko 1 month stability work chahiye. Business aur tech ke beech trade-off kaise negotiate karenge?"
                    )
                ),
                correct_explanation="Quantifying risk in business metrics (cost of downtime vs. revenue delay), proposing phased rollouts (canary/beta to small cohort), and mutual trade-off alignment.",
                better_possible_answer="I frame the discussion in terms of business impact: a catastrophic launch outage during launch week destroys customer trust and revenue. I propose a phased canary release to a 2% trusted beta group to validate market demand while our engineering team hardens the platform for general availability.",
            ),
            JobQuestionRecord(
                question_id="r5_q4_observability_slo",
                interviewer_id=dir1.id,
                interviewer_name=dir1.name,
                interviewer_title=dir1.title,
                question_text=(
                    f"Define SLA, SLO, and SLI for a mission-critical service at {clean_company}. How do you use Error Budgets to determine whether a team can deploy new features or must focus on reliability?"
                    if lang == "English"
                    else (
                        f"{clean_company} की सेवा के लिए SLA, SLO, और SLI को परिभाषित करें। आप नए फीचर्स को तैनात करने बनाम विश्वसनीयता पर काम करने के लिए एरर बजट का उपयोग कैसे करते हैं?"
                        if lang == "Hindi"
                        else f"SLA, SLO aur SLI mein kya difference hota hai aur Google SRE Error Budget philosophy ko team feature velocity decide karne ke liye kaise use kiya jata hai?"
                    )
                ),
                correct_explanation="SLI is the metric, SLO is the internal target (e.g. 99.9%), SLA is the customer contractual agreement. When Error Budget is exhausted, feature deployments pause for reliability hardening.",
                better_possible_answer="An SLI is the exact metric measured (e.g., successful request ratio). The SLO is the internal target (e.g., 99.95% over 30 days). The SLA is the contractual penalty threshold. If an incident burns 100% of our error budget, feature freezes kick in automatically until reliability stabilizes.",
            ),
            JobQuestionRecord(
                question_id="r5_q5_security_threat_model",
                interviewer_id=dir2.id,
                interviewer_name=dir2.name,
                interviewer_title=dir2.title,
                question_text=(
                    f"Perform a rapid STRIDE threat analysis for a new public API endpoint being launched at {clean_company}. What are your top mitigation controls?"
                    if lang == "English"
                    else (
                        f"{clean_company} पर लॉन्च किए जा रहे नए सार्वजनिक एपीआई के लिए त्वरित STRIDE खतरा विश्लेषण करें। आपके शीर्ष सुरक्षा नियंत्रण क्या होंगे?"
                        if lang == "Hindi"
                        else f"New public API ke liye STRIDE threat model analyze kijiye. Top security risks aur mitigations kya rahenge?"
                    )
                ),
                correct_explanation="STRIDE: Spoofing (mTLS/OAuth), Tampering (HMAC signatures), Repudiation (immutable audit logs), Information Disclosure (TLS/field encryption), Denial of Service (rate-limiting), Elevation of Privilege (RBAC).",
                better_possible_answer="Under STRIDE: Spoofing is mitigated via OAuth2 mTLS; Tampering via payload signatures; Repudiation via append-only audit logs; Information Disclosure via TLS 1.3 and masked PII; DoS via distributed API gateway throttling; and Elevation of Privilege via strict least-privilege RBAC.",
            ),
            JobQuestionRecord(
                question_id="r5_q6_mentorship_culture",
                interviewer_id=dir3.id,
                interviewer_name=dir3.name,
                interviewer_title=dir3.title,
                question_text=(
                    f"As you step into a {clean_role} at {clean_company}, how do you lift the technical capabilities of junior engineers and foster psychological safety in code reviews?"
                    if lang == "English"
                    else (
                        f"{clean_company} में {clean_role} के रूप में, आप जूनियर इंजीनियरों की तकनीकी क्षमता को कैसे बढ़ाते हैं और कोड समीक्षाओं में सकारात्मक वातावरण कैसे बनाते हैं?"
                        if lang == "Hindi"
                        else f"Senior level par junior engineers ki mentorship aur healthy engineering culture cultivate karne ke liye aapka approach kya rehta hai?"
                    )
                ),
                correct_explanation="Regular 1-on-1 pairing, review comments explaining 'why' instead of prescribing 'what', celebrating proactive questions, and encouraging ownership of end-to-end features.",
                better_possible_answer="I practice intentional pairing on complex architecture, explain the rationale behind suggestions in code reviews, and normalize mistakes as learning moments. I delegate high-visibility modules to junior engineers with safety nets to build genuine technical confidence.",
            ),
            JobQuestionRecord(
                question_id="r5_q7_strategic_tech_choice",
                interviewer_id=dir1.id,
                interviewer_name=dir1.name,
                interviewer_title=dir1.title,
                question_text=(
                    f"How do you evaluate whether to build an internal proprietary framework versus adopting an open-source solution or commercial SaaS at {clean_company}?"
                    if lang == "English"
                    else (
                        f"आप यह कैसे तय करते हैं कि किसी समाधान को स्वयं इन-हाउस बनाना चाहिए या ओपन-सोर्स / सास (SaaS) टूल अपनाना चाहिए?"
                        if lang == "Hindi"
                        else f"Build vs Buy decision lete waqt aap total cost of ownership (TCO) aur core competency ka evaluation kaise karte hain?"
                    )
                ),
                correct_explanation="Assesses core business differentiation: Build if it constitutes competitive advantage; Buy/adopt if it is commoditized infrastructure (TCO analysis including maintenance, staffing, and compliance).",
                better_possible_answer="If the capability represents {clean_company}'s core competitive moat, we build and own it. If it is commoditized infrastructure like authentication or logging, we adopt proven open-source or commercial SaaS, factoring in Total Cost of Ownership including maintenance, security patches, and talent costs.",
            ),
        ]

    # ── Round 6: Final — Executive Panel (4 Interviewers) + Closing Candidate Q&A
    else:
        vp = _next_interviewer()
        cpo = _next_interviewer()
        fellow = _next_interviewer()
        director = _next_interviewer()

        questions = [
            JobQuestionRecord(
                question_id="r6_q1_vision",
                interviewer_id=vp.id,
                interviewer_name=vp.name,
                interviewer_title=vp.title,
                question_text=(
                    f"Looking at where the industry is heading over the next three to five years, how will the {clean_role} discipline evolve at {clean_company}, and how are you preparing for that shift?"
                    if lang == "English"
                    else (
                        f"अगले तीन से पांच वर्षों में उद्योग की दिशा को देखते हुए, {clean_company} में {clean_role} की भूमिका कैसे विकसित होगी, और आप उस बदलाव के लिए कैसे तैयारी कर रहे हैं?"
                        if lang == "Hindi"
                        else f"Next 3-5 years mein {clean_role} domain kaise evolve hoga, especially AI aur distributed computing ke emergence ke saath? Aapka personal growth roadmap kya hai?"
                    )
                ),
                correct_explanation="Strategic awareness of AI-assisted engineering, serverless scale, edge computing, and adapting from writing boilerplate to systems orchestration and high-level architectural governance.",
                better_possible_answer="The role is shifting from manual boilerplate implementation to system-level synthesis, AI-augmented development, and data-driven reliability. I prepare by deepening my distributed systems fundamentals, mastering AI orchestration paradigms, and focusing on high-leverage architectural designs.",
            ),
            JobQuestionRecord(
                question_id="r6_q2_values_integrity",
                interviewer_id=cpo.id,
                interviewer_name=cpo.name,
                interviewer_title=cpo.title,
                question_text=(
                    f"Tell me about a time you discovered an uncomfortable ethical or data privacy concern in a project or company. What action did you take despite organizational pressure?"
                    if lang == "English"
                    else (
                        f"मुझे किसी ऐसे समय के बारे में बताएं जब आपने किसी परियोजना में डेटा गोपनीयता या नैतिक चिंता की पहचान की। आपने संगठनात्मक दबाव के बावजूद क्या कार्रवाई की?"
                        if lang == "Hindi"
                        else f"Jab aapne kisi project mein ethical ya data privacy concern identify kiya ho, toh organizational pressure ke bawajood aapne accountability kaise uphold ki?"
                    )
                ),
                correct_explanation="Demonstrates unwavering ethical integrity, whistleblowing or reporting through proper governance channels, prioritizing user trust over short-term release dates.",
                better_possible_answer="I discovered unencrypted customer identifiers entering analytics pipelines. Despite upcoming release deadlines, I escalated the vulnerability immediately to our security and privacy officers, drafted a hotfix that salted and masked the identifiers, and ensured our systems remained fully compliant before shipping.",
            ),
            JobQuestionRecord(
                question_id="r6_q3_deep_engineering_fellow",
                interviewer_id=fellow.id,
                interviewer_name=fellow.name,
                interviewer_title=fellow.title,
                question_text=(
                    f"Suppose you must guarantee consistent sub-50ms p99 latency for read-heavy global traffic while supporting strong write consistency on balance transfers. Walk us through your end-to-end distributed system topology."
                    if lang == "English"
                    else (
                        f"मान लीजिए कि आपको बैलेंस ट्रांसफर पर मजबूत राइट कंसिस्टेंसी का समर्थन करते हुए ग्लोबल ट्रैफ़िक के लिए 50ms से कम लेटेंसी की गारंटी देनी होगी। अपनी एंड-टू-एंड सिस्टम टोपोलॉजी समझाएं।"
                        if lang == "Hindi"
                        else f"Global read-heavy scale par sub-50ms p99 latency aur balance transfer writes ke liye strong consistency guarantee karne ke liye aapki end-to-end system topology kya hogi?"
                    )
                ),
                correct_explanation="Read/Write path segregation (CQRS), edge CDN caching with geo-DNS routing for reads, multi-region distributed consensus (Raft/Paxos or Spanner-style TrueTime) for transactional writes.",
                better_possible_answer="I would separate read and write paths using CQRS. Read queries are served from geo-distributed in-memory replica caches at edge PoPs via Anycast routing for sub-30ms response. Writes route directly to our primary transaction region utilizing Raft consensus with two-phase locking to guarantee absolute balance integrity.",
            ),
            JobQuestionRecord(
                question_id="r6_q4_business_roi",
                interviewer_id=director.id,
                interviewer_name=director.name,
                interviewer_title=director.title,
                question_text=(
                    f"At {clean_company}, engineering excellence must directly convert into customer and business value. How do you measure the return on investment of major refactoring initiatives?"
                    if lang == "English"
                    else (
                        f"{clean_company} में, इंजीनियरिंग उत्कृष्टता को व्यावसायिक मूल्य में बदलना चाहिए। आप बड़े रिफैक्टरिंग पहलों के रिटर्न ऑन इन्वेस्टमेंट (ROI) को कैसे मापते हैं?"
                        if lang == "Hindi"
                        else f"Major technical refactoring aur tech debt reduction ka ROI business stakeholders aur leadership ko kaise demonstrate karte hain?"
                    )
                ),
                correct_explanation="Translates tech metrics into revenue numbers: AWS/cloud infrastructure bill reduction, engineering cycle time reduction, incident reduction, and customer churn impact.",
                better_possible_answer="I quantify ROI using three tangible metrics: cloud infrastructure spend reduction (e.g. 25% lower compute costs), engineering velocity acceleration (PR cycle times dropping from 4 days to 6 hours), and reduced customer churn tied to decreased P0 production incidents.",
            ),
            JobQuestionRecord(
                question_id="r6_q5_handling_failure",
                interviewer_id=vp.id,
                interviewer_name=vp.name,
                interviewer_title=vp.title,
                question_text=(
                    f"Describe the most catastrophic professional failure of your career so far. What happened, what was your role in it, and how did it change you as an engineer?"
                    if lang == "English"
                    else (
                        f"अपने करियर की अब तक की सबसे बड़ी विफलता का वर्णन करें। क्या हुआ था, इसमें आपकी क्या भूमिका थी, और इसने आपको एक पेशेवर के रूप में कैसे बदल दिया?"
                        if lang == "Hindi"
                        else f"Aapke career ka sabse bada setback ya technical failure kya raha hai? Us experience se aapne personal aur professional life mein kya sikha?"
                    )
                ),
                correct_explanation="Authentic accountability without shifting blame, vulnerability, root-cause reflection, and lasting structural improvements adopted afterwards.",
                better_possible_answer="Early in my career, I deployed an untested schema migration script directly to production that locked customer tables for 40 minutes. Rather than making excuses, I owned the mistake, worked through the night to restore backups, and instituted our company's first automated CI/CD staging validation pipeline with rollback guardrails.",
            ),
            JobQuestionRecord(
                question_id="r6_q6_culture_fit",
                interviewer_id=cpo.id,
                interviewer_name=cpo.name,
                interviewer_title=cpo.title,
                question_text=(
                    f"Why should {clean_company} hire you over dozens of other highly qualified candidates applying for this exact {clean_role}?"
                    if lang == "English"
                    else (
                        f"{clean_company} को इस {clean_role} के लिए आवेदन करने वाले अन्य योग्य उम्मीदवारों के बजाय आपको क्यों चुनना चाहिए?"
                        if lang == "Hindi"
                        else f"{clean_company} ko is {clean_role} ke liye dusre candidates ke comparison mein aapko kyun select karna chahiye? Aapki unique value proposition kya hai?"
                    )
                ),
                correct_explanation="Synthesizes strong technical depth, collaborative ownership, self-starter work ethic, and passion for the company's specific mission and challenges.",
                better_possible_answer=f"Because I combine hands-on technical rigor with deep ownership. I do not just write code; I ensure that every system I build aligns with {clean_company}'s business goals, scales reliably, and elevates the team around me. I am ready to hit the ground running from day one.",
            ),
            JobQuestionRecord(
                question_id="r6_q7_closing_pitch",
                interviewer_id=director.id,
                interviewer_name=director.name,
                interviewer_title=director.title,
                question_text=(
                    f"If you receive an offer from {clean_company}, what are the specific milestones you plan to achieve during your first 90 days?"
                    if lang == "English"
                    else (
                        f"यदि आपको {clean_company} से प्रस्ताव मिलता है, तो आपके पहले 90 दिनों की कार्ययोजना क्या होगी?"
                        if lang == "Hindi"
                        else f"{clean_company} join karne ke baad aapke first 30-60-90 days ka execution plan kya rahega?"
                    )
                ),
                correct_explanation="First 30 days: Deep system context, architecture mapping, and shipping first bug fix. 60 days: Leading feature development and peer reviews. 90 days: Independent ownership and architectural optimization.",
                better_possible_answer="Days 1-30: Understand internal tooling, architecture, and team workflows, shipping my first bug fix into production within week two. Days 31-60: Take end-to-end ownership of a core feature and contribute to code reviews. Days 61-90: Identify reliability or performance optimizations and propose measurable architectural improvements.",
            ),
        ]

    return questions[:target_count], panel


def generate_clarification_response(
    question_text: str,
    language: str,
    interviewer_name: str,
) -> str:
    """Provides a natural clarification or restatement when candidate asks for clarification."""
    lang = language if language in ["English", "Hindi", "Hinglish"] else "English"
    if lang == "Hindi":
        return f"{interviewer_name}: मैं प्रश्न को स्पष्ट कर देता हूँ। मुख्य रूप से मैं यह जानना चाहता हूँ कि—{question_text}। कृपया इसे अपने अनुभव के अनुसार समझाएं।"
    elif lang == "Hinglish":
        return f"{interviewer_name}: Sure, main question ko simplify kar deta hoon. Basically hum yeh samajhna chahte hain: {question_text}."
    else:
        return f"{interviewer_name}: Certainly, let me clarify. In essence, I want to understand: {question_text}. Take your time to break it down."


def generate_closing_qa_response(
    candidate_question: str,
    company: str,
    job_role: str,
    language: str,
    panel_lead: PanelMember,
) -> str:
    """Generates a realistic panel answer to the candidate's closing question in Round 6."""
    clean_company = company.strip() if company else "our organization"
    clean_role = job_role.strip() if job_role else "this role"
    q_lower = candidate_question.lower()

    if any(k in q_lower for k in ["culture", "work life", "team", "environment"]):
        answer = f"That is a great question. At {clean_company}, our engineering culture emphasizes extreme ownership, psychological safety, and continuous learning. We encourage engineers in {clean_role} positions to take bold technical initiatives and fail fast without fear, while maintaining high collaboration and mutual respect."
    elif any(k in q_lower for k in ["tech stack", "tools", "architecture", "technologies"]):
        answer = f"Our technology stack is designed for extreme scale and resilience. While we use cutting-edge frameworks and cloud infrastructure, our primary philosophy is selecting the right tool for the job. As a {clean_role}, you will have the autonomy to influence tooling decisions based on data and benchmarks."
    elif any(k in q_lower for k in ["growth", "career", "progression", "next level"]):
        answer = f"Career progression at {clean_company} is merit-driven and transparent. We provide structured technical and leadership tracks, mentorship from distinguished fellows, and regular opportunities to lead high-visibility initiatives that directly impact millions of users."
    else:
        answer = f"Thank you for asking that thoughtful question. At {clean_company}, we believe in complete transparency with our candidates. In this {clean_role}, your work will directly touch our core mission, and you will work alongside exceptionally talented colleagues who care deeply about building world-class products."

    return f"{panel_lead.name} ({panel_lead.title}): \"{answer}\""

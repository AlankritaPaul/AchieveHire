"""
AchieveHire — Last-Minute Preparation Question Engine
Generates dynamic questions for the 30-minute intensive session:
Progression: Introduction ('Please introduce yourself.') → Easy → Moderate → Hard
Supports:
- Last-Minute Specialized Preparation (Dynamic technical questions per specialization)
- Last-Minute Job Related Preparation (Role + Company + Resume context)
"""

from typing import Dict, List, Any, Tuple
from modules.interview.last_minute.models import (
    LastMinuteQuestionRecord,
    LastMinutePanelMember,
    MODE_SPECIALIZED,
)
from modules.interview.last_minute.panel_generator import generate_last_minute_panel


def generate_last_minute_questions(
    mode: str,
    topic: str,
    company: str = "Technology Solutions",
    language: str = "English",
    resume: Dict[str, Any] = None,
) -> Tuple[List[LastMinuteQuestionRecord], List[LastMinutePanelMember]]:
    """Constructs a 6-question intensive 30-minute interview progression."""
    panel = generate_last_minute_panel(mode, topic, company)
    clean_topic = topic.strip() if topic else "Technical Core"
    clean_company = company.strip() if company else "Technology Solutions"
    resume = resume or {}
    lang = language if language in ["English", "Hindi", "Hinglish"] else "English"

    questions: List[LastMinuteQuestionRecord] = []

    # ── Question 1: Strictly 'Please introduce yourself.' ────────────────────
    intro_q = "Please introduce yourself."
    if lang == "Hindi":
        intro_q = "कृपया अपना संक्षिप्त परिचय दीजिए।"
    elif lang == "Hinglish":
        intro_q = "Please introduce yourself aur apne technical background ke baare mein brief bataiye."

    questions.append(
        LastMinuteQuestionRecord(
            question_id="lm_q1_intro",
            interviewer_id=panel[0].id,
            interviewer_name=panel[0].name,
            interviewer_title=panel[0].title,
            question_text=intro_q,
            difficulty="Intro",
            correct_explanation="A concise 60-90 second introduction covering education, key technical competencies, recent project highlights, and motivation.",
            better_possible_answer=f"I am an engineer with hands-on focus in {clean_topic}. Recently, I have built reliable systems and data pipelines, focusing on performance, code maintainability, and clean architecture.",
        )
    )

    if mode == MODE_SPECIALIZED:
        # Specialized technical trajectory (Easy → Moderate → Hard)
        # Q2: Easy - Foundational concepts
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q2_easy",
                interviewer_id=panel[1].id,
                interviewer_name=panel[1].name,
                interviewer_title=panel[1].title,
                question_text=f"In {clean_topic}, what are the primary memory management mechanisms or garbage collection paradigms, and how do they impact execution?",
                difficulty="Easy",
                correct_explanation=f"Core memory model, stack vs heap allocation, reference counting or generational garbage collection in {clean_topic}.",
                better_possible_answer=f"In {clean_topic}, objects are allocated on the heap while primitive references reside on the stack. Automatic garbage collection tracks object lifecycles using reference counting or mark-and-sweep, minimizing memory leaks while balancing latency during GC cycles.",
            )
        )
        # Q3: Easy/Moderate - Core language idioms
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q3_easy_mod",
                interviewer_id=panel[2].id,
                interviewer_name=panel[2].name,
                interviewer_title=panel[2].title,
                question_text=f"How does {clean_topic} handle concurrency and asynchronous I/O? What are the key synchronization primitives or pitfalls?",
                difficulty="Moderate",
                correct_explanation="Thread safety, race conditions, event loops, async/await or mutexes and atomic operations.",
                better_possible_answer=f"Concurrency in {clean_topic} relies on non-blocking asynchronous event loops or multi-threaded synchronization. To prevent data races and deadlocks, I use immutable data structures, mutex locks with explicit acquisition order, and thread-safe queues.",
            )
        )
        # Q4: Moderate - Profiling and optimization
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q4_mod",
                interviewer_id=panel[0].id,
                interviewer_name=panel[0].name,
                interviewer_title=panel[0].title,
                question_text=f"When debugging a critical memory leak or CPU spike in a production {clean_topic} application, what is your systematic diagnostic workflow?",
                difficulty="Moderate",
                correct_explanation="Heap profiling, CPU flamegraphs, thread dumps, telemetry metrics, and isolating memory leaks.",
                better_possible_answer="I start by generating a CPU flamegraph and heap dump under load using profiling tools. I inspect object allocation deltas to identify retained memory references, analyze thread dump states to locate locked threads, and deploy targeted unit tests to verify the patch.",
            )
        )
        # Q5: Hard - Architectural design under constraints
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q5_hard",
                interviewer_id=panel[1].id,
                interviewer_name=panel[1].name,
                interviewer_title=panel[1].title,
                question_text=f"How would you design a high-throughput, low-latency caching and query pipeline in {clean_topic} that sustains 50,000 requests per second with sub-10ms p99 latency?",
                difficulty="Hard",
                correct_explanation="In-memory cache with eviction policies, non-blocking I/O, connection pooling, and horizontal sharding.",
                better_possible_answer="I would leverage non-blocking async network I/O with connection pooling, backed by an in-memory LRU/LFU cache layer with read replicas. Writes are buffered asynchronously via event queues to keep read latency sub-10ms without blocking request worker threads.",
            )
        )
        # Q6: Hard - High-stakes trade-offs
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q6_hard_final",
                interviewer_id=panel[2].id,
                interviewer_name=panel[2].name,
                interviewer_title=panel[2].title,
                question_text=f"What are the most significant architectural limitations or trade-offs inherent to {clean_topic}, and in what enterprise scenario would you deliberately choose a different language or paradigm?",
                difficulty="Hard",
                correct_explanation="Deep technical reflection: GIL, GC pauses, type safety trade-offs, and choosing appropriate alternatives.",
                better_possible_answer=f"While {clean_topic} delivers high developer velocity and rich ecosystem support, its runtime overhead or GC pauses make it less suitable for hard real-time systems or kernel-level drivers where deterministic sub-millisecond execution is mandatory. In those domains, I would select Rust or C++.",
            )
        )

    else:
        # Job Related Trajectory (Role + Company + Resume + Difficulty)
        # Extract genuine resume skills/projects
        skills_raw = resume.get("skills", "") or "software design"
        if isinstance(skills_raw, list):
            skills_clean = skills_raw[0] if skills_raw else "core architecture"
        elif isinstance(skills_raw, str):
            skills_clean = skills_raw.split(",")[0].strip() if "," in skills_raw else skills_raw[:30].strip() or "core architecture"
        else:
            skills_clean = "core architecture"

        # Q2: Easy - Role competency & tooling
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q2_job_easy",
                interviewer_id=panel[1].id,
                interviewer_name=panel[1].name,
                interviewer_title=panel[1].title,
                question_text=f"In your day-to-day work as a {clean_topic}, how do you ensure the systems you build meet production-grade reliability and test coverage standards?",
                difficulty="Easy",
                correct_explanation="Test automation, CI/CD linting, peer code reviews, and structured documentation.",
                better_possible_answer="I practice test-driven principles with automated unit and integration tests in CI/CD, conduct detailed peer code reviews focusing on edge cases, and ensure clean API documentation for long-term maintainability.",
            )
        )
        # Q3: Moderate - Resume Project Dissection
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q3_job_mod_proj",
                interviewer_id=panel[2].id,
                interviewer_name=panel[2].name,
                interviewer_title=panel[2].title,
                question_text=f"Looking at your experience with {skills_clean}, walk us through a significant technical challenge you encountered. How did you resolve the trade-offs?",
                difficulty="Moderate",
                correct_explanation="Structured STAR response detailing specific problem, engineering action, trade-offs, and measurable outcome.",
                better_possible_answer=f"When integrating {skills_clean}, we faced high database write contention during traffic peaks. I decoupled the write pipeline using an asynchronous message queue with batch processing, reducing DB load by 45% while preserving data integrity.",
            )
        )
        # Q4: Moderate - High-Stakes Troubleshooting
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q4_job_mod_trouble",
                interviewer_id=panel[0].id,
                interviewer_name=panel[0].name,
                interviewer_title=panel[0].title,
                question_text=f"If a mission-critical service at {clean_company} begins throwing 5xx errors under sudden traffic spikes, what are your first three diagnostic and mitigation actions?",
                difficulty="Moderate",
                correct_explanation="Immediate triage: check error telemetry and recent deploys, engage circuit breakers/load-shedding, isolate blast radius.",
                better_possible_answer="First, I check recent canary releases and feature flags, rolling back immediately if correlated. Second, I inspect resource saturation and enable rate-limiting to protect upstream databases. Third, I isolate the failing dependency via circuit breakers while communicating incident updates.",
            )
        )
        # Q5: Hard - System Architecture & Scalability
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q5_job_hard_arch",
                interviewer_id=panel[1].id,
                interviewer_name=panel[1].name,
                interviewer_title=panel[1].title,
                question_text=f"At {clean_company}'s scale, how would you design a multi-region active-active data service that balances sub-second read latency with strong write consistency?",
                difficulty="Hard",
                correct_explanation="CQRS, distributed consensus (Raft/Paxos), multi-region replication, and idempotent event sourcing.",
                better_possible_answer="I would separate read and write pipelines using CQRS. Read traffic is routed to local regional caches via Anycast DNS for fast response, while transactional writes route to a primary consensus cluster using distributed locking and atomic ledgers to guarantee strict consistency.",
            )
        )
        # Q6: Hard - Leadership & Operational Trade-offs
        questions.append(
            LastMinuteQuestionRecord(
                question_id="lm_q6_job_hard_leader",
                interviewer_id=panel[2].id,
                interviewer_name=panel[2].name,
                interviewer_title=panel[2].title,
                question_text=f"When Product leadership at {clean_company} requests an aggressive launch deadline that conflicts with backend reliability hardening, how do you navigate the trade-off and secure consensus?",
                difficulty="Hard",
                correct_explanation="Quantifying risk in business impact, proposing a phased canary rollout, and aligning business and engineering stakeholders.",
                better_possible_answer="I frame the conversation around customer trust and downtime costs: an unstable launch destroys revenue. I propose a phased canary release to a 5% trusted cohort to validate product-market fit while engineering completes stability hardening for general availability.",
            )
        )

    return questions, panel


def generate_last_minute_clarification(question_text: str, interviewer_name: str) -> str:
    """Generates natural restatement or clarification for candidate questions."""
    return f"{interviewer_name}: Certainly, let me clarify. In essence, we want to understand your approach to: {question_text}. Take your time to break it down."


def check_level_completion(user_id: str, mode: str) -> Tuple[bool, int, str]:
    """
    Checks whether candidate has completed all required progressive levels:
    - Last-Minute Prep for Specialized: requires 4 levels completed.
    - Last-Minute Prep for Job Related: requires 6 levels completed.
    Returns (is_completed, required_level_count, level_label).
    """
    from pathlib import Path
    import json

    clean_u = "".join(c for c in (user_id or "guest").strip().lower() if c.isalnum() or c in "_-")

    if "Specialized" in mode:
        data_dir = Path("data/interviews")
        if data_dir.exists():
            for f in data_dir.glob(f"specialized_{clean_u}_*.json"):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    if len(data.get("rounds_completed", [])) >= 4:
                        return True, 4, "four level"
                except Exception:
                    pass
        return False, 4, "four level"
    else:
        from modules.interview.job_related.storage import load_job_interview_session
        session = load_job_interview_session(user_id)
        if session and len(session.get("completed_rounds", [])) >= 6:
            return True, 6, "six level"
        return False, 6, "six level"


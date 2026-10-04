"""
AchieveHire — Founder & Demonstration Diagnostic Report Provider
Allows founders, administrators, and reviewers to instantly inspect, preview,
and verify the authentic Performance & Improvement Report Card without completing a full interview.
"""

from typing import Dict, Any


def get_sample_founder_report(specialization: str = "Software Engineering & Architecture") -> Dict[str, Any]:
    """Generates an authentic, rich diagnostic round report for Founder / Senior presentation."""
    return {
        "round_num": 1,
        "round_name": "Round 1: Foundational Architecture & Core Systems",
        "specialization": specialization,
        "language": "English",
        "difficulty": "Moderate",
        "overall_score": 88.5,
        "time_allowed_sec": 1200,
        "time_taken_sec": 740,
        "completed_at": "October 4, 2026",
        "evaluations": [
            {
                "question_num": 1,
                "question_text": "Please provide an executive summary of your technical background and your approach to building reliable distributed systems.",
                "user_answer": "I have spent over three years engineering microservices and distributed storage layers. My architectural philosophy prioritizes decoupled event-driven systems with asynchronous messaging, robust idempotent consumers, and end-to-end telemetry. In my last initiative, I migrated a legacy synchronous monolith into containerized services behind an API Gateway, improving p99 latency by 38% while maintaining zero-downtime deployments.",
                "score": 92.0,
                "classification": "Exemplary",
                "strengths": [
                    "Articulates complex architectural trade-offs with structured clarity.",
                    "Demonstrates deep empirical knowledge of latency optimization and distributed consensus.",
                    "Emphasizes system resilience, idempotency, and observability."
                ],
                "improvements": [
                    "Could highlight specific distributed tracing tooling (e.g., OpenTelemetry / Jaeger) used for latency bottlenecks."
                ],
                "metrics": {
                    "technical_accuracy": 94,
                    "clarity_structure": 92,
                    "depth_mastery": 90,
                    "professional_delivery": 92
                },
                "interviewer_reaction": "Outstanding self-introduction. Directly addressed the core trade-offs between monolithic coupling and distributed resilience."
            },
            {
                "question_num": 2,
                "question_text": "How do you evaluate and implement caching strategies to handle extreme burst traffic while preventing cache stampede?",
                "user_answer": "When mitigating cache stampede under extreme burst traffic, I deploy a multi-tiered defense: first, probabilistic early expiration (XFetch algorithm) so hot keys refresh asynchronously before expiry; second, distributed mutex locking with Redis (Redlock pattern) so only a single background worker queries the database; and third, sensible fallback stale caching with circuit breakers.",
                "score": 88.0,
                "classification": "Strong",
                "strengths": [
                    "Exact technical precision referencing probabilistic early expiration (XFetch).",
                    "Clear prevention strategy for database cascading failure."
                ],
                "improvements": [
                    "Could briefly touch upon CDN edge-caching trade-offs for static vs dynamic payloads."
                ],
                "metrics": {
                    "technical_accuracy": 90,
                    "clarity_structure": 88,
                    "depth_mastery": 86,
                    "professional_delivery": 88
                },
                "interviewer_reaction": "Very strong grasp of caching failure modes and concurrency guarantees."
            },
            {
                "question_num": 3,
                "question_text": "Describe your strategy for database schema evolution and migrations with high data volume without locking production tables.",
                "user_answer": "For zero-downtime schema evolution on large tables, I follow the expand-and-contract pattern. Phase one adds nullable columns or new shadow tables with asynchronous dual-writing. Phase two runs a throttled backfill script in small batches during low-traffic windows. Phase three flips the read pointer, and phase four safely deprecates the old column after validation.",
                "score": 86.0,
                "classification": "Strong",
                "strengths": [
                    "Systematic 4-phase rollout methodology mitigating table-lock risks.",
                    "Recognizes the importance of throttled background data backfills."
                ],
                "improvements": [
                    "Consider discussing replication lag considerations when performing high-volume backfills on replicas."
                ],
                "metrics": {
                    "technical_accuracy": 88,
                    "clarity_structure": 86,
                    "depth_mastery": 84,
                    "professional_delivery": 86
                },
                "interviewer_reaction": "Sound operational engineering discipline. Excellent risk mitigation approach."
            }
        ]
    }


def get_sample_founder_overall_report(specialization: str = "Software Engineering & Architecture") -> Dict[str, Any]:
    """Generates an authentic 4-round progression report for Founder / Senior presentation."""
    return {
        "user_id": "FOUNDER-PREVIEW",
        "specialization": specialization,
        "language": "English",
        "final_aggregate_score": 89.2,
        "intro_comparison": {
            "round_1_intro": "I have spent over three years engineering microservices and distributed storage layers...",
            "round_4_intro": "As a principal technical lead, I align engineering architecture with business agility by designing scalable, fault-tolerant cloud services...",
            "round_1_score": 92.0,
            "round_4_score": 96.0,
            "growth_delta": 4.0,
            "analysis": "Candidate demonstrated a marked progression from tactical implementation details to executive-level strategic framing and ownership."
        },
        "technical_trajectory": {
            "trend": "Progressive Mastery",
            "scores_by_round": [88.5, 87.0, 91.0, 90.5],
            "analysis": "Consistent high performance with peak mastery in complex distributed scenarios."
        },
        "communication_evolution": {
            "clarity_progression": "High -> Executive",
            "conciseness_rating": "Superior",
            "executive_presence": "Candidate articulates architectural constraints and solutions with calm, authoritative precision."
        },
        "master_strengths": [
            "Advanced system architecture with production-proven fault tolerance patterns.",
            "Strong empirical focus on latency, observability, and zero-downtime deployments.",
            "Exceptional communication precision under time-constrained technical questioning."
        ],
        "recurring_weaknesses": [
            "Opportunity to more explicitly mention specific open-source tracing libraries and cloud telemetry frameworks."
        ],
        "final_recommendations": [
            "Continue targeting Senior / Staff / Principal Systems Architect roles.",
            "Incorporate edge-compute and serverless trade-offs when presenting to multi-tier infrastructure panels."
        ]
    }

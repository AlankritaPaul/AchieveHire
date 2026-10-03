"""
AchieveHire — Last-Minute Preparation Interview Module
Independent 30-minute intensive interview mode for immediate pre-interview rehearsal.
Features:
- Fixed 30-minute duration
- Unlimited attempts with permanent history (never overwritten)
- Two modes: Last-Minute Specialized Preparation & Last-Minute Job Related Preparation
- Voice-first interaction (questions not displayed as text during live session)
- Attempt-over-attempt score progression comparison
- Diagnostic Performance & Improvement Report with official AchieveHire stamp
"""

from modules.interview.last_minute.models import (
    MODE_SPECIALIZED,
    MODE_JOB_RELATED,
    LAST_MINUTE_DURATION_MINUTES,
    LAST_MINUTE_DURATION_SECONDS,
)

__all__ = [
    "MODE_SPECIALIZED",
    "MODE_JOB_RELATED",
    "LAST_MINUTE_DURATION_MINUTES",
    "LAST_MINUTE_DURATION_SECONDS",
]

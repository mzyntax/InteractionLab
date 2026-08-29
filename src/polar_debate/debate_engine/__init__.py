"""
NODE: Debate Engine

Architectural package for deterministic debate coordination.

Node 1 behavior is added incrementally after each component interface is
reviewed.
"""

from polar_debate.debate_engine.brief import DebaterBrief
from polar_debate.debate_engine.rounds import accept_statement, expected_speaker
from polar_debate.debate_engine.state import (
    DebateConfig,
    DebaterSide,
    DebateState,
    DebateStatement,
    DebateStatus,
)

__all__ = [
    "DebateConfig",
    "DebateState",
    "DebateStatement",
    "DebateStatus",
    "DebaterBrief",
    "DebaterSide",
    "accept_statement",
    "expected_speaker",
]

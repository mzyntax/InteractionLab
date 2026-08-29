"""
NODE: Debate Engine

Architectural package for deterministic debate coordination.

Node 1 behavior is added incrementally after each component interface is
reviewed.
"""

from polar_debate.debate_engine.debate_record import (
    DebateConfig,
    DebaterSide,
    DebateState,
    DebateStatement,
    DebateStatus,
)
from polar_debate.debate_engine.debater_identity import DebaterBrief
from polar_debate.debate_engine.debater_turn_contract import (
    Debater,
    DebaterSetup,
    ProposedStatement,
    TurnContext,
)
from polar_debate.debate_engine.turn_orchestrator import accept_statement, expected_speaker

__all__ = [
    "DebateConfig",
    "DebateState",
    "DebateStatement",
    "DebateStatus",
    "Debater",
    "DebaterBrief",
    "DebaterSetup",
    "DebaterSide",
    "ProposedStatement",
    "TurnContext",
    "accept_statement",
    "expected_speaker",
]

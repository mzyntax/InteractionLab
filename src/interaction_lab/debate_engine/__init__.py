"""
NODE: Debate Engine

Architectural package for deterministic debate coordination.

Node 1 behavior is added incrementally after each component interface is
reviewed.
"""

from interaction_lab.debate_engine.debate_prompt_builder import (
    DebatePrompt,
    build_debate_prompt,
)
from interaction_lab.debate_engine.debate_record import (
    DebateConfig,
    DebaterSide,
    DebateState,
    DebateStatement,
    DebateStatus,
)
from interaction_lab.debate_engine.debate_runner import run_debate
from interaction_lab.debate_engine.debater_identity import DebaterBrief
from interaction_lab.debate_engine.debater_turn_contract import (
    Debater,
    DebaterSetup,
    ProposedStatement,
    TurnContext,
)
from interaction_lab.debate_engine.model_debater import ModelDebater
from interaction_lab.debate_engine.text_generation_contract import (
    GenerationSettings,
    TextGenerator,
)
from interaction_lab.debate_engine.turn_orchestrator import accept_statement, expected_speaker

__all__ = [
    "DebateConfig",
    "DebatePrompt",
    "DebateState",
    "DebateStatement",
    "DebateStatus",
    "Debater",
    "DebaterBrief",
    "DebaterSetup",
    "DebaterSide",
    "GenerationSettings",
    "ModelDebater",
    "ProposedStatement",
    "TextGenerator",
    "TurnContext",
    "accept_statement",
    "build_debate_prompt",
    "expected_speaker",
    "run_debate",
]

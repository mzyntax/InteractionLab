"""
NODE: Debate Engine
COMPONENT: Debate Runner

PURPOSE:
Composes configured Debaters and deterministic turn orchestration into one
complete synchronous normal debate.

INPUTS:
An immutable ``DebateState`` and one ``Debater`` configured for each side.

OUTPUTS:
The completed ``DebateState`` containing every accepted statement.

RELATIONSHIPS:
The Turn Contract projects public context and defines proposal behavior. The
Turn Orchestrator remains the authority on legal speakers and state progression.
The runner only connects those components and does not select providers, retry
generation, or present the transcript.
"""

from model_battlegrounds.debate_engine.debate_record import DebaterSide, DebateState
from model_battlegrounds.debate_engine.debater_turn_contract import (
    Debater,
    DebaterSetup,
    TurnContext,
)
from model_battlegrounds.debate_engine.turn_orchestrator import (
    accept_statement,
    expected_speaker,
)


def _validate_debater(
    state: DebateState,
    side: DebaterSide,
    debater: Debater,
) -> None:
    """Reject participant wiring that does not match the authoritative config."""
    expected_setup = DebaterSetup.from_config(state.config, side)
    if debater.setup != expected_setup:
        raise ValueError(f"debater {side.value} setup does not match debate config")


def run_debate(
    initial_state: DebateState,
    debater_a: Debater,
    debater_b: Debater,
) -> DebateState:
    """Run or resume the normal debate protocol through its completed state."""
    _validate_debater(initial_state, DebaterSide.A, debater_a)
    _validate_debater(initial_state, DebaterSide.B, debater_b)

    debaters = {
        DebaterSide.A: debater_a,
        DebaterSide.B: debater_b,
    }
    state = initial_state

    while not state.is_complete:
        speaker = expected_speaker(state)
        context = TurnContext.from_state(state)
        proposal = debaters[speaker].propose_statement(context)
        state = accept_statement(state, speaker, proposal.content)

    return state

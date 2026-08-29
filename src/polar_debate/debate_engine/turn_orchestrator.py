"""
NODE: Debate Engine
COMPONENT: Turn Orchestrator

PURPOSE:
Enforces the initial normal A-then-B speaking order and progresses accepted
statements through immutable debate states.

INPUTS:
The current ``DebateState`` and a proposed speaker and statement.

OUTPUTS:
The expected speaker or a new ``DebateState`` containing an accepted statement.

RELATIONSHIPS:
The Debate Record owns structural validation and transcript storage. This
component owns normal speaker order and round progression. Prompt construction,
model calls, and interruption rules belong to later components.
"""

from polar_debate.debate_engine.debate_record import DebaterSide, DebateState

_NORMAL_ROUND_ORDER = (DebaterSide.A, DebaterSide.B)


def _speakers_in_round(state: DebateState, round_number: int) -> tuple[DebaterSide, ...]:
    """Return the recorded speaker order for one round."""
    return tuple(
        statement.speaker
        for statement in state.statements
        if statement.round_number == round_number
    )


def expected_speaker(state: DebateState) -> DebaterSide:
    """Return the side allowed to submit the next normal statement."""
    if state.is_complete:
        raise ValueError("a completed debate has no expected speaker")

    # Earlier rounds must contain one A statement followed by one B statement;
    # otherwise this controller cannot safely derive the next legal action.
    for round_number in range(1, state.current_round):
        if _speakers_in_round(state, round_number) != _NORMAL_ROUND_ORDER:
            raise ValueError("debate state does not follow the normal round protocol")

    current_speakers = _speakers_in_round(state, state.current_round)
    if current_speakers == ():
        return DebaterSide.A
    if current_speakers == (DebaterSide.A,):
        return DebaterSide.B
    raise ValueError("debate state does not follow the normal round protocol")


def accept_statement(
    state: DebateState,
    speaker: DebaterSide,
    content: str,
) -> DebateState:
    """Validate normal speaker order and return the resulting state snapshot."""
    expected = expected_speaker(state)
    if speaker is not expected:
        raise ValueError(f"expected debater {expected.value} to speak next")

    updated = state.record_statement(speaker, content)
    if speaker is DebaterSide.A:
        return updated

    # B closes the normal round. State owns the bounded lifecycle transitions;
    # orchestration chooses which transition follows the accepted response.
    if updated.current_round == updated.config.total_rounds:
        return updated.complete()
    return updated.advance_round()

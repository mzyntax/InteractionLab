"""Tests for the deterministic normal Turn Orchestrator."""

import pytest

from interaction_lab.debate_engine import (
    DebateConfig,
    DebaterBrief,
    DebaterSide,
    DebateState,
    accept_statement,
    expected_speaker,
)


def make_brief(position: str) -> DebaterBrief:
    """Build a valid brief for orchestration-focused tests."""
    return DebaterBrief(
        assigned_position=position,
        core_commitments=("Use clear reasoning",),
        allowed_flexibility="Concede supported details",
        debate_objective="Defend the assigned position",
    )


def make_state(total_rounds: int = 2) -> DebateState:
    """Start a debate with a configurable number of rounds."""
    config = DebateConfig(
        topic="Nuclear energy policy",
        debater_a=make_brief("Support expanded nuclear energy"),
        debater_b=make_brief("Support renewable-only energy"),
        total_rounds=total_rounds,
    )
    return DebateState.start(config)


def test_a_is_expected_at_the_start_of_a_round() -> None:
    assert expected_speaker(make_state()) is DebaterSide.A


def test_b_is_expected_after_a_statement() -> None:
    state = accept_statement(make_state(), DebaterSide.A, "Opening argument")

    assert expected_speaker(state) is DebaterSide.B


def test_b_cannot_open_a_round() -> None:
    state = make_state()

    with pytest.raises(ValueError, match="expected debater a"):
        accept_statement(state, DebaterSide.B, "Out-of-order response")

    assert state.statements == ()


def test_a_cannot_submit_twice_in_one_normal_round() -> None:
    state = accept_statement(make_state(), DebaterSide.A, "Opening argument")

    with pytest.raises(ValueError, match="expected debater b"):
        accept_statement(state, DebaterSide.A, "Second opening statement")

    assert len(state.statements) == 1


def test_accepted_statement_is_recorded_by_debate_state() -> None:
    initial = make_state()

    updated = accept_statement(initial, DebaterSide.A, "  Opening argument  ")

    assert initial.statements == ()
    assert updated.statements[0].speaker is DebaterSide.A
    assert updated.statements[0].content == "Opening argument"
    assert updated.statements[0].round_number == 1


def test_b_response_advances_to_the_next_round() -> None:
    state = accept_statement(make_state(), DebaterSide.A, "Opening argument")

    state = accept_statement(state, DebaterSide.B, "Response")

    assert state.current_round == 2
    assert not state.is_complete
    assert expected_speaker(state) is DebaterSide.A
    assert [statement.speaker for statement in state.statements] == [
        DebaterSide.A,
        DebaterSide.B,
    ]


def test_final_b_response_completes_the_debate() -> None:
    state = make_state(total_rounds=1)
    state = accept_statement(state, DebaterSide.A, "Opening argument")

    state = accept_statement(state, DebaterSide.B, "Final response")

    assert state.is_complete
    assert state.current_round == 1


def test_completed_debate_rejects_more_statements() -> None:
    state = make_state(total_rounds=1)
    state = accept_statement(state, DebaterSide.A, "Opening argument")
    state = accept_statement(state, DebaterSide.B, "Final response")

    with pytest.raises(ValueError, match="no expected speaker"):
        accept_statement(state, DebaterSide.A, "Too late")


def test_content_validation_remains_owned_by_debate_state() -> None:
    with pytest.raises(ValueError, match="content"):
        accept_statement(make_state(), DebaterSide.A, " ")


def test_incomplete_previous_round_is_not_accepted_as_normal_protocol() -> None:
    state = make_state().advance_round()

    with pytest.raises(ValueError, match="normal round protocol"):
        expected_speaker(state)


def test_consecutive_recorded_speakers_are_not_accepted_as_normal_protocol() -> None:
    state = make_state()
    state = state.record_statement(DebaterSide.A, "First")
    state = state.record_statement(DebaterSide.A, "Second")

    with pytest.raises(ValueError, match="normal round protocol"):
        expected_speaker(state)

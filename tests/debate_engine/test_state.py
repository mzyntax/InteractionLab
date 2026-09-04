"""Tests for the Debate Record structural contract."""

from dataclasses import FrozenInstanceError

import pytest

from interaction_lab.debate_engine import (
    DebateConfig,
    DebaterBrief,
    DebaterSide,
    DebateState,
    DebateStatus,
)


def make_brief(position: str) -> DebaterBrief:
    """Build a small valid brief for state-focused tests."""
    return DebaterBrief(
        assigned_position=position,
        core_commitments=("Use clear reasoning",),
        allowed_flexibility="Concede supported details",
        debate_objective="Defend the assigned position",
    )


def make_config(**overrides: object) -> DebateConfig:
    """Build a valid baseline configuration."""
    values: dict[str, object] = {
        "topic": "Nuclear energy policy",
        "debater_a": make_brief("Support expanded nuclear energy"),
        "debater_b": make_brief("Support renewable-only energy"),
        "total_rounds": 2,
    }
    values.update(overrides)
    return DebateConfig(**values)  # type: ignore[arg-type]


def test_config_normalizes_topic() -> None:
    config = make_config(topic="  Nuclear energy policy  ")

    assert config.topic == "Nuclear energy policy"


@pytest.mark.parametrize("topic", ["", " ", "\t"])
def test_config_rejects_empty_topic(topic: str) -> None:
    with pytest.raises(ValueError, match="topic"):
        make_config(topic=topic)


@pytest.mark.parametrize("total_rounds", [0, -1])
def test_config_requires_at_least_one_round(total_rounds: int) -> None:
    with pytest.raises(ValueError, match="at least 1"):
        make_config(total_rounds=total_rounds)


def test_start_creates_an_empty_active_first_round() -> None:
    config = make_config()

    state = DebateState.start(config)

    assert state.config is config
    assert state.current_round == 1
    assert state.status is DebateStatus.ACTIVE
    assert state.statements == ()
    assert not state.is_complete


def test_record_statement_normalizes_content_and_preserves_old_state() -> None:
    initial = DebateState.start(make_config())

    updated = initial.record_statement(DebaterSide.A, "  Opening argument  ")

    assert initial.statements == ()
    assert len(updated.statements) == 1
    assert updated.statements[0].sequence_number == 1
    assert updated.statements[0].round_number == 1
    assert updated.statements[0].speaker is DebaterSide.A
    assert updated.statements[0].content == "Opening argument"


def test_record_statement_rejects_empty_content() -> None:
    state = DebateState.start(make_config())

    with pytest.raises(ValueError, match="content"):
        state.record_statement(DebaterSide.A, " ")


def test_state_allows_consecutive_statements_from_one_side() -> None:
    state = DebateState.start(make_config())

    state = state.record_statement(DebaterSide.A, "First statement")
    state = state.record_statement(DebaterSide.A, "Continued statement")

    assert [statement.sequence_number for statement in state.statements] == [1, 2]
    assert [statement.speaker for statement in state.statements] == [
        DebaterSide.A,
        DebaterSide.A,
    ]


def test_advance_round_stamps_later_statements_with_the_new_round() -> None:
    state = DebateState.start(make_config())
    state = state.record_statement(DebaterSide.A, "Round one")

    state = state.advance_round()
    state = state.record_statement(DebaterSide.B, "Round two")

    assert state.current_round == 2
    assert [statement.round_number for statement in state.statements] == [1, 2]
    assert [statement.sequence_number for statement in state.statements] == [1, 2]


def test_state_cannot_advance_beyond_the_final_round() -> None:
    state = DebateState.start(make_config(total_rounds=1))

    with pytest.raises(ValueError, match="final round"):
        state.advance_round()


def test_state_cannot_complete_before_the_final_round() -> None:
    state = DebateState.start(make_config(total_rounds=2))

    with pytest.raises(ValueError, match="before its final round"):
        state.complete()


def test_complete_finalizes_the_debate() -> None:
    state = DebateState.start(make_config(total_rounds=2)).advance_round()

    completed = state.complete()

    assert completed.status is DebateStatus.COMPLETE
    assert completed.is_complete
    assert not state.is_complete


def test_completed_state_rejects_further_transitions() -> None:
    state = DebateState.start(make_config(total_rounds=1)).complete()

    with pytest.raises(ValueError, match="cannot be changed"):
        state.record_statement(DebaterSide.A, "Too late")
    with pytest.raises(ValueError, match="cannot be changed"):
        state.advance_round()
    with pytest.raises(ValueError, match="cannot be changed"):
        state.complete()


def test_state_and_configuration_are_immutable() -> None:
    state = DebateState.start(make_config())

    with pytest.raises(FrozenInstanceError):
        state.current_round = 2  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        state.config.topic = "Changed topic"  # type: ignore[misc]

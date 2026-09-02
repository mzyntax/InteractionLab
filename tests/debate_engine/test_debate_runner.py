"""Tests for the synchronous normal Debate Runner."""

from dataclasses import dataclass, field

import pytest

from polar_debate.debate_engine import (
    DebateConfig,
    DebaterBrief,
    DebaterSetup,
    DebaterSide,
    DebateState,
    ProposedStatement,
    TurnContext,
    accept_statement,
    run_debate,
)


def make_brief(position: str) -> DebaterBrief:
    """Build a stable identity for runner-focused tests."""
    return DebaterBrief(
        assigned_position=position,
        core_commitments=("Use evidence",),
        allowed_flexibility="Concede supported details",
        debate_objective="Defend the assigned position",
    )


def make_state(total_rounds: int = 2) -> DebateState:
    """Start a debate with a configurable number of rounds."""
    return DebateState.start(
        DebateConfig(
            topic="Cities should expand public transit",
            debater_a=make_brief("Support expansion"),
            debater_b=make_brief("Oppose expansion"),
            total_rounds=total_rounds,
        )
    )


@dataclass
class RecordingDebater:
    """Return numbered proposals and retain the public contexts received."""

    setup: DebaterSetup
    contexts: list[TurnContext] = field(default_factory=list)

    def propose_statement(self, context: TurnContext) -> ProposedStatement:
        self.contexts.append(context)
        return ProposedStatement(f"{self.setup.side.value} proposal {len(self.contexts)}")


@dataclass
class FailingDebater:
    """Expose runner failure behavior without a model provider."""

    setup: DebaterSetup

    def propose_statement(self, context: TurnContext) -> ProposedStatement:
        raise RuntimeError("generation failed")


def make_debaters(state: DebateState) -> tuple[RecordingDebater, RecordingDebater]:
    """Create correctly configured participants for a state."""
    return (
        RecordingDebater(DebaterSetup.from_config(state.config, DebaterSide.A)),
        RecordingDebater(DebaterSetup.from_config(state.config, DebaterSide.B)),
    )


def test_runner_completes_deterministic_multi_round_debate() -> None:
    initial = make_state(total_rounds=2)
    debater_a, debater_b = make_debaters(initial)

    result = run_debate(initial, debater_a, debater_b)

    assert result.is_complete
    assert [statement.speaker for statement in result.statements] == [
        DebaterSide.A,
        DebaterSide.B,
        DebaterSide.A,
        DebaterSide.B,
    ]
    assert [statement.content for statement in result.statements] == [
        "a proposal 1",
        "b proposal 1",
        "a proposal 2",
        "b proposal 2",
    ]
    assert initial.statements == ()


def test_runner_projects_each_updated_state_into_the_next_turn_context() -> None:
    initial = make_state(total_rounds=1)
    debater_a, debater_b = make_debaters(initial)

    run_debate(initial, debater_a, debater_b)

    assert debater_a.contexts == [TurnContext(current_round=1, transcript=())]
    assert len(debater_b.contexts) == 1
    assert [statement.content for statement in debater_b.contexts[0].transcript] == ["a proposal 1"]


def test_runner_resumes_a_valid_partial_debate() -> None:
    initial = make_state(total_rounds=1)
    partial = accept_statement(initial, DebaterSide.A, "Existing opening")
    debater_a, debater_b = make_debaters(partial)

    result = run_debate(partial, debater_a, debater_b)

    assert debater_a.contexts == []
    assert len(debater_b.contexts) == 1
    assert [statement.content for statement in result.statements] == [
        "Existing opening",
        "b proposal 1",
    ]


def test_completed_input_returns_without_requesting_proposals() -> None:
    initial = make_state(total_rounds=1)
    complete = accept_statement(initial, DebaterSide.A, "Opening")
    complete = accept_statement(complete, DebaterSide.B, "Response")
    debater_a, debater_b = make_debaters(complete)

    result = run_debate(complete, debater_a, debater_b)

    assert result is complete
    assert debater_a.contexts == []
    assert debater_b.contexts == []


def test_mismatched_debater_fails_before_any_proposal() -> None:
    initial = make_state()
    debater_a, debater_b = make_debaters(initial)
    swapped_a = RecordingDebater(debater_b.setup)

    with pytest.raises(ValueError, match="debater a setup"):
        run_debate(initial, swapped_a, debater_b)

    assert swapped_a.contexts == []
    assert debater_b.contexts == []


def test_proposal_error_propagates_without_changing_initial_state() -> None:
    initial = make_state()
    failing_a = FailingDebater(DebaterSetup.from_config(initial.config, DebaterSide.A))
    _, debater_b = make_debaters(initial)

    with pytest.raises(RuntimeError, match="generation failed"):
        run_debate(initial, failing_a, debater_b)

    assert initial.statements == ()
    assert debater_b.contexts == []

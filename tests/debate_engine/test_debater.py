"""Tests for the provider-independent Debater boundary."""

from dataclasses import FrozenInstanceError

import pytest

from polar_debate.debate_engine import (
    DebateConfig,
    Debater,
    DebaterBrief,
    DebaterSetup,
    DebaterSide,
    DebateState,
    ProposedStatement,
    TurnContext,
    accept_statement,
)


def make_brief(position: str) -> DebaterBrief:
    """Build a valid brief for boundary-focused tests."""
    return DebaterBrief(
        assigned_position=position,
        core_commitments=("Use clear reasoning",),
        allowed_flexibility="Concede supported details",
        debate_objective="Defend the assigned position",
    )


def make_config() -> DebateConfig:
    """Build one authoritative setup source for both sides."""
    return DebateConfig(
        topic="Nuclear energy policy",
        debater_a=make_brief("Support expanded nuclear energy"),
        debater_b=make_brief("Support renewable-only energy"),
        total_rounds=2,
    )


class FakeDebater:
    """Return predetermined content without a model or provider dependency."""

    def __init__(self, setup: DebaterSetup, response: str) -> None:
        self._setup = setup
        self.response = response
        self.last_context: TurnContext | None = None

    @property
    def setup(self) -> DebaterSetup:
        return self._setup

    def propose_statement(self, context: TurnContext) -> ProposedStatement:
        self.last_context = context
        return ProposedStatement(self.response)


def request_proposal(debater: Debater, context: TurnContext) -> ProposedStatement:
    """Exercise structural Protocol compatibility through a typed consumer."""
    return debater.propose_statement(context)


def test_setup_for_a_uses_a_brief_and_b_public_position() -> None:
    config = make_config()

    setup = DebaterSetup.from_config(config, DebaterSide.A)

    assert setup.side is DebaterSide.A
    assert setup.topic == config.topic
    assert setup.brief is config.debater_a
    assert setup.opponent_position == config.debater_b.assigned_position
    assert setup.total_rounds == config.total_rounds


def test_setup_for_b_uses_b_brief_and_a_public_position() -> None:
    config = make_config()

    setup = DebaterSetup.from_config(config, DebaterSide.B)

    assert setup.side is DebaterSide.B
    assert setup.brief is config.debater_b
    assert setup.opponent_position == config.debater_a.assigned_position


def test_setup_does_not_expose_the_opponents_complete_brief() -> None:
    setup = DebaterSetup.from_config(make_config(), DebaterSide.A)

    assert not hasattr(setup, "opponent_brief")


def test_setup_rejects_an_invalid_side() -> None:
    with pytest.raises(TypeError, match="side"):
        DebaterSetup.from_config(make_config(), "a")  # type: ignore[arg-type]


def test_turn_context_projects_current_public_state() -> None:
    state = DebateState.start(make_config())
    state = accept_statement(state, DebaterSide.A, "Opening argument")

    context = TurnContext.from_state(state)

    assert context.current_round == 1
    assert context.transcript is state.statements
    assert context.transcript[0].content == "Opening argument"


def test_proposed_statement_normalizes_content() -> None:
    proposal = ProposedStatement("  Opening argument  ")

    assert proposal.content == "Opening argument"


def test_proposed_statement_rejects_empty_content() -> None:
    with pytest.raises(ValueError, match="content"):
        ProposedStatement(" ")


def test_setup_context_and_proposal_are_immutable() -> None:
    setup = DebaterSetup.from_config(make_config(), DebaterSide.A)
    context = TurnContext.from_state(DebateState.start(make_config()))
    proposal = ProposedStatement("Opening argument")

    with pytest.raises(FrozenInstanceError):
        setup.topic = "Changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        context.current_round = 2  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        proposal.content = "Changed"  # type: ignore[misc]


def test_fake_debater_satisfies_protocol_without_model_generation() -> None:
    state = DebateState.start(make_config())
    fake = FakeDebater(
        setup=DebaterSetup.from_config(state.config, DebaterSide.A),
        response="Predetermined argument",
    )
    context = TurnContext.from_state(state)

    proposal = request_proposal(fake, context)

    assert proposal.content == "Predetermined argument"
    assert fake.last_context is context


def test_proposal_flows_through_orchestration_before_state_records_it() -> None:
    state = DebateState.start(make_config())
    fake = FakeDebater(
        setup=DebaterSetup.from_config(state.config, DebaterSide.A),
        response="Predetermined argument",
    )
    proposal = request_proposal(fake, TurnContext.from_state(state))

    updated = accept_statement(state, fake.setup.side, proposal.content)

    assert state.statements == ()
    assert updated.statements[0].content == "Predetermined argument"
    assert updated.statements[0].speaker is DebaterSide.A

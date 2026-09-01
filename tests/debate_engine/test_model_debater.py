"""Tests for the model-backed Debater implementation."""

from dataclasses import FrozenInstanceError

import pytest

from polar_debate.debate_engine import (
    DebateConfig,
    Debater,
    DebaterBrief,
    DebaterSetup,
    DebaterSide,
    DebateState,
    GenerationSettings,
    ModelDebater,
    ProposedStatement,
    TurnContext,
    build_debate_prompt,
)


class FakeTextGenerator:
    """Return controlled text while exposing exactly what the debater supplied."""

    def __init__(self, response: str) -> None:
        self.response = response
        self.last_prompt: str | None = None
        self.last_settings: GenerationSettings | None = None

    @property
    def model_identity(self) -> str:
        return "fake/model-for-tests"

    def generate(self, prompt: str, settings: GenerationSettings) -> str:
        self.last_prompt = prompt
        self.last_settings = settings
        return self.response


class FailingTextGenerator:
    """Represent a provider failure without introducing a real provider."""

    @property
    def model_identity(self) -> str:
        return "fake/failing-model"

    def generate(self, prompt: str, settings: GenerationSettings) -> str:
        raise RuntimeError("provider unavailable")


def make_brief(position: str) -> DebaterBrief:
    """Build one stable identity for Model Debater tests."""
    return DebaterBrief(
        assigned_position=position,
        core_commitments=("Use evidence",),
        allowed_flexibility="Concede supported details",
        debate_objective="Defend the assigned position clearly",
    )


def make_state() -> DebateState:
    """Create an empty public debate record for the first model turn."""
    config = DebateConfig(
        topic="Cities should expand public transit",
        debater_a=make_brief("Support expansion"),
        debater_b=make_brief("Oppose expansion"),
        total_rounds=2,
    )
    return DebateState.start(config)


def ask_for_statement(debater: Debater, context: TurnContext) -> ProposedStatement:
    """Exercise ModelDebater through the existing Debater protocol."""
    return debater.propose_statement(context)


def test_model_debater_builds_prompt_generates_text_and_returns_proposal() -> None:
    state = make_state()
    setup = DebaterSetup.from_config(state.config, DebaterSide.A)
    context = TurnContext.from_state(state)
    settings = GenerationSettings(temperature=0.7, max_output_tokens=300, seed=5)
    generator = FakeTextGenerator("Generated transit argument")
    debater = ModelDebater(setup, generator, settings)

    proposal = ask_for_statement(debater, context)

    assert generator.last_prompt == build_debate_prompt(setup, context).render()
    assert generator.last_settings is settings
    assert proposal == ProposedStatement("Generated transit argument")


def test_model_debater_carries_its_stable_setup() -> None:
    state = make_state()
    setup = DebaterSetup.from_config(state.config, DebaterSide.B)
    debater = ModelDebater(
        setup=setup,
        text_generator=FakeTextGenerator("Response"),
        generation_settings=GenerationSettings(temperature=0, max_output_tokens=100),
    )

    assert debater.setup is setup


def test_model_debater_does_not_record_its_proposal() -> None:
    state = make_state()
    debater = ModelDebater(
        setup=DebaterSetup.from_config(state.config, DebaterSide.A),
        text_generator=FakeTextGenerator("Unaccepted argument"),
        generation_settings=GenerationSettings(temperature=0, max_output_tokens=100),
    )

    proposal = debater.propose_statement(TurnContext.from_state(state))

    assert proposal.content == "Unaccepted argument"
    assert state.statements == ()


def test_different_generators_can_be_injected_without_changing_the_debater() -> None:
    state = make_state()
    setup = DebaterSetup.from_config(state.config, DebaterSide.A)
    context = TurnContext.from_state(state)
    settings = GenerationSettings(temperature=0, max_output_tokens=100)

    first = ModelDebater(setup, FakeTextGenerator("First model"), settings)
    second = ModelDebater(setup, FakeTextGenerator("Second model"), settings)

    assert first.propose_statement(context).content == "First model"
    assert second.propose_statement(context).content == "Second model"


def test_empty_generated_text_is_rejected_as_an_invalid_proposal() -> None:
    state = make_state()
    debater = ModelDebater(
        setup=DebaterSetup.from_config(state.config, DebaterSide.A),
        text_generator=FakeTextGenerator(" "),
        generation_settings=GenerationSettings(temperature=0, max_output_tokens=100),
    )

    with pytest.raises(ValueError, match="content"):
        debater.propose_statement(TurnContext.from_state(state))


def test_generation_errors_remain_visible_to_the_caller() -> None:
    state = make_state()
    debater = ModelDebater(
        setup=DebaterSetup.from_config(state.config, DebaterSide.A),
        text_generator=FailingTextGenerator(),
        generation_settings=GenerationSettings(temperature=0, max_output_tokens=100),
    )

    with pytest.raises(RuntimeError, match="provider unavailable"):
        debater.propose_statement(TurnContext.from_state(state))


def test_model_debater_dependencies_are_immutable() -> None:
    state = make_state()
    debater = ModelDebater(
        setup=DebaterSetup.from_config(state.config, DebaterSide.A),
        text_generator=FakeTextGenerator("Response"),
        generation_settings=GenerationSettings(temperature=0, max_output_tokens=100),
    )

    with pytest.raises(FrozenInstanceError):
        debater.setup = DebaterSetup.from_config(state.config, DebaterSide.B)  # type: ignore[misc]

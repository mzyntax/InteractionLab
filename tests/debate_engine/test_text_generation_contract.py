"""Tests for the provider-independent Text Generator contract."""

import math
from dataclasses import FrozenInstanceError

import pytest

from interaction_lab.debate_engine import GenerationSettings, TextGenerator


class FakeTextGenerator:
    """Capture a generation call without choosing or contacting a provider."""

    def __init__(self, model_identity: str, response: str) -> None:
        self._model_identity = model_identity
        self.response = response
        self.last_prompt: str | None = None
        self.last_settings: GenerationSettings | None = None

    @property
    def model_identity(self) -> str:
        return self._model_identity

    def generate(self, prompt: str, settings: GenerationSettings) -> str:
        self.last_prompt = prompt
        self.last_settings = settings
        return self.response


def request_text(
    generator: TextGenerator,
    prompt: str,
    settings: GenerationSettings,
) -> str:
    """Exercise structural Protocol compatibility through a typed consumer."""
    return generator.generate(prompt, settings)


def test_settings_preserve_reproducible_generation_controls() -> None:
    settings = GenerationSettings(
        temperature=0.7,
        max_output_tokens=512,
        seed=42,
    )

    assert settings.temperature == 0.7
    assert settings.max_output_tokens == 512
    assert settings.seed == 42


def test_settings_default_to_no_seed() -> None:
    settings = GenerationSettings(temperature=0, max_output_tokens=1)

    assert settings.temperature == 0.0
    assert settings.seed is None


@pytest.mark.parametrize("temperature", [-0.01, math.inf, -math.inf, math.nan])
def test_settings_reject_invalid_temperatures(temperature: float) -> None:
    with pytest.raises(ValueError, match="temperature"):
        GenerationSettings(temperature=temperature, max_output_tokens=1)


def test_settings_reject_a_boolean_temperature() -> None:
    with pytest.raises(TypeError, match="temperature"):
        GenerationSettings(temperature=True, max_output_tokens=1)


@pytest.mark.parametrize("max_output_tokens", [0, -1])
def test_settings_reject_non_positive_output_limits(max_output_tokens: int) -> None:
    with pytest.raises(ValueError, match="max_output_tokens"):
        GenerationSettings(temperature=0.7, max_output_tokens=max_output_tokens)


def test_settings_reject_a_non_integer_output_limit() -> None:
    with pytest.raises(TypeError, match="max_output_tokens"):
        GenerationSettings(
            temperature=0.7,
            max_output_tokens=10.5,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("seed", [True, 4.2])
def test_settings_reject_a_non_integer_seed(seed: object) -> None:
    with pytest.raises(TypeError, match="seed"):
        GenerationSettings(
            temperature=0.7,
            max_output_tokens=100,
            seed=seed,  # type: ignore[arg-type]
        )


def test_settings_are_immutable() -> None:
    settings = GenerationSettings(temperature=0.7, max_output_tokens=100)

    with pytest.raises(FrozenInstanceError):
        settings.temperature = 1.0  # type: ignore[misc]


def test_fake_generator_exposes_identity_and_returns_raw_text() -> None:
    settings = GenerationSettings(temperature=0.7, max_output_tokens=100, seed=7)
    generator = FakeTextGenerator("local/example-model@checkpoint-12", "Raw response")
    prompt = "Rendered debate prompt"

    response = request_text(generator, prompt, settings)

    assert generator.model_identity == "local/example-model@checkpoint-12"
    assert generator.last_prompt == prompt
    assert generator.last_settings is settings
    assert response == "Raw response"

"""Tests for the interactive application CLI boundary."""

import json
from collections.abc import Iterator
from types import TracebackType
from typing import cast
from urllib.request import Request

import pytest

import interaction_lab.model_providers.openai_compatible as adapter_module
from interaction_lab.cli import run_cli
from interaction_lab.debate_engine import DebaterSide


class FakeResponse:
    """Provide one context-managed provider response for CLI integration tests."""

    def __init__(self, content: str) -> None:
        self.content = content

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps({"choices": [{"message": {"content": self.content}}]}).encode()


def scripted_input(values: tuple[str, ...]) -> tuple[Iterator[str], list[str]]:
    """Create terminal answers and a place to retain the prompts shown."""
    return iter(values), []


def test_cli_assembles_independent_models_runs_debate_and_prints_transcript(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers, prompts = scripted_input(
        (
            "Public transit policy",
            "Support expansion",
            "Oppose expansion",
            "1",
            "https://a.example.test/v1",
            "model-a",
            "http://127.0.0.1:8000/v1",
            "model-b",
        )
    )
    outputs: list[str] = []
    requests: list[Request] = []

    def fake_input(prompt: str) -> str:
        prompts.append(prompt)
        return next(answers)

    def fake_urlopen(request: Request, timeout: float) -> FakeResponse:
        requests.append(request)
        assert isinstance(request.data, bytes)
        payload = cast(dict[str, object], json.loads(request.data))
        return FakeResponse(f"Argument from {payload['model']}")

    monkeypatch.setattr(adapter_module, "urlopen", fake_urlopen)

    result = run_cli(
        input_function=fake_input,
        output_function=outputs.append,
        environment={"INTERACTIONLAB_A_API_KEY": "secret-a"},
    )

    assert result.is_complete
    assert [statement.speaker for statement in result.statements] == [
        DebaterSide.A,
        DebaterSide.B,
    ]
    assert [request.full_url for request in requests] == [
        "https://a.example.test/v1/chat/completions",
        "http://127.0.0.1:8000/v1/chat/completions",
    ]
    assert requests[0].get_header("Authorization") == "Bearer secret-a"
    assert requests[1].get_header("Authorization") is None
    assert outputs[0] == "Running debate..."
    assert "[Round 1 — Debater A]\nArgument from model-a" in outputs[1]
    assert "[Round 1 — Debater B]\nArgument from model-b" in outputs[1]
    assert "secret-a" not in "".join(prompts + outputs)


def test_cli_rejects_an_invalid_round_count_before_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    answers = iter(("Topic", "Position A", "Position B", "zero"))

    def unexpected_urlopen(request: Request, timeout: float) -> FakeResponse:
        pytest.fail("provider must not be called for invalid CLI input")

    monkeypatch.setattr(adapter_module, "urlopen", unexpected_urlopen)

    with pytest.raises(ValueError, match="rounds must be an integer"):
        run_cli(input_function=lambda prompt: next(answers), environment={})


def test_cli_rejects_empty_required_input() -> None:
    with pytest.raises(ValueError, match="topic must not be empty"):
        run_cli(input_function=lambda prompt: " ", environment={})

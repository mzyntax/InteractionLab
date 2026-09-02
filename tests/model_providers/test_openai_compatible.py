"""Tests for the OpenAI-compatible Text Generator adapter."""

import json
import math
from email.message import Message
from types import TracebackType
from typing import cast
from urllib.error import HTTPError, URLError
from urllib.request import Request

import pytest

import model_battlegrounds.model_providers.openai_compatible as adapter_module
from model_battlegrounds.debate_engine import GenerationSettings, TextGenerator
from model_battlegrounds.model_providers import (
    OpenAICompatibleError,
    OpenAICompatibleTextGenerator,
)


class FakeResponse:
    """Provide a context-managed HTTP response without external network access."""

    def __init__(self, response_data: object) -> None:
        self.body = json.dumps(response_data).encode("utf-8")

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
        return self.body


def request_text(
    generator: TextGenerator,
    prompt: str,
    settings: GenerationSettings,
) -> str:
    """Exercise adapter compatibility through the shared generator contract."""
    return generator.generate(prompt, settings)


def request_payload(request: Request) -> dict[str, object]:
    """Decode the JSON body captured from one adapter request."""
    assert isinstance(request.data, bytes)
    payload: object = json.loads(request.data)
    assert isinstance(payload, dict)
    return cast(dict[str, object], payload)


def test_generate_translates_prompt_settings_and_authentication(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(request: Request, timeout: float) -> FakeResponse:
        captured["request"] = request
        captured["timeout"] = timeout
        return FakeResponse({"choices": [{"message": {"content": "  Generated argument  "}}]})

    monkeypatch.setattr(adapter_module, "urlopen", fake_urlopen)
    generator = OpenAICompatibleTextGenerator(
        base_url=" https://models.example.test/v1/ ",
        model=" debate-model ",
        api_key="secret-key",
        timeout_seconds=12,
    )
    settings = GenerationSettings(temperature=0.8, max_output_tokens=250, seed=17)

    result = request_text(generator, "Rendered debate prompt", settings)

    request = captured["request"]
    assert isinstance(request, Request)
    assert request.full_url == "https://models.example.test/v1/chat/completions"
    assert request.method == "POST"
    assert request.get_header("Authorization") == "Bearer secret-key"
    assert request.get_header("Content-type") == "application/json"
    assert captured["timeout"] == 12.0
    assert request_payload(request) == {
        "model": "debate-model",
        "messages": [{"role": "user", "content": "Rendered debate prompt"}],
        "temperature": 0.8,
        "max_tokens": 250,
        "seed": 17,
    }
    assert result == "  Generated argument  "


def test_current_output_token_field_can_be_selected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_payload: dict[str, object] = {}

    def fake_urlopen(request: Request, timeout: float) -> FakeResponse:
        captured_payload.update(request_payload(request))
        return FakeResponse({"choices": [{"message": {"content": "Response"}}]})

    monkeypatch.setattr(adapter_module, "urlopen", fake_urlopen)
    generator = OpenAICompatibleTextGenerator(
        base_url="https://models.example.test/v1",
        model="current-model",
        output_token_field="max_completion_tokens",
    )

    generator.generate(
        "Prompt",
        GenerationSettings(temperature=0, max_output_tokens=100),
    )

    assert captured_payload["max_completion_tokens"] == 100
    assert "max_tokens" not in captured_payload
    assert "seed" not in captured_payload


def test_api_key_is_not_required_for_a_local_endpoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_request: Request | None = None

    def fake_urlopen(request: Request, timeout: float) -> FakeResponse:
        nonlocal captured_request
        captured_request = request
        return FakeResponse({"choices": [{"message": {"content": "Local response"}}]})

    monkeypatch.setattr(adapter_module, "urlopen", fake_urlopen)
    generator = OpenAICompatibleTextGenerator(
        base_url="http://127.0.0.1:8000/v1",
        model="local-checkpoint",
    )

    generator.generate(
        "Prompt",
        GenerationSettings(temperature=0, max_output_tokens=100),
    )

    assert captured_request is not None
    assert captured_request.get_header("Authorization") is None
    assert generator.model_identity == "local-checkpoint"


def test_api_key_is_excluded_from_object_representation() -> None:
    generator = OpenAICompatibleTextGenerator(
        base_url="https://models.example.test/v1",
        model="private-model",
        api_key="do-not-display-this-key",
    )

    assert "do-not-display-this-key" not in repr(generator)


@pytest.mark.parametrize(
    ("field_name", "value", "error_type"),
    [
        ("base_url", "relative/path", ValueError),
        ("base_url", " ", ValueError),
        ("model", " ", ValueError),
        ("api_key", " ", ValueError),
        ("timeout_seconds", 0, ValueError),
        ("timeout_seconds", math.inf, ValueError),
        ("timeout_seconds", True, TypeError),
        ("output_token_field", "unknown", ValueError),
    ],
)
def test_invalid_configuration_is_rejected(
    field_name: str,
    value: object,
    error_type: type[Exception],
) -> None:
    configuration: dict[str, object] = {
        "base_url": "https://models.example.test/v1",
        "model": "model",
    }
    configuration[field_name] = value

    with pytest.raises(error_type):
        OpenAICompatibleTextGenerator(**configuration)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "response_data",
    [
        {},
        {"choices": []},
        {"choices": [None]},
        {"choices": [{"message": None}]},
        {"choices": [{"message": {"content": None}}]},
    ],
)
def test_malformed_responses_are_reported(
    monkeypatch: pytest.MonkeyPatch,
    response_data: object,
) -> None:
    def fake_urlopen(request: Request, timeout: float) -> FakeResponse:
        return FakeResponse(response_data)

    monkeypatch.setattr(adapter_module, "urlopen", fake_urlopen)
    generator = OpenAICompatibleTextGenerator(
        base_url="https://models.example.test/v1",
        model="model",
    )

    with pytest.raises(OpenAICompatibleError, match="response"):
        generator.generate(
            "Prompt",
            GenerationSettings(temperature=0, max_output_tokens=100),
        )


def test_unreachable_endpoint_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: Request, timeout: float) -> FakeResponse:
        raise URLError("connection refused")

    monkeypatch.setattr(adapter_module, "urlopen", fake_urlopen)
    generator = OpenAICompatibleTextGenerator(
        base_url="https://models.example.test/v1",
        model="model",
    )

    with pytest.raises(OpenAICompatibleError, match="could not be reached"):
        generator.generate(
            "Prompt",
            GenerationSettings(temperature=0, max_output_tokens=100),
        )


def test_http_error_status_is_preserved(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: Request, timeout: float) -> FakeResponse:
        raise HTTPError(request.full_url, 429, "rate limited", hdrs=Message(), fp=None)

    monkeypatch.setattr(adapter_module, "urlopen", fake_urlopen)
    generator = OpenAICompatibleTextGenerator(
        base_url="https://models.example.test/v1",
        model="model",
    )

    with pytest.raises(OpenAICompatibleError, match="HTTP status 429"):
        generator.generate(
            "Prompt",
            GenerationSettings(temperature=0, max_output_tokens=100),
        )

"""
NODE: Model Provider Integrations
COMPONENT: OpenAI-Compatible Text Generator

PURPOSE:
Connects the provider-independent text-generation contract to a configurable
OpenAI-compatible Chat Completions HTTP endpoint.

INPUTS:
Endpoint and model configuration plus prompt text and ``GenerationSettings``.

OUTPUTS:
Raw assistant text returned by the configured model endpoint.

RELATIONSHIPS:
``ModelDebater`` calls this adapter only through the ``TextGenerator`` contract.
Provider-specific request formatting, authentication, transport, and response
validation remain isolated here.
"""

import json
import math
from dataclasses import InitVar, dataclass, field
from typing import Literal, cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from polar_debate.debate_engine.text_generation_contract import GenerationSettings


class OpenAICompatibleError(RuntimeError):
    """Report a failed or malformed OpenAI-compatible generation request."""


def _normalized_text(value: str, field_name: str) -> str:
    """Normalize public configuration text and reject empty values."""
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _object_mapping(value: object, location: str) -> dict[str, object]:
    """Require one JSON object before reading its expected response fields."""
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise OpenAICompatibleError(f"response {location} must be a JSON object")
    return cast(dict[str, object], value)


def _extract_generated_text(response_data: object) -> str:
    """Extract the first assistant message from a Chat Completions response."""
    response = _object_mapping(response_data, "body")
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise OpenAICompatibleError("response choices must be a non-empty list")

    first_choice = _object_mapping(choices[0], "choices[0]")
    message = _object_mapping(first_choice.get("message"), "choices[0].message")
    content = message.get("content")
    if not isinstance(content, str):
        raise OpenAICompatibleError("response choices[0].message.content must be text")
    return content


@dataclass(frozen=True, slots=True)
class OpenAICompatibleTextGenerator:
    """Generate text through one configured Chat Completions endpoint."""

    base_url: str
    model: str
    api_key: InitVar[str | None] = None
    timeout_seconds: float = 60.0
    output_token_field: Literal["max_tokens", "max_completion_tokens"] = "max_tokens"
    _api_key: str | None = field(init=False, repr=False)

    def __post_init__(self, api_key: str | None) -> None:
        """Validate connection configuration before the first model request."""
        base_url = _normalized_text(self.base_url, "base_url").rstrip("/")
        parsed_url = urlparse(base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("base_url must be an absolute HTTP or HTTPS URL")
        object.__setattr__(self, "base_url", base_url)
        object.__setattr__(self, "model", _normalized_text(self.model, "model"))

        if not isinstance(self.timeout_seconds, int | float) or isinstance(
            self.timeout_seconds, bool
        ):
            raise TypeError("timeout_seconds must be a number")
        if not math.isfinite(self.timeout_seconds) or self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be finite and greater than zero")
        object.__setattr__(self, "timeout_seconds", float(self.timeout_seconds))

        if self.output_token_field not in {"max_tokens", "max_completion_tokens"}:
            raise ValueError("output_token_field is not supported")

        normalized_key = None if api_key is None else _normalized_text(api_key, "api_key")
        object.__setattr__(self, "_api_key", normalized_key)

    @property
    def model_identity(self) -> str:
        """Return the model identifier sent to the endpoint."""
        return self.model

    def generate(self, prompt: str, settings: GenerationSettings) -> str:
        """Send one non-streaming request and return its raw assistant text."""
        payload: dict[str, object] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": settings.temperature,
            self.output_token_field: settings.max_output_tokens,
        }
        if settings.seed is not None:
            payload["seed"] = settings.seed

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self._api_key is not None:
            headers["Authorization"] = f"Bearer {self._api_key}"

        request = Request(
            url=f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                response_body = response.read()
        except HTTPError as error:
            raise OpenAICompatibleError(
                f"generation request failed with HTTP status {error.code}"
            ) from error
        except (URLError, TimeoutError) as error:
            raise OpenAICompatibleError("generation endpoint could not be reached") from error

        try:
            response_data: object = json.loads(response_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise OpenAICompatibleError("generation endpoint returned invalid JSON") from error

        return _extract_generated_text(response_data)

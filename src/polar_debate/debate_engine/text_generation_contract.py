"""
NODE: Debate Engine
COMPONENT: Text Generator Contract

PURPOSE:
Defines the provider-independent boundary for turning one rendered prompt into
raw model-generated text.

INPUTS:
Prompt text and immutable, reproducible generation settings.

OUTPUTS:
Raw generated text from an identified model or checkpoint.

RELATIONSHIPS:
Future hosted and local provider adapters implement ``TextGenerator``. A future
model-backed Debater will combine this contract with the Debate Prompt Builder
and wrap successful output in a ``ProposedStatement``.
"""

import math
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class GenerationSettings:
    """Provider-independent controls that should be reproducible per model call."""

    temperature: float
    max_output_tokens: int
    seed: int | None = None

    def __post_init__(self) -> None:
        """Reject settings that cannot represent a valid generation request."""
        if not isinstance(self.temperature, int | float) or isinstance(self.temperature, bool):
            raise TypeError("temperature must be a number")
        if not math.isfinite(self.temperature) or self.temperature < 0:
            raise ValueError("temperature must be finite and non-negative")
        if not isinstance(self.max_output_tokens, int) or isinstance(self.max_output_tokens, bool):
            raise TypeError("max_output_tokens must be an integer")
        if self.max_output_tokens < 1:
            raise ValueError("max_output_tokens must be at least 1")
        if self.seed is not None and (
            not isinstance(self.seed, int) or isinstance(self.seed, bool)
        ):
            raise TypeError("seed must be an integer or None")

        object.__setattr__(self, "temperature", float(self.temperature))


class TextGenerator(Protocol):
    """Synchronous text-generation behavior required from every provider adapter."""

    @property
    def model_identity(self) -> str:
        """Return the provider's exact public model or checkpoint identifier."""
        ...

    def generate(self, prompt: str, settings: GenerationSettings) -> str:
        """Generate raw text without applying debate-specific behavior."""
        ...

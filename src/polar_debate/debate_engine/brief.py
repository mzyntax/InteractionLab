"""
NODE: Debate Engine
COMPONENT: Debater Brief

PURPOSE:
Defines the stable position and commitments a debater carries through one
debate. The brief is deliberately separate from the evolving transcript so a
debater can adapt its argument without silently changing its assigned identity.

INPUTS:
An assigned position, core commitments, permitted flexibility, and objective.

OUTPUTS:
An immutable ``DebaterBrief``. ``state.py`` will retain one brief per debater,
and ``context.py`` will include the current speaker's brief in each model turn.
"""

from dataclasses import dataclass


def _normalized_text(value: str, field_name: str) -> str:
    """Return stable text for downstream prompts, rejecting empty domain values."""
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


# Keep each brief immutable and limited to its declared fields.
@dataclass(frozen=True, slots=True)
class DebaterBrief:
    """Stable identity and strategic boundaries assigned to one debater.

    The brief describes what the debater should remain grounded in; it does not
    contain transcript history or judge analysis. That separation lets the next
    modules expose public debate context without leaking private evaluation.
    """

    assigned_position: str
    core_commitments: tuple[str, ...]
    allowed_flexibility: str
    debate_objective: str

    def __post_init__(self) -> None:
        """Validate once so later state and context code can trust this value."""
        if not self.core_commitments:
            raise ValueError("core_commitments must contain at least one commitment")

        normalized_commitments = tuple(
            _normalized_text(commitment, "core_commitments item")
            for commitment in self.core_commitments
        )

        # Normalize here so later prompt construction receives consistent values.
        object.__setattr__(
            self,
            "assigned_position",
            _normalized_text(self.assigned_position, "assigned_position"),
        )
        object.__setattr__(self, "core_commitments", normalized_commitments)
        object.__setattr__(
            self,
            "allowed_flexibility",
            _normalized_text(self.allowed_flexibility, "allowed_flexibility"),
        )
        object.__setattr__(
            self,
            "debate_objective",
            _normalized_text(self.debate_objective, "debate_objective"),
        )

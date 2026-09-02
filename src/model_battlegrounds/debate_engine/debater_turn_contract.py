"""
NODE: Debate Engine
COMPONENT: Debater Turn Contract

PURPOSE:
Defines the stable setup, changing turn context, and provider-independent
contract used by a debater to propose one completed statement.

INPUTS:
Validated debate configuration and state exposed as a stable setup and public
turn context.

OUTPUTS:
An unaccepted ``ProposedStatement`` for the Turn Orchestrator to evaluate.

RELATIONSHIPS:
Concrete model or human implementations satisfy the ``Debater`` protocol. The
Turn Orchestrator decides whether a proposal is legal, and the Debate Record
assigns its authoritative transcript metadata only after acceptance.
"""

from dataclasses import dataclass
from typing import Protocol

from model_battlegrounds.debate_engine.debate_record import (
    DebateConfig,
    DebaterSide,
    DebateState,
    DebateStatement,
)
from model_battlegrounds.debate_engine.debater_identity import DebaterBrief


def _normalized_text(value: str, field_name: str) -> str:
    """Normalize boundary text and reject values with no visible content."""
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


@dataclass(frozen=True, slots=True)
class DebaterSetup:
    """Stable identity and public debate information owned by one Debater."""

    side: DebaterSide
    topic: str
    brief: DebaterBrief
    opponent_position: str
    total_rounds: int

    def __post_init__(self) -> None:
        """Validate setup even when callers construct it without a config."""
        if not isinstance(self.side, DebaterSide):
            raise TypeError("side must be a DebaterSide")
        if not isinstance(self.brief, DebaterBrief):
            raise TypeError("brief must be a DebaterBrief")
        if self.total_rounds < 1:
            raise ValueError("total_rounds must be at least 1")
        object.__setattr__(self, "topic", _normalized_text(self.topic, "topic"))
        object.__setattr__(
            self,
            "opponent_position",
            _normalized_text(self.opponent_position, "opponent_position"),
        )

    @classmethod
    def from_config(cls, config: DebateConfig, side: DebaterSide) -> "DebaterSetup":
        """Create one side's setup from the authoritative debate configuration."""
        if side is DebaterSide.A:
            own_brief = config.debater_a
            opponent_brief = config.debater_b
        elif side is DebaterSide.B:
            own_brief = config.debater_b
            opponent_brief = config.debater_a
        else:
            raise TypeError("side must be a DebaterSide")

        return cls(
            side=side,
            topic=config.topic,
            brief=own_brief,
            opponent_position=opponent_brief.assigned_position,
            total_rounds=config.total_rounds,
        )


@dataclass(frozen=True, slots=True)
class TurnContext:
    """Changing public debate information supplied for one proposed statement."""

    current_round: int
    transcript: tuple[DebateStatement, ...]

    def __post_init__(self) -> None:
        """Protect the public context from malformed direct construction."""
        if self.current_round < 1:
            raise ValueError("current_round must be at least 1")
        if not isinstance(self.transcript, tuple):
            raise TypeError("transcript must be a tuple")
        if any(not isinstance(statement, DebateStatement) for statement in self.transcript):
            raise TypeError("transcript must contain only DebateStatement values")
        if any(statement.round_number > self.current_round for statement in self.transcript):
            raise ValueError("transcript cannot contain a statement from a future round")

    @classmethod
    def from_state(cls, state: DebateState) -> "TurnContext":
        """Project only changing public turn information from the Debate Record."""
        return cls(current_round=state.current_round, transcript=state.statements)


@dataclass(frozen=True, slots=True)
class ProposedStatement:
    """Completed content awaiting protocol acceptance and transcript identity."""

    content: str

    def __post_init__(self) -> None:
        """Reject an empty result before orchestration attempts to accept it."""
        object.__setattr__(self, "content", _normalized_text(self.content, "content"))


class Debater(Protocol):
    """Provider-independent behavior required from an instantiated debater."""

    @property
    def setup(self) -> DebaterSetup:
        """Return the stable assignment owned by this debater."""
        ...

    def propose_statement(self, context: TurnContext) -> ProposedStatement:
        """Return one completed statement without changing debate state."""
        ...

"""
NODE: Debate Engine
COMPONENT: Debate State

PURPOSE:
Stores the configuration, completed statements, round, and lifecycle status for
one debate without deciding which conversational actions are legal.

INPUTS:
A topic, two stable debater briefs, a round count, and completed statements.

OUTPUTS:
Immutable ``DebateState`` snapshots consumed by future orchestration, context,
research, and judging components.

RELATIONSHIPS:
The future Round Orchestrator decides speaker order, yields, and interruptions.
This module records accepted statements and protects structural invariants.
"""

from dataclasses import dataclass, replace
from enum import StrEnum

from polar_debate.debate_engine.brief import DebaterBrief


def _normalized_text(value: str, field_name: str) -> str:
    """Normalize domain text and reject values with no visible content."""
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


class DebaterSide(StrEnum):
    """Stable identifiers for the two assigned sides of a debate."""

    A = "a"
    B = "b"


class DebateStatus(StrEnum):
    """Lifecycle states currently owned by Debate State."""

    ACTIVE = "active"
    COMPLETE = "complete"


@dataclass(frozen=True, slots=True)
class DebateConfig:
    """Validated inputs that remain stable for one debate session."""

    topic: str
    debater_a: DebaterBrief
    debater_b: DebaterBrief
    total_rounds: int

    def __post_init__(self) -> None:
        """Normalize configuration once for all later state snapshots."""
        object.__setattr__(self, "topic", _normalized_text(self.topic, "topic"))
        if self.total_rounds < 1:
            raise ValueError("total_rounds must be at least 1")


@dataclass(frozen=True, slots=True)
class DebateStatement:
    """One atomic statement that has finished and entered the transcript."""

    sequence_number: int
    round_number: int
    speaker: DebaterSide
    content: str

    def __post_init__(self) -> None:
        """Protect statement identity and content invariants."""
        if self.sequence_number < 1:
            raise ValueError("sequence_number must be at least 1")
        if self.round_number < 1:
            raise ValueError("round_number must be at least 1")
        if not isinstance(self.speaker, DebaterSide):
            raise TypeError("speaker must be a DebaterSide")
        object.__setattr__(self, "content", _normalized_text(self.content, "content"))


@dataclass(frozen=True, slots=True)
class DebateState:
    """Authoritative immutable record of one debate session.

    State deliberately permits consecutive statements by the same side. The
    Round Orchestrator will decide whether a continuation or interruption is
    legal before asking this component to record it.
    """

    config: DebateConfig
    current_round: int
    status: DebateStatus
    statements: tuple[DebateStatement, ...]

    def __post_init__(self) -> None:
        """Reject snapshots that could produce an inconsistent transcript."""
        if not 1 <= self.current_round <= self.config.total_rounds:
            raise ValueError("current_round must be within the configured rounds")
        if not isinstance(self.status, DebateStatus):
            raise TypeError("status must be a DebateStatus")
        if not isinstance(self.statements, tuple):
            raise TypeError("statements must be a tuple")

        previous_round = 0
        for expected_sequence, statement in enumerate(self.statements, start=1):
            if statement.sequence_number != expected_sequence:
                raise ValueError("statement sequence numbers must be contiguous")
            if statement.round_number < previous_round:
                raise ValueError("statement round numbers must not decrease")
            if statement.round_number > self.current_round:
                raise ValueError("a statement cannot belong to a future round")
            previous_round = statement.round_number

        if self.status is DebateStatus.COMPLETE and (
            self.current_round != self.config.total_rounds
        ):
            raise ValueError("a debate can only be complete in its final round")

    @classmethod
    def start(cls, config: DebateConfig) -> "DebateState":
        """Create the initial empty state for a validated configuration."""
        return cls(
            config=config,
            current_round=1,
            status=DebateStatus.ACTIVE,
            statements=(),
        )

    @property
    def is_complete(self) -> bool:
        """Return whether the debate has completed its lifecycle."""
        return self.status is DebateStatus.COMPLETE

    def record_statement(self, speaker: DebaterSide, content: str) -> "DebateState":
        """Return a snapshot containing one newly completed statement."""
        self._require_active()
        statement = DebateStatement(
            sequence_number=len(self.statements) + 1,
            round_number=self.current_round,
            speaker=speaker,
            content=content,
        )
        return replace(self, statements=(*self.statements, statement))

    def advance_round(self) -> "DebateState":
        """Move to the next configured round without applying speaking rules."""
        self._require_active()
        if self.current_round == self.config.total_rounds:
            raise ValueError("cannot advance beyond the final round")
        return replace(self, current_round=self.current_round + 1)

    def complete(self) -> "DebateState":
        """Complete an active debate after it reaches its final round."""
        self._require_active()
        if self.current_round != self.config.total_rounds:
            raise ValueError("cannot complete a debate before its final round")
        return replace(self, status=DebateStatus.COMPLETE)

    def _require_active(self) -> None:
        """Prevent transitions after the transcript has been finalized."""
        if self.is_complete:
            raise ValueError("a completed debate cannot be changed")

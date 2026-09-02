"""Tests for the Debater Identity contract."""

from dataclasses import FrozenInstanceError

import pytest

from model_battlegrounds.debate_engine import DebaterBrief


def make_brief(**overrides: object) -> DebaterBrief:
    """Build a valid baseline so each test highlights one domain rule."""
    values: dict[str, object] = {
        "assigned_position": "Support expanded nuclear energy",
        "core_commitments": (
            "Reliable low-carbon power is necessary",
            "Safety claims should be supported by evidence",
        ),
        "allowed_flexibility": "Concede valid points without abandoning the position",
        "debate_objective": "Defend and refine the assigned position",
    }
    values.update(overrides)
    return DebaterBrief(**values)  # type: ignore[arg-type]


def test_brief_preserves_identity_fields() -> None:
    brief = make_brief()

    assert brief.assigned_position == "Support expanded nuclear energy"
    assert brief.core_commitments == (
        "Reliable low-carbon power is necessary",
        "Safety claims should be supported by evidence",
    )
    assert brief.allowed_flexibility == ("Concede valid points without abandoning the position")
    assert brief.debate_objective == "Defend and refine the assigned position"


def test_brief_normalizes_surrounding_whitespace() -> None:
    brief = make_brief(
        assigned_position="  Support nuclear energy  ",
        core_commitments=("  Reliability matters  ",),
        allowed_flexibility="  Concede supported details  ",
        debate_objective="  Defend the assigned position  ",
    )

    assert brief.assigned_position == "Support nuclear energy"
    assert brief.core_commitments == ("Reliability matters",)
    assert brief.allowed_flexibility == "Concede supported details"
    assert brief.debate_objective == "Defend the assigned position"


@pytest.mark.parametrize(
    ("field_name", "empty_value"),
    [
        ("assigned_position", " "),
        ("allowed_flexibility", ""),
        ("debate_objective", "\t"),
    ],
)
def test_brief_rejects_empty_text_fields(field_name: str, empty_value: str) -> None:
    with pytest.raises(ValueError, match=field_name):
        make_brief(**{field_name: empty_value})


def test_brief_requires_a_core_commitment() -> None:
    with pytest.raises(ValueError, match="at least one"):
        make_brief(core_commitments=())


def test_brief_rejects_blank_core_commitments() -> None:
    with pytest.raises(ValueError, match="core_commitments item"):
        make_brief(core_commitments=("Evidence matters", " "))


def test_brief_is_immutable() -> None:
    brief = make_brief()

    with pytest.raises(FrozenInstanceError):
        brief.assigned_position = "A different position"  # type: ignore[misc]

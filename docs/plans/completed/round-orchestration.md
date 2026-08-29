# Round Orchestration

## Goal

Add deterministic control flow for the initial normal `A -> B` debate protocol.

## Affected node

Node 1: Debate Engine / Round Orchestration

## Scope

- Determine the expected speaker from a `DebateState` snapshot.
- Reject statements submitted out of order.
- Delegate accepted statement storage to `DebateState.record_statement()`.
- Advance after B speaks or complete after B speaks in the final round.
- Reject state that cannot represent the normal turn protocol safely.
- Add focused tests and update architecture documentation.

## Decisions

- Orchestration is implemented with pure functions rather than a second stateful
  session object.
- A speaks first and B responds once in every initial round.
- Debate State continues to own structural validation and immutable storage.
- Model calls, prompt construction, interruptions, multiple statements per turn,
  research, and judging are deferred.

## Public interface

- `expected_speaker(state)`
- `accept_statement(state, speaker, content)`

## Verification

- 36 tests pass, including 11 focused Round Orchestration tests.
- Ruff lint passes.
- Ruff format check passes.
- Mypy passes for all source files.

## Deferred questions

- Multiple completed statements and explicit turn yields.
- Interrupt allowances, targets, and scoring.
- Alternating or configurable opening speakers.
- Debater and model-provider integration.

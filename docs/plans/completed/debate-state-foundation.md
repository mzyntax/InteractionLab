# Debate State Foundation

## Goal

Add the smallest useful state model for one deterministic debate session.

## Affected node

Node 1: Debate Engine / Debate State

## Scope

- Immutable debate configuration containing the topic, two debater briefs, and
  total round count.
- Immutable completed statements with deterministic sequence and round numbers.
- Immutable debate state containing the active round, status, and ordered
  transcript.
- Explicit transitions for recording a completed statement, advancing a round,
  and completing a debate.
- Focused unit tests and architecture documentation updates.

## Decisions

- State transitions return new snapshots rather than mutating existing state.
- A recorded statement is an atomic, completed statement; model end signaling
  belongs to the future Debater boundary.
- Debate State does not enforce speaker order or interruption rules. The future
  Round Orchestrator owns conversational legality.
- Consecutive statements from the same side are structurally valid.
- No provider, research, judge, persistence, timing, or concurrency behavior is
  included.

## Public interface

- `DebaterSide`
- `DebateStatus`
- `DebateConfig`
- `DebateStatement`
- `DebateState.start(config)`
- `DebateState.record_statement(speaker, content)`
- `DebateState.advance_round()`
- `DebateState.complete()`

## Verification

- 25 tests pass, including 16 focused Debate State tests.
- Ruff lint passes.
- Mypy passes for all source files.
- New and changed implementation files pass the Ruff format check.
- The repository-wide format check remains blocked by a pre-existing
  unformatted comment in `brief.py`.

## Deferred questions

- Statements per turn and explicit yield behavior.
- Interrupt allowance, targeting, and scoring.
- Representation of research and other transcript events.
- Provider failure and retry behavior.

# Debate Runner

## Goal

Compose the existing debate contracts, model-independent Debaters, and Turn
Orchestrator into one complete synchronous normal debate.

## Affected node

Node 1: Debate Engine / Debate Runner

## Scope

- Validate that the two supplied Debaters match the debate configuration.
- Execute the existing deterministic turn protocol until completion.
- Project each immutable state snapshot into the existing `TurnContext`.
- Return the completed `DebateState`.
- Add focused tests and update architecture documentation.

## Decisions

- The runner is synchronous and owns only workflow composition.
- The Turn Orchestrator remains the authority on legal speakers and acceptance.
- A Debater setup must exactly match the setup derived from the state config.
- Generation and proposal errors propagate to the caller without retry.
- Provider selection, CLI presentation, callbacks, and logging remain deferred.

## Progress

- [x] Implement the runner.
- [x] Add focused tests.
- [x] Run project verification.
- [x] Update architecture documentation.

## Verification

- 102 tests pass, including 6 focused Debate Runner tests.
- Ruff lint passes.
- Ruff format check passes.
- Mypy passes for all source and test files.

## Tests

- Deterministic multi-round order and complete transcript.
- State-derived context reaches each Debater.
- Resumption from a valid partial state.
- Completed input performs no generation.
- Miswired participants fail before generation.
- Proposal errors propagate without changing the supplied immutable state.

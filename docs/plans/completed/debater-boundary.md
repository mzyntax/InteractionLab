# Debater Boundary

## Goal

Define a provider-independent contract for an instantiated debater to propose a
completed statement.

## Affected node

Node 1: Debate Engine / Debater Boundary

## Scope

- Immutable stable setup derived from `DebateConfig` for either side.
- Immutable changing turn context derived from `DebateState`.
- A validated statement proposal that has not entered the transcript.
- A synchronous `Debater` protocol implemented by test doubles and future model
  adapters.
- Focused tests and architecture documentation updates.

## Decisions

- A Debater owns stable setup; changing transcript and round data arrive per turn.
- Opponents expose only their public assigned position, not their complete brief.
- Proposed statements contain no authoritative sequence or round metadata.
- Round Orchestration accepts proposals; Debate State records accepted content.
- No prompt renderer, model provider, API call, generation, character, or skill
  behavior is included.

## Public interface

- `DebaterSetup.from_config(config, side)`
- `TurnContext.from_state(state)`
- `ProposedStatement`
- `Debater` protocol

## Verification

- 46 tests pass, including 10 focused Debater Boundary tests.
- Ruff lint passes.
- Ruff format check passes.
- Mypy passes for all source files.

## Deferred questions

- Prompt construction and position-adherence behavior.
- Model-provider selection and failure handling.
- Character profiles and installed skills.
- Multiple statements, yields, and interruption proposals.

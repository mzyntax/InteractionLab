# Model Debater

## Goal

Connect a debater's identity and turn context to an injected text generator and
return the generated argument as an unaccepted proposal.

## Affected node

Node 1: Debate Engine / Model Debater

## Scope

- One immutable `ModelDebater` implementing the existing `Debater` protocol.
- Fresh prompt construction and one synchronous generation request per turn.
- Conversion of raw generated text into `ProposedStatement`.
- Focused tests and architecture documentation updates.

## Decisions

- The component receives a configured generator; it does not create one.
- Prompt construction remains owned by the Debate Prompt Builder.
- Provider behavior remains owned by concrete Text Generator adapters.
- Generation errors propagate to the future runner instead of being hidden here.
- Proposal acceptance and transcript storage remain outside this component.

## Public interface

- `ModelDebater`

## Verification

- 77 tests pass, including 7 focused Model Debater tests.
- Ruff lint passes.
- Ruff format check passes.
- Mypy passes for all source files.

## Deferred questions

- Provider-neutral failure and retry policy.
- Reproducibility recording around generation calls.
- The first concrete provider adapter.

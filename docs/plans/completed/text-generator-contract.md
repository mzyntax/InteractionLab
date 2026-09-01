# Text Generator Contract

## Goal

Define the smallest provider-independent boundary needed to send a rendered
prompt to a hosted, local, or modified model and receive its raw text.

## Affected node

Node 1: Debate Engine / Text Generator Boundary

## Scope

- Immutable generation settings for temperature, output limit, and optional seed.
- A synchronous `TextGenerator` protocol exposing exact model identity.
- Focused tests and architecture documentation updates.

## Decisions

- The contract accepts plain prompt text and returns raw generated text.
- It does not build prompts, choose providers, parse responses, or retain memory.
- Shared settings enforce only provider-independent validity.
- Provider adapters translate settings, errors, authentication, and transport.
- Additional request and result wrappers are deferred until recording or provider
  behavior demonstrates a need for them.

## Public interface

- `GenerationSettings`
- `TextGenerator` protocol

## Verification

- 70 tests pass, including 14 focused Text Generator tests.
- Ruff lint passes.
- Ruff format check passes.
- Mypy passes for all source files.

## Deferred questions

- The first concrete hosted or local provider adapter.
- Provider-neutral error categories and retry ownership.
- Streaming or asynchronous generation.
- Additional sampling settings and exact checkpoint metadata.

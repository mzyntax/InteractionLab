# 001: Inject Configured Model Provider Adapters

## Problem

The application must switch among hosted, local, and modified models without
placing provider-specific requests inside the Debate Engine.

## Options considered

- Branch on the provider inside every Model Debater generation call.
- Build one universal adapter containing every provider's transport behavior.
- Select a configured adapter at application startup and inject it through the
  shared `TextGenerator` contract.

## Decision

Use configured provider adapters implementing `TextGenerator`. Application setup
may use a small `if/elif` factory once multiple provider protocols exist. Runtime
debate components call only the selected object's common `generate()` method.

The first adapter supports configurable OpenAI-compatible Chat Completions
endpoints. It uses the standard library HTTP client and adds no runtime dependency.

## Consequences

- Models sharing one API shape can be switched through configuration alone.
- A genuinely different provider protocol requires a small adapter, but no Debate
  Engine changes.
- Provider authentication, request fields, transport errors, and response parsing
  remain independently testable.
- A factory is deferred until there is a second concrete choice to select.

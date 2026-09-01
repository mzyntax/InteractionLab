# OpenAI-Compatible Provider Adapter

## Goal

Provide the first real `TextGenerator` implementation using a configurable
OpenAI-compatible Chat Completions HTTP endpoint.

## Affected architecture

Model Provider Integrations / OpenAI-Compatible Adapter

## Scope

- A configured generator object holding endpoint, model, private API key, and timeout.
- Translation from `GenerationSettings` to one synchronous HTTP request.
- Extraction of raw generated text from a Chat Completions response.
- Clear provider-specific configuration, transport, and response errors.
- Unit tests without contacting an external model.

## Decisions

- Use Python's standard HTTP library; add no runtime dependency.
- Support either `max_tokens` or `max_completion_tokens` as a configuration choice.
- Omit seed when unset and send it unchanged when configured.
- Keep API keys private and exclude them from object representations.
- Do not add a provider factory until a second provider protocol exists.

## Public interface

- `OpenAICompatibleTextGenerator`
- `OpenAICompatibleError`

## Verification

- 96 tests pass, including 19 focused provider-adapter tests.
- Ruff lint passes.
- Ruff format check passes.
- Mypy passes for all source files.

## Deferred questions

- A provider-selection factory after a second adapter exists.
- Connection pooling or an HTTP client dependency if measurements justify it.
- Retries, streaming, and asynchronous generation.
- Live integration tests against a developer-selected endpoint.

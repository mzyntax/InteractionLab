# Debate Prompt Builder

## Goal

Construct one deterministic, provider-independent model prompt from a debater's
stable setup and current public turn context.

## Affected node

Node 1: Debate Engine / Debate Prompt Builder

## Scope

- An immutable prompt value with explicit, consistently ordered sections.
- Strong but evidence-bounded guidance for representing the assigned position.
- Complete assignment, current-round, opponent-position, and transcript context.
- Machine-safe serialization that marks transcript statements as untrusted data.
- Focused tests and architecture documentation updates.

## Decisions

- The builder is a pure function and retains no memory between calls.
- Debate continuity comes only from the supplied `TurnContext`.
- The complete accepted transcript is included for the initial implementation.
- The requested action is one completed normal debate statement in natural prose.
- Prompt guidance does not decide turn legality or mutate the Debate Record.
- Provider messages, model calls, generation settings, and response parsing remain
  outside this component.

## Public interface

- `DebatePrompt`
- `build_debate_prompt(setup, context)`

## Verification

- 56 tests pass, including 10 focused Debate Prompt Builder tests.
- Ruff lint passes.
- Ruff format check passes.
- Mypy passes for all source files.

## Deferred questions

- Transcript selection or summarization for context-window limits.
- Prompt version identifiers and controlled prompt comparisons.
- Additional action types after yields or interruptions have protocol rules.
- Reproducibility records containing exact rendered prompts and generation data.

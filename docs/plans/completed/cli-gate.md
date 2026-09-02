# CLI Gate

## Goal

Provide the first interactive terminal entry point for configuring and running a
complete two-model debate.

## Affected boundary

Application / CLI -> Node 1: Debate Engine and Model Provider Integrations

## Scope

- Collect topic, two positions, round count, and an endpoint/model for each side.
- Read optional API keys from environment variables without displaying them.
- Construct the existing configuration, provider adapters, and Model Debaters.
- Invoke the existing Debate Runner and print the completed transcript.
- Add an executable `python -m polar_debate` entry point and focused tests.

## Decisions

- Use the Python standard library without a CLI framework dependency.
- Keep provider connections independently configurable for A and B.
- Use `POLAR_DEBATE_A_API_KEY` and `POLAR_DEBATE_B_API_KEY` only for secrets.
- Use visible fixed brief and generation defaults for the first milestone.
- Print the transcript after completion; live events require a later runner contract.
- Keep source ingestion, reference material, retries, and provider discovery out of scope.

## Progress

- [x] Implement terminal input, assembly, and transcript presentation.
- [x] Add the module entry point.
- [x] Add focused tests without real model calls.
- [x] Update architecture and user documentation.
- [x] Run project verification.

## Verification

- 105 tests pass, including 3 focused CLI tests.
- Ruff lint passes.
- Ruff format check passes.
- Mypy passes for all source and test files.

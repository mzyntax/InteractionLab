# Architecture

Polar Debate is organized as modular nodes. Each node owns one understandable
responsibility, exposes explicit inputs and outputs, and can be tested and
replaced independently where practical.

## Current system

```text
Application
├── Node 1: Debate Engine [IN PROGRESS]
│   ├── Debater Identity [IMPLEMENTED]
│   ├── Debate Record [IMPLEMENTED]
│   ├── Turn Orchestrator [IMPLEMENTED]
│   ├── Debater Turn Contract [IMPLEMENTED — NO MODEL]
│   ├── Debate Prompt Builder [IMPLEMENTED — NO MODEL]
│   ├── Text Generator Contract [IMPLEMENTED]
│   └── Model Debater [IMPLEMENTED]
└── Model Provider Integrations [IN PROGRESS]
    └── OpenAI-Compatible Adapter [IMPLEMENTED]
```

Node 1 will coordinate deterministic debate rounds. Its internal components and
public interfaces are introduced incrementally after design review. The Debate
Record provides immutable configuration, lifecycle, and completed-statement
records. The Turn Orchestrator enforces the initial deterministic A-then-B
order, then advances or completes that record. The Debater Turn Contract defines
stable setup, changing turn context, and unaccepted statement proposals without
selecting or calling a model provider. The Debate Prompt Builder deterministically
turns that setup and context into a structured prompt for one normal statement.
It retains no memory and does not enforce turns. The Text Generator Contract
defines the common synchronous call, model identity, and reproducible settings
that future provider adapters must expose. The Model Debater combines those
pieces into one proposal-producing turn without accepting or recording it.
Provider selection, complete debate execution, and interruption behavior do not
yet exist.

The first concrete provider integration lives outside the Debate Engine in
`polar_debate.model_providers`. Its OpenAI-compatible adapter holds endpoint and
model configuration, translates generation settings into a Chat Completions HTTP
request, and returns raw assistant text through the shared contract. Provider
selection and the CLI do not yet exist.

The Python source uses a `src` layout. The `polar_debate.debate_engine` package
is the architectural home of Node 1. Provider-specific integrations live in
`polar_debate.model_providers`; the CLI boundary has not yet been designed.

See `docs/NODE_MAP.md` for node status and
`docs/design/node-01-debate-engine.md` for the approved initial package plan.

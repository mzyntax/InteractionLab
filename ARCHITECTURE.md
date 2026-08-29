# Architecture

Polar Debate is organized as modular nodes. Each node owns one understandable
responsibility, exposes explicit inputs and outputs, and can be tested and
replaced independently where practical.

## Current system

```text
Application
└── Node 1: Debate Engine [IN PROGRESS]
    ├── Debater Brief [IMPLEMENTED]
    ├── Debate State [IMPLEMENTED]
    ├── Round Orchestration [IMPLEMENTED]
    └── Debater Boundary [IMPLEMENTED — NO MODEL]
```

Node 1 will coordinate deterministic debate rounds. Its internal components and
public interfaces are introduced incrementally after design review. Debate
State now provides immutable configuration, lifecycle, and completed-statement
records. Round Orchestration enforces the initial deterministic A-then-B order,
then advances or completes the immutable state. The Debater Boundary defines
stable setup, changing turn context, and unaccepted statement proposals without
selecting or calling a model provider. Model generation and interruption
behavior do not yet exist.

The Python source uses a `src` layout. The `polar_debate.debate_engine` package
is the architectural home of Node 1, while provider-specific integrations and a
CLI will be placed behind boundaries that have not yet been designed.

See `docs/NODE_MAP.md` for node status and
`docs/design/node-01-debate-engine.md` for the approved initial package plan.

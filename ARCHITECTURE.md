# Architecture

Polar Debate is organized as modular nodes. Each node owns one understandable
responsibility, exposes explicit inputs and outputs, and can be tested and
replaced independently where practical.

## Current system

```text
Application
└── Node 1: Debate Engine [IN PROGRESS]
    └── Debater Brief [IMPLEMENTED]
```

Node 1 will coordinate deterministic debate rounds. Its internal components and
public interfaces are introduced incrementally after design review. The first
component is an immutable Debater Brief; orchestration behavior does not yet
exist.

The Python source uses a `src` layout. The `polar_debate.debate_engine` package
is the architectural home of Node 1, while provider-specific integrations and a
CLI will be placed behind boundaries that have not yet been designed.

See `docs/NODE_MAP.md` for node status and
`docs/design/node-01-debate-engine.md` for the approved initial package plan.

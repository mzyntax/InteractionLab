# Project Agent Instructions

This project is being developed collaboratively with the human developer.

The project vision lives in `docs/PROJECT_VISION.md`. Current architecture and
node status live in `ARCHITECTURE.md` and `docs/NODE_MAP.md`.

Do not attempt to build the entire application in one pass.

Before implementing or changing architecture, read:

- docs/PROJECT_VISION.md
- docs/DESIGN_CONCERNS.md
- relevant architectural decisions

Known concerns are not automatically approved features. Code should preserve
a graceful implementation path without prematurely implementing unresolved
behavior.

## Collaboration

For major architectural work:

1. Explain what problem is being solved.
2. Show where the component belongs in the node architecture.
3. Explain proposed inputs and outputs.
4. Identify important design alternatives.
5. Identify coupling or future-extension concerns.
6. Discuss major decisions with the developer before implementation.

Implement small, understandable pieces.

After meaningful implementations, explain:

- what was added
- where it sits in the architecture
- how the execution path works
- important design decisions
- extension points
- what the developer should understand before continuing

## Architecture

The application is composed of modular nodes.

Each node should:

- have one understandable responsibility
- expose clear interfaces
- be independently testable
- minimize coupling
- be replaceable where practical
- have documented inputs and outputs

Do not blur responsibilities between nodes.

## Code Documentation

Major modules should identify their architectural location.

Example:

NODE: Debate Engine
COMPONENT: Debate State

Briefly document purpose, inputs, outputs, and important relationships.

Add comments for complex or non-obvious mechanisms when their role in accomplishing the component’s goal is not immediately clear.

Comments should connect the mechanism to the surrounding system:

# Append to a new transcript tuple so earlier DebateState snapshots remain
# unchanged and can still represent previous debate states.
return replace(self, statements=(*self.statements, statement))

Do not explain Python syntax in isolation:

# Bad: The asterisk unpacks the tuple.

Explain what the mechanism achieves here:

# Good: Preserve the existing transcript while creating the next immutable
# state snapshot with the accepted statement appended.

A useful comment should allow both a junior and an experienced developer to understand why the mechanism belongs in this component.

Do not:

comment every line
restate names, types, or error messages
narrate straightforward control flow
duplicate nearby docstrings
add generic language tutorials unrelated to the component’s goal

Prefer concise comments that explain architectural intent, protected invariants, ownership boundaries, or the system-level purpose of a complex mechanism.

## Review Gates

Discuss with the developer before:

- adding major dependencies
- changing node boundaries
- changing public interfaces
- choosing persistent storage
- introducing concurrency
- choosing model-provider architecture
- beginning a major new node
- beginning frontend implementation

## Development

Prefer:

DISCUSS -> DESIGN -> IMPLEMENT SMALL PIECE -> TEST -> EXPLAIN -> REVIEW

over large autonomous implementations.

Use small meaningful Git commits.

Keep architecture documentation updated.

## Verification

Run the project checks with:

```text
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

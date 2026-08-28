# Node 1: Debate Engine

Status: planned

## Purpose

The Debate Engine will coordinate a deterministic, round-based debate without
embedding model-provider, research-provider, or frontend behavior.

## Planned inputs

- Debate topic
- Position A and Position B
- Number of rounds
- Replaceable debater, research, claim-tracking, and judge collaborators

## Planned outputs

- Ordered debate state and transcript
- Basic claims and research evidence
- Structured final debate result

## Initial package plan

The architectural package is `polar_debate.debate_engine`. Modules will be
added one milestone at a time rather than scaffolded before their interfaces
are understood.

The first proposed implementation milestone is Debate State: define the input
configuration, invariants, initial state, and deterministic state transitions.
Its mutability model and public interface require review before implementation.

## Boundaries

- Orchestration must depend on small interfaces rather than concrete providers.
- Debate state must not know how model or research calls are executed.
- Basic claim tracking must not grow into the future argument graph prematurely.
- The initial execution model is synchronous; concurrency requires review.
- Persistence and CLI boundaries remain undecided.

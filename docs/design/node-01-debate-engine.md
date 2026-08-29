# Node 1: Debate Engine

Status: in progress

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

The first implemented component is Debater Identity in
`debater_identity.py`. It establishes an immutable assigned position, core
commitments, allowed flexibility, and debate objective without introducing the
future Character or Skill systems.

The Debate Record in `debate_record.py` owns immutable debate configuration,
completed atomic statements, the active round, and lifecycle status. Its
transitions record statements, advance rounds, and complete a debate without
mutating previous snapshots.

The Debate Record accepts consecutive statements from either side because it
records what has been accepted rather than deciding what may happen next. The
Turn Orchestrator owns speaker order and will own future statement allowances,
yields, and interrupt legality. A stored statement is complete; model end
signaling belongs to a future argument-generation component.

The Turn Orchestrator in `turn_orchestrator.py` is implemented as pure
control-flow functions over `DebateState`. The initial protocol requires A to
submit one completed statement followed by B. B's accepted response advances to
the next round or completes the debate after the final round. The orchestrator
rejects records that do not follow this normal protocol and delegates transcript
storage to the Debate Record.

The provider-independent Debater Turn Contract in
`debater_turn_contract.py` is implemented. It defines immutable setup derived
from Debate Configuration, immutable public turn context, unaccepted statement
proposals, and the interface every future Debater implementation must follow.
It supports the runtime flow but is not itself a runtime step. The Turn
Orchestrator decides whether to accept a proposal before the Debate Record stores
its content.

The boundary is synchronous and can be implemented by deterministic test
doubles, future model adapters, or human-controlled debaters. It contains no
prompt renderer, provider client, API call, or model generation. Choosing a
model-provider boundary and prompt-construction responsibility requires the next
design review.

## Boundaries

- Orchestration must depend on small interfaces rather than concrete providers.
- The Debate Record must not know how model or research calls are executed.
- Basic claim tracking must not grow into the future argument graph prematurely.
- The initial execution model is synchronous; concurrency requires review.
- Persistence and CLI boundaries remain undecided.
- Debater identities are stable inputs; evolving transcripts and private judge
  analysis must not be added to them.

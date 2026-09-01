# Future Attributes

This document tracks the maturity of each Python module. Finished modules have
completed their approved responsibility. Beta modules include likely extensions
and guidance for integrating them without blurring component boundaries.

## POLAR_DEBATE/\_\_INIT\_\_.PY (BETA)

Marks the application package. Future nodes may add public exports; keep this
file lightweight and expose only reviewed interfaces.

## DEBATE_ENGINE/\_\_INIT\_\_.PY (BETA)

Defines the public Debate Engine package surface. Add exports only after a
component contract has been reviewed, implemented, and tested.

## DEBATER_IDENTITY.PY (FINISH)

Defines the immutable position, commitments, flexibility, and objective assigned
to one debater. It is finished because that approved identity contract is fully
implemented and tested. Transcript, prompt, and character data belong elsewhere.

## DEBATE_RECORD.PY (BETA)

Stores immutable debate configuration, completed statements, round position,
and lifecycle status. The current tuple transcript is simple and appropriate for
short debates, but `(*state.statements, statement)` copies all existing statement
references on every append. Long debates may therefore require a different
storage boundary.

An append-only SQLite statement table is a future candidate. Keep SQLite outside
the domain model behind a transcript repository, preserve deterministic sequence
and round ordering, and ensure a statement append and its state transition cannot
diverge. Persistent storage requires design review before implementation.

## TURN_ORCHESTRATOR.PY (BETA)

Enforces the initial A-then-B protocol and advances or completes the Debate Record.
Potential extensions include multiple statements, explicit yields, configurable
opening order, and controlled interruptions. Add them as explicit protocol rules
while continuing to delegate transcript storage to the Debate Record.

## DEBATER_TURN_CONTRACT.PY (BETA)

Defines stable Debater setup, changing public turn context, unaccepted statement
proposals, and the provider-independent Debater protocol. Future model, human,
or character-backed implementations should satisfy this protocol rather than
add generation behavior to orchestration or state. Extend proposal types only
when yields or interruptions have approved protocol rules.

## DEBATE_PROMPT_BUILDER.PY (BETA)

Builds a fresh, immutable prompt from stable setup and current public context.
Future extensions may add prompt versioning, context-window selection, and new
approved action types. Keep it stateless, deterministic, provider-independent,
and separate from model calls and turn enforcement.

## TEXT_GENERATION_CONTRACT.PY (BETA)

Defines immutable shared generation settings and the synchronous,
provider-independent text-generation protocol. Future extensions may add sampling
controls or error categories after concrete adapters expose a shared need. Keep
provider clients, authentication, retries, and debate behavior outside this file.

## TEST_PACKAGE.PY (BETA)

Smoke-tests the package boundary. Extend it when new public components are
intentionally exported.

## TEST_BRIEF.PY (FINISH)

Covers the finished Debater Brief validation and immutability contract.

## TEST_STATE.PY (BETA)

Covers the current Debate State structural and lifecycle contract. If transcript
storage moves behind a repository, retain these domain tests and add persistence,
ordering, and failed-write consistency tests at the new boundary.

## TEST_ROUNDS.PY (BETA)

Covers the initial normal round protocol. Add focused cases alongside each new
yield, statement-allocation, opening-order, or interruption rule.

## TEST_DEBATER.PY (BETA)

Covers setup projection, opponent privacy, turn context, proposal validation,
fake Protocol compatibility, and proposal acceptance without model generation.
Add provider-specific tests later at the provider boundary, not here.

## TEST_DEBATE_PROMPT_BUILDER.PY (BETA)

Covers prompt completeness, opponent privacy, transcript isolation, deterministic
rendering, immutability, and fresh-context continuity. Add versioning and context
selection cases only when those extensions are approved.

## TEST_TEXT_GENERATION_CONTRACT.PY (BETA)

Covers settings validation and immutability, exact model identity, raw text
return, and structural fake-generator compatibility. Add adapter-specific tests
beside each future adapter rather than expanding this contract test suite.

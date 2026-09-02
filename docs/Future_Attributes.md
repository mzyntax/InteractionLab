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

A future reviewed contract may let an assignment identify a represented
perspective and attach normalized reference material. Keep the perspective
(whose view is being represented), grounding material (what defines that view),
and debate evidence (what supports a factual claim) conceptually distinct. Do not
add URL retrieval, document parsing, or video transcript extraction to this
module.

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

## MODEL_DEBATER.PY (BETA)

Connects stable debater setup and current turn context to an injected Text
Generator, returning raw output as an unaccepted proposal. Future extensions may
integrate approved recording or failure policies around the call. Keep provider
creation, turn enforcement, transcript storage, and judging outside this file.

## DEBATE_RUNNER.PY (BETA)

Validates that two Debaters match the authoritative debate configuration, then
composes state-derived turn context, proposal generation, and deterministic
acceptance until the debate is complete. Potential extensions include observable
execution events or an injected recording boundary after those contracts are
reviewed. Keep CLI interaction, provider selection, source ingestion, retries,
research, and transcript presentation outside this module.

## REFERENCE MATERIAL CONTRACT (FUTURE)

May represent normalized material used to ground an assigned perspective. Likely
attributes include exact content, a human-readable title, optional author, source
kind, and original locator. The contract should preserve the exact content used
for reproducibility and identify imported text as untrusted prompt data. Its final
location and relationship to `DebaterBrief` require design review.

Identity-grounding references must remain distinguishable from evidence offered
for debate claims. A single source may eventually serve both roles, but that must
be explicit rather than inferred from its presence.

## SOURCE INGESTION (FUTURE)

May turn pasted text, files, webpages, or video links into normalized Reference
Material before debate execution. Provider-specific retrieval, transcript
extraction, provenance capture, and failures belong here or behind its adapters,
not in the CLI, Debate Runner, or Prompt Builder. Automatic retrieval and its
dependency choices require architectural review.

## CLI.PY AND \_\_MAIN\_\_.PY (BETA)

Collect simple debate inputs, construct provider and debater dependencies, invoke
`run_debate()`, and present its result through an executable package entry point.
The initial version uses standard-library terminal input and output, accepts an
independent endpoint and model for each side, and reads optional secrets only
from environment variables. Future flags, configuration files, named provider
profiles, generation controls, and source locators should translate into reviewed
application contracts rather than adding debate, retrieval, or prompt-building
rules to the CLI. Live transcript output requires a separate observable runner
contract rather than placing turn execution in this boundary.

## TEST_CLI.PY (BETA)

Covers input-to-application assembly, independent authenticated and keyless model
connections, completed transcript presentation, secret non-disclosure, and early
input validation. Future configuration formats and presentation modes should be
tested here without real network calls.

## MODEL_PROVIDERS/\_\_INIT\_\_.PY (BETA)

Exposes reviewed concrete model-provider adapters. Keep imports lightweight and
do not turn this package boundary into provider-selection control flow.

## MODEL_PROVIDERS/OPENAI_COMPATIBLE.PY (BETA)

Implements synchronous Chat Completions generation for a configured compatible
endpoint. Future work may add connection pooling or broader response support when
real endpoints demonstrate a need. Keep secrets out of representations and keep
debate behavior, retries, provider selection, and logging outside this adapter.

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

## TEST_MODEL_DEBATER.PY (BETA)

Covers prompt handoff, exact settings, replaceable generators, proposal creation,
state separation, visible failures, and immutability. Add provider behavior to
adapter-specific tests rather than this component suite.

## TEST_DEBATE_RUNNER.PY (BETA)

Covers deterministic completion, state-derived context, partial-state resumption,
completed input, participant wiring, and visible proposal failures. Add event or
recording tests only if those future runner extension contracts are approved.

## TEST_OPENAI_COMPATIBLE.PY (BETA)

Covers request translation, model identity, authentication privacy, optional
settings, raw response extraction, configuration validation, and provider errors.
Add live endpoint tests only when their credentials and execution policy are
explicitly designed.

# Design Concerns

This is a short, living list of known concerns that may affect current work.
It records what to keep in mind without requiring speculative features.

When a concern becomes an actual design decision, record the chosen approach in
`docs/decisions/`.

## Active concerns

### Model adherence to assigned positions

**Affected module:** Debate Prompt Builder

Some models may weaken, disclaim, or refuse certain assigned positions. The
current `DebaterBrief` only stores the assignment; it does not control model
behavior.

For now, preserve a clear separation between representing a position and
personally endorsing it. Observe real transcripts before changing prompts or
adding adherence mechanisms.

### Untrusted transcript content

**Affected module:** Debate Prompt Builder

An accepted statement can contain text that resembles model instructions. The
prompt builder serializes the transcript as explicitly untrusted data and tells
the model not to follow it as instruction. Keep this boundary visible if future
context selection or provider-specific message formatting is introduced.

### Interruptions

**Affected modules:** Debate Record and Turn Orchestrator

Interruptions may make rebuttals feel more natural, but they can also fragment
the debate or be overused.

Keep the initial design compatible with completed statements and a configurable
interrupt allowance. Do not add streaming, concurrency, live muting, or complex
moderation until basic turn-taking works and can be observed.

### Deterministic debate flow

**Affected modules:** Debate Record and Turn Orchestrator

Natural conversation features can make execution difficult to reproduce and
test.

Use rounds, turns, statements, and explicit allowances instead of wall-clock
time. Keep initial execution synchronous.

### Provider-specific behavior

**Affected module:** Text Generator and future provider adapters

Different providers may refuse requests, format output differently, or impose
different restrictions.

Do not place provider-specific rules or errors inside the Debate Record. Translate
them in concrete adapters implementing the shared `TextGenerator` contract.

### Judge influence during a debate

**Affected modules:** Judge and future Moderator

Live scoring or muting could help debaters adapt, but it could also bias the
conversation and blur component responsibilities.

For the first version, let the Judge evaluate the completed debate. Revisit live
moderation only after the basic engine and interrupt behavior can be tested.

## Working rule

Add a concern here only when it affects a current or near-term design. State the
affected module and one practical guardrail. Avoid implementing a workaround
until the behavior is observable or the component requires a decision.

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

### Growing transcript context

**Affected modules:** Debate Prompt Builder and future Transcript Context Selector

Resending the complete transcript increases token cost and generation latency,
eventually exceeds model context limits, and may reduce attention to important
earlier arguments. Keep the Debate Record complete, but allow a future stateless
selector to produce a bounded, reproducible prompt projection. Never silently
truncate or replace original statements with an unaudited summary.

### Key-point lifecycle

**Affected modules:** future Basic Claim Tracking and Transcript Context Selector

Recency alone cannot determine whether a key point remains important, while an
opaque model or live Judge decision could bias what later debaters are allowed to
see. Preserve source-statement references and explicit lifecycle events. Do not
mark a point resolved merely because it has not been mentioned recently.

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
them in concrete adapters implementing the shared `TextGenerator` contract. Keep
compatibility differences, such as output-token parameter names, explicit in
adapter configuration rather than silently changing a request.

### Judge influence during a debate

**Affected modules:** Judge and future Moderator

Live scoring or muting could help debaters adapt, but it could also bias the
conversation and blur component responsibilities.

For the first version, let the Judge evaluate the completed debate. Revisit live
moderation only after the basic engine and interrupt behavior can be tested.

### Perspective grounding versus debate evidence

**Affected modules:** Debater Identity, Debate Prompt Builder, future Reference
Material contract, future Source Ingestion, and future CLI

A debater may eventually represent a person's documented viewpoint or use supplied
material such as pasted text, a document, webpage, or video transcript. Material
that defines the perspective being represented is not the same as evidence cited
to support a factual claim during the debate. Preserve that distinction in data
and prompts so future research and claim verification do not reinterpret identity
grounding as verified evidence.

Keep the first CLI limited to simple debate configuration. It may later collect
text or source locators, but retrieval and normalization must belong to a separate
ingestion boundary. The Debate Runner should receive already configured Debaters
and must not fetch, parse, or classify sources.

### Reproducible and untrusted reference material

**Affected modules:** future Reference Material contract, future Source Ingestion,
and Debate Prompt Builder

A URL alone is neither stable model input nor a guarantee that a provider can
access its content. Webpages, files, and video links should eventually be resolved
into normalized text plus provenance before a debate begins. Preserve the source
locator, title or author when known, and the exact extracted content used for the
run so later results can be understood and reproduced.

Treat imported material as untrusted data when it enters a prompt. Source text
must not become model instructions merely because it was supplied as grounding.
Automatic retrieval, transcript extraction, trust scoring, and citation
verification require separate design review and are not part of the initial CLI.

## Working rule

Add a concern here only when it affects a current or near-term design. State the
affected module and one practical guardrail. Avoid implementing a workaround
until the behavior is observable or the component requires a decision.

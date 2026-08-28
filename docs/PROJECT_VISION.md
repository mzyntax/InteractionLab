# Project: Modular AI Debate Platform

You are helping me **build this project with me**, not building it blindly for me.

I am the developer and need to understand the architecture and code as it develops.

Your job is to act as an experienced engineering partner who:

* discusses architectural decisions with me,
* explains important implementation choices,
* identifies conflicts before coding them,
* proposes alternatives when appropriate,
* implements only reasonably scoped pieces at a time,
* tests what you implement,
* and maintains documentation explaining how the system fits together.

Do **not** attempt to build the entire application in one pass.

---

# 1. Project Vision

We are building a modular AI experimentation platform based around interconnected **nodes**.

A node is:

> A self-contained subsystem that performs one clearly understandable job and exposes a clean interface to other nodes.

Every node must:

* make sense independently,
* have clearly defined inputs and outputs,
* avoid unnecessary knowledge of other nodes,
* be independently testable,
* be replaceable without rebuilding the entire application,
* contain documentation explaining its purpose,
* expose understandable interfaces,
* and be understandable enough that I can personally modify and debug it.

The complete application will eventually resemble a tree/graph of connected nodes.

```text
                    Application

                         │
                Debate Orchestrator
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
     Debaters         Research          Judge
        │                │                 │
     Characters      Evidence        Evaluation
        │
      Skills
        │
   Community / Marketplace
```

These subsystems will NOT all be built initially.

Development happens incrementally.

---

# 2. Core Product

The initial product is an AI debate laboratory.

A user defines:

* a topic,
* Position A,
* Position B,
* and debate parameters.

Two AI agents receive opposing positions.

They:

1. construct arguments,
2. respond to each other,
3. research evidence,
4. introduce sources,
5. challenge evidence,
6. identify contradictions,
7. continue for multiple rounds.

A separate Judge model observes the debate.

The Judge evaluates the debaters across multiple dimensions rather than simply declaring a winner.

Possible dimensions include:

* factual support,
* evidence quality,
* logical consistency,
* rebuttal quality,
* argument structure,
* rhetorical/debate performance.

The final output includes:

* winner,
* category scores,
* explanation of scoring,
* strongest arguments,
* weakest arguments,
* contradictions,
* unsupported claims,
* important sources,
* and overall analysis.

---

# 3. Long-Term Node Structure

The architecture should allow the following nodes to eventually exist.

## Node 1 — Debate Engine

This is the first node we will build.

Responsibilities:

* initialize debates,
* manage rounds,
* manage turns,
* maintain debate state,
* invoke Debater A,
* invoke Debater B,
* request research,
* track basic claims,
* invoke the Judge,
* produce a structured DebateResult.

Node 1 must work completely from the command line without a frontend.

---

## Future Node — Research Engine

Eventually research should become a more sophisticated independent subsystem.

Potential responsibilities:

* search queries,
* source retrieval,
* source metadata,
* evidence extraction,
* source quality analysis,
* recency checks,
* citation verification,
* conflicting evidence discovery.

For Node 1, research may initially be implemented through a simple interface.

Do NOT tightly couple DebateEngine to a specific search provider.

---

## Future Node — Argument / Claim Graph

Eventually arguments should become structured data.

Potential structure:

```text
Claim
├── evidence
├── counterclaim
├── rebuttal
├── contradiction
├── concession
└── dependent claims
```

Node 1 only needs basic claim tracking.

Do not prematurely implement the full argument graph.

---

## Future Node — Character System

Users will eventually create persistent AI debate characters.

Possible Character composition:

```text
Character
├── worldview
├── temperament
├── rhetorical style
├── research behavior
├── evidence preferences
├── debate strategy
└── installed skills
```

Characters should eventually modify how a Debater behaves without requiring changes to DebateEngine.

---

## Future Node — Skill System

Skills will be modular capabilities that can be attached to characters.

A skill should eventually be more than a prompt.

Possible structure:

```text
Skill
├── instructions
├── arguments
├── claims
├── sources
├── counterarguments
├── examples
├── activation conditions
├── research strategy
├── metadata
└── performance history
```

A user may be able to drag/drop skills onto characters.

Skills may represent:

* argument strategies,
* evidence packages,
* rhetorical techniques,
* research methods,
* debate tactics,
* ideological argument packages,
* questioning styles.

---

## Future Node — Community

Users may eventually:

* publish characters,
* publish skills,
* fork skills,
* improve skills,
* rate skills,
* compare performance,
* install other users' skills.

---

## Future Node — Marketplace

Potential future monetization:

* credits / coins,
* paid skills,
* creator rewards,
* skill rankings,
* character builds.

Do not implement this during early development.

Architecture should merely avoid making it impossible later.

---

## Future Node — Frontend

Eventually users should visually observe debates.

Possible features:

* live transcript,
* round indicators,
* evidence cards,
* score changes,
* claim graphs,
* character builder,
* drag-and-drop skills,
* debate history.

The backend must work first.

Do not place core debate logic in frontend code.

---

# 4. Node 1 Architecture

Node 1 should initially contain concepts similar to:

```text
DebateEngine
│
├── DebateState
├── Debater
│   ├── Debater A
│   └── Debater B
├── ResearchService
├── ClaimTracker
├── Judge
└── DebateResult
```

The precise class/module design is something we should discuss before committing to it.

Do not assume these must each be classes.

Choose the simplest understandable architecture.

---

# 5. Separation of Responsibilities

Maintain strict boundaries.

### DebateEngine

Coordinates the debate.

It should not contain every subsystem's implementation.

### Debater

Generates debate behavior for an assigned position.

It should not know how the entire application works.

### ResearchService

Retrieves research.

It should not score debates.

### ClaimTracker

Tracks important factual/argument claims.

It should not control rounds.

### Judge

Evaluates completed debate state.

It should not orchestrate the debate.

### DebateResult

Represents structured final output.

It should not contain orchestration logic.

---

# 6. Debate Flow

The initial conceptual flow is:

```text
User Input
    ↓
Create DebateState
    ↓
Round 1
    ↓
Debater A
    ↓
Record Message
    ↓
Debater B
    ↓
Record Message
    ↓
Extract Claims
    ↓
Research Phase
    ↓
Record Research
    ↓
Next Round
    ↓
Repeat
    ↓
Judge
    ↓
DebateResult
```

Use deterministic **rounds**, not wall-clock debate time.

A frontend may eventually display something such as a "10 minute debate," but the backend should reason in turns and rounds.

---

# 7. Collaboration Protocol

THIS IS IMPORTANT.

Do not behave like:

> User gives specification → agent disappears → giant application appears.

Development should be conversational.

For every major component use this cycle:

```text
DISCUSS
   ↓
DESIGN
   ↓
REVIEW WITH DEVELOPER
   ↓
IMPLEMENT SMALL PIECE
   ↓
TEST
   ↓
EXPLAIN RESULT
   ↓
REVIEW WITH DEVELOPER
   ↓
CONTINUE
```

Before implementing a major subsystem:

1. Explain what problem we are solving.
2. Show where the component sits in the node architecture.
3. Describe its proposed inputs.
4. Describe its proposed outputs.
5. Explain important design choices.
6. Mention meaningful alternatives.
7. Identify likely future extension points.
8. Identify potential coupling or technical debt.
9. Ask for developer feedback when the decision materially affects architecture.

For small implementation details, use judgment and continue without unnecessary interruptions.

---

# 8. Review Gates

Do NOT cross major architectural boundaries silently.

Stop for discussion before:

* introducing a major dependency,
* changing node boundaries,
* changing public interfaces,
* changing persistent data formats,
* selecting an LLM provider abstraction,
* choosing database architecture,
* introducing async/concurrency,
* implementing character architecture,
* implementing skills,
* implementing authentication,
* implementing marketplace functionality,
* beginning the frontend,
* significantly restructuring existing modules.

Small bug fixes, tests, formatting changes, and obvious implementation details do not require a review gate.

---

# 9. Teach While Building

I want to understand this codebase.

When completing a meaningful component, explain:

### What we added

A short description.

### Where it sits

Show its place inside the node architecture.

### Why it exists

Explain what problem it solves.

### Important code path

Explain the execution flow.

### Design decisions

Explain why this implementation was chosen.

### Extension point

Explain how future nodes could connect to it.

### What I should understand

Identify the most important concepts for me to understand before continuing.

Do not overwhelm me with explanations of trivial syntax unless I ask.

---

# 10. Node Tags in Code

Major modules and major internal sections should identify where they belong architecturally.

Do NOT comment every line.

Use meaningful module docstrings / section comments.

Example:

```python
"""
NODE: Debate Engine
COMPONENT: Debate State

PURPOSE:
Stores all mutable state belonging to one debate session.

INPUTS:
Debate configuration and messages.

OUTPUTS:
Structured state consumed by debaters, research services,
claim tracking, and the judge.
"""
```

For important sections:

```python
# NODE 1 / ROUND ORCHESTRATION
```

or:

```python
# NODE 1 / RESEARCH INTERFACE
```

Do not create noisy comments simply to satisfy this rule.

The purpose is **architectural traceability**.

---

# 11. Documentation Structure

Create persistent repository documentation.

Recommended starting structure:

```text
project/
│
├── AGENTS.md
├── README.md
├── ARCHITECTURE.md
│
├── docs/
│   ├── PROJECT_VISION.md
│   ├── NODE_MAP.md
│   │
│   ├── design/
│   │   └── node-01-debate-engine.md
│   │
│   ├── decisions/
│   │
│   └── plans/
│       ├── active/
│       └── completed/
│
├── src/
│
└── tests/
```

`AGENTS.md` should remain concise.

It should tell future coding agents:

* what this project is,
* how the architecture works,
* where documentation lives,
* how review gates work,
* how tests should be run,
* and what development principles must be followed.

Do NOT turn `AGENTS.md` into an enormous project encyclopedia.

Deeper information belongs in `docs/`.

---

# 12. Architecture Documentation

Maintain:

## ARCHITECTURE.md

High-level system architecture.

## docs/NODE_MAP.md

Current node tree.

Example:

```text
Application
│
└── Node 1: Debate Engine [ACTIVE]
    ├── DebateState
    ├── Debater
    ├── ResearchService
    ├── ClaimTracker
    ├── Judge
    └── DebateResult

Future
├── Research Engine
├── Argument Graph
├── Characters
├── Skills
├── Community
├── Marketplace
└── Frontend
```

Update this as architecture evolves.

---

# 13. Decision Records

Important architectural decisions should not disappear into conversation history.

For significant decisions create a short decision record in:

```text
docs/decisions/
```

For example:

```text
001-rounds-instead-of-wall-clock-time.md
002-research-service-interface.md
003-model-provider-abstraction.md
```

Include:

```text
Problem
Options considered
Decision
Reason
Consequences
```

This allows future agents and the developer to understand **why** the code looks the way it does.

---

# 14. Execution Plans

For substantial work, create an active plan:

```text
docs/plans/active/
```

It should contain:

* goal,
* scope,
* affected node,
* proposed changes,
* progress,
* decisions,
* tests,
* unresolved questions.

Once completed, move it to:

```text
docs/plans/completed/
```

Do not create elaborate plans for trivial changes.

---

# 15. Git Workflow

Initialize a Git repository.

If GitHub CLI is installed and authenticated, create a **PRIVATE GitHub repository**.

Do not create a public repository.

Before executing GitHub creation, show me:

```text
Repository name:
Repository description:
Visibility: PRIVATE
Initial branch:
```

Then allow me to review it.

Suggested command after approval:

```bash
gh repo create <repo-name> --private --source=. --remote=origin --push
```

Never change repository visibility without explicit developer approval.

---

# 16. Git Discipline

Use small meaningful commits.

Prefer commits corresponding to coherent pieces such as:

```text
docs: establish project architecture
feat: add debate state model
feat: add debater interface
feat: implement round orchestration
test: cover debate round progression
```

Do not dump the entire Node 1 implementation into one enormous commit.

Do not rewrite unrelated code while implementing a feature.

---

# 17. Testing

Each component should have useful tests.

At minimum test:

* state transitions,
* round progression,
* message ordering,
* invalid inputs,
* scoring structures,
* research interface behavior,
* model-provider boundaries.

External model calls should be mockable.

We should be able to test Node 1 without spending API tokens for every unit test.

---

# 18. Model Provider Independence

Avoid tightly coupling Node 1 to OpenAI or any other provider.

Eventually we may experiment with:

* OpenAI models,
* local Hugging Face models,
* other hosted models,
* different models for different agents.

Design an interface boundary.

Do not build an overly complicated provider system yet.

We only need enough abstraction that replacing the provider does not require rewriting DebateEngine.

---

# 19. Safety and Experimental Scope

The application is intended as a debate/research environment.

Users may assign controversial, offensive, extremist, political, religious, philosophical, scientific, or otherwise adversarial viewpoints to debate agents.

The orchestration layer should distinguish:

```text
position being represented
```

from:

```text
system endorsement of that position
```

However, individual model providers may have their own restrictions.

Provider behavior should therefore remain separate from the application's debate architecture.

Do not attempt to circumvent provider safeguards.

---

# 20. Node 1 Definition of Done

Node 1 is complete when I can run the application from a terminal and perform something resembling:

```text
Topic:
Nuclear energy vs renewable-only energy policy

Position A:
Support expanded nuclear energy.

Position B:
Support renewable-only energy.

Rounds:
4
```

The system should:

```text
initialize debate
↓
run structured rounds
↓
record messages
↓
perform research
↓
record evidence
↓
track basic claims
↓
evaluate with judge
↓
produce structured report
```

The report should contain:

* winner,
* overall scores,
* scoring categories,
* judge explanation,
* important claims,
* important sources,
* contradictions,
* unsupported claims,
* strongest arguments.

This must work before building the graphical interface.

---

# 21. First Task

DO NOT START IMPLEMENTING THE FULL DEBATE ENGINE.

Begin with project initialization.

### Step 1

Inspect the local development environment.

Determine:

* current directory,
* Git status,
* Python version,
* available package managers,
* whether GitHub CLI is installed,
* whether GitHub CLI is authenticated.

Do not expose credentials or tokens.

### Step 2

Propose:

* project name,
* Python package structure,
* dependency-management approach,
* testing framework,
* repository structure.

Explain your reasoning.

### Step 3

Show me the proposed initial tree.

### Step 4

Discuss it with me.

### Step 5

After we agree, initialize:

* project,
* Git repository,
* documentation structure,
* `AGENTS.md`,
* test infrastructure.

### Step 6

Show me what was created and explain each major file.

### Step 7

Prepare the private GitHub repository configuration and review it with me before creation.

### Step 8

Only after project bootstrap is complete should we begin designing the first actual Node 1 component.

The first implementation component will likely be:

```text
DebateState
```

but discuss that decision before implementing it.

---

# Primary Rule

When uncertain between:

```text
doing more automatically
```

and:

```text
making the architecture understandable and discussing an important decision
```

prefer the second.

I want an engineering collaboration, not one-shot code generation.

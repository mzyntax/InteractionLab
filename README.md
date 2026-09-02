# Model Battlegrounds

Model Battlegrounds is a modular AI experimentation platform centered on structured,
multi-round debates. The backend is being developed as independently testable
nodes, beginning with the Debate Engine.

Node 1 is under incremental development. Stable debater briefs and the
structural debate state are implemented, along with deterministic normal round
orchestration, a provider-independent Debater contract, and deterministic prompt
construction. A provider-independent text-generation contract is also implemented;
the Model Debater now connects these pieces into unaccepted statement proposals.
The synchronous Debate Runner connects two configured debaters to deterministic
orchestration and returns a completed debate record. The first concrete adapter
can call configurable OpenAI-compatible Chat Completions endpoints. Provider
selection is explicit in the initial interactive CLI.

## Run a debate

Set an API key for either side that needs one. Unset keys are supported for local
or otherwise unauthenticated endpoints.

```bash
export POLAR_DEBATE_A_API_KEY="..."
export POLAR_DEBATE_B_API_KEY="..."
uv run model-battlegrounds
```

The CLI asks for the topic, positions, rounds, and independent endpoint and model
values for Debaters A and B. API keys are read only from the environment and are
not displayed. The initial transcript is printed after the debate completes.

## Development

Requires Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

Read `docs/PROJECT_VISION.md` for the product vision and `ARCHITECTURE.md` for
the current system boundaries.

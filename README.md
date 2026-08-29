# Model Battlegrounds

Model Battlegrounds is a modular AI experimentation platform centered on structured,
multi-round debates. The backend is being developed as independently testable
nodes, beginning with the Debate Engine.

Node 1 is under incremental development. Stable debater briefs and the
structural debate state are implemented, along with deterministic normal round
orchestration and a provider-independent Debater contract. Model integration
does not yet exist.

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

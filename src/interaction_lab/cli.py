"""
APPLICATION BOUNDARY: Command-Line Interface

PURPOSE:
Collects simple debate and model-connection inputs, assembles existing application
components, runs the debate, and presents its completed transcript.

INPUTS:
Interactive terminal values and optional API keys from the process environment.

OUTPUTS:
A readable completed debate transcript written to the terminal.

RELATIONSHIPS:
This boundary configures the Debate Engine and provider adapters but owns no turn
rules, prompt construction, model transport, or source ingestion behavior.
"""

import os
import sys
from collections.abc import Callable, Mapping

from interaction_lab.debate_engine import (
    DebateConfig,
    DebaterBrief,
    DebaterSetup,
    DebaterSide,
    DebateState,
    GenerationSettings,
    ModelDebater,
    run_debate,
)
from interaction_lab.model_providers import (
    OpenAICompatibleError,
    OpenAICompatibleTextGenerator,
)

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]

_GENERATION_SETTINGS = GenerationSettings(temperature=0.7, max_output_tokens=600)


def _read_required(label: str, input_function: InputFunction) -> str:
    """Read and normalize one required terminal value."""
    value = input_function(f"{label}: ").strip()
    if not value:
        raise ValueError(f"{label.lower()} must not be empty")
    return value


def _read_rounds(input_function: InputFunction) -> int:
    """Read a positive deterministic round count."""
    value = _read_required("Rounds", input_function)
    try:
        rounds = int(value)
    except ValueError as error:
        raise ValueError("rounds must be an integer") from error
    if rounds < 1:
        raise ValueError("rounds must be at least 1")
    return rounds


def _brief_for(position: str) -> DebaterBrief:
    """Create the visible baseline assignment used by the first CLI milestone."""
    return DebaterBrief(
        assigned_position=position,
        core_commitments=("Represent the assigned position faithfully",),
        allowed_flexibility="Concede well-supported details without abandoning the position",
        debate_objective="Present the strongest evidence-bounded case for the position",
    )


def _optional_api_key(environment: Mapping[str, str], name: str) -> str | None:
    """Return a configured secret while treating missing or blank values as absent."""
    value = environment.get(name)
    if value is None or not value.strip():
        return None
    return value


def _render_transcript(state: DebateState) -> str:
    """Format the authoritative transcript without adding debate interpretation."""
    sections = [f"Debate complete: {state.config.topic}"]
    for statement in state.statements:
        heading = f"Round {statement.round_number} — Debater {statement.speaker.value.upper()}"
        sections.append(f"[{heading}]\n{statement.content}")
    return "\n\n".join(sections)


def run_cli(
    input_function: InputFunction = input,
    output_function: OutputFunction = print,
    environment: Mapping[str, str] | None = None,
) -> DebateState:
    """Collect one debate, run it synchronously, and print its final transcript."""
    active_environment = os.environ if environment is None else environment

    topic = _read_required("Topic", input_function)
    position_a = _read_required("Position A", input_function)
    position_b = _read_required("Position B", input_function)
    rounds = _read_rounds(input_function)
    endpoint_a = _read_required("Debater A endpoint", input_function)
    model_a = _read_required("Debater A model", input_function)
    endpoint_b = _read_required("Debater B endpoint", input_function)
    model_b = _read_required("Debater B model", input_function)

    config = DebateConfig(
        topic=topic,
        debater_a=_brief_for(position_a),
        debater_b=_brief_for(position_b),
        total_rounds=rounds,
    )
    state = DebateState.start(config)
    debater_a = ModelDebater(
        setup=DebaterSetup.from_config(config, DebaterSide.A),
        text_generator=OpenAICompatibleTextGenerator(
            base_url=endpoint_a,
            model=model_a,
            api_key=_optional_api_key(active_environment, "INTERACTIONLAB_A_API_KEY"),
        ),
        generation_settings=_GENERATION_SETTINGS,
    )
    debater_b = ModelDebater(
        setup=DebaterSetup.from_config(config, DebaterSide.B),
        text_generator=OpenAICompatibleTextGenerator(
            base_url=endpoint_b,
            model=model_b,
            api_key=_optional_api_key(active_environment, "INTERACTIONLAB_B_API_KEY"),
        ),
        generation_settings=_GENERATION_SETTINGS,
    )

    output_function("Running debate...")
    completed = run_debate(state, debater_a, debater_b)
    output_function(_render_transcript(completed))
    return completed


def main() -> int:
    """Run the terminal application and translate expected failures to exit codes."""
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\nDebate cancelled.", file=sys.stderr)
        return 130
    except (EOFError, ValueError, OpenAICompatibleError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0

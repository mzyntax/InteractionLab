"""
NODE: Debate Engine
COMPONENT: Model Debater

PURPOSE:
Applies one debater's identity and current public context to an injected text
generator, producing a statement proposal for deterministic orchestration.

INPUTS:
Stable ``DebaterSetup``, a ``TextGenerator``, ``GenerationSettings``, and the
current ``TurnContext``.

OUTPUTS:
An unaccepted ``ProposedStatement`` containing the model's generated text.

RELATIONSHIPS:
The Debate Prompt Builder creates the model-facing instructions. The injected
Text Generator performs generation. The Turn Orchestrator decides whether the
returned proposal may enter the Debate Record.
"""

from dataclasses import dataclass

from polar_debate.debate_engine.debate_prompt_builder import build_debate_prompt
from polar_debate.debate_engine.debater_turn_contract import (
    DebaterSetup,
    ProposedStatement,
    TurnContext,
)
from polar_debate.debate_engine.text_generation_contract import (
    GenerationSettings,
    TextGenerator,
)


@dataclass(frozen=True, slots=True)
class ModelDebater:
    """Use an injected model connection while carrying one stable debate identity."""

    setup: DebaterSetup
    text_generator: TextGenerator
    generation_settings: GenerationSettings

    def propose_statement(self, context: TurnContext) -> ProposedStatement:
        """Generate one completed argument without accepting or recording it."""
        prompt = build_debate_prompt(self.setup, context)
        response_text = self.text_generator.generate(
            prompt.render(),
            self.generation_settings,
        )
        return ProposedStatement(content=response_text)

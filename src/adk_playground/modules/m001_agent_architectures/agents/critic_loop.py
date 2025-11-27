from typing import Any

from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools.tool_context import ToolContext

from adk_playground.core.settings import MODEL

# Pattern: Loop (writer ↔ critic) with an explicit stop via ToolContext escalation

COMPLETION_PHRASE = "No major issues found."


def exit_loop(tool_context: ToolContext) -> dict[str, Any]:
    tool_context.actions.escalate = True
    return {}


def build_agent():
    # 1) Initial draft (runs once before the loop)
    initial_writer = Agent(
        name="initial_writer",
        model=MODEL,
        description="Creates the first short draft.",
        instruction=(
            "Write a short, 3–5 sentence draft strictly about the user's topic. "
            "Keep it concise and factual."
        ),
        output_key="current_doc",
    )

    # 2a) Critic (inside the loop)
    critic = Agent(
        name="critic",
        model=MODEL,
        description="Reviews the current draft and either suggests fixes or says it's good.",
        instruction=(
            "Review the draft:\n{current_doc}\n\n"
            f"If it is already acceptable, reply EXACTLY with '{COMPLETION_PHRASE}'. "
            "Otherwise, list 2–3 concrete improvements."
        ),
        output_key="critique",
    )

    # 2b) Refiner (inside the loop) - can trigger loop exit - function `exit_loop`
    refiner = Agent(
        name="refiner",
        model=MODEL,
        description="Applies critique; if none needed, triggers exit.",
        instruction=(
            f"If the critique equals '{COMPLETION_PHRASE}', call the tool 'exit_loop' to stop. "
            "Else, rewrite the draft applying the critique and store it to {current_doc}."
        ),
        tools=[exit_loop],
        output_key="current_doc",
    )

    # Loop performs: critic → refiner (repeat) up to N iterations or until exit tool escalates
    refinement_loop = LoopAgent(
        name="refinement_loop",
        sub_agents=[critic, refiner],
        max_iterations=4,
    )

    # Finalizer after the loop to produce the final_output for the CLI/Web
    finalizer = Agent(
        name="finalizer",
        model=MODEL,
        description="Returns the final version for the user.",
        instruction="Return the latest draft found in {current_doc} as the final answer.",
        output_key="final_output",
    )

    # Orchestrate: initial_writer → refinement_loop → finalizer
    root = SequentialAgent(
        name="writer_critic_pipeline",
        sub_agents=[initial_writer, refinement_loop, finalizer],
        description="Iterative improvement loop followed by finalization.",
    )
    return root

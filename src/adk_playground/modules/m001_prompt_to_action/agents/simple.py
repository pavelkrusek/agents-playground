from google.adk.agents import Agent
from google.adk.runners import Runner

from adk_playground.core.settings import MODEL


def build_agent() -> Agent:
    return Agent(
        name="action_agent",
        model=MODEL,
        instruction=(
            "You are a helpful assistant. Understand the user's request and produce a direct, high-quality answer."
            "If the request is open-ended, produce the content directly."
        ),
        output_key="final_output",
    )


def build_runner() -> Runner:
    pass

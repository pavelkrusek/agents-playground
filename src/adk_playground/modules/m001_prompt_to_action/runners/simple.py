from google.adk.agents import Agent
from google.adk.runners import Runner, InMemoryRunner

from adk_playground.core.settings import MODEL


def build_runner() -> Runner:
    action_agent = Agent(
        name="action_agent",
        model=MODEL,
        instruction=(
            "You are a helpful assistant. Understand the user's request and produce a direct, high-quality answer. "
            "If the request is open-ended, produce the content directly."
        ),
        output_key="final_output",
    )
    runner = InMemoryRunner(agent=action_agent)
    return runner

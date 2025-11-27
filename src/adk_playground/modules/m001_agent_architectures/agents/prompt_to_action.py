from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.tools import google_search

from adk_playground.core.settings import MODEL


def build_agent() -> Agent:
    return Agent(
        name="action_agent",
        model=MODEL,
        description="A simple agent that can answer general questions.",
        instruction=(
            "You are a helpful assistant. Understand the user's request and produce a direct, high-quality answer."
            "If the request is open-ended, produce the content directly."
            "Use Google Search for current info or if unsure."
        ),
        tools=[google_search],
        output_key="final_output",
    )


def build_runner() -> Runner:
    pass

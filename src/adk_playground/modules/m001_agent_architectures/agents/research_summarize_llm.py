from google.adk import Agent
from google.adk.tools import AgentTool, google_search

from adk_playground.core.settings import MODEL


# Multi-agent pattern: Manager delegates to workers via AgentTool.
# based on LLM instructions to control the order - sometimes be unpredictable
def build_agent() -> Agent:
    # Specialists
    researcher = Agent(
        name="researcher",
        model=MODEL,
        description="Finds facts and organizes notes.",
        instruction=(
            """
            You are a research specialist. Extract key facts, figures, and brief references.
            Your only job is to use the google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.
            Return a concise bullet-point research memo.
            """
        ),
        tools=[google_search],
        output_key="research_notes",
    )

    summarizer = Agent(
        name="summarizer",
        model=MODEL,
        description="Writes a clear, short summary from research notes.",
        instruction=(
            """
            Write a clear, short summary for the user using {research_notes}.
            Focus on correctness and brevity. Return the final answer.
            """
        ),
        output_key="final_output",
    )

    # Manager (coordinator) that can call sub-agents as tools
    coordinator = Agent(
        name="coordinator",
        model=MODEL,
        description="Plans and delegates the workflow to specialists.",
        instruction=(
            """
            Plan the workflow. Usually call 'researcher' first to gather notes,
            then call 'summarizer' to produce the final answer.
            If research seems unnecessary, you may call 'summarizer' directly.
            Always finish by calling 'summarizer'.
            """
        ),
        tools=[AgentTool(agent=researcher), AgentTool(agent=summarizer)],
        output_key="final_output",
    )
    return coordinator

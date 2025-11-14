from google.adk.agents import Agent, SequentialAgent

from adk_playground.core.settings import MODEL


def build_agent():
    research = Agent(
        name="research_stage",
        model=MODEL,
        description="Always runs first.",
        instruction=(
            "Research the topic. Produce a compact bullet memo with facts and pointers. "
            "Keep it 5-8 bullets, no fluff."
        ),
        output_key="research_notes",
    )

    summarize = Agent(
        name="summarize_stage",
        model=MODEL,
        description="Always runs second.",
        instruction=(
            "Using the memo {research_notes}, write a clean, concise summary for the user. "
            "Return only the final answer."
        ),
        output_key="final_output",
    )

    # Guaranteed order: research -> summarize
    pipeline = SequentialAgent(
        name="research_then_summarize",
        sub_agents=[research, summarize],
        description="Deterministic two-step pipeline."
    )
    return pipeline

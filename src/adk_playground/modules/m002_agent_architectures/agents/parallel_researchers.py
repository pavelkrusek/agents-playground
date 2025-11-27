from google.adk.agents import Agent, ParallelAgent, SequentialAgent

from adk_playground.core.settings import MODEL


# Three independent researchers in parallel → aggregator in sequence.
def build_agent():
    # Independent researchers (run concurrently)
    r_sources = Agent(
        name="researcher_sources",
        model=MODEL,
        description="Collects key sources and brief quotes.",
        instruction=(
            "Find 3–5 high-quality sources and extract 1–2 key points from each. "
            "Return a compact, deduplicated bullet memo with short attributions."
        ),
        output_key="notes_sources",
    )

    r_stats = Agent(
        name="researcher_stats",
        model=MODEL,
        description="Finds numbers, dates, and concrete facts.",
        instruction=(
            "List 5–8 concrete facts (numbers/dates/names) relevant to the topic. "
            "Be precise and avoid duplication."
        ),
        output_key="notes_stats",
    )

    r_context = Agent(
        name="researcher_context",
        model=MODEL,
        description="Adds background and counterpoints.",
        instruction=(
            "Provide 3–5 context bullets: historical background, counter-arguments, and caveats. "
            "Keep each bullet under 20 words."
        ),
        output_key="notes_context",
    )

    parallel_team = ParallelAgent(
        name="independent_researchers",
        sub_agents=[r_sources, r_stats, r_context],
        description="Runs three specialists in parallel to gather complementary notes.",
    )

    aggregator = Agent(
        name="aggregator",
        model=MODEL,
        description="Merges parallel notes into one brief.",
        instruction=(
            "Merge {notes_sources}, {notes_stats}, and {notes_context} into a single 8–12 bullet brief. "
            "Deduplicate, keep strongest items, and ensure a clear structure (Sources / Facts / Context). "
            "Finish with a 2-sentence takeaway. Return only the final brief."
        ),
        output_key="final_output",
    )

    # Deterministic pipeline: parallel → aggregate
    return SequentialAgent(
        name="parallel_researchers_pipeline",
        sub_agents=[parallel_team, aggregator],
        description="Parallel research followed by a single aggregation step.",
    )

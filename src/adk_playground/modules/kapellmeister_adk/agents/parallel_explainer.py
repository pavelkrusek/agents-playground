from __future__ import annotations

from google.adk.agents import Agent, ParallelAgent, SequentialAgent

from adk_playground.core.mcp import get_mcp_tools
from adk_playground.core.settings import MODEL


def build_agent() -> SequentialAgent:
    """
    Kapellmeister pipeline:

    1) Wikidata + Wikipedia researchers in parallel  → notes_wikidata / notes_wikipedia
    2) Aggregator merges both into a concert-program style explanation.
    """

    # --- Wikidata researcher: facts via Wikidata MCP ---
    wikidata_researcher = Agent(
        name="kapellmeister_wikidata_researcher",
        model=MODEL,
        tools=get_mcp_tools(),
        description="Uses Wikidata MCP to fetch structured facts about composers and works.",
        instruction=(
            "You are a Wikidata-based researcher for classical music.\n"
            "For the user's question (composer or work):\n"
            "- Use Wikidata MCP tools such as search_entities and get_entity.\n"
            "- Find the best matching entity.\n"
            "- Extract hard facts: full name, birth/death dates, nationality, roles, "
            "  style/period, work type, key, opus/catalogue numbers, and 2–4 notable works if applicable.\n"
            "- Return a compact factual note (5–10 sentences max), no markdown.\n"
            "- Do NOT mention tools or MCP; just state the facts.\n"
        ),
        output_key="notes_wikidata",
    )

    # --- Wikipedia researcher: narrative via Wikipedia MCP ---
    wikipedia_researcher = Agent(
        name="kapellmeister_wikipedia_researcher",
        model=MODEL,
        tools=get_mcp_tools(),
        description="Uses Wikipedia MCP to fetch narrative context and listening guidance.",
        instruction=(
            "You are a Wikipedia-based researcher for classical music.\n"
            "For the user's question (composer or work):\n"
            "- Use Wikipedia MCP tools such as search_wikipedia and get_article or get_summary.\n"
            "- Focus on narrative aspects: historical context, why the composer/work is important, "
            "  how it sounds, any famous movements, and reception.\n"
            "- Return 1–3 short paragraphs, no markdown, aimed at a concert audience.\n"
            "- Do NOT mention tools, MCP, or Wikipedia itself; just explain.\n"
        ),
        output_key="notes_wikipedia",
    )

    parallel_team = ParallelAgent(
        name="kapellmeister_parallel_researchers",
        sub_agents=[wikidata_researcher, wikipedia_researcher],
        description="Runs Wikidata and Wikipedia researchers in parallel on the same musical question.",
    )

    # --- Aggregator ---
    aggregator = Agent(
        name="kapellmeister_aggregator",
        model=MODEL,
        description="Merges Wikidata and Wikipedia notes into a single concert-program style explanation.",
        instruction=(
            "You receive two note fields from the session state about the SAME musical topic:\n"
            "- {notes_wikidata}\n"
            "- {notes_wikipedia}\n\n"
            "Task:\n"
            "- Read both carefully.\n"
            "- Merge them into a single, coherent answer written like a concert program note.\n"
            "- Length: usually 1–3 short paragraphs.\n"
            "- Use Wikidata notes mainly for precise facts (names, dates, opus/catalogue numbers).\n"
            "- Use Wikipedia notes mainly for story, context, and listening guidance.\n"
            "- Remove duplication and keep only the strongest, most relevant points.\n"
            "- If they disagree, use cautious wording (e.g. 'around 1904', 'most likely composed between …').\n"
            "- Do NOT mention Wikidata, Wikipedia, MCP, tools, or agents explicitly.\n"
            "- Speak directly to the listener in clear English.\n"
        ),
        output_key="final_output",
    )

    return SequentialAgent(
        name="kapellmeister_parallel_pipeline",
        sub_agents=[parallel_team, aggregator],
        description="Parallel Wikidata/Wikipedia research followed by aggregation.",
    )

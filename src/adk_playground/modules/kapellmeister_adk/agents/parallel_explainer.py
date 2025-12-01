from __future__ import annotations

from google.adk.agents import Agent, ParallelAgent, SequentialAgent

from adk_playground.core.mcp import get_mcp_tools
from adk_playground.core.settings import MODEL


def build_agent() -> SequentialAgent:
    """
    Kapellmeister pipeline:

    - Wikidata chain = search → details (sequential)
    - Wikipedia researcher
    - Both run in parallel
    - Aggregator merges into concert-program style note
    """

    # --- Wikidata chain: 1) search_entity (one call) ---
    wikidata_search = Agent(
        name="kapellmeister_wikidata_search",
        model=MODEL,
        tools=get_mcp_tools(),
        description="Finds the best Wikidata entity ID for the given musical query.",
        instruction=(
            "You are a strict Wikidata search agent.\n"
            "TOOL RULES (MANDATORY):\n"
            "- You MUST call the 'search_entities' tool EXACTLY ONCE.\n"
            "- You MUST NOT call any other tools.\n\n"
            "Use search_entities with the name from the user's question "
            "(composer or work title).\n"
            "Take the single best matching entity and output ONLY its ID "
            "(e.g. 'Q1151') as plain text, no explanation, no extra words."
        ),
        output_key="wikidata_entity_id",
    )

    # --- Wikidata chain: 2) get_entity (one call, fixed properties) ---
    wikidata_details = Agent(
        name="kapellmeister_wikidata_details",
        model=MODEL,
        tools=get_mcp_tools(),
        description="Fetches structured facts from Wikidata for a known entity ID.",
        instruction=(
            "You receive a Wikidata entity id in {wikidata_entity_id}.\n\n"
            "TOOL RULES (MANDATORY):\n"
            "- You MUST call the 'get_entity' tool EXACTLY ONCE.\n"
            "- Call it with that id and a SMALL, FIXED set of properties, for example:\n"
            "  ['P569','P570','P106','P136','P27','P31']. \n"
            "- After that single get_entity call, you MUST NOT call any tools again.\n\n"
            "From the tool result, write a compact factual note (5–8 sentences) about "
            "the composer or work: full name, birth/death dates, nationality, roles, "
            "style/period and 2–3 notable works if applicable.\n"
            "Return plain text, no markdown, and do NOT mention tools or MCP."
        ),
        output_key="notes_wikidata",
    )

    wikidata_chain = SequentialAgent(
        name="kapellmeister_wikidata_chain",
        sub_agents=[wikidata_search, wikidata_details],
        description="Sequential Wikidata chain: search entity → fetch details.",
    )

    # --- Wikipedia researcher ---
    wikipedia_researcher = Agent(
        name="kapellmeister_wikipedia_researcher",
        model=MODEL,
        tools=get_mcp_tools(),
        description="Uses Wikipedia MCP to fetch narrative context and listening guidance.",
        instruction=(
            "You are a Wikipedia-based researcher for classical music.\n"
            "For the user's question (composer or work):\n"
            "- Use Wikipedia MCP tools such as search_wikipedia and get_summary or get_article.\n"
            "- Focus on narrative aspects: historical context, why the composer/work is important, "
            "  how it sounds, any famous movements, and reception.\n"
            "- Return 1–3 short paragraphs, no markdown, aimed at a concert audience.\n"
            "- Do NOT mention tools, MCP, or Wikipedia itself; just explain.\n"
        ),
        output_key="notes_wikipedia",
    )

    parallel_team = ParallelAgent(
        name="kapellmeister_parallel_researchers",
        sub_agents=[wikidata_chain, wikipedia_researcher],
        description="Runs Wikidata (search+details) and Wikipedia researchers in parallel.",
    )

    # --- Aggregator uses context variables from both branches ---
    aggregator = Agent(
        name="kapellmeister_aggregator",
        model=MODEL,
        description="Merges Wikidata and Wikipedia notes into a single concert-program style explanation.",
        instruction=(
            "You receive two note fields from the session state about the SAME musical topic:\n"
            "- {notes_wikidata}\n"
            "- {notes_wikipedia}\n\n"
            "Task:\n"
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

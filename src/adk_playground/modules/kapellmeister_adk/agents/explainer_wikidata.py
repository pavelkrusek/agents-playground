from __future__ import annotations

from google.adk.agents import Agent

from adk_playground.core.mcp import get_mcp_tools
from adk_playground.core.settings import MODEL  # nebo odkud bereš MODEL teď


def build_agent() -> Agent:
    """
    Very simple Kapellmeister agent that talks to a single Wikidata MCP server.

    Goal: try MCP – no fancy orchestration, just:
      - one search call
      - optional one detail call
      - then answer.
    """
    return Agent(
        name="kapellmeister_explainer_wikidata",
        description=(
            "Explain classical composers and works using Wikidata via MCP."
            "Answers basic questions about composers using Wikidata tools."
        ),
        model=MODEL,
        tools=get_mcp_tools(),
        instruction=(
            "You are Kapellmeister, a simple classical-music explainer.\n\n"
            "You have access to ONE MCP server (Wikidata). That server exposes "
            "multiple TOOLS such as 'search_entities' and 'get_entity'.\n\n"

            "TOOL USAGE RULES (VERY IMPORTANT):\n"
            "- Per user question you may call at most:\n"
            "  * 1x search_entities\n"
            "  * 1x get_entity\n"
            "- Never call the same tool twice in a row with the same arguments.\n"
            "- Never try to 'fix' results by repeating tool calls in a loop.\n"
            "- After you have called get_entity once, STOP using tools and "
            "  write the answer in natural language.\n"
            "- If search_entities returns no good result, say you couldn't find "
            "  a reliable Wikidata match and answer briefly from general knowledge.\n\n"

            "FLOW FOR A QUESTION LIKE 'Who was Mahler?':\n"
            "1) Call search_entities to find the best matching entity.\n"
            "2) Take the top result (e.g. Gustav Mahler) and call get_entity once.\n"
            "3) From that, extract: birth/death, nationality, profession, period, "
            "   a couple of notable works.\n"
            "4) Stop calling tools and answer in 1–3 short paragraphs.\n\n"

            "STYLE:\n"
            "- Be concise and friendly.\n"
            "- Don't show raw JSON or tool internals.\n"
            "- Just give a clear explanation based on the data you fetched.\n"
        ),
    )

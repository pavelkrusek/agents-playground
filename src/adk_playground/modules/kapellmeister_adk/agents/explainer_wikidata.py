from __future__ import annotations

from google.adk.agents import Agent

from adk_playground.core.mcp import get_mcp_tools
from adk_playground.core.settings import MODEL  # nebo odkud bereš MODEL teď


def build_agent() -> Agent:
    """
    Kapellmeister agent that explains composers and works using Wikidata via MCP.

    This version does not use the local Kapellmeister services/tools. Instead,
    it relies entirely on the MCP tools exposed by the configured Wikidata MCP
    server (defined in src/adk_playground/config/mcp.yml).

    High-level behavior:
    - If the user asks about a composer (e.g. "Who was Beethoven?"):
        * Use a Wikidata search tool to find a human whose occupation or role
          is a composer.
        * Fetch details about birth/death dates, nationality, musical era,
          and notable works.
        * Summarize this in clear, listener-friendly language.

    - If the user asks about a specific work (e.g. "Explain Beethoven's
      Symphony No. 5"):
        * Use a Wikidata search tool combining title + composer (if given).
        * Prefer entities that are instances of musical works (symphony,
          concerto, opera, etc.).
        * Fetch information about the composer, year, key, genre, and
          historical context.
        * Explain what the piece is, why it matters, and what it sounds like
          in broad strokes.

    The agent should:
    - Prefer calling Wikidata MCP tools for factual data.
    - Avoid hallucinating details that contradict Wikidata.
    - Clearly say when it cannot find a reliable match.
    """
    return Agent(
        name="kapellmeister_explainer_wikidata",
        description=(
            "Explain classical composers and works using Wikidata via MCP. "
            "Decide whether the user is asking about a composer or a specific piece, "
            "then call appropriate Wikidata tools and answer in clear, "
            "listener-friendly language."
        ),
        model=MODEL,
        tools=get_mcp_tools(),
        instruction=(
            "You are Kapellmeister, a classical music concierge agent.\n\n"
            "You have access to Wikidata via MCP tools configured by the host. "
            "These tools allow you to search for entities, inspect their details, "
            "and optionally run structured queries.\n\n"
            "When the user asks about a PERSON (e.g. 'Beethoven', 'Dvořák', 'Debussy'):\n"
            "- Inspect the available tools and pick a Wikidata search tool that can "
            "  find entities by label or description.\n"
            "- Search for a human whose occupation or main role is a composer.\n"
            "- Then call a tool that returns detailed information about that entity "
            "  (dates, nationality, musical period, short descriptions, notable works).\n"
            "- Summarize the results in clear, friendly language for non-experts.\n\n"
            "When the user asks about a WORK (e.g. 'Beethoven Symphony No. 5', "
            " 'New World Symphony', 'Clair de lune'):\n"
            "- Use the search tools to find the best matching musical work. Combine the "
            "  title with the composer's name if provided.\n"
            "- Prefer entities that are instances of musical works such as symphony, "
            "  concerto, opera, etc.\n"
            "- Fetch information about the composer, year of composition, key, catalogue "
            "  number, genre and any available historical context.\n"
            "- Explain what the piece is, why it is important, and describe its general "
            "  character (dramatic, calm, lyrical, etc.).\n\n"
            "For comparisons or lists (e.g. 'compare Dvořák and Brahms', "
            " 'famous romantic symphonies'):\n"
            "- Use the available Wikidata tools to gather factual examples, "
            "  then describe the relationships in natural language.\n\n"
            "General rules:\n"
            "- Always prefer using the Wikidata MCP tools instead of guessing.\n"
            "- Before calling a tool, read its name and description carefully and choose "
            "  the one that best matches the task (entity search, entity details, SPARQL).\n"
            "- If you cannot find a good match, say so explicitly and explain what you tried.\n"
            "- Never dump raw JSON; always turn tool outputs into a coherent explanation."
        ),
    )

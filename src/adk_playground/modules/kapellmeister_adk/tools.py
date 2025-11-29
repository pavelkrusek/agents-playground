from __future__ import annotations

from typing import Any

from google.adk.tools.tool_context import ToolContext

from kapellmeister.services.composers import get_composer_profile
from kapellmeister.services.works import get_work_facts


def get_composer_profile_tool(
        tool_context: ToolContext,
        *,
        name: str,
) -> dict[str, Any]:
    """
    Look up a classical music composer profile.

    This tool is used by the Kapellmeister agents when the user asks about a composer,
    e.g.:
      - "Who was Beethoven?"
      - "Tell me about Dvořák."
      - "What kind of music did Debussy write?"

    Parameters
    ----------
    tool_context : ToolContext
        ADK tool context. Not used in the MVP implementation, but available for
        logging, tracing, or accessing session/memory in later versions.
    name : str
        Free-form human name for the composer, for example:
        "Beethoven", "Ludwig van Beethoven", "Antonín Dvořák".

    Behavior
    --------
    - Delegates to `kapellmeister.services.composers.get_composer_profile`.
    - The service currently returns a stub profile (with a richer example for Beethoven).
    - Future versions will resolve the composer via Wikidata (MCP) or other datasources.

    Returns
    -------
    Dict[str, Any]
        A JSON-serializable dictionary with this shape:

        {
          "composer": {
            "name": str,
            "birth_year": int | None,
            "death_year": int | None,
            "nationality": str | None,
            "era": str | None,
            "tags": list[str],
          },
          "short_bio": str | None,
          "style_traits": list[str],
          "representative_works": [
            {
              "title": str,
              "genre": str | None,
              "catalogue_number": str | None,
              "key": str | None,
              "year_composed": int | None,
              "duration_min": int | None,
              "tags": list[str],
            },
            ...
          ],
        }

    Notes
    -----
    - This tool is side effect free and safe to call multiple times.
    - The output is intended to be both machine-readable (for further reasoning)
      and human-friendly (for direct explanation to the user).
    """
    profile = get_composer_profile(name)
    composer = profile.composer

    return {
        "composer": {
            "name": composer.name,
            "birth_year": composer.birth_year,
            "death_year": composer.death_year,
            "nationality": composer.nationality,
            "era": composer.epoch,
            "tags": composer.tags,
        },
        "short_bio": profile.short_bio,
        "style_traits": profile.style_traits,
        "representative_works": [
            {
                "title": w.title,
                "genre": w.genre,
                "catalogue_number": w.catalogue_number,
                "key": w.key,
                "year_composed": w.year_composed,
                "duration_min": w.duration_min,
                "tags": w.tags,
            }
            for w in profile.representative_works
        ],
    }


def get_work_facts_tool(
        tool_context: ToolContext,
        *,
        title: str,
        composer_name: str = "",
) -> dict[str, Any]:
    """
    Look up basic facts about a specific classical work.

    This tool is used by the Kapellmeister agents when the user asks about a piece,
    for example:
      - "What is Beethoven's Symphony No. 5?"
      - "Explain Dvořák's New World Symphony."
      - "Tell me about Debussy's Clair de lune."

    Parameters
    ----------
    tool_context : ToolContext
        ADK tool context. Not used in the MVP implementation, but reserved for logging,
        tracing or session-aware behavior in later versions.
    title : str
        Title or partial title of the work, such as:
        "Symphony No. 5", "Symphony No. 5 in C minor", "New World Symphony".
    composer_name : str, optional
        Optional composer name to disambiguate the work, e.g. "Beethoven" or
        "Antonín Dvořák". If omitted, the service may try to infer or treat it as
        an unknown composer, depending on the implementation.

    Behavior
    --------
    - Delegates to `kapellmeister.services.works.get_work_facts`.
    - The service currently returns a stub description, with a richer example
      for Beethoven's Symphony No. 5.
    - Future versions will fetch structured data from Wikidata (MCP) or other sources.

    Returns
    -------
    Dict[str, Any]
        A JSON-serializable dictionary with this shape:

        {
          "work": {
            "title": str,
            "composer_name": str,
            "genre": str | None,
            "catalogue_number": str | None,
            "key": str | None,
            "year_composed": int | None,
            "duration_min": int | None,
            "tags": list[str],
          },
          "program_note_short": str | None,
          "program_note_long": str | None,
          "interesting_facts": list[str],
          "difficulty_for_listener": str | None,
        }

    Notes
    -----
    - This tool is side effect free and safe to call multiple times.
    - The short and long program notes are meant to be directly quoted,
      adapted or summarized in the agent's final answer to the user.
    """
    facts = get_work_facts(title=title, composer_name=composer_name)
    w = facts.work

    return {
        "work": {
            "title": w.title,
            "composer_name": w.composer_name,
            "genre": w.genre,
            "catalogue_number": w.catalogue_number,
            "key": w.key,
            "year_composed": w.year_composed,
            "duration_min": w.duration_min,
            "tags": w.tags,
        },
        "program_note_short": facts.program_note_short,
        "program_note_long": facts.program_note_long,
        "interesting_facts": facts.interesting_facts,
        "difficulty_for_listener": facts.difficulty_for_listener,
    }

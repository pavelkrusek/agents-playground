from __future__ import annotations

from google.adk import Agent

from adk_playground.core.settings import MODEL
from adk_playground.modules.kapellmeister_adk import tools


def build_agent() -> Agent:
    """
    Root agent that can explain composers and works using Kapellmeister tools.
    """
    return Agent(
        name="kapellmeister_explainer",
        description=(
            "Explain classical composers and works. "
            "Decide whether to look up a composer or a specific piece, "
            "then answer in clear, listener-friendly language."
        ),
        model=MODEL,
        tools=[
            tools.get_composer_profile_tool,
            tools.get_work_facts_tool,
        ],
        instruction=(
            "You are Kapellmeister, a classical music concierge. "
            "If the user mentions a person like 'Beethoven' or 'Dvořák', "
            "use the composer profile tool. "
            "If the user mentions a specific piece (e.g. 'Beethoven Symphony No. 5'), "
            "use the work facts tool. "
            "Explain things in a way that is friendly to non-experts."
        ),
    )

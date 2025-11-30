from __future__ import annotations

from kapellmeister.models import Work, WorkFacts

"""
Stub service for future custom work data layer.
Currently unused — MCP/Wikidata handles data retrieval.
"""


def get_work_facts(title: str, composer_name: str | None = None) -> WorkFacts:
    work = Work(
        title="Symphony No. 5 in C minor, Op. 67",
        composer_name="Ludwig van Beethoven",
        genre="symphony",
        catalogue_number="Op. 67",
        key="C minor",
        year_composed=1808,
        duration_min=32,
        tags=["famous", "intro-friendly", "orchestral"],
    )

    program_note_short = (
        "Beethoven's Fifth Symphony is one of the most famous pieces in Western music. "
        "It opens with a short four-note motif that is developed throughout the work."
    )

    program_note_long = (
        "Beethoven's Symphony No. 5 in C minor, Op. 67, was completed in 1808. "
        "The symphony is built around the iconic four-note motif often described as "
        "“fate knocking at the door.” Across its four movements, Beethoven transforms "
        "this simple idea into a large-scale dramatic journey that moves from C minor "
        "darkness to C major triumph. The work became a symbol of resilience and has "
        "remained a central part of the orchestral repertoire."
    )

    interesting_facts = [
        "The premiere took place in Vienna in 1808 in a marathon concert.",
        "The opening motif appears in all four movements in different forms.",
        "The symphony ends in a bright and triumphant C major.",
    ]

    difficulty_for_listener = "easy"

    return WorkFacts(
        work=work,
        program_note_short=program_note_short,
        program_note_long=program_note_long,
        interesting_facts=interesting_facts,
        difficulty_for_listener=difficulty_for_listener,
    )

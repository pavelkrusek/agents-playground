from __future__ import annotations

from kapellmeister.models import Composer, ComposerProfile, Work

"""
Stub service for future custom composer data layer.
Currently unused — MCP/Wikidata handles data retrieval.
"""


def get_composer_profile(name: str) -> ComposerProfile:
    """
    MVP stub: return a generic composer profile.
    This will be replaced later by a Wikidata-backed implementation.
    """
    normalized_name = name.strip() or "Unknown composer"

    composer = Composer(
        name="Ludwig van Beethoven",
        birth_year=1770,
        death_year=1827,
        nationality="German",
        epoch="Classical / early Romantic",
        tags=["symphonic", "piano", "canonical"],
    )

    representative_works = [
        Work(
            title="Symphony No. 5 in C minor, Op. 67",
            composer_name=composer.name,
            genre="symphony",
            catalogue_number="Op. 67",
            key="C minor",
            year_composed=1808,
            duration_min=32,
            tags=["famous", "intro-friendly"],
        ),
        Work(
            title="Symphony No. 9 in D minor, Op. 125 “Choral”",
            composer_name=composer.name,
            genre="symphony",
            catalogue_number="Op. 125",
            key="D minor",
            year_composed=1824,
            duration_min=70,
            tags=["monumental", "choral"],
        ),
    ]

    short_bio = (
        "Ludwig van Beethoven (1770–1827) was a German composer who bridged the Classical "
        "and Romantic eras. His music is known for its strong motivic development, dramatic "
        "contrasts, and emotional depth. He expanded the scale and expressive range of the "
        "symphony, piano sonata, and string quartet."
    )

    style_traits = [
        "motivic development",
        "strong contrasts",
        "dramatic architecture",
        "expanded symphonic scale",
    ]

    profile = ComposerProfile(
        composer=composer,
        short_bio=short_bio,
        style_traits=style_traits,
        representative_works=representative_works,
    )

    return profile

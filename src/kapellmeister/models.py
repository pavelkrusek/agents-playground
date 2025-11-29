from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

AudienceLevel = Literal["beginner", "intermediate", "advanced"]
StreamingService = Literal["spotify", "apple_music", "youtube_music"]


@dataclass
class Composer:
    name: str
    birth_year: int | None = None
    death_year: int | None = None
    nationality: str | None = None
    epoch: str | None = None
    wikidata_id: str | None = None
    openopus_id: int | None = None
    tags: list[str] = field(default_factory=list)


@dataclass
class Movement:
    name: str
    number: int | None = None
    tempo_marking: str | None = None
    duration_min: int | None = None


@dataclass
class Work:
    title: str
    composer_name: str
    genre: str | None = None
    catalogue_number: str | None = None
    key: str | None = None
    year_composed: int | None = None
    duration_min: int | None = None

    wikidata_id: str | None = None
    openopus_id: int | None = None

    movements: list[Movement] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


@dataclass
class ComposerProfile:
    """Enriched info for explaining a composer to the listener."""
    composer: Composer
    short_bio: str | None = None
    style_traits: list[str] = field(default_factory=list)
    representative_works: list[Work] = field(default_factory=list)


@dataclass
class WorkFacts:
    """Enriched info for explaining a single piece."""
    work: Work
    program_note_short: str | None = None
    program_note_long: str | None = None
    interesting_facts: list[str] = field(default_factory=list)
    difficulty_for_listener: str | None = None


@dataclass
class ProgramConstraints:
    """Input from the user → what kind of concert they want."""
    min_duration_min: int | None = None
    max_duration_min: int | None = None
    target_duration_min: int | None = None

    audience_level: AudienceLevel = "beginner"
    mood: str | None = None

    include_composers: list[str] = field(default_factory=list)
    exclude_composers: list[str] = field(default_factory=list)
    required_genres: list[str] = field(default_factory=list)

    venue_type: str | None = None
    allow_encores: bool = True


@dataclass
class ProgramItem:
    work: Work
    position: int
    notes: str | None = None


@dataclass
class Program:
    title: str | None = None
    items: list[ProgramItem] = field(default_factory=list)
    total_duration_min: int | None = None
    constraints: ProgramConstraints | None = None


@dataclass
class PlaylistReference:
    """Optional mapping of the program to a streaming service playlist."""
    service: StreamingService
    playlist_id: str | None = None
    playlist_url: str | None = None


@dataclass
class ProgramWithNarrative:
    """What the concierge agent might ultimately return."""
    program: Program
    narrative: str | None = None
    playlist: PlaylistReference | None = None

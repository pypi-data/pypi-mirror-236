"""Custom types for TVSD """
from typing import TYPE_CHECKING, List, TypedDict

from tvsd.types.episode import Episode
from tvsd.types.season import Season
from tvsd.types.show import Show

# if TYPE_CHECKING:
#     from tvsd.types.episode import Episode

__all__ = ["Episode", "Season", "Show", "SeasonDetailsFromURL", "EpisodeDetailsFromURL"]


class SeasonDetailsFromURL(TypedDict):
    """DetailsFromURL type object

    Args:
        TypedDict (TypedDict): TypedDict from typings package
    """

    title: str
    description: str
    episodes: List["Episode"]
    year: str


class EpisodeDetailsFromURL(TypedDict):
    """DetailsFromURL type object

    Args:
        TypedDict (TypedDict): TypedDict from typings package
    """

    title: str
    url: str

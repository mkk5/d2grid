from enum import Enum
from pydantic import BaseModel, Field


# SpectralParam
class Position(Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"


class SpectralParam(BaseModel):
    top: int
    position: Position
    league: str | None = None


# SpectralResponse
class HeroStats(BaseModel):
    matches_s: int
    winrate_s: float
    rank: float
    picks_to_median: float


type HeroesData = dict[int, HeroStats]


class Result(BaseModel):
    P1: HeroesData = Field(validation_alias="1.1")
    P2: HeroesData = Field(validation_alias="1.2")
    P3: HeroesData = Field(validation_alias="1.3")
    P4: HeroesData = Field(validation_alias="0.1")
    P5: HeroesData = Field(validation_alias="0.3")


class SpectralResponse(BaseModel):
    version: str
    report: str
    result: Result

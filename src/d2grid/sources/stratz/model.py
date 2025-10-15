from enum import Enum
from pydantic import BaseModel, Field


# StratzParam
class RankBracket(Enum):
    UNCALIBRATED = "UNCALIBRATED"
    HERALD = "HERALD"
    GUARDIAN = "GUARDIAN"
    CRUSADER = "CRUSADER"
    ARCHON = "ARCHON"
    LEGEND = "LEGEND"
    ANCIENT = "ANCIENT"
    DIVINE = "DIVINE"
    IMMORTAL = "IMMORTAL"


class Position(Enum):
    P1 = "POSITION_1"
    P2 = "POSITION_2"
    P3 = "POSITION_3"
    P4 = "POSITION_4"
    P5 = "POSITION_5"


class Region(Enum):
    CHINA = "CHINA"
    SEA = "SEA"
    NA = "NORTH_AMERICA"
    SA = "SOUTH_AMERICA"
    EUROPE = "EUROPE"


class GameMode(Enum):
    ALL_PICK_RANKED = "ALL_PICK_RANKED"
    ALL_PICK = "ALL_PICK"
    TURBO = "TURBO"


class Sort(Enum):
    RANK = "rank"
    WINRATE = "winrate"


class StratzParam(BaseModel):
    top: int = Field(exclude=True)
    sort: Sort = Field(default=Sort.RANK, exclude=True)
    days: int = Field(default=14, ge=1, le=30)
    ranks: list[RankBracket] = [RankBracket.IMMORTAL]
    positions: list[Position] = []
    regions: list[Region] = []
    game_modes: list[GameMode] = [GameMode.ALL_PICK_RANKED]


# WinDayResponse
class WinDay(BaseModel):
    day: int
    heroId: int
    winCount: int
    matchCount: int


class HeroStats(BaseModel):
    winDay: list[WinDay]


class Data(BaseModel):
    heroStats: HeroStats


class WinDayResponse(BaseModel):
    data: Data


# query string
query_string = '''
query HeroWinDayStats(
  $days: Int,
  $ranks: [RankBracket!],
  $positions: [MatchPlayerPositionType!],
  $regions: [BasicRegionType!],
  $gameModes: [GameModeEnumType!]
) {
  heroStats {
    winDay(
      take: $days
      bracketIds: $ranks
      positionIds: $positions
      regionIds: $regions
      gameModeIds: $gameModes
    ) {
      day
      heroId
      winCount
      matchCount
    }
  }
}
'''

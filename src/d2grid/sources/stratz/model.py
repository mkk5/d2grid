from typing import Literal
from pydantic import BaseModel, Field

# StratzParam
type RankBracket = Literal[
    "UNCALIBRATED",
    "HERALD",
    "GUARDIAN",
    "CRUSADER",
    "ARCHON",
    "LEGEND",
    "ANCIENT",
    "DIVINE",
    "IMMORTAL"
]

type Position = Literal[
    "POSITION_1",
    "POSITION_2",
    "POSITION_3",
    "POSITION_4",
    "POSITION_5"
]

type Region = Literal[
    "CHINA",
    "SEA",
    "NORTH_AMERICA",
    "SOUTH_AMERICA",
    "EUROPE"
]

type GameMode = Literal[
    "ALL_PICK_RANKED",
    "ALL_PICK",
    "TURBO"
]

type Sort = Literal["rank", "winrate"]


class StratzParam(BaseModel):
    top: int = Field(exclude=True)
    sort: Sort = Field(default="rank", exclude=True)
    days: int = Field(default=14, ge=1, le=30)
    ranks: list[RankBracket] = ["IMMORTAL"]
    positions: list[Position] = []
    regions: list[Region] = []
    game_modes: list[GameMode] = ["ALL_PICK_RANKED"]


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

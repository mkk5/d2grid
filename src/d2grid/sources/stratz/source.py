from typing import TypedDict, Callable
from math import sqrt
import httpx
from .model import StratzParam, WinDayResponse, query_string, Sort


class HeroAggregatedStats(TypedDict):
    hero: int
    wins: int
    matches: int


def aggregate(response_data: WinDayResponse) -> list[HeroAggregatedStats]:
    aggregated_counts = {}
    for record in response_data.data.heroStats.winDay:
        count = aggregated_counts.setdefault(record.heroId, {"wins": 0, "matches": 0})
        count["wins"] += record.winCount
        count["matches"] += record.matchCount
    return [HeroAggregatedStats(hero=hero_id, wins=stats["wins"], matches=stats["matches"])
            for hero_id, stats in aggregated_counts.items()]


def by_winrate(item: HeroAggregatedStats) -> float:
    return item["wins"] / item["matches"]


def by_rank(item: HeroAggregatedStats) -> float:
    """Lower bound of Wilson score confidence interval for winrate"""
    z = 3  # lower ~0.13%
    n = item["matches"]
    p = item["wins"] / n
    z2 = z ** 2
    return (p + z2 / (2 * n) - z * sqrt((p * (1 - p) + z2 / (4 * n)) / n)) / (1 + z2 / n)


SORT_MAP: dict[Sort, Callable[[HeroAggregatedStats], float]] = {
    Sort.WINRATE: by_winrate,
    Sort.RANK: by_rank,
}


class StratzSource:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._client = None

    def __call__(self, param: StratzParam) -> list[int]:
        if self._client is None:
            headers = {"Authorization": f"Bearer {self.api_key}", "User-Agent": "STRATZ_API"}
            self._client = httpx.Client(base_url="https://api.stratz.com", headers=headers)

        res = self._client.post("/graphql", json={
            "query": query_string,
            "variables": param.model_dump(mode="json"),
        }).raise_for_status()

        response_data = WinDayResponse.model_validate_json(res.text)
        agg_data = aggregate(response_data)
        return [hero["hero"] for hero in sorted(agg_data, key=SORT_MAP[param.sort], reverse=True)][:param.top]

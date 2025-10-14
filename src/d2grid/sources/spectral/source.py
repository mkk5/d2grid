import httpx
from .model import SpectralParam, SpectralResponse, HeroesData, Result


class SpectralSource:
    def __init__(self):
        self._client = None
        self._cache: dict[str | None, Result] = {} # TODO: lru_cache?

    def _load_data(self, league: str | None):
        if self._client is None:
            self._client = httpx.Client(base_url="https://stats.spectral.gg/lrg2/api")
        p = {"mod": "heroes-positions"}
        if league is None:
            p["cat"] = "ranked_patches"
            p["latest"] = ""
        else:
            p["league"] = league
        res = self._client.get("/", params=p).raise_for_status()
        response_data = SpectralResponse.model_validate_json(res.text)
        self._cache[league] = response_data.result

    def __call__(self, param: SpectralParam) -> list[int]:
        league = param.league
        if league not in self._cache:
            self._load_data(league)
        result = self._cache[league]
        position_data: HeroesData = getattr(result, param.position.value) # sorted by rank by default
        return list(position_data)[:param.top]

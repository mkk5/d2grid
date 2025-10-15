import functools
import httpx
from .model import SpectralParam, SpectralResponse, HeroesData, Result


class SpectralSource:
    def __init__(self):
        self._client = None

    @functools.cache
    def _load_data(self, league: str | None) -> Result:
        if self._client is None:
            self._client = httpx.Client(base_url="https://stats.spectral.gg/lrg2/api")
        params = {"mod": "heroes-positions"}
        if league is None:
            params |= {"cat": "ranked_patches", "latest": ""}
        else:
            params["league"] = league
        res = self._client.get("/", params=params).raise_for_status()
        response_data = SpectralResponse.model_validate_json(res.text)
        return response_data.result

    def __call__(self, param: SpectralParam) -> list[int]:
        result = self._load_data(param.league)
        position_data: HeroesData = getattr(result, param.position.value)  # sorted by rank by default
        return list(position_data)[:param.top]

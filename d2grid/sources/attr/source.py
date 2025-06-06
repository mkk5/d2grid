import httpx
from .model import AttrResponse, AttrParam, query_string


class AttrSource:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._data = None

    def _load_data(self) -> None:
        if self._data is None:
            headers = {"Authorization": f"Bearer {self.api_key}", "User-Agent": "STRATZ_API"}
            with httpx.Client(headers=headers) as client:
                res = client.post("https://api.stratz.com/graphql", json={"query": query_string})
            self._data = AttrResponse.model_validate_json(res.text)

    def __call__(self, param: AttrParam) -> list[int]:
        self._load_data()
        return [hero.id for hero in sorted(self._data.data.constants.heroes, key=lambda h: h.displayName) if
                hero.stats.primaryAttribute == param]

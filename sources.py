from typing import Literal
from pathlib import Path
from pydantic import ValidationError, BaseModel
from utils import read_data
import httpx


class Category(BaseModel):
    category_name: str
    x_position: float
    y_position: float
    width: float
    height: float
    hero_ids: list[int]

class Config(BaseModel):
    config_name: str
    categories: list[Category]

class HeroGrid(BaseModel):
    version: int = 3
    configs: list[Config]

def get_item[T](items: list[T], key: str | int, name_field: str) -> T:
    if isinstance(key, int):
        return items[key]
    if isinstance(key, str):
        return next(i for i in items if getattr(i, name_field) == key)

class FileParam(BaseModel):
    config: int | str
    category: int | str

class FileSource:
    def __init__(self, path: Path | str) -> None:
        self.path = path
        self._data = None

    def _load_data(self) -> None:
        if self._data is None:
            try:
                self._data = read_data(self.path, HeroGrid)
            except (FileNotFoundError, ValidationError):
                self._data = HeroGrid(configs=[])

    def hero_list(self, param: FileParam) -> list[int]:
        self._load_data()
        config = get_item(self._data.configs, key=param.config, name_field="config_name")
        category = get_item(config.categories, key=param.category, name_field="category_name")
        return category.hero_ids

# =============================================================================

type AttrParam = Literal["str", "agi", "int", "all"]

class Stats(BaseModel):
    primaryAttribute: AttrParam

class Heroes(BaseModel):
    id: int
    displayName: str
    stats: Stats

class Constants(BaseModel):
    heroes: list[Heroes]

class Data(BaseModel):
    constants: Constants

class AttrResponse(BaseModel):
    data: Data

class AttrSource:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._data = None

    def _load_data(self) -> None:
        if self._data is None:
            headers = {"Authorization": f"Bearer {self.api_key}", "User-Agent": "STRATZ_API"}
            with httpx.Client(headers=headers) as client:
                res = client.post("https://api.stratz.com/graphql", json={"query": "{constants{heroes{id displayName stats{primaryAttribute}}}}"})
            self._data = AttrResponse.model_validate_json(res.text)

    def hero_list(self, param: AttrParam) -> list[int]:
        self._load_data()
        return [hero.id for hero in sorted(self._data.data.constants.heroes, key=lambda h: h.displayName) if hero.stats.primaryAttribute == param]

from pydantic import ValidationError
from pathlib import Path
from d2grid.utils import read_data
from .model import HeroGrid, FileParam


def get_item[T](items: list[T], key: int | str, name_field: str) -> T:
    if isinstance(key, int):
        return items[key]
    if isinstance(key, str):
        return next(i for i in items if getattr(i, name_field) == key)
    raise TypeError(f"{key=} Key type expected: int|str, got: {type(key)}")


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

    def __call__(self, param: FileParam) -> list[int]:
        self._load_data()
        config = get_item(self._data.configs, key=param.config, name_field="config_name")
        category = get_item(config.categories, key=param.category, name_field="category_name")
        return category.hero_ids

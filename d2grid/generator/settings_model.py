from typing import Annotated, Literal, Union
from pathlib import Path
from pydantic import BaseModel, AfterValidator, Field
from d2grid.sources import FileParam, AttrParam


class BaseCategorySettings(BaseModel):
    name: str


class FileCategorySettings(BaseCategorySettings):
    source: Literal["file"]
    param: FileParam


class AttrCategorySettings(BaseCategorySettings):
    source: Literal["attr"]
    param: AttrParam


type CategorySettings = Annotated[
    Union[FileCategorySettings, AttrCategorySettings],
    Field(discriminator="source")
]


class ColumnSettings(BaseModel):
    x: float = Field(ge=0)
    width: float = Field(gt=0)
    width_heroes: int = Field(gt=0)


class ConfigSettings(BaseModel):
    name: str
    columns: list[ColumnSettings]
    row_gap: float = Field(ge=0)
    categories: list[CategorySettings]


def json_extension(path: Path) -> Path:
    if path.suffix != '.json':
        raise ValueError(f'Path should have .json extension.')
    return path


class GlobalSettings(BaseModel):
    file_source: Annotated[Path, AfterValidator(json_extension)]
    stratz_api_key: str


class Settings(BaseModel):
    version: int = 1
    globals: GlobalSettings
    result_paths: list[Annotated[Path, AfterValidator(json_extension)]]
    configs: list[ConfigSettings]

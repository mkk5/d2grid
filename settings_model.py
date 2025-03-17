from pydantic import BaseModel, AfterValidator, Field
from pathlib import Path
from typing import Annotated, Literal
from sources import FileParam, AttrParam

def json_extension(path: Path) -> Path:
    if path.suffix != '.json':
        raise ValueError(f'Path should have .json extension.')
    return path

class CategorySettings(BaseModel):
    name: str
    source: Literal["file", "attr"]
    param: FileParam | AttrParam

class ColumnSettings(BaseModel):
    x: float = Field(ge=0)
    width: float = Field(gt=0)
    width_heroes: int = Field(gt=0)

class ConfigSettings(BaseModel):
    name: str
    columns: list[ColumnSettings]
    row_gap: float = Field(ge=0)
    categories: list[CategorySettings]

class Settings(BaseModel):
    api_key: str
    file_source: Annotated[Path, AfterValidator(json_extension)]
    result_paths: list[Annotated[Path, AfterValidator(json_extension)]]
    configs: list[ConfigSettings]

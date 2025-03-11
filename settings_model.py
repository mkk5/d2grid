from pydantic import BaseModel, AfterValidator
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
    x: float
    width: float
    width_heroes: int

class ConfigSettings(BaseModel):
    name: str
    columns: list[ColumnSettings]
    row_gap: float
    categories: list[CategorySettings]

class Settings(BaseModel):
    api_key: str
    file_source: Annotated[Path, AfterValidator(json_extension)]
    result_path: Annotated[Path, AfterValidator(json_extension)]
    configs: list[ConfigSettings]

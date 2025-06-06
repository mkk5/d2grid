from pydantic import BaseModel


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


class FileParam(BaseModel):
    config: int | str
    category: int | str

from pydantic import BaseModel
from typing import Literal

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


query_string = "{constants{heroes{id displayName stats{primaryAttribute}}}}"

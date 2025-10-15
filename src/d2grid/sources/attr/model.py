from enum import Enum
from pydantic import BaseModel, Field


# AttrParam
class AttrParam(Enum):
    STRENGTH = "str"
    AGILITY = "agi"
    INTELLIGENCE = "int"
    UNIVERSAL = "all"


# AttrResponse
class PrimaryAttr(Enum):
    STRENGTH = 0
    AGILITY = 1
    INTELLIGENCE = 2
    UNIVERSAL = 3


class Hero(BaseModel):
    id: int
    display_name: str = Field(validation_alias="name_english_loc")
    primary_attr: PrimaryAttr


class Data(BaseModel):
    heroes: list[Hero]


class Result(BaseModel):
    data: Data


class AttrResponse(BaseModel):
    result: Result

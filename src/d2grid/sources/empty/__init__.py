__all__ = ["empty_source", "EmptyParam"]

from typing import Annotated
from pydantic import Field

type EmptyParam = Annotated[None, Field(None)]


def empty_source(param: EmptyParam) -> list[int]:
    return []

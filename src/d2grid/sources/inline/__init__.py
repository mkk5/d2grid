__all__ = ["inline_source", "InlineParam"]


type InlineParam = list[int]


def inline_source(param: InlineParam) -> list[int]:
    return param

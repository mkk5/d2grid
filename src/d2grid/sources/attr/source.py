import functools
import httpx
from .model import AttrResponse, AttrParam, Hero


@functools.cache
def _load_data() -> list[Hero]:
    res = httpx.get("https://www.dota2.com/datafeed/herolist?language=english").raise_for_status()
    response_data = AttrResponse.model_validate_json(res.text)
    return response_data.result.data.heroes


def attr_source(param: AttrParam) -> list[int]:
    heroes = _load_data()
    return [hero.id for hero in sorted(heroes, key=lambda h: h.display_name) if hero.primary_attr.name == param.name]

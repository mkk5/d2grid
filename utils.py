from pathlib import Path
from pydantic import BaseModel


def read_data[M: BaseModel](path: Path | str, model: type[M]) -> M:
    with open(path, "r") as f:
        json_string = f.read()
    return model.model_validate_json(json_string, strict=True)

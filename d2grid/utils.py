from pathlib import Path
from pydantic import BaseModel


def read_data[M: BaseModel](path: Path | str, model: type[M]) -> M:
    with open(path, "r") as f:
        json_string = f.read()
    return model.model_validate_json(json_string, strict=True)

def write_data(paths: list[Path], data: BaseModel) -> None:
    json_string = data.model_dump_json()
    for path in paths:
        with open(path, "w") as f:
            f.write(json_string)

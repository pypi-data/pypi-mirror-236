# library
import json
from pathlib import Path


# for compatibility with python 3.8, 3.9 and 3.10 (from https://github.com/hukkin/tomli)
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def get_pypt_version(path_pypt: Path) -> str:
    """fonction pour récupérer la version du pyproject.toml, définie ici et uniquement ici"""
    with open(path_pypt, "rb") as f:
        return tomllib.load(f)["tool"]["poetry"]["version"]


def get_config_json(path_json: Path) -> dict:
    """pour charger un json classique"""
    with open(path_json, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


# end

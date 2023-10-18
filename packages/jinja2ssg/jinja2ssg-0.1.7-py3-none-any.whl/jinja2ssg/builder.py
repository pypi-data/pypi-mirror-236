import os
import logging
from typing import List
from collections import namedtuple
from pathlib import Path

from yaml import safe_load
from jinja2 import Environment, FileSystemLoader


def freeze(data):
    """
    Used to turn a dict into a named tuple so that key words do not clash. For
    example `items` cannot be used in a dict since it will clash with the
    `items()` function name.
    """
    if isinstance(data, dict):
        Data = namedtuple("Data", " ".join(data.keys()))
        return Data(**{k: freeze(v) for k, v in data.items()})
    if isinstance(data, list):
        return tuple(data)
    return data


def load_yaml(template_path: Path):
    """
    Given a path to a template, find yaml files located near it and returns
    them in a dictionary.
    """
    yaml = {}
    for ext in ["yaml", "yml"]:
        for datafile in template_path.parents[0].glob(f"*.{ext}"):
            print(f"\t{template_path.name} -> {datafile.name}")
            with open(datafile, "r", encoding="utf-8") as fl:
                data = safe_load(fl.read())
                yaml[datafile.name[: -len(datafile.suffix)]] = freeze(data)
    return yaml


def build(*, src: str, dest: str, ext: List[str]):
    """
    - Walk a given `src` folder and generate output inside a `dest` folder.
    - If will generate files using the Jinja2 template engine.
        - You can use any imports etc
    - Any file name starting with `_` will be ignored.
    - Only files with extensions that are provided in `ext` will be rendered.
    - Variables that are available:
        - All environment variables can be used via `{{ env.MY_VARIABLE }}`.
        - `{{ relative_path }}` refers to the path of the current file being rendered.
    """
    src_path = Path(src).resolve()
    dest_path = Path(dest).resolve()
    env = Environment(loader=FileSystemLoader(str(src)))
    env.globals["env"] = os.environ
    if not dest_path.exists():
        os.makedirs(dest_path)
    for path in src_path.glob("**/*"):
        if any(part.startswith("_") for part in path.relative_to(src_path).parts):
            continue
        if path.name.startswith("_") or path.is_dir() or path.suffix not in ext:
            continue
        relative_path = path.relative_to(src_path)
        out_path = dest_path / relative_path
        if not out_path.parent.exists():
            os.makedirs(out_path.parent)
        template_path = str(path.relative_to(src_path))
        print(f"{template_path} -> {out_path}")
        template = env.get_template(template_path)
        html = template.render(relative_path=relative_path, yaml=load_yaml(path))
        with open(out_path, "w", encoding="utf-8") as output:
            output.write(html)

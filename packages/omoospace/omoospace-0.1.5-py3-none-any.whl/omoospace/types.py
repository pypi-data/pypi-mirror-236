
from pathlib import Path
import os
from enum import Enum
from typing import TypedDict, Union

Structure = dict[str, "Structure"]

Entity = Path

Item = Path

Route = list[str]

PathLike = Union[str, os.PathLike]


class Work(TypedDict):
    name: str
    paths: list[str]


class Creator(TypedDict):
    name: str
    email: str
    role: str
    website: str


class Plugin(TypedDict):
    name: str
    version: str


class Software(TypedDict):
    name: str
    version: str
    plugins: list[Plugin]

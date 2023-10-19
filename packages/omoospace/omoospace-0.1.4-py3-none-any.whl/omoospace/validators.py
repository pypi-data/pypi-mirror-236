from pathlib import Path
import re

from omoospace.types import PathLike


def is_version(s: str):
    pattern = r'^v?\d+(\.\d+)*$'
    return bool(re.match(pattern, s))


def is_number(s: str):
    pattern = r'^-?\d*\.?\d+$'
    return bool(re.match(pattern, s))


def is_resolution(s: str):
    pattern = r'^\d+(k|p|px)$'
    return bool(re.match(pattern, s))


def is_email(s: str):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, s))


def is_url(s: str):
    pattern = r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    return bool(re.match(pattern, s))


def is_entity(path: PathLike) -> bool:
    path = Path(path).resolve()
    if path.is_dir():
        is_subspace = Path(path, 'Subspace.yml').is_file()
        is_void = 'Void' in path.name.split("_")
        return is_subspace or is_void
    else:
        not_marker = path.name != 'Subspace.yml'
        return not_marker


def is_item(path: PathLike) -> bool:
    path = Path(path).resolve()

    exists = path.exists()
    not_package_profile_file = path.name != 'Package.yml'
    not_omoospace_profile_file = path.name != "Omoospace.yml"
    not_subspace_profile_file = path.name != 'Subspace.yml'

    return exists \
        and not_package_profile_file \
        and not_omoospace_profile_file \
        and not_subspace_profile_file

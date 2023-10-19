import os
from pathlib import Path
from typing import TypedDict
from zipfile import ZipFile


from omoospace.exceptions import NotFoundError
from omoospace.types import Creator, Item, PathLike
from omoospace.common import console, yaml
from omoospace.ui import Board, Info
from omoospace.validators import is_item


class PackageProfile(TypedDict):
    name: str
    description: str
    version: str
    creators: list[Creator]


class Package:
    """The class of omoospace package.

    A package class instance is always refer to a existed package directory, not in ideal. 

    Attributes:
        name (str): Package's name.
        description (str): Package's description.
        version (str): Package's version.
        creators (list[Creator]): Creator list.
        root_path (Path): Root path.
    """

    def __init__(self, detect_dir: PathLike):
        """Initialize package .

        Args:
            detect_dir (PathLike): [description]

        Raises:
            NotFoundError: [description]
            NotFoundError: [description]
        """
        package_path = Path(detect_dir).resolve()
        if (package_path.suffix == ".zip"):
            with ZipFile(package_path, 'r') as zip:
                try:
                    with zip.open('Package.yml') as file:
                        package_profile = yaml.load(file)
                except:
                    raise NotFoundError("package", detect_dir)
        else:
            package_profile_path = Path(package_path, 'Package.yml')
            if package_profile_path.exists():
                with package_profile_path.open('r', encoding='utf-8') as file:
                    package_profile = yaml.load(file)
            else:
                raise NotFoundError("package", detect_dir)

        self.root_path = package_path
        self.name = package_profile.get('name')
        self.description = package_profile.get('description')
        self.version = package_profile.get('version')
        self.creators = package_profile.get('creators')

    @property
    def items(self) -> list[Item]:
        """list[Item]: The list of Item objects."""
        items: list[Item] = []
        for root, dirs, files in os.walk(self.root_path):
            for path in files:
                child = Path(root, path).resolve()
                if is_item(child):
                    items.append(child)
        return items

    def show_summary(self):
        """Print a summary of the package.
        """
        items = [str(item.relative_to(self.root_path)) for item in self.items]
        console.print(Board(
            Info("Name", "%s [dim](%s)[/dim]" %
                 (self.name, self.root_path)),
            Info("Description", self.description),
            Info("Version", self.version),
            Info("Items", "\n".join(items)),
            title="Summary"
        ))


from enum import Enum
import os
from pathlib import Path
from typing import TypedDict, Union
from nutree import Tree, Node
from omoospace.exceptions import InvalidError

from omoospace.graph import draw_graph
from omoospace.types import Entity, PathLike, Route
from omoospace.common import console, yaml
from omoospace.ui import Grid, Instruction, Table
from omoospace.utils import format_name
from omoospace.validators import is_entity, is_number, is_version


# TODO: dont't read .spp.painter_lock, autosave_0

class SubspaceType(Enum):
    DIRECTORY = "directory"
    FILE = "file"
    PHANTOM = "phantom"


class SubspaceProfile(TypedDict):
    name: str
    comments: list[str]


class Subspace():
    def __init__(
        self,
        pathname: str,
        profile: Union[str, list, SubspaceProfile] = None,
    ):
        self.pathname = pathname
        self.entities: list[Entity] = []
        self.flow: int = 0
        self.type: SubspaceType = None

        if isinstance(profile, str):
            self.name = pathname
            self.comments = [profile]
        elif isinstance(profile, list):
            self.name = pathname
            self.comments = profile
        elif isinstance(profile, dict):
            self.name = profile.get('name') or pathname
            comments = profile.get('comments')
            if isinstance(comments, str) and comments:
                self.comments = [comments]
            elif isinstance(comments, list):
                self.comments = [*comments]
            else:
                self.comments = []
        else:
            self.name = pathname
            self.comments = []

    def __repr__(self):
        return self.pathname

    @property
    def ui_name(self):
        if self.type == SubspaceType.DIRECTORY:
            icon = "📁"
            link = self.entities[0]
            name_str = "[link=%s]%s[/link]" % (link, self.name)
        elif self.type == SubspaceType.FILE:
            icon = "📄"
            link = self.entities[0].parent
            name_str = "[link=%s]%s[/link]" % (link, self.name)
        elif self.type == SubspaceType.PHANTOM:
            icon = "💿"
            name_str = self.name
        else:
            icon = "⛔"
            name_str = self.name

        if self.pathname == self.name:
            pathname_str = ""
        else:
            pathname_str = " [dim](%s)[/dim]" % self.pathname
        return "%s %s%s" % (icon, name_str, pathname_str)

    @property
    def html_name(self):
        if self.pathname == self.name:
            pathname_str = ""
        else:
            pathname_str = " (%s)" % self.pathname
        return "%s%s" % (self.name, pathname_str)

    @property
    def ui_comments(self):
        return ["[dim]- %s[/dim]" %
                comment for comment in self.comments]

    @property
    def ui_entities(self):
        entity_links: list[str] = []
        for entity in self.entities:
            path = entity if entity.is_dir() else entity.parent
            entity_links.append("[link=%s]%s[/link]" %
                                (path, entity.name))
        return entity_links

    @property
    def html_entities(self):
        entity_links: list[str] = []
        for entity in self.entities:
            entity_links.append("&nbsp<a href='%s' target='_blank'>%s</a>&nbsp"
                                % (entity, entity.name))
        return entity_links


class SubspaceTree(Tree):
    """The class of subspace tree.

    An subspace tree instance is always refer to a existed SourceFiles directory, not in ideal. 

    """

    def __init__(
        self,
        search_dir: PathLike = None
    ):
        """Initialize the subspace tree from the given directory.

        Args:
            search_dir (PathLike): [description]
        """
        super().__init__()
        if (search_dir):
            self.from_dir(search_dir)

    @classmethod
    def get_entity_route(cls, path: PathLike) -> Route:
        """Returns the route of entity path.

        **This is a useful function to generate correct path of sourcefile output.**
        
        For example:
        ```python
        filepath = "c:/path/to/Project/SourceFiles/SQ010_SH0100.blend"
        route = SubspaceTree.get_entity_route(filepath)
        >>> ["SQ010","SH0100"]
        route_str = "_".join(route)
        >>> "SQ010_SH0100"
        ```
        So the render ouput filename should be `SQ010_SH0100.####.png`

        Args:
            path (PathLike): [description]

        Returns:
            Route: The list of pathname of subspace.
        """
        subspace_tree = cls()
        entity_end_node = subspace_tree.add_entity(path)
        return entity_end_node.path.split("/")[1:]

    def from_dir(
        self,
        search_dir: PathLike,
        recursive: bool = True
    ):
        """Set the subspace tree from the given directory.

        Args:
            search_dir (PathLike): [description]
            recursive (bool, optional): [description]. Defaults to True.
        """
        entities = self.get_entities(search_dir, recursive=recursive)
        for entity in entities:
            self.add_entity(entity)

    def add_entity(self, path: PathLike) -> Node:
        """Add subspace node to the tree based on entity.

        The entity path must be real, not in ideal.

        Args:
            path (PathLike): [description]

        Returns:
            Route: List of subspace name along the route.

        Raises:
            InvalidError: entity path is invalid.
        """
        entity = Path(path).resolve()
        if not is_entity(entity) == 0:
            InvalidError(entity, 'entity')

        # Get relpath parts. remove those directory that is not entity.
        entities = [entity]
        for parent in entity.parents:
            if is_entity(parent):
                entities.append(parent)
        entities.reverse()

        # Get route nodes. remove duplicate prefix.
        def is_valid_name(namespace):
            return not is_version(namespace) \
                and not is_number(namespace)

        route: Route = []
        node = self
        for entity in entities:
            entity_name: str = entity.stem

            namespaces: list[str] = entity_name.split('_')
            subspace_profile_path = Path(entity, "Subspace.yml").resolve()

            # clip matched prefix spaces
            for i in range(len(route)):
                route_str_suffix = '_'.join(route[i:])
                name_prefix = '_'.join(namespaces[:len(route) - i])
                if route_str_suffix == name_prefix:
                    namespaces = namespaces[len(route) - i:]
                    break

            namespaces = list(filter(is_valid_name, namespaces))

            # create or get subspace by namespace
            for i in range(len(namespaces)+1):
                # if all namespace is match,the entity will be add to current route
                # so the index is start from -1
                i = i - 1
                is_last = i == len(namespaces)-1
                subspace_route = route + namespaces[:i+1]
                if (len(subspace_route) == 0):
                    continue

                node_path = "/" + "/".join(subspace_route)
                subspace_node = self.find(
                    match=lambda node: node.path == node_path
                )
                if not subspace_node:
                    if is_last and subspace_profile_path.is_file():
                        with subspace_profile_path.open('r', encoding='utf-8') as file:
                            subspace_profile = yaml.load(file) or {}
                    else:
                        subspace_profile = {}
                    subspace = Subspace(
                        pathname=namespaces[i],
                        profile=subspace_profile,
                    )
                    subspace_node = node.add(subspace)

                # if is last, add enitity to it.
                if is_last and entity not in subspace_node.data.entities:
                    subspace_node.data.entities.append(entity)

                # assign type
                subspace_type = subspace_node.data.type
                if is_last and entity.is_dir():
                    subspace_node.data.type = SubspaceType.DIRECTORY
                elif subspace_type != SubspaceType.DIRECTORY \
                        and is_last and entity.is_file():
                    subspace_node.data.type = SubspaceType.FILE
                elif subspace_type != SubspaceType.DIRECTORY \
                        and subspace_type != SubspaceType.FILE\
                        and entity.exists():
                    subspace_node.data.type = SubspaceType.PHANTOM

                # what ever is end node or not, all nodes are passed through.
                subspace_node.data.flow += 1

                node = subspace_node
            route.extend(namespaces)
        return node

    @classmethod
    def get_entities(
        cls,
        search_dir: PathLike,
        recursive: bool = True
    ) -> list[Entity]:
        """Recursively find all entities in the search directory .

        Args:
            search_dir (PathLike): [description]
            recursive (bool, optional): [description]. Defaults to True.

        Returns:
            list[Entity]: [description]
        """
        search_path: Path = Path(search_dir).resolve()
        entities: list[Entity] = []
        if recursive:
            # FIXME: replace this with Path.walk (python 3.12)
            # https://docs.python.org/3/library/pathlib.html
            for root, dirs, files in os.walk(search_path):
                for path in [*dirs, *files]:
                    child = Path(root, path).resolve()
                    if is_entity(child):
                        entities.append(child)
        else:
            for child in search_path.iterdir():
                if is_entity(child):
                    entities.append(child)
        return entities

    def render_tree(self) -> str:
        """Render the tree as rich str.

        Returns:
            str: [description]
        """

        label_dict = {
            "📁": "direcotry subspace\nwhich contains Subspace.yml.",
            "📄": "file subspace\nwhich refers to a leaf file.",
            "💿": "phantom | unknown subspace\nwhich has no entity.",
            "⛔": "dummy subspace\nwhich have not created yet."
        }

        return Grid(
            self.format(repr="{node.data.ui_name}", title="(Root)"),
            Instruction(label_dict)
        )

    def render_table(self) -> str:
        """List subspaces in table as rich str.

        Returns:
            str: [description]
        """

        table = Table(
            "Subspace",
            "Comments",
            "Entities"
        )

        for node in self:
            subspace: Subspace = node.data
            table.add_row(
                subspace.ui_name,
                "\n".join(subspace.ui_comments),
                "\n".join(subspace.ui_entities)
            )
        return table

    def draw_graph(
        self,
        output_dir: PathLike,
        reveal_when_success: bool = True
    ):
        """Draws the graph and export html file.

        Args:
            output_dir (PathLike): [description]
            reveal_when_success (bool, optional): [description]. Defaults to True.
        """
        node_dict = {
            ".": {
                "name": "(Root)",
                "content": "&nbsp(Root)&nbsp",
                "color": "#BEBEBE",
                "size": len(self)+20,
                "level": 0,
                "border_width": 0,
            }
        }
        for node in self:
            subspace: Subspace = node.data
            parent: Subspace = node.parent.data if node.parent else None

            if (subspace.type == SubspaceType.PHANTOM):
                color = "#939393"
            elif (subspace.type == SubspaceType.DIRECTORY):
                color = "#F6B330"
            else:
                color = "#585858"

            node_dict[node.path] = {
                "name": subspace.html_name,
                "parent": node.parent.path if parent else ".",
                "content": "<br>".join(subspace.html_entities),
                "color": color,
                "size": 5+subspace.flow,
                # "level": node.depth,
                "border_width": 0,
                "edge_width": 5+subspace.flow,
                "edge_color": '#3F3F3F',
            }

        draw_graph(
            node_dict,
            bgcolor="#111112",
            font_color="#F4F4F4",
            output_dir=output_dir,
            reveal_when_success=reveal_when_success
        )

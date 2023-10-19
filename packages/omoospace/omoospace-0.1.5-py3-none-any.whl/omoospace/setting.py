from pathlib import Path

from omoospace.directory import DirectoryTree, Structure
from omoospace.exceptions import InvalidError
from omoospace.types import Creator
from omoospace.omoospace import OmoospaceTree, OmoospaceStructure
from omoospace.common import console, yaml


class OmoospaceTemplate():
    def __init__(
        self,
        name: str = None,
        description: str = None,
        structure: OmoospaceStructure = None
    ) -> None:
        self.name = name
        self.description = description
        self.structure = structure or {}
        self.tree = OmoospaceTree(structure=structure)


class ProcessTemplate():
    def __init__(
        self,
        name: str,
        description: str,
        structure: Structure = None
    ) -> None:
        self.name = name
        self.description = description
        self.structure = structure or {}
        self.tree = DirectoryTree(structure=structure)


class Setting():
    working_omoospace: str
    working_directory: str
    recent_omoospaces: list[str]
    omoospace_templates: list[OmoospaceTemplate]
    process_templates: list[ProcessTemplate]
    registered_creators: list[Creator]
    registered_softwares: list[str]
    registered_roles: list[str]

    SETTING_PATH = "~/.omoospace/setting.yml"

    DEFAULT_SETTING = {
        "working_omoospace": None,
        "working_directory": None,
        "recent_omoospaces": None,
        "omoospace_templates": [
            {
                "name": "3D Asset",
                "description": "For 3D asset creation",
                "structure": {
                    "Contents": {
                        'Images': None,
                        'Materials': None,
                        'Models': None,
                        'Renders': None
                    },
                    "SourceFiles": {
                        '*AssetName': None,
                        'Void': None
                    }
                }
            },
            {
                "name": "CG Film",
                "description": "For short CG film producton",
                "structure": {
                    "Contents": {
                        'Audios': None,
                        'Dynamics': None,
                        'Images': None,
                        'Materials': None,
                        'Models': None,
                        'Renders': None,
                        'Videos': None,
                    },
                    "SourceFiles": {
                        '*FilmName': None,
                        'Void': None
                    }
                }
            }
        ],
        "process_templates": [
            {
                "name": "Asset Creation",
                "description": "Asset Creation Process",
                "structure": {
                    "001-Modeling": None,
                    "002-Texturing": None,
                    "003-Shading": None
                }
            },
            {
                "name": "Film Production",
                "description": "Film Production Process",
                "structure": {
                    "001-PreProduction": None,
                    "002-Production": None,
                    "003-PostProduction": None
                }
            }
        ],
        "registered_creators": [],
        "registered_roles": [
            "Owner",
            "Menber",
            "Modeller",
            "Rigger",
            "Animator",
            "Compositor",
            "Concept Artist",
            "Layout Artist",
            "Lighting Artist",
            "Colourist",
            "Editor",
            "Composer",
            "Sound Designer",
            "Director",
            "Supervisor",
            "Art Director",
            "Technical Director",
            "Technical Artist",
            "Technical Animator",
            "Scientific Adviser",
        ],
        "registered_softwares": [
            "3ds Max",
            "Maya",
            "Houdini",
            "Blender",
            "Cinema4D",
            "Zbrush",
            "3D Coat",
            "KeyShot",
            "Rhinoceros",
            "Nuke",
            "Mari",
            "Modo",
            "Katana",
            "Marmoset Toolbag",
            "RizomUV",
            "EmberGen",
            "Marvelous Designer",
            "DaVinci Resolve",
            "Illustrator",
            "Photoshop",
            "Premiere Pro",
            "After Effect",
            "Substance 3D Modeler",
            "Substance 3D Painter",
            "Substance 3D Designer",
            "Substance 3D Sampler",
            "Substance 3D Stager",
            "Affinity Photo",
            "Affinity Designer",
            "Affinity Publisher",
            "Fusion 360",
        ]
    }

    def __read_setting_file(self):
        setting: dict = {}
        setting_filepath = Path(self.SETTING_PATH).expanduser().resolve()
        if setting_filepath.exists():
            with setting_filepath.open('r', encoding='utf-8') as file:
                # aviod empty or invalid ifle
                setting = yaml.load(file) or {}
        return setting

    def __write_setting_file(self, setting):
        setting_filepath = Path(self.SETTING_PATH).expanduser().resolve()
        # create if not dir exist
        setting_filepath.parent.mkdir(parents=True,exist_ok=True)
        with setting_filepath.open('w', encoding='utf-8') as file:
            yaml.dump(setting, file)

    def __getattr__(self, key):
        if key not in self.__annotations__.keys():
            raise InvalidError(key, "key")
        setting = self.__read_setting_file()
        if (key == "omoospace_templates"):
            omoospace_templates = setting.get("omoospace_templates") or []
            omoospace_templates.extend(
                self.DEFAULT_SETTING["omoospace_templates"])
            return [OmoospaceTemplate(
                name=template.get('name'),
                description=template.get('description'),
                structure=template.get('structure')
            ) for template in omoospace_templates]
        elif (key == "process_templates"):
            process_templates = setting.get("process_templates") or []
            process_templates.extend(
                self.DEFAULT_SETTING["process_templates"])
            return [ProcessTemplate(
                name=template.get('name'),
                description=template.get('description'),
                structure=template.get('structure')
            ) for template in process_templates]
        elif (key == "registered_softwares"):
            registered_softwares = setting.get("registered_softwares") or []
            registered_softwares += list(
                set(self.DEFAULT_SETTING["registered_softwares"])
                - set(registered_softwares))
            return registered_softwares
        elif (key == "registered_roles"):
            registered_roles = setting.get("registered_roles") or []
            registered_roles += list(
                set(self.DEFAULT_SETTING["registered_roles"])
                - set(registered_roles))
            return registered_roles
        else:
            return setting.get(key) or self.DEFAULT_SETTING.get(key)

    def __setattr__(self, key, value):
        if key not in self.__annotations__.keys():
            raise InvalidError(key, "key")
        setting = self.__read_setting_file()
        if (key == "registered_softwares"):
            value = list(
                set(value)
                - set(self.DEFAULT_SETTING["registered_softwares"]))
        if (key == "registered_roles"):
            value = list(
                set(value)
                - set(self.DEFAULT_SETTING["registered_roles"]))
        setting[key] = value
        self.__write_setting_file(setting)

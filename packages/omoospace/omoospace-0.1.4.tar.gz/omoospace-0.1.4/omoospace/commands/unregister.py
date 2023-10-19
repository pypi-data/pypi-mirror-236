import click
from InquirerPy import inquirer
from InquirerPy.base import Choice

from omoospace.setting import Setting
from omoospace.types import Creator
from omoospace.commands.common import inquirer_style
from omoospace.common import console


UNREGISTER_CREATOR_HELP = "Remove creator from setting presets."
UNREGISTER_SOFTWARE_HELP = "Remove software from setting presets."
UNREGISTER_ROLE_HELP = "Remove role from setting presets."


def _unregister_creator():
    registered_creators = Setting().registered_creators
    creator_choices = [Choice(
        name="%s (%s)" % (creator.get("name"), creator.get("email")),
        value=id
    ) for id, creator in enumerate(registered_creators)]

    creator_id = inquirer.fuzzy(
        message="Choose the creator to remove",
        choices=creator_choices,
        style=inquirer_style
    ).execute()
    creator_profile = registered_creators[creator_id]
    console.print(Creator(creator_profile))

    is_confirm = inquirer.confirm(
        message="Confirm",
        default=True,
        style=inquirer_style
    ).execute()
    if is_confirm:
        del registered_creators[creator_id]
        Setting().registered_creators = registered_creators


def _unregister_software():
    registered_softwares = Setting().registered_softwares
    registered_softwares = list(
        set(registered_softwares)-set(Setting.DEFAULT_SETTING["registered_softwares"]))
    if (len(registered_softwares) == 0):
        console.print("No registered software found", style="warning")
        return
    software_name = inquirer.fuzzy(
        message="Choose from preunregisters",
        choices=registered_softwares,
        style=inquirer_style
    ).execute()
    console.print(software_name)
    is_confirm = inquirer.confirm(
        message="Confirm",
        default=True,
        style=inquirer_style
    ).execute()
    if is_confirm:
        registered_softwares.remove(software_name)
        Setting().registered_softwares = registered_softwares


def _unregister_role():
    registered_roles = Setting().registered_roles
    registered_roles = list(
        set(registered_roles)-set(Setting.DEFAULT_SETTING["registered_roles"]))
    if (len(registered_roles) == 0):
        console.print("No registered role found", style="warning")
        return
    software_name = inquirer.fuzzy(
        message="Choose from preunregisters",
        choices=registered_roles,
        style=inquirer_style
    ).execute()
    console.print(software_name)
    is_confirm = inquirer.confirm(
        message="Confirm",
        default=True,
        style=inquirer_style
    ).execute()
    if is_confirm:
        registered_roles.remove(software_name)
        Setting().registered_roles = registered_roles


@click.group(
    'unregister',
    help="Add or update stuffs to omoospace.",
    invoke_without_command=True
)
@click.option(
    "-c", "--creator",
    is_flag=True,
    help=UNREGISTER_CREATOR_HELP
)
@click.option(
    "-so", "--software",
    is_flag=True,
    help=UNREGISTER_SOFTWARE_HELP
)
@click.option(
    "-r", "--role",
    is_flag=True,
    help=UNREGISTER_ROLE_HELP
)
@click.pass_context
def cli_unregister(ctx, creator, software, role):
    if not ctx.invoked_subcommand:
        if creator:
            _unregister_creator()
        elif software:
            _unregister_software()
        elif role:
            _unregister_role()
        else:
            console.print("unregister something")


@click.command('creator', help=UNREGISTER_CREATOR_HELP)
def cli_unregister_creator():
    _unregister_creator()


@click.command('software', help=UNREGISTER_SOFTWARE_HELP)
def cli_unregister_software():
    _unregister_software()


@click.command('role', help=UNREGISTER_ROLE_HELP)
def cli_unregister_role():
    _unregister_role()


cli_unregister.add_command(cli_unregister_creator)
cli_unregister.add_command(cli_unregister_software)
cli_unregister.add_command(cli_unregister_role)

import click
from omoospace.commands.common import get_omoospace, option_omoospace

SHOW_PROFILE_HELP = "Show omoospace profile."
SHOW_DIRECTORY_HELP = "Show omoospace directory tree."
SHOW_SUBSPACES_HELP = "Show omoospace subspace tree."
SHOW_ENTITIES_HELP = "Show omoospace entities."
SHOW_PACKAGES_HELP = "Show omoospace packages."
STRUCTURE_DIR_HELP = "Set Directory of structure.html for structure visualization"


def _show_summary(omoospace,output_dir):
    omoospace = get_omoospace(omoospace)
    omoospace.show_summary(output_dir)


def _show_profile(omoospace):
    omoospace = get_omoospace(omoospace)
    omoospace.show_profile()


def _show_directories(omoospace):
    omoospace = get_omoospace(omoospace)
    omoospace.show_directory_tree()


def _show_subspaces(omoospace):
    omoospace = get_omoospace(omoospace)
    omoospace.show_subspace_tree()


def _show_entities(omoospace):
    omoospace = get_omoospace(omoospace)
    omoospace.show_subspace_entities()


def _show_packages(omoospace):
    omoospace = get_omoospace(omoospace)
    omoospace.show_imported_packages()


@click.group(
    'show',
    help="Show omoospace statistics",
    invoke_without_command=True
)
@click.option(
    "-i", "--profile",
    is_flag=True,
    help=SHOW_PROFILE_HELP
)
@click.option(
    "-d", "--directories",
    is_flag=True,
    help=SHOW_DIRECTORY_HELP
)
@click.option(
    "-s", "--subspaces",
    is_flag=True,
    help=SHOW_SUBSPACES_HELP
)
@click.option(
    "-e", "--entities",
    is_flag=True,
    help=SHOW_ENTITIES_HELP
)
@click.option(
    "-p", "--packages",
    is_flag=True,
    help=SHOW_PACKAGES_HELP
)
@option_omoospace()
@click.option(
    "-r", "--report-dir",
    type=click.Path(),
    help=STRUCTURE_DIR_HELP
)
@click.pass_context
def cli_show(ctx, profile, directories, subspaces, entities, packages, omoospace, report_dir):
    if not ctx.invoked_subcommand:
        if profile:
            _show_profile(omoospace)
        elif directories:
            _show_directories(omoospace)
        elif subspaces:
            _show_subspaces(omoospace)
        elif entities:
            _show_entities(omoospace)
        elif packages:
            _show_packages(omoospace)
        else:
            _show_summary(omoospace, report_dir)


@click.command('profile', help=SHOW_PROFILE_HELP)
@option_omoospace()
def cli_show_profile(omoospace):
    _show_profile(omoospace)


@click.command('directories', help=SHOW_DIRECTORY_HELP)
@option_omoospace()
def cli_show_directories(omoospace):
    _show_directories(omoospace)


@click.command('subspaces', help=SHOW_SUBSPACES_HELP)
@option_omoospace()
def cli_show_subspaces(omoospace):
    _show_subspaces(omoospace)


@click.command('entities', help=SHOW_PACKAGES_HELP)
@option_omoospace()
def cli_show_entities(omoospace):
    _show_entities(omoospace)


@click.command('packages', help=SHOW_ENTITIES_HELP)
@option_omoospace()
def cli_show_packages(omoospace):
    _show_packages(omoospace)


cli_show.add_command(cli_show_directories)
cli_show.add_command(cli_show_subspaces)
cli_show.add_command(cli_show_entities)
cli_show.add_command(cli_show_packages)

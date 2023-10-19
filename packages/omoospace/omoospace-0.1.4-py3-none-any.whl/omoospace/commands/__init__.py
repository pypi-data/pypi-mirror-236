import click
import importlib

from omoospace.commands.create import cli_create
from omoospace.commands.set import cli_set
from omoospace.commands.to import cli_to
from omoospace.commands.export import cli_export
from omoospace.commands.show import cli_show
from omoospace.commands.unregister import cli_unregister
module_import = importlib.import_module("omoospace.commands.import")
cli_import = module_import.cli_import

# TODO: more manage of templates


@click.group()
def cli():
    pass


cli.add_command(cli_set)
cli.add_command(cli_create)
cli.add_command(cli_show)
cli.add_command(cli_to)
cli.add_command(cli_export)
cli.add_command(cli_import)
cli.add_command(cli_unregister)

if __name__ == "__main__":
    cli()

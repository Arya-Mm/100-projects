import click
from .config import load_config
from .utils import greet_user


@click.group()
@click.option(
    "--config", "-c", 
    default="config.json", 
    help="Path to config file."
)
@click.pass_context
def cli(ctx, config):
    """
    This is the main CLI command group.
    It loads the config file and stores it in context for subcommands.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config(config)


@cli.command()
@click.argument("name")
@click.pass_context
def hello(ctx, name):
    """Say hello to a user."""
    cfg = ctx.obj["config"]
    greet_user(name, cfg)


@cli.command()
@click.pass_context
def config(ctx):
    """Show loaded configuration."""
    click.echo(ctx.obj["config"])

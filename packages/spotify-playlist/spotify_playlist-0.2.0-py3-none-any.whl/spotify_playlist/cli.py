import concurrent.futures
import json
import logging
import os
from importlib.metadata import version

import click

from .util import random_list, save_all_lists, save_specific_list

logger = logging.getLogger(__name__)
env = os.environ.get("DEPLOYMENT_ENV", "prod")
log_level = logging.INFO
if env != "prod":
    log_level = logging.DEBUG
logging.basicConfig(level=log_level)


def print_version(ctx, param, value):
    # print(ctx.__dict__)
    # print(param.__dict__)
    # print(value)
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'Version: {version("spotify-playlist")}')
    ctx.exit()


@click.group()
@click.option(
    '--version',
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Package version.",
)
def cli():
    os.chdir("F:/repos/spotify-playlist")
    pass


@cli.command()
@click.option(
    "--client-id", "-i",
    default="0870ef8bcf4c4cb486ff36b7be69ff94",
    show_default=True,
    type=str,
    required=False,
    help="client id",
)
@click.option(
    "--client-secret", "-s",
    default="00fd11990b6f40b6b4dd043500429f7d",
    show_default=True,
    type=str,
    required=False,
    help="client secret",
)
@click.option(
    "--redirect", "-r",
    default="https://localhost:8080/callback",
    show_default=True,
    type=str,
    required=False,
    help="redirect url",
)
def all(**kwargs):
    env = {
        "SPOTIPY_CLIENT_ID": kwargs.get("client_id"),
        "SPOTIPY_CLIENT_SECRET": kwargs.get("client_secret"),
        "SPOTIPY_REDIRECT_URI": kwargs.get("redirect")
    }
    save_all_lists(env)


@cli.command()
@click.option(
    "--client-id", "-i",
    default="0870ef8bcf4c4cb486ff36b7be69ff94",
    show_default=True,
    type=str,
    required=False,
    help="client id",
)
@click.option(
    "--client-secret", "-s",
    default="00fd11990b6f40b6b4dd043500429f7d",
    show_default=True,
    type=str,
    required=False,
    help="client secret",
)
@click.option(
    "--redirect", "-r",
    default="https://localhost:8080/callback",
    show_default=True,
    type=str,
    required=False,
    help="redirect url",
)
@click.argument('playlist', nargs=-1)
def name(**kwargs):
    env = {
        "SPOTIPY_CLIENT_ID": kwargs.get("client_id"),
        "SPOTIPY_CLIENT_SECRET": kwargs.get("client_secret"),
        "SPOTIPY_REDIRECT_URI": kwargs.get("redirect")
    }
    save_specific_list(env, kwargs.get("playlist"))


@cli.command()
@click.option(
    "--client-id", "-i",
    default="0870ef8bcf4c4cb486ff36b7be69ff94",
    show_default=True,
    type=str,
    required=False,
    help="client id",
)
@click.option(
    "--client-secret", "-s",
    default="00fd11990b6f40b6b4dd043500429f7d",
    show_default=True,
    type=str,
    required=False,
    help="client secret",
)
@click.option(
    "--redirect", "-r",
    default="https://localhost:8080/callback",
    show_default=True,
    type=str,
    required=False,
    help="redirect url",
)
def rand(**kwargs):
    env = {
        "SPOTIPY_CLIENT_ID": kwargs.get("client_id"),
        "SPOTIPY_CLIENT_SECRET": kwargs.get("client_secret"),
        "SPOTIPY_REDIRECT_URI": kwargs.get("redirect")
    }
    random_list(env)


if __name__ == "__main__":
    cli()

import shutil

import click
from git import Repo
from slugify import slugify

from .utils import Config, FunctionArgumentsParser, Zipper


@click.group()
def cli():
    pass


@cli.group()
def config():
    """Edit Open NU config"""
    pass


@config.command()
@click.argument("token")
def auth_key(token):
    """Set Open NU Authentication token"""
    Config.write_auth_key(token)
    click.echo(f"Set auth token to: {token}")


@config.command()
@click.argument("url")
def server_url(url):
    """Set Open NU server base URL"""
    Config.write_base_url(url)
    click.echo(f"Set server URL to: {url}")


@cli.group()
def function():
    """Function related utility"""
    pass


@function.command()
@click.argument("name")
def init(name):
    slug_name = slugify(name)
    click.echo(f"Init new function: {slug_name}")
    Repo.clone_from("https://github.com/open-nu/python-template.git", slug_name)

    yaml_path = f"{slug_name}/config.yaml"
    config_yaml = None
    with open(yaml_path, "r") as file:
        config_yaml = file.read()

    config_yaml = config_yaml.replace("AppName: 'Sample App'", f"AppName: '{slug_name}'")  # TODO
    with open(yaml_path, "w") as file:
        file.write(config_yaml)

    shutil.rmtree(f"{slug_name}/.git")
    print("Done")


@function.command()
def deploy():
    click.echo(f"Deploy new function")

    auth_key = Config.get_auth_key()

    click.echo("Parsing args")
    args_json = FunctionArgumentsParser().find_and_get_json()

    click.echo(f"Zipping files")
    zipper = Zipper()
    zipper.zip_files()

    click.echo(f"uploading files")
    zipper.upload_zip()

    print("Done")

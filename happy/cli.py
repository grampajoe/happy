"""
The command-line interface for happy!
"""
import json
import os
import subprocess
import sys

import click

import happy


def _infer_tarball_url():
    """Returns the tarball URL inferred from an app.json, if present."""
    try:
        with click.open_file('app.json', 'r') as f:
            contents = f.read()

        app_json = json.loads(contents)
    except IOError:
        return None

    return app_json.get('repository') + '/tarball/master/'


def _write_app_name(app_name):
    """Writes the app name to the .happy file."""
    with click.open_file('.happy', 'w') as f:
        f.write(str(app_name))


def _read_app_name():
    """Reads the app name from the .happy file."""
    try:
        with click.open_file('.happy', 'r') as f:
            return f.read().strip()
    except IOError:
        return None


def _delete_app_name_file():
    """Deletes the .happy file. :("""
    os.remove('.happy')


@click.group(name='happy')
def cli():
    """Quickly set up and tear down Heroku apps!"""


@cli.command(name='up')
@click.option('--tarball-url', help='URL of the tarball containing app.json.')
def up(tarball_url):
    """Brings up a Heroku app."""
    tarball_url = tarball_url or _infer_tarball_url()

    if not tarball_url:
        click.echo('No tarball URL found.')
        sys.exit(1)

    click.echo('Creating app... ', nl=False)

    build_id, app_name = happy.create(tarball_url=tarball_url)

    click.echo(app_name)

    click.echo('Building... ', nl=False)

    happy.wait(build_id)

    _write_app_name(app_name)

    click.echo('done')
    click.echo("It's up! :) https://%s.herokuapp.com" % app_name)


@cli.command(name='down')
def down():
    """Brings down a Heroku app."""
    app_name = _read_app_name()

    if not app_name:
        click.echo('No app is running.')
        sys.exit(1)

    click.echo('Destroying app %s... ' % app_name, nl=False)

    happy.delete(app_name=app_name)

    _delete_app_name_file()

    click.echo('done')
    click.echo("It's down. :(")

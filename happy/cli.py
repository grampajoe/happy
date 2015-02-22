"""
The command-line interface for happy!
"""
import json
import os
import subprocess
import sys

import click

from happy import Happy


def _infer_tarball_url():
    """Returns the tarball URL inferred from an app.json, if present."""
    try:
        with click.open_file('app.json', 'r') as f:
            contents = f.read()

        app_json = json.loads(contents)
    except IOError:
        return None

    repository = app_json.get('repository')

    if not repository:
        return None
    else:
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
@click.option('--auth-token', help='Heroku API auth token.')
@click.option('--env', multiple=True, help='Env override, e.g. KEY=value.')
def up(tarball_url, auth_token, env):
    """Brings up a Heroku app."""
    tarball_url = tarball_url or _infer_tarball_url()

    if not tarball_url:
        click.echo('No tarball URL found.')
        sys.exit(1)

    if env:
        # Split ["KEY=value", ...] into {"KEY": "value", ...}
        env = {
            arg.split('=')[0]: arg.split('=')[1]
            for arg in env
        }

    happy = Happy(auth_token=auth_token)

    click.echo('Creating app... ', nl=False)

    build_id, app_name = happy.create(tarball_url=tarball_url, env=env)

    click.echo(app_name)

    click.echo('Building... ', nl=False)

    happy.wait(build_id)

    _write_app_name(app_name)

    click.echo('done')
    click.echo("It's up! :) https://%s.herokuapp.com" % app_name)


@cli.command(name='down')
@click.option('--auth-token', help='Heroku API auth token.')
def down(auth_token):
    """Brings down a Heroku app."""
    app_name = _read_app_name()

    if not app_name:
        click.echo('No app is running.')
        sys.exit(1)

    happy = Happy(auth_token=auth_token)

    click.echo('Destroying app %s... ' % app_name, nl=False)

    happy.delete(app_name=app_name)

    _delete_app_name_file()

    click.echo('done')
    click.echo("It's down. :(")

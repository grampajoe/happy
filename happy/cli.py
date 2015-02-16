"""
The command-line interface for happy!
"""
import json
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

    _write_app_name(app_name)

    click.echo('Building... ', nl=False)

    happy.wait(build_id)

    click.echo('done')
    click.echo("It's up! :) https://%s.herokuapp.com" % app_name)

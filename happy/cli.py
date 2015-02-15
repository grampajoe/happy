"""
The command-line interface for happy!
"""
import click

import happy


@click.group(name='happy')
def cli():
    """Quickly set up and tear down Heroku apps!"""


@cli.command(name='up')
def command_up():
    """Brings up a Heroku app."""
    happy.up()

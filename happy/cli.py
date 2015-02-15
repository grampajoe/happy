"""
The command-line interface for happy!
"""
import click


@click.group(name='happy')
def cli():
    """Quickly set up and tear down Heroku apps!"""

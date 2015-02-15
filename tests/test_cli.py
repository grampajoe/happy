"""
Tests for the cli commands.
"""
import mock
from click.testing import CliRunner

from happy.cli import cli


def test_help():
    """Running happy should print the help."""
    runner = CliRunner()

    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert 'Usage: happy' in result.output


@mock.patch('happy.up')
def test_up(up):
    """`happy up` should call happy:up."""
    runner = CliRunner()

    result = runner.invoke(cli, ['up'])

    assert result.exit_code == 0
    assert up.called

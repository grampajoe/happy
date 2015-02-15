"""
Tests for the cli commands.
"""
from click.testing import CliRunner

from happy.cli import cli


def test_help():
    """Running happy should print the help."""
    runner = CliRunner()

    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert 'Usage: happy' in result.output

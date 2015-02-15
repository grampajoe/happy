"""
Tests for the cli commands.
"""
import subprocess

import mock
import pytest
from click.testing import CliRunner

from happy.cli import cli


@pytest.fixture
def runner():
    """Returns a CliRunner instance."""
    return CliRunner()


@pytest.fixture
def auth_token():
    """Returns the current user's Heroku auth token."""
    output = subprocess.check_output(['heroku', 'auth:token'])
    return output.decode().strip()


def test_help(runner):
    """Running happy should print the help."""
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert 'Usage: happy' in result.output


@mock.patch('happy.up')
def test_up(up, runner):
    """`happy up` should call happy:up."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['up', '--tarball-url=example.com'])

    assert result.exit_code == 0
    assert up.called


@mock.patch('happy.up')
def test_up_tarball_url(up, runner):
    """`happy up` should pass in the --tarball-url option."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ['up', '--tarball-url=example.com'])

    args_, kwargs = up.call_args

    assert kwargs['tarball_url'] == 'example.com'


@mock.patch('happy.up')
def test_up_tarball_url_app_json(up, runner):
    """`happy up` should infer the tarball URL from app.json."""
    with runner.isolated_filesystem():
        with open('app.json', 'w') as f:
            f.write('{"repository": "https://github.com/butt/man"}')

        runner.invoke(cli, ['up'])

    args_, kwargs = up.call_args

    assert kwargs['tarball_url'] == \
        'https://github.com/butt/man/tarball/master/'


@mock.patch('happy.up')
def test_up_no_tarball_url(up, runner):
    """`happy up` should fail if it can't infer the tarball URL."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['up'])

    assert result.exit_code == 1
    assert 'no tarball' in result.output.lower()


@mock.patch('happy.up')
def test_up_writes_app_name(up, runner):
    """`happy up` should write the app name to .happy."""
    up.return_value = 'butt-man-123'

    with runner.isolated_filesystem():
        runner.invoke(cli, ['up', '--tarball-url=example.com'])

        with open('.happy') as f:
            app_name = f.read()

    assert app_name == 'butt-man-123'


@mock.patch('happy.up')
def test_up_prints_info(up, runner):
    """`happy.up` should print status info."""
    up.return_value = 'butt-man-123'

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['up', '--tarball-url=example.com'])

    expected = (
        "Creating app...\n"
        "It's up! :) https://butt-man-123.herokuapp.com\n"
    )

    assert result.output == expected

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


@mock.patch('happy.wait')
@mock.patch('happy.create')
def test_up(create, wait, runner):
    """`happy up` should call happy:create and happy:wait."""
    create.return_value = ('12345', 'butt-man-123')

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['up', '--tarball-url=example.com'])

    assert result.exit_code == 0
    assert create.called
    assert wait.called


@mock.patch('happy.wait')
@mock.patch('happy.create')
def test_up_tarball_url(create, wait, runner):
    """`happy up` should pass in the --tarball-url option."""
    create.return_value = ('12345', 'butt-man-123')

    with runner.isolated_filesystem():
        runner.invoke(cli, ['up', '--tarball-url=example.com'])

    args_, kwargs = create.call_args

    assert kwargs['tarball_url'] == 'example.com'


@mock.patch('happy.wait')
@mock.patch('happy.create')
def test_up_tarball_url_app_json(create, wait, runner):
    """`happy up` should infer the tarball URL from app.json."""
    create.return_value = ('12345', 'butt-man-123')

    with runner.isolated_filesystem():
        with open('app.json', 'w') as f:
            f.write('{"repository": "https://github.com/butt/man"}')

        runner.invoke(cli, ['up'])

    args_, kwargs = create.call_args

    assert kwargs['tarball_url'] == \
        'https://github.com/butt/man/tarball/master/'


@mock.patch('happy.wait')
@mock.patch('happy.create')
def test_up_no_tarball_url(create, wait, runner):
    """`happy up` should fail if it can't infer the tarball URL."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['up'])

    assert result.exit_code == 1
    assert 'no tarball' in result.output.lower()


@mock.patch('happy.wait')
@mock.patch('happy.create')
def test_up_writes_app_name(create, wait, runner):
    """`happy up` should write the app name to .happy."""
    create.return_value = ('12345', 'butt-man-123')

    with runner.isolated_filesystem():
        runner.invoke(cli, ['up', '--tarball-url=example.com'])

        with open('.happy') as f:
            app_name = f.read()

    assert app_name == 'butt-man-123'


@mock.patch('happy.wait')
@mock.patch('happy.create')
def test_up_prints_info(create, wait, runner):
    """`happy.up` should print status info."""
    create.return_value = ('12345', 'butt-man-123')

    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['up', '--tarball-url=example.com'])

    expected = (
        "Creating app... butt-man-123\n"
        "Building... done\n"
        "It's up! :) https://butt-man-123.herokuapp.com\n"
    )

    assert result.output == expected

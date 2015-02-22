"""
Tests for the cli commands.
"""
import subprocess
from functools import wraps

import mock
import pytest
from click.testing import CliRunner

from happy.cli import cli


@pytest.fixture
def happy(request):
    """Returns a mocked Happy class."""
    patcher = mock.patch('happy.cli.Happy')
    cls = patcher.start()

    def teardown():
        """Stops the patcher."""
        patcher.stop()
    request.addfinalizer(teardown)

    happy_instance = cls()
    happy_instance.create.return_value = ('12345', 'butt-man-123')

    return cls


@pytest.fixture
def runner():
    """Returns a CliRunner instance."""
    return CliRunner()


def isolated(func):
    """Runs a method in an isolated filesystem.

    This also stubs out an app.json for convenience.
    """
    @wraps(func)
    def wrapped(runner, *args, **kwargs):
        with runner.isolated_filesystem():
            with open('app.json', 'w') as f:
                f.write('{"repository": "https://github.com/butt/man"}')

            return func(runner, *args, **kwargs)

    return wrapped


def test_help(runner):
    """Running happy should print the help."""
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert 'Usage: happy' in result.output


@isolated
def test_up(runner, happy):
    """Running up should exit cleanly."""
    result = runner.invoke(cli, ['up'])

    assert result.exit_code == 0


@isolated
def test_up_app_name(runner, happy):
    """Running up should pass the first param as the app name."""
    runner.invoke(cli, ['up', 'app-name-123'])

    args_, kwargs = happy().create.call_args

    assert kwargs['app_name'] == 'app-name-123'


@isolated
def test_up_auth_token(runner, happy):
    """Running up should pass the --auth-token option to Happy."""
    runner.invoke(cli, [
        'up',
        '--auth-token=12345',
    ])

    args_, kwargs = happy.call_args

    assert kwargs['auth_token'] == '12345'


@isolated
def test_up_tarball_url(runner, happy):
    """Running up should pass the --tarball-url option to Happy.create."""
    runner.invoke(cli, ['up', '--tarball-url=passed-in.com'])

    args_, kwargs = happy().create.call_args

    assert kwargs['tarball_url'] == 'passed-in.com'


@isolated
def test_up_tarball_url_app_json(runner, happy):
    """Running up should infer the tarball URL from app.json."""
    runner.invoke(cli, ['up'])

    args_, kwargs = happy().create.call_args

    assert kwargs['tarball_url'] == \
        'https://github.com/butt/man/tarball/master/'


@isolated
def test_up_no_tarball_url(runner, happy):
    """Running up should fail if it can't infer the tarball URL."""
    with open('app.json', 'w') as f:
        f.write('{"description": "No repository????"}')

    result = runner.invoke(cli, ['up'])

    assert result.exit_code == 1
    assert 'no tarball' in result.output.lower()


@isolated
def test_up_env(runner, happy):
    """Running up --env should pass environment overrides."""
    runner.invoke(cli, [
        'up',
        '--env',
        'FART=test',
        '--env',
        'BUTT=wow',
    ])

    args_, kwargs = happy().create.call_args

    assert kwargs['env'] == {
        'FART': 'test',
        'BUTT': 'wow',
    }


@isolated
def test_up_writes_app_name(runner, happy):
    """Running up should write the app name to .happy."""
    runner.invoke(cli, ['up'])

    with open('.happy') as f:
        app_name = f.read()

    assert app_name == 'butt-man-123'


@isolated
def test_up_waits_for_build(runner, happy):
    """The up command should wait for builds to complete."""
    runner.invoke(cli, ['up'])

    assert happy().wait.called


@isolated
def test_up_prints_info(runner, happy):
    """Running up should print status info."""
    result = runner.invoke(cli, ['up'])

    assert result.output == (
        "Creating app... butt-man-123\n"
        "Building... done\n"
        "It's up! :) https://butt-man-123.herokuapp.com\n"
    )


@isolated
def test_down(runner, happy):
    """Running down should delete the app."""
    with open('.happy', 'w') as f:
        f.write('butt-man-123')

    result = runner.invoke(cli, ['down'])

    happy().delete.assert_called_with(app_name='butt-man-123')
    assert result.exit_code == 0


@isolated
def test_down_auth_token(runner, happy):
    """Running down should pass the --auth-token option to Happy."""
    with open('.happy', 'w') as f:
        f.write('butt-man-123')

    runner.invoke(cli, [
        'down',
        '--auth-token=12345',
    ])

    args_, kwargs = happy.call_args

    assert kwargs['auth_token'] == '12345'


@isolated
def test_down_deletes_app_name_file(runner, happy):
    """Running down should delete the .happy file."""
    with open('.happy', 'w') as f:
        f.write('butt-man-123')

    runner.invoke(cli, ['down'])

    with pytest.raises(IOError):
        open('.happy', 'r')


@isolated
def test_down_no_app(runner, happy):
    """With no app to delete, down should fail."""
    result = runner.invoke(cli, ['down'])

    assert happy().delete.called is False
    assert result.exit_code == 1


@isolated
def test_down_prints_info(runner, happy):
    """Running down should print status info."""
    with open('.happy', 'w') as f:
        f.write('butt-man-123')

    result = runner.invoke(cli, ['down'])

    assert result.output == (
        "Destroying app butt-man-123... done\n"
        "It's down. :(\n"
    )

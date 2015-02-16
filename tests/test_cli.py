"""
Tests for the cli commands.
"""
import subprocess

import mock
import pytest
from click.testing import CliRunner

from happy.cli import cli


@pytest.fixture
def happy(request):
    """Returns a mocked Happy instance."""
    patcher = mock.patch('happy.cli.Happy')
    cls = patcher.start()

    def teardown():
        """Stops the patcher."""
        patcher.stop()
    request.addfinalizer(teardown)

    happy_instance = cls()
    happy_instance.create.return_value = ('12345', 'butt-man-123')

    return happy_instance


@pytest.fixture
def runner():
    """Returns a CliRunner instance."""
    return CliRunner()


def test_help(runner):
    """Running happy should print the help."""
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert 'Usage: happy' in result.output


def test_up(happy, runner):
    """Running up should exit cleanly."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['up', '--tarball-url=example.com'])

    assert result.exit_code == 0


def test_up_tarball_url(happy, runner):
    """Running up should pass the --tarball-url option to Happy.create."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ['up', '--tarball-url=example.com'])

    args_, kwargs = happy.create.call_args

    assert kwargs['tarball_url'] == 'example.com'


def test_up_tarball_url_app_json(happy, runner):
    """Running up should infer the tarball URL from app.json."""
    with runner.isolated_filesystem():
        with open('app.json', 'w') as f:
            f.write('{"repository": "https://github.com/butt/man"}')

        runner.invoke(cli, ['up'])

    args_, kwargs = happy.create.call_args

    assert kwargs['tarball_url'] == \
        'https://github.com/butt/man/tarball/master/'


def test_up_no_tarball_url(happy, runner):
    """Running up should fail if it can't infer the tarball URL."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['up'])

    assert result.exit_code == 1
    assert 'no tarball' in result.output.lower()


def test_up_writes_app_name(happy, runner):
    """Running up should write the app name to .happy."""
    with runner.isolated_filesystem():
        runner.invoke(cli, ['up', '--tarball-url=example.com'])

        with open('.happy') as f:
            app_name = f.read()

    assert app_name == 'butt-man-123'


def test_up_waits_for_build(happy, runner):
    """The up command should wait for builds to complete."""


def test_up_prints_info(happy, runner):
    """Running up should print status info."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['up', '--tarball-url=example.com'])

    assert result.output == (
        "Creating app... butt-man-123\n"
        "Building... done\n"
        "It's up! :) https://butt-man-123.herokuapp.com\n"
    )


def test_down(happy, runner):
    """Running down should delete the app."""
    with runner.isolated_filesystem():
        with open('.happy', 'w') as f:
            f.write('butt-man-123')

        result = runner.invoke(cli, ['down'])

    happy.delete.assert_called_with(app_name='butt-man-123')
    assert result.exit_code == 0


def test_down_deletes_app_name_file(happy, runner):
    """Running down should delete the .happy file."""
    with runner.isolated_filesystem():
        with open('.happy', 'w') as f:
            f.write('butt-man-123')

        runner.invoke(cli, ['down'])

        with pytest.raises(IOError):
            open('.happy', 'r')


def test_down_no_app(happy, runner):
    """With no app to delete, down should fail."""
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['down'])

    assert happy.delete.called is False
    assert result.exit_code == 1


def test_down_prints_info(happy, runner):
    """Running down should print status info."""
    with runner.isolated_filesystem():
        with open('.happy', 'w') as f:
            f.write('butt-man-123')

        result = runner.invoke(cli, ['down'])

    assert result.output == (
        "Destroying app butt-man-123... done\n"
        "It's down. :(\n"
    )

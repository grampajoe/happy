"""
Tests for core happy functionality.
"""
import mock
import pytest

import happy
from happy.heroku import Heroku


@pytest.fixture
def heroku(request):
    patcher = mock.patch('happy.Heroku')
    cls = patcher.start()

    def teardown():
        patcher.stop()
    request.addfinalizer(teardown)

    return cls()


def test_up(heroku):
    """Should create an app build on Heroku."""
    happy.up(tarball_url='tarball-url')

    heroku.create_build.assert_called_with(tarball_url='tarball-url')


def test_up_returns_app_name(heroku):
    """Should return the app name from the build."""
    heroku.create_build.return_value = {
        'app': {
            'name': 'butt-man-123',
        },
    }

    app_name = happy.up(tarball_url='example.com')

    assert app_name == 'butt-man-123'

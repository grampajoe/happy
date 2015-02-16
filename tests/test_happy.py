"""
Tests for core happy functionality.
"""
import mock
import pytest

from happy import Happy


@pytest.fixture
def happy():
    return Happy()


@pytest.fixture
def heroku(request):
    patcher = mock.patch('happy.Heroku')
    cls = patcher.start()

    def teardown():
        patcher.stop()
    request.addfinalizer(teardown)

    return cls


def test_auth_token(heroku):
    """Happy should pass an API token to Heroku."""
    happy = Happy(auth_token='12345')

    happy.create('example.com')

    args_, kwargs = heroku.call_args

    assert kwargs['auth_token'] == '12345'


def test_create(heroku, happy):
    """Should create an app build on Heroku."""
    happy.create(tarball_url='tarball-url')

    heroku().create_build.assert_called_with(tarball_url='tarball-url')


def test_create_returns_app_name(heroku, happy):
    """Should return the app name and id from the build."""
    heroku().create_build.return_value = {
        'id': '12345',
        'app': {
            'name': 'butt-man-123',
        },
    }

    build_id, app_name = happy.create(tarball_url='example.com')

    assert build_id == '12345'
    assert app_name == 'butt-man-123'


def test_wait(heroku, happy):
    """Should wait for the build to complete."""
    heroku().check_build_status.side_effect = (False, False, True)

    with mock.patch('happy.sleep'):  # Ain't nobody got time etc.
        happy.wait('12345')

    heroku().check_build_status.assert_has_calls([
        mock.call('12345'),
        mock.call('12345'),
        mock.call('12345'),
    ])


def test_delete(heroku, happy):
    """Should delete the app."""
    happy.delete(app_name='butt-man-123')

    heroku().delete_app.assert_called_with(app_name='butt-man-123')

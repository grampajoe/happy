"""
Tests for Heroku API interaction.
"""
import json
import mock
import pytest

from happy.heroku import Heroku, APIError, BuildError


def test_heroku():
    """The Heroku class should initialize."""
    heroku = Heroku()

    assert heroku


@mock.patch('happy.heroku.Session')
def test_heroku_api_request(session):
    """Heroku.api_request should send an API request."""
    heroku = Heroku()

    heroku.api_request(
        'POST',
        '/endpoint',
        data={'butt': 'man'},
        headers={'test': 'header'},
    )

    session().request.assert_called_with(
        'POST',
        'https://api.heroku.com/endpoint',
        data=json.dumps({'butt': 'man'}),
        headers={
            'test': 'header',
        },
    )


@mock.patch('happy.heroku.Session')
def test_heroku_api_request_headers(session):
    """Heroku.api_request should attach common headers to the session."""
    heroku = Heroku()

    heroku.api_request('GET', '/test')

    assert session().trust_env
    assert session().headers == {
        'Content-type': 'application/json',
        'Accept': 'application/vnd.heroku+json; version=3',
    }


@mock.patch('happy.heroku.Session')
def test_heroku_api_request_auth_token(session):
    """Heroku.api_request should send its auth token."""
    heroku = Heroku(auth_token='12345')

    heroku.api_request('GET', '/test')

    assert session().trust_env is False
    assert session().headers['Authorization'] == 'Bearer 12345'


@mock.patch('happy.heroku.Session')
def test_heroku_api_request_fail(session):
    """Heroku.api_request should raise APIError on failures."""
    heroku = Heroku()

    bad_response = mock.Mock(ok=False)
    bad_response.json.return_value = {
        'id': 'beta_tayne',
        'message': 'IMPROPER CODING',
    }

    session().request.return_value = bad_response

    with pytest.raises(APIError) as exc:
        heroku.api_request('GET', '/celery-man', data={
            'dancer': 'Tayne',
            'dance': 'flarhgunnstow',
            '4d3d3d3': 'true',
        })

    assert 'IMPROPER CODING' in str(exc.value)


@mock.patch('happy.heroku.Session')
def test_heroku_api_request_big_fail(session):
    """Heroku.api_request should raise all content if it's not JSON."""
    heroku = Heroku()

    bad_response = mock.Mock(ok=False, content='not JSON at all')
    bad_response.json.side_effect = ValueError('Bad JSON????')

    session().request.return_value = bad_response

    with pytest.raises(APIError) as exc:
        heroku.api_request('GET', '/something')

    assert 'not JSON at all' in str(exc.value)


@mock.patch.object(Heroku, 'api_request')
def test_heroku_create_build(api_request):
    """Heroku.create_build should send a POST to /app-setups."""
    fake_json = {
        'app': {
            'name': 'butt-man-123',
        },
    }
    api_request.return_value = fake_json

    heroku = Heroku()

    result = heroku.create_build('tarball-url')

    api_request.assert_called_with(
        'POST',
        '/app-setups',
        data={'source_blob': {'url': 'tarball-url'}},
    )

    assert result == fake_json


@mock.patch.object(Heroku, 'api_request')
def test_heroku_create_build_env(api_request):
    """Heroku.create_build should send env overrides."""
    heroku = Heroku()

    result = heroku.create_build('tarball-url', env={'HELLO': 'world'})

    api_request.assert_called_with(
        'POST',
        '/app-setups',
        data={
            'source_blob': {'url': 'tarball-url'},
            'overrides': {'env': {'HELLO': 'world'}},
        },
    )


@mock.patch.object(Heroku, 'api_request')
def test_heroku_create_build_app_name(api_request):
    """Heroku.create_build should send the app name."""
    heroku = Heroku()

    result = heroku.create_build('tarball-url', app_name='app-name-123')

    api_request.assert_called_with(
        'POST',
        '/app-setups',
        data={
            'source_blob': {'url': 'tarball-url'},
            'app': {'name': 'app-name-123'},
        },
    )


@mock.patch.object(Heroku, 'api_request')
def test_heroku_check_build_status(api_request):
    """Heroku.check_build_status should send a GET to /app-setups/:id."""
    api_request.return_value = {'status': 'pending'}
    heroku = Heroku()

    heroku.check_build_status('123')

    api_request.assert_called_with('GET', '/app-setups/123')


@mock.patch.object(Heroku, 'api_request')
def test_heroku_check_build_status_pending(api_request):
    """Heroku.check_build_status should return False on pending."""
    api_request.return_value = {'status': 'pending'}

    heroku = Heroku()

    assert not heroku.check_build_status('123')


@mock.patch.object(Heroku, 'api_request')
def test_heroku_check_build_status_succeeded(api_request):
    """Heroku.check_build_status should return True on succeeded."""
    api_request.return_value = {'status': 'succeeded'}

    heroku = Heroku()

    assert heroku.check_build_status('123')


@mock.patch.object(Heroku, 'api_request')
def test_heroku_check_build_status_failed(api_request):
    """Heroku.check_build_status should raise BuildError on failed."""
    api_request.return_value = result = {
        'status': 'failed',
        'failure_message': 'oops',
    }

    heroku = Heroku()

    with pytest.raises(BuildError) as exc:
        heroku.check_build_status('123')

    assert str(result) in str(exc.value)


@mock.patch.object(Heroku, 'api_request')
def test_heroku_delete_app(api_request):
    """Heroku.delete_app should delete an app."""
    heroku = Heroku()

    heroku.delete_app(app_name='butt-man-123')

    api_request.assert_called_with(
        'DELETE',
        '/apps/butt-man-123',
    )

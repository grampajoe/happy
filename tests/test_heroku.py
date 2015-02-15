"""
Tests for Heroku API interaction.
"""
import json
import mock
import pytest

from happy.heroku import Heroku, APIError


def test_heroku():
    """The Heroku class should initialize."""
    heroku = Heroku()

    assert heroku


@mock.patch('happy.heroku.requests')
def test_heroku_api_request(requests):
    """Heroku.api_request should send an API request."""
    heroku = Heroku()

    heroku.api_request(
        'POST',
        '/endpoint',
        data={'butt': 'man'},
        headers={'test': 'header'},
    )

    requests.request.assert_called_with(
        'POST',
        'https://api.heroku.com/endpoint',
        data=json.dumps({'butt': 'man'}),
        headers={
            'Content-type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3',
            'test': 'header',
        },
    )


@mock.patch('happy.heroku.requests')
def test_heroku_api_request_fail(requests):
    """Heroku.api_request should raise APIError on failures."""
    heroku = Heroku()

    bad_response = mock.Mock(ok=False)
    bad_response.json.return_value = {
        'id': 'beta_tayne',
        'message': 'IMPROPER CODING',
    }

    requests.request.return_value = bad_response

    with pytest.raises(APIError) as exc:
        heroku.api_request('GET', '/celery-man', data={
            'dancer': 'Tayne',
            'dance': 'flarhgunnstow',
            '4d3d3d3': 'true',
        })

    assert 'IMPROPER CODING' in str(exc.value)


@mock.patch('happy.heroku.requests')
def test_heroku_api_request_big_fail(requests):
    """Heroku.api_request should raise all content if it's not JSON."""
    heroku = Heroku()

    bad_response = mock.Mock(ok=False, content='not JSON at all')
    bad_response.json.side_effect = ValueError('Bad JSON????')

    requests.request.return_value = bad_response

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

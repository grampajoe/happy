"""
Heroku API helpers.
"""
import json

import requests


class APIError(Exception):
    """A Heroku API error!!! Oh no!!!!!!!"""


class BuildError(Exception):
    """Something went wrong with the build!!!!!"""


class Heroku():
    """Methods for interacting with the Heroku API."""
    def api_request(self, method, endpoint, data=None, *args, **kwargs):
        """Sends an API request to Heroku.

        :param method: HTTP method.
        :param endpoint: API endpoint, e.g. ``/apps``.
        :param data: A dict sent as JSON in the body of the request.
        :returns: A dict represntation of the JSON response.
        """
        api_root = 'https://api.heroku.com'
        url = api_root + endpoint

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3',
        }

        if data:
            data = json.dumps(data)

        kwargs.setdefault('headers', {})
        kwargs['headers'].update(headers)

        response = requests.request(method, url, data=data, *args, **kwargs)

        if not response.ok:
            try:
                message = response.json().get('message')
            except ValueError:
                message = response.content

            raise APIError(message)

        return response.json()

    def create_build(self, tarball_url):
        """Creates an app-setups build. Returns response data as a dict.

        :param tarball_url: URL of a tarball containing an ``app.json``.
        :returns: Response data as a ``dict``.
        """
        data = {
            'source_blob': {
                'url': tarball_url
            }
        }

        return self.api_request('POST', '/app-setups', data=data)

    def check_build_status(self, build_id):
        """Checks the status of an app-setups build.

        :param build_id: ID of the build to check.
        :returns: ``True`` if succeeded, ``False`` if pending.
        """
        data = self.api_request('GET', '/app-setups/%s' % build_id)

        status = data.get('status')

        if status == 'pending':
            return False
        elif status == 'succeeded':
            return True
        else:
            raise BuildError(data.get('failure_message'))

    def delete_app(self, app_name):
        """Deletes an app.

        :param app_name: Name of the app to delete.
        """
        self.api_request('DELETE', '/apps/%s' % app_name)

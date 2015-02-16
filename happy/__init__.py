"""
Quickly set up and tear down Heroku apps!
"""
from .heroku import Heroku

from time import sleep


class Happy(object):
    """The happiest interface of all."""
    def __init__(self, auth_token=None):
        """Initializes the class.

        :param auth_token: A Heroku API auth token.
        """
        self._api = Heroku(auth_token=auth_token)

    def create(self, tarball_url):
        """Creates a Heroku app-setup build.

        :param tarball_url: URL of a tarball containing an ``app.json``.
        :returns: A tuple with ``(build_id, app_name)``.
        """
        data = self._api.create_build(tarball_url=tarball_url)

        return (data['id'], data['app']['name'])

    def wait(self, build_id):
        """Waits for an app-setup build to finish.

        :param build_id: ID of the app-setup build for which to wait.
        """
        while True:
            if self._api.check_build_status(build_id):
                break
            sleep(3)

    def delete(self, app_name):
        """Deletes a Heroku app.

        :param app_name: Name of the Heroku app to delete.
        """
        self._api.delete_app(app_name=app_name)

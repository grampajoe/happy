"""
Quickly set up and tear down Heroku apps!
"""
from .heroku import Heroku

from time import sleep


def create(tarball_url):
    """Creates a Heroku app-setup build.

    :param tarball_url: URL of a tarball containing an ``app.json``.
    :returns: A tuple with ``(build_id, app_name)``.
    """
    api = Heroku()

    data = api.create_build(tarball_url=tarball_url)

    return (data['id'], data['app']['name'])


def wait(build_id):
    """Waits for an app-setup build to finish.

    :param build_id: ID of the app-setup build for which to wait.
    """
    api = Heroku()

    while True:
        if api.check_build_status(build_id):
            break
        sleep(3)


def delete(app_name):
    """Deletes a Heroku app.

    :param app_name: Name of the Heroku app to delete.
    """
    api = Heroku()

    api.delete_app(app_name=app_name)

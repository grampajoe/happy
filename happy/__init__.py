"""
Quickly set up and tear down Heroku apps!
"""
from .heroku import Heroku


def up(tarball_url):
    """Brings up a Heroku app.

    :param tarball_url: URL of a tarball containing an ``app.json``.
    :returns: The app name.
    """
    api = Heroku()

    data = api.create_build(tarball_url=tarball_url)

    return data['app']['name']

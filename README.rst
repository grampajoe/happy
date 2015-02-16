happy
=====

.. image:: https://img.shields.io/travis/grampajoe/happy.svg
  :target: https://travis-ci.org/grampajoe/happy
.. image:: https://img.shields.io/coveralls/grampajoe/happy.svg
  :target: https://coveralls.io/r/grampajoe/happy
.. image:: https://img.shields.io/scrutinizer/g/grampajoe/happy.svg
  :target: https://scrutinizer-ci.com/g/grampajoe/happy/

Quickly set up and tear down Heroku apps!

Quickly starting
----------------

Add an `app.json manifest`_
that looks kinda like this:

.. code:: json

  {
    "name": "My App Thing",
    "repository": "https://github.com/helloitsme/thingy",
    "env": {
      "FROBULATION_LIMIT": {
        "description": "Maximum frobulations per lunar cycle.",
        "value": "7"
      }
    },
    "addons": [
      "pusher"
    ]
  }

Push that to your thing's ``master`` branch on GitHub so Heroku can find it.

Log in with the `Heroku toolbelt`_ , then do this:

.. code:: text

  $ pip install happy
  $ happy up
  Creating app... butt-man-123
  Building... done
  It's up! :) https://butt-man-123.herokuapp.com

That's it! You made a temporary app with all the fixins, which you can
use to continuously integrate or whatever you want to do.

Then, you can get rid of it like:

.. code:: text

  $ happy down
  Destroying app butt-man-123... done
  It's down. :(

.. _app.json manifest: https://devcenter.heroku.com/articles/app-json-schema
.. _Heroku toolbelt: https://toolbelt.heroku.com/

Commands
-------

up
~~

Brings up a Heroku app.

The app name is stored in a file called ``.happy`` in the working directory so
happy can find it later.

- ``--tarball-url``

  (optional) URL of the tarball containing app.json. If this is not given,
  happy tries to infer it from an ``app.json`` file in the current directory.

down
~~~~

Brings down a Heroku app.

The app name is read from a file called ``.happy`` in the working directory.

Running the tests
-----------------

1. Install tox_ with ``pip install tox``.
2. Run the tests with ``tox``.

.. _tox: https://tox.readthedocs.org

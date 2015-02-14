# happy

[![Travis](https://img.shields.io/travis/grampajoe/happy.svg)](https://travis-ci.org/grampajoe/happy)
[![Coveralls](https://img.shields.io/coveralls/grampajoe/happy.svg)](https://coveralls.io/r/grampajoe/happy)

Quickly set up and tear down Heroku apps!

> Note: This doesn't work yet! I'm just getting it started!!!!!!!!!
> (Don't use it.)

## Quickly starting

Add an [app.json manifest](https://devcenter.heroku.com/articles/app-json-schema)
that looks kinda like this:

```json
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
```

Push that to your thing's `master` branch on GitHub so Heroku can find it.

Log in with the [Heroku toolbelt](https://toolbelt.heroku.com/), then do this:

```
$ pip install happy
$ happy up
Creating app...
It's up! :) https://butt-man-123.herokuapp.com
```

That's it! You made a temporary app with all the fixins, which you can
use to continuously integrate or whatever you want to do.

Then, you can get rid of it like:

```
$ happy down
Destroying app...
It's down. :(
```

## Running the tests

1. Install [tox](https://tox.readthedocs.org) with `pip install tox`.
2. Run the tests with `tox`.

# happy

Quickly set up and tear down Heroku apps!

## Quickly starting

Add an [app.json manifest](https://devcenter.heroku.com/articles/app-json-schema)
that looks kinda like this:

```json
{
  "name": "My App Thing",
  "repository": "https://github.com/helloitsme/thingy"
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

Do some things, then get rid of it like:

```
$ happy down
Destroying app...
It's down. :(
```

> Note: This doesn't work yet! I'm just getting it started!!!!!!!!!
> (Don't use it)

## Running the tests

1. Install [tox](https://tox.readthedocs.org) with `pip nstall tox`.
2. Run the tests with `tox`.

# happy

Quickly set up and tear down Heroku apps!

## Quickly starting

Log in with the [Heroku toolbelt](https://toolbelt.heroku.com/), add an
[app.json manifest](https://devcenter.heroku.com/articles/app-json-schema)
to your thing on GitHub, then do this:

```bash
$ pip install happy
$ happy up username/repo --token=`heroku auth:token`
```

Then get rid of it like:

```bash
$ happy down
```

> Note: This doesn't work yet! I'm just getting it started!!!!!!!!!
> (Don't use it)

## Running the tests

1. Install [tox](https://tox.readthedocs.org) with `pip nstall tox`.
2. Run the tests with `tox`.

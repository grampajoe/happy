# happy

Quickly set up and tear down Heroku apps!

## Quickly starting

Log in with the [Heroku toolbelt](https://toolbelt.heroku.com/), add an
[app.json manifest](https://devcenter.heroku.com/articles/app-json-schema)
to your thing, then do this:

```bash
$ pip install happy
$ happy up username/repo --token=`heroku auth:token`
Starting app...
It's up! :) https://butt-man-321.herokuapp.com
$ happy down
Destroying app...
It's down. :(
```

> Note: This doesn't work yet! I'm just getting it started!!!!!!!!!
> (Don't use it)

## Running the tests

1. Install [tox](https://tox.readthedocs.org) with `pip nstall tox`.
2. Run the tests with `tox`.

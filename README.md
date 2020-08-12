# Haste [![Travis-CI Build Status](https://travis-ci.org/nrel/haste.svg?branch=develop)](https://travis-ci.org/github/nrel/haste)
web app to create semantic metadata models, namely, Haystack and Brick

# Setup
We recommend using the following:
- [pyenv](https://github.com/pyenv/pyenv#installation) for managing python versions
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv#installation) for managing packages and versions
- [pre-commit](https://pre-commit.com/#install) for managing code styling

1. Install `pyenv` and `pyenv-virtualenv` for your system
1. Install a python version through pyenv: `$ pyenv install 3.6.5`
1. Create a new `haste` specific environment: `$ pyenv virtualenv 3.6.5 haste`
1. Activate the environment in the root of the `path/to/Haste`: `$ pyenv local haste`
1. Check it is set correctly:
    ```
    $ pyenv version
    haste (set by /Users/user/path/to/haste/.python-version)
    ```
1. Install dependencies: `$ pip install -r requirements.txt`
1. Activate pre-commit: `$ pre-commit install`
1. Check that pre-commit is installed: `$ pre-commit --version`
1. Check that tests are able to run: `$ py.test`
```
cmosiman-34078s:haste cmosiman$ py.test
=============================================== test session starts ================================================
platform darwin -- Python 3.6.5, pytest-5.3.5, py-1.8.2, pluggy-0.13.1
django: settings: haste.settings (from env)
rootdir: /Users/cmosiman/Github/Haste/haste, inifile: pytest.ini
plugins: django-3.9.0
collected 2 items

tests/test_helpers.py ..                                                                                     [100%]

================================================ 2 passed in 0.08s =================================================
```

# Running Haste
After [setup](#setup) is complete, the web app can be run.  We have committed migrations in order to populate the following:
- Versions: Only Haystack 3.9.9 and Brick 1.1 are supported at this time
- Haystack marker tags: `q = "SELECT ?m WHERE { ?m rdfs:subClassOf* ph:marker}"`
- Brick tags
- Haystack Point tagsets: (generated using Haystack's `pointProtos` webpage)
- Brick Point classes: `q = "SELECT ?p WHERE { ?p rdfs:subClassOf* brick:Point}"`
- Haystack Equipment types: `q = "SELECT ?m WHERE { ?m rdfs:subClassOf* phIoT:equip }"`

Before starting the server, make sure to do the following:
- `python manage.py makemigrations`
- `python manage.py migrate`

Now the server can be run:
- `python manage.py runserver`

## TODO:
- Create migrations for mappings between Brick Classes <-> Haystack Point Tagsets
- Create migrations for equipment templates
- Create migrations for fault templates

# Understanding Mappings
Point protos in Project Haystack are mapped to Brick Classes at different release versions.  The mapping happens via use of the [py-brickschema](https://pypi.org/project/brickschema/) package, which means that there are three 'versions' to consider when a mapping is made:
- Haystack Version
- Brick Version (although this is currently embedded as part of the py-brickschema package)
- py-brickschema Version


## Third-Party Licenses
This project utilizes code written by [Patrick Coffey](https://patrickcoffey.bitbucket.io) under an [MIT](https://opensource.org/licenses/MIT) license.

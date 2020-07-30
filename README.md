# Haste
web app to create haystack json files (for now)

## Setup
- `pip install -r requirements.txt`
- `python manage.py runserver`

### Setup Pre-Commit
- Install pre-commit `pre-commit install`
- Run pre-commit on all files `pre-commit run --all-files`
  - If you get failures, run same command again to see if they have been auto-fixed

## Testing
Testing is implemented via `pytest`:
- `cd Haste/haste`
- `pytest`
```
cmosiman-34078s:haste cmosiman$ pytest
=============================================== test session starts ================================================
platform darwin -- Python 3.6.5, pytest-5.3.5, py-1.8.2, pluggy-0.13.1
django: settings: haste.settings (from env)
rootdir: /Users/cmosiman/Github/Haste/haste, inifile: pytest.ini
plugins: django-3.9.0
collected 2 items

tests/test_helpers.py ..                                                                                     [100%]

================================================ 2 passed in 0.08s =================================================
```

# Populate Database
Point protos in Project Haystack are mapped to Brick Classes at different release versions.  The mapping happens via use of the [py-brickschema](https://pypi.org/project/brickschema/) package, which means that there are three 'versions' to consider when a mapping is made:
- Haystack Version
- Brick Version (although this is currently embedded as part of the py-brickschema package)
- py-brickschema Version

In order to populate the database initially, it is necessary to do a few things:
- Make and run initial migrations:
```
$ python manage.py makemigrations
$ python manage.py migrate
```
- Create a migration to add a a mapping for your current version of the `brickschema` package.
    - Start by creating an empty migration: `$ python manage.py makemigrations mapp --empty`
    - Add the following line at the top of the new empty migration: `from mapp.resources.utils import create_initial_mapper, infer_points`
    - Add the following two operations:
  ```
      operations = [
        migrations.RunPython(create_initial_mapper),
        migrations.RunPython(infer_points)
    ]
  ```
    - Run the migration: `$ python manage.py migrate mapp`
- Repeat the above sequence of steps for multiple versions of the `brickschema` package (see the `.brick-inference-version` file for suggested versions) by running:
```
$ pip uninstall brickschema
$ pip install brickschema==X.X.X
```

## Third-Party Licenses
This project utilizes code written by [Patrick Coffey](https://patrickcoffey.bitbucket.io) under an [MIT](https://opensource.org/licenses/MIT) license

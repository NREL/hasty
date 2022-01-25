# Hasty [![codecov](https://codecov.io/gh/NREL/hasty/branch/develop/graph/badge.svg)](https://codecov.io/gh/NREL/hasty)
A web app to create and edit semantic metadata models of buildings with the following schemas. 

- [Brick](https://brickschema.org/)
- [Project Haystack](https://project-haystack.org/)
- [ASHRAE Standard 223P](https://www.ashrae.org/about/news/2018/ashrae-s-bacnet-committee-project-haystack-and-brick-schema-collaborating-to-provide-unified-data-semantic-modeling-solution) (future)

# Installing
## With Docker
The following dependencies are required:
- [Docker](https://docs.docker.com/get-docker/)

Project Setup:
1. Navigate to project root
1. Set postgres name, username, and password in `.env`
1. Build Docker images `docker compose build`
1. Create and run containers `docker compose up` for first time startup

### Run Server
- Start `docker compose start`
- Stop `docker compose stop`
- Tests `docker compose run web pytest`
### Reset Procedure
If the environment gets messed up this is what you need to start from scratch again.
1. Stop and remove containers and volumes `docker compose down -v`
### Containers
#### hasty-web
Django server container responsible for serving webpages and managing app. This container reads code from the working directory of the repo and will auto update on changes.
### hasty-db
Postgres database container. Data is stored in `hasty_pg_data` volume.

<!-- ## Without Docker
We recommend using the following:
- [pyenv](https://github.com/pyenv/pyenv#installation) for managing python versions
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv#installation) for managing packages and versions
- [pre-commit](https://pre-commit.com/#install) for managing code styling

1. Install `pyenv` and `pyenv-virtualenv` for your system
1. Install a python version through pyenv: `$ pyenv install 3.8.1`
1. Create a new `hasty` specific environment: `$ pyenv virtualenv 3.8.1 hasty`
1. Activate the environment in the root of the `path/to/Hasty`: `$ pyenv local hasty`
1. Check it is set correctly:
    ```
    $ pyenv version
    hasty (set by /Users/user/path/to/hasty/.python-version)
    ```
1. Install dependencies: `$ pip install -r requirements.txt`
1. Activate pre-commit: `$ pre-commit install`
1. Check that pre-commit is installed: `$ pre-commit --version`
1. Check that tests are able to run: `$ tox` -->

# Running
After installation is complete, the web app can be run.  We have committed migrations in order to populate the following:
- Versions: Only Haystack 3.9.9 and Brick 1.1 are supported at this time
- Haystack marker tags: `q = "SELECT ?m WHERE { ?m rdfs:subClassOf* ph:marker}"`
- Brick tags
- Haystack Point tagsets: (generated using Haystack's `pointProtos` webpage)
- Brick Point classes: `q = "SELECT ?p WHERE { ?p rdfs:subClassOf* brick:Point}"`
- Haystack Equipment types: `q = "SELECT ?m WHERE { ?m rdfs:subClassOf* phIoT:equip }"`

Before starting the server, make sure to do the following:
- `python manage.py makemigrations`
- `python manage.py migrate --run-syncdb`

Now the server can be run:
- `python manage.py runserver`

# TODO:
- Create migrations for mappings between Brick Classes <-> Haystack Point Tagsets
- Create migrations for equipment templates
- Create migrations for fault templates

# Understanding Mappings
Point protos in Project Haystack are mapped to Brick Classes at different release versions.  The mapping happens via use of the [py-brickschema](https://pypi.org/project/brickschema/) package, which means that there are three 'versions' to consider when a mapping is made:
- Haystack Version
- Brick Version (although this is currently embedded as part of the py-brickschema package)
- py-brickschema Version

# Third-Party Licenses
This project utilizes code written by [Patrick Coffey](https://patrickcoffey.bitbucket.io) under an [MIT](https://opensource.org/licenses/MIT) license.

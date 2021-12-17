#!/bin/sh
set -e

./wait-for-it.sh db:5432
python manage.py makemigrations
python manage.py migrate

exec "$@"

#!/usr/bin/env bash
set -o errexit

cd recipe_project
pip install -r requirements/prod.txt
python manage.py collectstatic --no-input --settings=config.settings.prod
python manage.py migrate --settings=config.settings.prod

#!/bin/bash -e

APPNAME="app"
LISTEN="0.0.0.0:8753"

export STATIC_URL="/static/p200/586b5b17386f8cd28ee1bdaf8274f784a/"
export STATIC_ROOT="${PWD}/${APPNAME}/static/"

source p200-venv/bin/activate

# The "insecure" option enables static files...
exec python manage.py runserver $LISTEN --insecure --noreload

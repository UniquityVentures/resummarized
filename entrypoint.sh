#!/bin/sh

cd "$(dirname "$0")"

uv run celery -A resummarized_django worker &
uv run manage.py runserver

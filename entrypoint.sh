#!/bin/sh

uv run celery -A resummarized_django worker &
uv run manage.py runserver

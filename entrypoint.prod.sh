#!/usr/bin/env bash

cd starthub
uv run manage.py collectstatic --noinput
uv run manage.py migrate --noinput
uv run gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi

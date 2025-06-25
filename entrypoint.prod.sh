#!/usr/bin/env bash

# shellcheck disable=SC2164
cd starthub
uv run manage.py collectstatic --noinput
uv run manage.py migrate --noinput
uv run gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi

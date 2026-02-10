#!/usr/bin/env sh
set -eu

# Collect static files for production
python manage.py collectstatic --noinput --clear

exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:8000" \
  --workers "${WEB_CONCURRENCY:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-60}" \
  --access-logfile - \
  --error-logfile -

#!/usr/bin/env sh
set -eu

PORT_VALUE="${PORT:-8000}"

# If PORT is accidentally passed as a literal like "$PORT", fallback to 8000
if [ "$PORT_VALUE" = "\$PORT" ]; then
  PORT_VALUE="8000"
fi

# Basic numeric check
case "$PORT_VALUE" in
  ''|*[!0-9]*) PORT_VALUE="8000" ;;
  *) : ;;
esac

# Collect static files for production
python manage.py collectstatic --noinput --clear

exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT_VALUE}" \
  --workers "${WEB_CONCURRENCY:-3}" \
  --timeout "${GUNICORN_TIMEOUT:-60}"

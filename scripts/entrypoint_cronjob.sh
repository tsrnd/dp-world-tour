#!/bin/sh
set -e

until psql "$DATABASE_URL" -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

if [ "$AUTO_CRONJOBS" = '1' ]; then
  python manage.py cus_crontab remove --settings=myproject.settings_cronjob
  python manage.py cus_crontab add --settings=myproject.settings_cronjob
fi

exec "$@"

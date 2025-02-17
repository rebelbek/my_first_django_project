#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Postgres еще не запущен..."

    # Проверяем доступность хоста и порта
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 1
    done

    echo "PostgreSQL запущен"
fi

exec "$@"

# If this is going to be a cron container, set up the crontab.
if [ "$1" = cron ]; then
  ./manage.py crontab add
fi

# Launch the main container command passed as arguments.
exec "$@"
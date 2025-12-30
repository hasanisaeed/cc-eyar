#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started. Running Migrations..."

python manage.py makemigrations users --noinput
python manage.py makemigrations orders --noinput

python manage.py migrate --noinput

python manage.py collectstatic --noinput --clear

echo "Database is ready. Starting server..."

exec "$@"
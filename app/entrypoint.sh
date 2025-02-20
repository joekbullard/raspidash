#!/bin/bash

# dockerize -wait tcp://"${POSTGRES_HOST}":"${POSTGRES_PORT}" -timeout 0.1s

until nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  echo "Waiting for database..."
  sleep 1
done

echo "PostgreSQL started"

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py init_admin

exec "$@"
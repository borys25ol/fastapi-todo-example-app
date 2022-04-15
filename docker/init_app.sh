#!/bin/sh

echo "Waiting for Postgres..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.1
done

echo "PostgreSQL started"

make migrate
make runserver_docker

exec "$@"
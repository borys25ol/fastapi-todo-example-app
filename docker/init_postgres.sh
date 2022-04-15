#!/bin/bash

DATABASE_NAME=${POSTGRES_DB}

# create default database
gosu postgres postgres --single <<EOSQL
  CREATE DATABASE "$DATABASE_NAME";
  ALTER USER postgres CREATEDB;
  GRANT ALL PRIVILEGES ON DATABASE "$DATABASE_NAME" TO postgres;
EOSQL

echo "database created!"

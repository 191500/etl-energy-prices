#!/bin/bash
set -e

until pg_isready -U "$POSTGRES_USER"; do
  sleep 2
done

pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" -F c /docker-entrypoint-initdb.d/dump.backup

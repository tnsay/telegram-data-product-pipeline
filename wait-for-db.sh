#!/bin/sh

set -e

host="$1"
port="$2"
shift 2
cmd="$@"

echo "⏳ Waiting for Postgres at $host:$port..."
until pg_isready -h "$host" -p "$port" > /dev/null 2>&1; do
  sleep 1
done

echo "✅ Postgres is ready! Running command..."
exec $cmd

#!/usr/bin/env bash
set -o errexit

compose_file="docker-compose.yaml"

function finish() {
    # make sure nothing is left running
    docker-compose down --remove-orphans || true
}

# trap those exit signals
trap finish INT TERM ERR
trap finish EXIT

echo "Starting Listle server..."
docker-compose -f $compose_file build --pull --force-rm &&
docker-compose -f $compose_file up

wait

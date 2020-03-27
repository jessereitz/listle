#!/usr/bin/env bash

set -o errexit

TAG="listle-test"
TEST_ARGS=$@

docker build --tag $TAG --target tester .

# No arguments were passed in, so we'll assume you want to run everything
if [ $# -eq 0 ]; then
    echo "Running flake8..."
    docker run --rm "$TAG" flake8

    echo "Running autopep8..."
    OUT=$(docker run --rm "$TAG" autopep8 --recursive --diff --max-line-length 99999999 --exclude .env .)
    if [ ! -z "$OUT" ]; then
        echo "autopep8 returned a diff, please run autopep8."
        echo $OUT
        exit 1
    fi
fi

echo "Running tests in container $TAG $@..."
docker run --rm "$TAG" pytest $TEST_ARGS

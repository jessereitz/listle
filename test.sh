#!/usr/bin/env bash

set -o errexit

TAG="listle-test"
TEST_ARGS=$@

docker build --tag $TAG --target tester .

# No arguments were passed in, so we'll assume you want to run everything
if [ $# -eq 0 ]; then
    echo "No arguments. Running cloud-build test locally"
    cloud-build-local --config ./cloudbuild.test.yaml --dryrun=false .
else
    echo "Running tests in container $TAG $@..."
    docker run --rm "$TAG" pytest $TEST_ARGS
fi

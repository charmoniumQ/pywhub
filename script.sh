#!/usr/bin/env

set -x -e

mypy --strict --package whub
black .
isort .
mypy --strict --package test
PYTHONPATH=. pytest
pylint --recursive y .

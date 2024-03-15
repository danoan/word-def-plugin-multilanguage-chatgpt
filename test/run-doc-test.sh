#! /usr/bin/env bash

SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd "${SCRIPT_PATH}" >/dev/null
python -m doctest ../docs/*.md
popd >/dev/null

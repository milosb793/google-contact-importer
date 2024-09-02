#/bin/env bash

source .venv/bin/activate

run src.scripts.main --input "$1" --output "$2" --dry
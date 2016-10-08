#!/bin/bash -e

LISTEN="0.0.0.0:30877"

source p100-venv/bin/activate
exec python src/app.py --listen="${LISTEN}" \
                       --debug

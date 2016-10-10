#!/bin/bash -e

LISTEN="127.0.0.1:50001"

source p200-venv/bin/activate
exec python src/app.py --listen="${LISTEN}"

#!/bin/bash -e

LISTEN="127.0.0.1:30002"

source venv/bin/activate
exec python src/app.py --listen="${LISTEN}"

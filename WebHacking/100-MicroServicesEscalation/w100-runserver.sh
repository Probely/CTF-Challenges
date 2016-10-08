#!/bin/bash -e

LISTEN="0.0.0.0:30878"

EMPLOYEE_FILE="data/employees.csv"
CTF_PARTICIPANTS="data/participants_hashed.csv"
SAVE_FILE="data/db.json"

source w100-venv/bin/activate
exec python src/app.py --employees "${EMPLOYEE_FILE}" \
                       --participants "${CTF_PARTICIPANTS}" \
                       --save "${SAVE_FILE}" \
                       --listen="${LISTEN}" \
		      # --debug

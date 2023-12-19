#!/bin/bash
set -e

if [[ ! -z "$1" ]]; then
    echo ${*}
    exec  ${*}
else
    python /app/lib/main.py
fi
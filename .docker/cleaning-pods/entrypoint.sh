#!/bin/bash
set -e

if [[ ! -z "$1" ]]; then
    echo ${*}
    exec  ${*}
else
    /usr/local/bin/python /app/lib/main.py
fi
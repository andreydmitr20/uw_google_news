#!/bin/bash
LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
# PYTHONPATH=/lib/

cd sender

python3 sender.py

exec "$@"

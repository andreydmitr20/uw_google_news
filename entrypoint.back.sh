#!/bin/bash
LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
# PYTHONPATH=/lib/

cd back

python3 m migrate

celery -A back worker -P threads --loglevel=info &
uwsgi --ini uwsgi.ini

exec "$@"

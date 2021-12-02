#!/bin/bash

if [ "$CONTAINER_NAME" = 'web' ]; then
    echo 'launching web'
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    python manage.py generateschema --file openapi-schema.yml
    python manage.py runserver 0.0.0.0:8000
fi

if [ "$CONTAINER_NAME" = 'swarm' ]; then
    echo 'launching swarm'
    bash -c "cd /code/ && celery -A swarm worker -l warning -c 1 -Q swarm -n swarm.%h --without-mingle --without-gossip"
fi

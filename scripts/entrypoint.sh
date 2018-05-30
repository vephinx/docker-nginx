#!/bin/sh
set -e

if [ ! -f /touched ]; then
    touch /touched
    python /opt/scripts/entrypoint.py
fi

nginx &
exec confd \
    -interval $GLUU_CONFD_INTERVAL \
    -log-level $GLUU_CONFD_LOG_LEVEL \
    -backend $GLUU_CONFD_BACKEND \
    -node $GLUU_KV_HOST:$GLUU_KV_PORT

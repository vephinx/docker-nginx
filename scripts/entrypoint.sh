#!/bin/sh
set -e

if [ ! -f /touched ]; then
    touch /touched
    python /opt/scripts/entrypoint.py
fi

exec consul-template \
    -log-level info \
    -consul-addr $GLUU_KV_HOST:$GLUU_KV_PORT \
    -template "/opt/templates/gluu_https.conf.ctmpl:/etc/nginx/conf.d/default.conf" \
    -wait 5s \
    -exec "nginx" \
    -exec-reload-signal SIGHUP \
    -exec-kill-signal SIGQUIT

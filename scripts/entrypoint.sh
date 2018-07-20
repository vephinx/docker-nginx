#!/bin/sh
set -e

if [ "$GLUU_CONFIG_ADAPTER" != "consul" ]; then
    echo "This container only support Consul as config backend."
    exit 1
fi

if [ ! -f /touched ]; then
    touch /touched
    python /opt/scripts/entrypoint.py
fi

exec consul-template \
    -log-level info \
    -consul-addr $GLUU_CONSUL_HOST:$GLUU_CONSUL_PORT \
    -template "/opt/templates/gluu_https.conf.ctmpl:/etc/nginx/conf.d/default.conf" \
    -wait 5s \
    -exec "nginx" \
    -exec-reload-signal SIGHUP \
    -exec-kill-signal SIGQUIT

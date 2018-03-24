#!/bin/sh
set -e

enable_gluu_https() {
    mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.orig
}

if [ ! -f /touched ]; then
    touch /touched
    python /opt/scripts/entrypoint.py
    enable_gluu_https
fi

exec /usr/sbin/nginx -g "daemon off;"

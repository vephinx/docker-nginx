#!/bin/sh
set -e

if [ "$GLUU_CONFIG_ADAPTER" != "consul" ]; then
    echo "This container only support Consul as config backend."
    exit 1
fi

if [ ! -f /touched ]; then
    if [ -f /etc/redhat-release ]; then
        source scl_source enable python27 && python /opt/scripts/entrypoint.py
    else
        python /opt/scripts/entrypoint.py
    fi
    touch /touched
fi

get_consul_opts() {
    local consul_scheme=0

    local consul_opts="-consul-addr $GLUU_CONSUL_HOST:$GLUU_CONSUL_PORT"

    if [ $GLUU_CONSUL_SCHEME = "https" ]; then
        consul_opts="${consul_opts} -consul-ssl"

        if [ -f $GLUU_CONSUL_CACERT_FILE ]; then
            consul_opts="${consul_opts} -consul-ssl-ca-cert $GLUU_CONSUL_CACERT_FILE"
        fi

        if [ -f $GLUU_CONSUL_CERT_FILE ]; then
            consul_opts="${consul_opts} -consul-ssl-cert $GLUU_CONSUL_CERT_FILE"
        fi

        if [ -f $GLUU_CONSUL_KEY_FILE ]; then
            consul_opts="${consul_opts} -consul-ssl-key $GLUU_CONSUL_KEY_FILE"
        fi

        if [ $GLUU_CONSUL_VERIFY = "true" ]; then
            consul_opts="${consul_opts} -consul-ssl-verify"
        fi
    fi

    if [ -f $GLUU_CONSUL_TOKEN_FILE ]; then
        consul_opts="${consul_opts} -consul-token $(cat $GLUU_CONSUL_TOKEN_FILE)"
    fi
    echo $consul_opts
}

exec consul-template \
    -log-level info \
    -template "/opt/templates/gluu_https.conf.ctmpl:/etc/nginx/conf.d/default.conf" \
    -wait 5s \
    -exec "nginx" \
    -exec-reload-signal SIGHUP \
    -exec-kill-signal SIGQUIT \
    $(get_consul_opts)

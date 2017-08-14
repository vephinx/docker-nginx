import os

import consulate


GLUU_OXAUTH_BACKEND = os.environ.get("GLUU_OXAUTH_BACKEND", "localhost:8081")
GLUU_OXTRUST_BACKEND = os.environ.get("GLUU_OXTRUST_BACKEND", "localhost:8082")
GLUU_KV_HOST = os.environ.get("GLUU_KV_HOST", "localhost")
GLUU_KV_PORT = os.environ.get("GLUU_KV_PORT", 8500)

consul = consulate.Consul(host=GLUU_KV_HOST, port=GLUU_KV_PORT)


def render_ssl_cert():
    ssl_cert = consul.kv.get("ssl_cert")
    if ssl_cert:
        with open("/etc/certs/gluu_https.crt", "w") as fd:
            fd.write(ssl_cert)


def render_ssl_key():
    ssl_key = consul.kv.get("ssl_key")
    if ssl_key:
        with open("/etc/certs/gluu_https.key", "w") as fd:
            fd.write(ssl_key)


def render_nginx_conf():
    txt = ""
    with open("/opt/templates/gluu_https.conf.tmpl") as fd:
        txt = fd.read()

    if txt:
        with open("/etc/nginx/sites-available/gluu_https.conf", "w") as fd:
            rendered_txt = txt % {
                "gluu_domain": consul.kv.get("hostname", "localhost"),
                "gluu_oxauth_backend": upstream_config(GLUU_OXAUTH_BACKEND.split(",")),
                "gluu_oxtrust_backend": upstream_config(GLUU_OXTRUST_BACKEND.split(",")),
            }
            fd.write(rendered_txt)


def upstream_config(backends):
    cfg = "".join([
        "\tserver {} fail_timeout=10s;\n".format(backend)
        for backend in backends
    ])
    return cfg


if __name__ == "__main__":
    render_ssl_cert()
    render_ssl_key()
    render_nginx_conf()

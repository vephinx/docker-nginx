import os

import consulate


GLUU_OXAUTH_BACKEND = os.environ.get("GLUU_OXAUTH_BACKEND", "localhost:8081")
GLUU_OXTRUST_BACKEND = os.environ.get("GLUU_OXTRUST_BACKEND", "localhost:8082")
GLUU_KV_HOST = os.environ.get("GLUU_KV_HOST", "localhost")
GLUU_KV_PORT = os.environ.get("GLUU_KV_PORT", 8500)

consul = consulate.Consul(host=GLUU_KV_HOST, port=GLUU_KV_PORT)


CONFIG_PREFIX = "gluu/config/"


def merge_path(name):
    # example: `hostname` renamed to `gluu/config/hostname`
    return "".join([CONFIG_PREFIX, name])


def unmerge_path(name):
    # example: `gluu/config/hostname` renamed to `hostname`
    return name[len(CONFIG_PREFIX):]


def get_config(name, default=None):
    return consul.kv.get(merge_path(name), default)


def render_ssl_cert():
    ssl_cert = get_config("ssl_cert")
    if ssl_cert:
        with open("/etc/certs/gluu_https.crt", "w") as fd:
            fd.write(ssl_cert)


def render_ssl_key():
    ssl_key = get_config("ssl_key")
    if ssl_key:
        with open("/etc/certs/gluu_https.key", "w") as fd:
            fd.write(ssl_key)


def render_nginx_conf():
    txt = ""
    with open("/opt/templates/gluu_https.conf.tmpl") as fd:
        txt = fd.read()

    if txt:
        with open("/etc/nginx/conf.d/gluu_https.conf", "w") as fd:
            rendered_txt = txt % {
                "gluu_domain": get_config("hostname", "localhost"),
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

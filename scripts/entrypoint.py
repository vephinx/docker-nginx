import os

import consulate


GLUU_OXAUTH_BACKEND = os.environ.get("GLUU_OXAUTH_BACKEND", "localhost:8081")
GLUU_OXTRUST_BACKEND = os.environ.get("GLUU_OXTRUST_BACKEND", "localhost:8082")
GLUU_OXSHIBBOLETH_BACKEND = os.environ.get("GLUU_OXSHIBBOLETH_BACKEND", "localhost:8086")
GLUU_KV_HOST = os.environ.get("GLUU_KV_HOST", "localhost")
GLUU_KV_PORT = os.environ.get("GLUU_KV_PORT", 8500)

GLUU_OX_PROXY_MODE = os.environ.get("GLUU_OX_PROXY_MODE", False)
GLUU_OXAUTH_HOST_HEADER = os.environ.get("GLUU_OXAUTH_HOST_HEADER", "$host")
GLUU_OXTRUST_HOST_HEADER = os.environ.get("GLUU_OXTRUST_HOST_HEADER", "$host")
GLUU_OXSHIBBOLETH_HOST_HEADER = os.environ.get("GLUU_OXSHIBBOLETH_HOST_HEADER", "$host")
GLUU_RESOLVER_ADDR = os.environ.get("GLUU_RESOLVER_ADDR", "127.0.0.11")

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


def as_boolean(val, default=False):
    truthy = set(('t', 'T', 'true', 'True', 'TRUE', '1', 1, True))
    falsy = set(('f', 'F', 'false', 'False', 'FALSE', '0', 0, False))

    if val in truthy:
        return True
    if val in falsy:
        return False
    return default


def render_nginx_conf():
    ctx = {
        "gluu_domain": get_config("hostname", "localhost"),
    }

    if as_boolean(GLUU_OX_PROXY_MODE):
        tmpl_fn = "/opt/templates/gluu_https.proxy.conf.tmpl"
        ctx["gluu_oxauth_backend"] = GLUU_OXAUTH_BACKEND.split(",")[0]
        ctx["gluu_oxtrust_backend"] = GLUU_OXTRUST_BACKEND.split(",")[0]
        ctx["gluu_oxshibboleth_backend"] = GLUU_OXSHIBBOLETH_BACKEND.split(",")[0]
        ctx["gluu_resolver"] = GLUU_RESOLVER_ADDR
        ctx["oxauth_host_header"] = GLUU_OXAUTH_HOST_HEADER
        ctx["oxtrust_host_header"] = GLUU_OXTRUST_HOST_HEADER
        ctx["oxshibboleth_host_header"] = GLUU_OXSHIBBOLETH_HOST_HEADER
    else:
        tmpl_fn = "/opt/templates/gluu_https.upstream.conf.tmpl"
        ctx["gluu_oxauth_backend"] = upstream_config(GLUU_OXAUTH_BACKEND.split(","))
        ctx["gluu_oxtrust_backend"] = upstream_config(GLUU_OXTRUST_BACKEND.split(","))
        ctx["gluu_oxshibboleth_backend"] = upstream_config(GLUU_OXSHIBBOLETH_BACKEND.split(","))

    with open(tmpl_fn) as fr:
        txt = fr.read()

        with open("/etc/nginx/conf.d/gluu_https.conf", "w") as fw:
            fw.write(txt % ctx)


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

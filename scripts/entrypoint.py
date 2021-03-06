from gluu_config import ConfigManager

config_manager = ConfigManager()


def render_ssl_cert():
    ssl_cert = config_manager.get("ssl_cert")
    if ssl_cert:
        with open("/etc/certs/gluu_https.crt", "w") as fd:
            fd.write(ssl_cert)


def render_ssl_key():
    ssl_key = config_manager.get("ssl_key")
    if ssl_key:
        with open("/etc/certs/gluu_https.key", "w") as fd:
            fd.write(ssl_key)


if __name__ == "__main__":
    render_ssl_cert()
    render_ssl_key()

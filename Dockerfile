FROM nginx:alpine

LABEL maintainer="Gluu Inc. <support@gluu.org>"

# ===============
# Alpine packages
# ===============
RUN apk update && apk add --no-cache \
    openssl \
    py-pip


# =====
# nginx
# =====
RUN mkdir -p /etc/certs
RUN openssl dhparam -out /etc/certs/dhparams.pem 2048
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Ports for nginx
EXPOSE 80
EXPOSE 443

# ======
# Python
# ======
RUN pip install -U pip \
    && pip install "consulate==0.6.0"

# =====
# confd
# =====
ENV CONFD_VERSION 0.16.0
RUN wget -q https://github.com/kelseyhightower/confd/releases/download/v${CONFD_VERSION}/confd-${CONFD_VERSION}-linux-amd64 -O /usr/bin/confd \
    && chmod +x /usr/bin/confd

# ==========
# misc stuff
# ==========
LABEL vendor="Gluu Federation"

ENV GLUU_KV_HOST localhost
ENV GLUU_KV_PORT 8500
ENV GLUU_CONFD_INTERVAL 30
ENV GLUU_CONFD_LOG_LEVEL info
ENV GLUU_CONFD_BACKEND consul

RUN mkdir -p /opt/scripts /etc/confd/conf.d/ /etc/confd/templates
COPY templates/confd/gluu_https.conf.tmpl /etc/confd/templates/
COPY templates/confd/gluu_https.toml /etc/confd/conf.d/
COPY scripts /opt/scripts/

RUN chmod +x /opt/scripts/entrypoint.sh
CMD ["/opt/scripts/wait-for-it", "/opt/scripts/entrypoint.sh"]

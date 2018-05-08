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

# Ports for nginx
EXPOSE 80
EXPOSE 443

# ======
# Python
# ======
RUN pip install -U pip \
    && pip install "consulate==0.6.0"

# ==========
# misc stuff
# ==========
LABEL vendor="Gluu Federation"

ENV GLUU_OXAUTH_BACKEND localhost:8081
ENV GLUU_OXTRUST_BACKEND localhost:8082
ENV GLUU_KV_HOST localhost
ENV GLUU_KV_PORT 8500

RUN mkdir -p /opt/scripts /opt/templates

COPY templates /opt/templates/
COPY scripts /opt/scripts/

RUN chmod +x /opt/scripts/entrypoint.sh
CMD ["/opt/scripts/wait-for-it", "/opt/scripts/entrypoint.sh"]

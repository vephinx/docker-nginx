# nginx

A docker image version of nginx.

## Versioning/Tagging

This image uses its own versioning/tagging format.

    <IMAGE-NAME>:<GLUU-SERVER-VERSION>_<INTERNAL-REV-VERSION>

For example, `gluufederation/nginx:3.0.1_rev1.0.0` consists of:

- glufederation/nginx as `<IMAGE_NAME>`; the actual image name
- 3.0.1 as `GLUU-SERVER-VERSION`; the Gluu Server version as setup reference
- rev1.0.0 as `<INTERNAL-REV-VERSION>`; revision made when developing the image

## Installation

Build the image:

```
docker build --rm --force-rm -t gluufederation/nginx:latest .
```

Or get it from Docker Hub:

```
docker pull gluufederation/nginx:latest
```

## Environment Variables

- `GLUU_KV_HOST`: hostname or IP address of Consul.
- `GLUU_KV_PORT`: port of Consul.
- `GLUU_OXAUTH_BACKEND`: Host and port of oxAuth backend, i.e. `oxauth.domain.com:8081`. Multiple backends is supported (separate each backend with comma character, i.e. `oxauth1.domain.com:8081,oxauth2.domain.com:8081`).
- `GLUU_OXTRUST_BACKEND`: Host and port of oxTrust backend, i.e. `oxtrust.domain.com:8082`. Multiple backends is supported (separate each backend with comma character, i.e. `oxtrust1.domain.com:8082,oxtrust2.domain.com:8082`).

## Running The Container

Here's an example to run the container:

```
docker run -d \
    --name nginx \
    -e GLUU_KV_HOST=my.consul.domain.com \
    -e GLUU_KV_PORT=8500 \
    -e GLUU_OXAUTH_BACKEND=my.oxauth.domain.com:8081 \
    -e GLUU_OXTRUST_BACKEND=my.oxtrust.domain.com:8082 \
    gluufederation/nginx:containership
```

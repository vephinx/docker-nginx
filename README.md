# nginx

A docker image version of nginx.

## Latest Stable Release

Latest stable release is `gluufederation/nginx:3.1.3_01`. See `CHANGES.md` for archives.

## Versioning/Tagging

This image uses its own versioning/tagging format.

    <IMAGE-NAME>:<GLUU-SERVER-VERSION>_<RELEASE_VERSION>

For example, `gluufederation/nginx:3.1.3_01` consists of:

- `glufederation/nginx` as `<IMAGE_NAME>`; the actual image name
- `3.1.3` as `GLUU-SERVER-VERSION`; the Gluu Server version as setup reference
- `01` as `<RELEASE_VERSION>`

## Installation

Pull the image:

    docker pull gluufederation/nginx:3.1.3_01

## Environment Variables

- `GLUU_KV_HOST`: hostname or IP address of Consul.
- `GLUU_KV_PORT`: port of Consul.

> Note that you can use IP addresses in lieu of FQDN's

## Running The Container

Here's an example to run the container:

```
docker run -d \
    --name nginx \
    -e GLUU_KV_HOST=consul.example.com \
    -e GLUU_KV_PORT=8500 \
    gluufederation/nginx:3.1.3_01
```

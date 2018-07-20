# nginx

A docker image version of nginx.

## Latest Stable Release

Latest stable release is `gluufederation/nginx:3.1.3_02`. See `CHANGES.md` for archives.

## Versioning/Tagging

This image uses its own versioning/tagging format.

    <IMAGE-NAME>:<GLUU-SERVER-VERSION>_<RELEASE_VERSION>

For example, `gluufederation/nginx:3.1.3_02` consists of:

- `glufederation/nginx` as `<IMAGE_NAME>`; the actual image name
- `3.1.3` as `GLUU-SERVER-VERSION`; the Gluu Server version as setup reference
- `02` as `<RELEASE_VERSION>`

## Installation

Pull the image:

    docker pull gluufederation/nginx:3.1.3_02

## Environment Variables

- `GLUU_CONFIG_ADAPTER`: config backend (either `consul` for Consul KV or `kubernetes` for Kubernetes configmap)

The following environment variables are activated only if `GLUU_CONFIG_ADAPTER` is set to `consul`:

- `GLUU_CONSUL_HOST`: hostname or IP of Consul (default to `localhost`)
- `GLUU_CONSUL_PORT`: port of Consul (default to `8500`)
- `GLUU_CONSUL_CONSISTENCY`: Consul consistency mode (choose one of `default`, `consistent`, or `stale`). Default to `stale` mode.

otherwise, if `GLUU_CONFIG_ADAPTER` is set to `kubernetes`:

- `GLUU_KUBERNETES_NAMESPACE`: Kubernetes namespace (default to `default`)
- `GLUU_KUBERNETES_CONFIGMAP`: Kubernetes configmap name (default to `gluu`)

Note:

1. You can use IP addresses in lieu of FQDN's
2. Only `GLUU_CONFIG_ADAPTER=consul` that is fully supported at the moment, hence deploying Consul is mandatory.
3. When using Kubernetes, use Ingress directly.

## Running The Container

Here's an example to run the container:

```
docker run -d \
    --name nginx \
    -e GLUU_CONFIG_ADAPTER=consul \
    -e GLUU_CONSUL_HOST=consul.example.com \
    -e GLUU_CONSUL_PORT=8500 \
    gluufederation/nginx:3.1.3_02
```

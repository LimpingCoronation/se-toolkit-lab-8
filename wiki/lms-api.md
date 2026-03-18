# LMS API

## About the LMS API

## LMS API host port

The [port number](./computer-networks.md#port-number) (without `<` and `>`) which the [LMS API](#about-the-lms-api) is available at on the [host](./computer-networks.md#host).

The port number is the value of [`LMS_API_HOST_PORT`](./dotenv-docker-secret.md#lms_api_host_port) in [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).

### `<lms-api-host-port>` placeholder

The [LMS API host port](#lms-api-host-port).

## LMS API base URL

> [!NOTE]
>
> See [URL](./computer-networks.md#url).

- (REMOTE) When running the request on the VM:
  
  `http://localhost:<lms-api-host-port>`

- (LOCAL) When running the request on the local machine:
  
  `http://<your-vm-ip-address>:<lms-api-host-port>`

Replace the placeholders:

- [`<your-vm-ip-address>`](./vm.md#your-vm-ip-address-placeholder)
- [`<lms-api-host-port>`](./lms-api.md#lms-api-host-port-placeholder)

### `<lms-api-base-url>` placeholder

[LMS API base URL](#lms-api-base-url) (without `<` and `>`).

## `Caddy`

In this project, `Caddy` [is configured using the `Caddyfile`](#caddyfile).

### `Caddyfile`

The [`Caddyfile`](./caddy.md#caddyfile) at [`caddy/Caddyfile`](../caddy/Caddyfile) specifies the [`Caddy` duties](#caddy-duties).

## `Caddy` duties

<!-- no toc -->
- [Listen on the specific port](./computer-networks.md#listen-on-a-port) inside a [`Docker` container](./docker.md#container).
- [Forward requests to the backend](#forward-requests-to-the-backend)
- [Forward requests to the `Qwen Code` API](#forward-requests-to-the-qwen-code-api)
- [Forward requests to the `pgAdmin`](#forward-requests-to-pgadmin)
- [Serve the frontend files](#serve-frontend-files)

### Listen on the specific port

`Caddy` listens on the port whose port number is the value of [`CADDY_CONTAINER_PORT`](./dotenv-docker-secret.md#caddy_container_port) from [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).

### Forward requests to the backend

`Caddy` routes to the [`app` service](./docker-compose-yml.md#app-service) these [API endpoints](./web-api.md#endpoint):

- `/items*`
- `/learners*`
- `/interactions*`
- `/pipeline*`
- `/analytics*`
- `/docs*`
- `/openapi.json`

### Forward requests to the `Qwen Code` API

`Caddy` routes to the [`Qwen Code` API](./qwen-code-api.md#what-is-qwen-code-api) these [API endpoints](./web-api.md#endpoint):

- `/utils/qwen-code-api*`

### Forward requests to `pgAdmin`

`Caddy` routes to [`pgAdmin`](./pgadmin#what-is-pgadmin) these [API endpoints](./web-api.md#endpoint):

- `/utils/pgadmin*`

### Serve frontend files

`Caddy` serves static front-end files from `/srv` for all other paths.

The `try_files` directive falls back to `index.html` for client-side routing.

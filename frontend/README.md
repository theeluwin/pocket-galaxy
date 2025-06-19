# Pocket Galaxy Frontend

Basic features like login and displaying the list are included by default.

Usually, when using it individually, you might also use things like list filtering or gallery views. However, from this point on, you'll need to implement those yourself using Vue and Vuetify.

## Environment Variables (Required)

Example `.env` file (place it under `frontend/`):

```bash
WEB_PORT=8002
API_PREFIX=http://localhost:8001/api
MEDIA_PREFIX=http://localhost:8001/media
```

## Development Environment

The folder `frontend/src/` is volume-bound. Since it's in development mode, changes are reflected in real time.

### Development Build

```bash
docker-compose --project-directory . -f compose/dev.yml build
```

### Run Development Server

```bash
docker-compose --project-directory . -f compose/dev.yml up --build
```

## Production Environment

This project does not assume a production environment by default, but support is provided for long-running deployments.

Built files are packaged into the Docker image, and it runs stably enough. NGINX is used for serving.

### Production Build

```bash
docker-compose --project-directory . -f compose/prod.yml build
```

### Run in Production

```bash
docker-compose --project-directory . -f compose/prod.yml up -d --build
```

## NPM-Related

In the development environment, only the `frontend/src/` folder is volume-bound. So if you want to modify things like `package.json`, you'll need to run a separate container. See `run_example.sh` for reference.

```bash
x () {
    docker run \
        -it \
        --rm \
        --init \
        --workdir /app \
        -v "${PWD}:/app" \
        node:24-alpine3.21 \
        "$@"
}

x npm audit fix
```

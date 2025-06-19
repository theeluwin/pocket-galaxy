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
